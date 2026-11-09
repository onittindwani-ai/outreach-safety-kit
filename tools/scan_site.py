"""Scan a website folder or pasted HTML for LinkedIn name and brand mentions.

Usage:
    python3 tools/scan_site.py path/to/site-folder
    python3 tools/scan_site.py path/to/page.html
    python3 tools/scan_site.py --stdin < page.html
    python3 tools/scan_site.py --html '<p>Paste HTML here</p>'
    python3 tools/scan_site.py path/to/site --json --fail-on medium

What it does: reads your files locally, looks for the LinkedIn name, its product
names and its logos in visible copy and in hidden places (image alt text, meta
tags, comments, scripts, link addresses, file names), and tells you which of the
30 checks each finding belongs to.

What it does not do: it never opens a web page, never logs in anywhere and never
changes a file. A clean result means it found no mention in the files it could
read. It does not mean you are safe, and it is not legal advice.

Exit codes: 0 nothing at or above --fail-on, 1 findings at or above --fail-on,
2 the input could not be read.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from typing import Callable, Dict, List, Optional, Set, Tuple
from urllib.parse import urlsplit

SEVERITY_ORDER = {"high": 3, "medium": 2, "low": 1, "info": 0}
MAX_BYTES = 5_000_000
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".cache"}
HTML_SUFFIXES = {".html", ".htm", ".xhtml", ".vue", ".svelte", ".astro", ".ejs", ".hbs", ".liquid", ".erb", ".php"}
PROSE_SUFFIXES = {".md", ".mdx", ".txt", ".rst"}
CODE_SUFFIXES = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".json", ".yml", ".yaml", ".xml", ".svg", ".css", ".scss", ".csv", ".toml"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".avif"}
UNREADABLE_SUFFIXES = {".pdf", ".docx", ".pptx", ".key"}

BLOCK_TAGS = {
    "address", "article", "aside", "blockquote", "body", "br", "button", "dd", "div", "dl", "dt",
    "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head",
    "header", "hr", "html", "li", "main", "nav", "ol", "option", "p", "pre", "section", "table", "td",
    "th", "title", "tr", "ul",
}
URL_ATTRS = {"href", "src", "srcset", "action", "poster", "data-src", "data-href"}
TEXT_ATTRS = {"alt", "title", "aria-label", "placeholder", "value", "name"}

BRAND = re.compile(r"l[i1]nked[i1]n|linkdin|lnkd\.in|sales\s+navigator|sales\s+nav\b|\binmail\b", re.I)
BRAND_CASED = re.compile(r"\bLinked[- ]In\b")
TOKEN = re.compile(
    r"mailto:[^\s\"'<>)]+|https?://[^\s\"'<>)]+|www\.[^\s\"'<>)]+|[\w.+-]+@[\w.-]+\.[a-z]{2,}"
    r"|\b[\w-]*linkedin[\w-]*\.(?:com|io|ai|co|net|org|app|dev)\b",
    re.I,
)
LINKEDIN_HOST = re.compile(r"(^|\.)(linkedin\.com|licdn\.com|lnkd\.in)$", re.I)
ALLOWED_PATH = re.compile(r"^/(in|company|school|showcase|groups?)/[^/]+/?$", re.I)
LOGO_WORD = re.compile(r"logo|icon|badge|\bbug\b|-bug|in-blue", re.I)
ICON_CLASS = re.compile(r"(?:\bfa|\bbi|\bbx|icon|logo|social)[-_ ][\w -]*linkedin|linkedin[-_ ]*(?:logo|icon|bug|square)", re.I)

GAP = r"\W+(?:\w+\W+){0,2}"
RULES: List[Tuple[int, str, re.Pattern, str]] = [
    (5, "partner or endorsement claim", re.compile(
        r"(?:official|certified|approved|authori[sz]ed|verified|preferred|accredited)" + GAP + r"linkedin"
        r"|linkedin\W+(?:\w+\W+){0,2}(?:partner|certified|approved|endorsed|accredited)"
        r"|(?:partner\w*|endorsed by|approved by|backed by|powered by|built on|integrat\w+ (?:with|into)|works? with|plugs? into|syncs? with|native\w*)" + GAP + r"linkedin"
    ), "Implies LinkedIn is connected to, approves of or endorses you."),
    (7, "promise of safe automation or beating limits", re.compile(
        r"undetect\w*|bypass\w*|ban.?proof|stealth|get around|no bans?\b|warm.?up"
        r"|avoid\w*" + GAP + r"(?:ban|bans|restrict\w*|limit\w*|detect\w*)"
        r"|safe\w*" + GAP + r"automat\w*|automat\w*" + GAP + r"safe\w*"
        r"|beat\w*" + GAP + r"limit\w*"
    ), "Advertises getting around LinkedIn's limits or detection."),
    (6, "copy saying data comes from LinkedIn", re.compile(
        r"(?:data|leads?|contacts?|profiles?|emails?|prospects?|records?)\W+(?:\w+\W+){0,2}from" + GAP + r"linkedin"
        r"|(?:scrap\w*|extract\w*|export\w*|pull\w*|harvest\w*|crawl\w*|import\w*|enrich\w*)\W+(?:\w+\W+){0,3}linkedin"
        r"|linkedin\W+(?:\w+\W+){0,1}(?:data|profiles|leads?|contacts?|emails|lists?|database|scrap\w*|extract\w*|export\w*|crawl\w*|enrich\w*)"
    ), "Says or suggests your data comes from LinkedIn."),
    (1, "comparison that names LinkedIn", re.compile(
        r"(?:vs\b|versus|compared? (?:to|with)|better than|than|beats?|replac\w*|alternative to|instead of|unlike|like)" + GAP + r"linkedin"
        r"|\b(?:than|vs|versus|like|unlike)\s+linkedin"
        r"|linkedin\W+(?:alternative|vs\b|versus|competitor|comparison)"
    ), "Compares you with LinkedIn by name, the use Artisan's CEO described."),
    (3, "name that contains LinkedIn", re.compile(
        r"\blinkedin\s*(?:ai|bot|pro|boost\w*|hack\w*|wizard|genius|sdr|machine)\b|@linkedin\w+"
    ), "Reads like a product, business or handle built on LinkedIn's name."),
]


@dataclass(frozen=True)
class Finding:
    file: str
    line: int
    severity: str
    check: int
    rule: str
    where: str
    text: str
    why: str


Locate = Callable[[int], int]


def snippet(text: str, start: int = 0, end: Optional[int] = None) -> str:
    end = len(text) if end is None else end
    left = max(0, start - 50)
    if left:
        space = text.find(" ", left, start)
        left = space + 1 if space != -1 else left
    piece = re.sub(r"\s+", " ", text[left:end + 50]).strip()
    return piece[:140]


def window(text: str, start: int, end: int) -> str:
    """The sentence around a mention, in lower case, with every brand word written the same way."""
    left = text[max(0, start - 90):start].replace("vs.", "vs ")
    right = text[end:end + 90].replace("vs.", "vs ")
    cut = max(left.rfind(". "), left.rfind("! "), left.rfind("? "))
    if cut != -1:
        left = left[cut + 2:]
    match = re.search(r"[.!?](\s|$)", right)
    if match:
        right = right[:match.start()]
    joined = re.sub(r"\s+", " ", left + "linkedin" + right).lower()
    return BRAND.sub("linkedin", BRAND_CASED.sub("linkedin", joined))


class Collector:
    def __init__(self, file_label: str) -> None:
        self.file = file_label
        self.findings: List[Finding] = []
        self._seen: Set[Tuple[int, int, str]] = set()

    def add(self, line: int, severity: str, check: int, rule: str, where: str, text: str, why: str) -> None:
        key = (line, check, severity)
        if key in self._seen:
            return
        self._seen.add(key)
        self.findings.append(Finding(self.file, line, severity, check, rule, where, text, why))

    def token(self, token: str, where: str, line: int, allowed: bool) -> None:
        """Classify a link, an email address or a bare domain that holds a brand word."""
        low = token.lower()
        clean = token[7:] if low.startswith("mailto:") else token
        if "@" in clean and "/" not in clean:
            if clean.lower().endswith("@linkedin.com"):
                self.add(line, "medium", 10, "LinkedIn email address", where, clean, "Check why this address is on your site.")
            else:
                self.add(line, "high", 3, "email address containing LinkedIn", where, clean,
                         "LinkedIn's agreement restricts its name in any email.")
            return
        parsed = urlsplit(clean if "://" in clean else f"https://{clean}")
        host = parsed.hostname or ""
        path = parsed.path or "/"
        if LINKEDIN_HOST.search(host):
            if not ALLOWED_PATH.match(path):
                self.add(line, "medium", 9, "deep link into LinkedIn", where, token,
                         "LinkedIn's agreement limits deep links to promoting your profile or a Group.")
            else:
                self.add(line, "info", 9, "link to a profile, company page or group", where, token,
                         "A plain link to your own page is an allowed shape. Confirm it is yours.")
            return
        if BRAND.search(host):
            self.add(line, "high", 2, "LinkedIn in a domain name", where, token,
                     "LinkedIn's Brand Guidelines say not to use a domain that includes its name.")
            return
        is_image = pathlib.PurePath(path).suffix.lower() in IMAGE_SUFFIXES
        if is_image or LOGO_WORD.search(path):
            if allowed:
                self.add(line, "info", 4, "icon inside a link to your own page", where, token,
                         "The [in] Logo may be a hyperlink to your profile or page. Use LinkedIn's own file.")
            else:
                self.add(line, "high", 4, "logo or image file named after LinkedIn", where, token,
                         "Logos have narrow allowed uses. See check 4.")
            return
        self.add(line, "high", 2, "LinkedIn in a URL path", where, token,
                 "LinkedIn's agreement restricts its name in a URL.")

    def segment(self, text: str, where: str, locate: Locate, allowed: bool, default: Tuple[str, int, str, str]) -> None:
        """Scan one run of text. `default` is what a plain mention with no matching rule becomes."""
        spans: List[Tuple[int, int]] = []
        for match in TOKEN.finditer(text):
            token = match.group(0).rstrip(".,;:")
            if BRAND.search(token) or BRAND_CASED.search(token):
                spans.append(match.span())
                self.token(token, where, locate(match.start()), allowed)
        mentions = [*BRAND.finditer(text), *BRAND_CASED.finditer(text)]
        for match in sorted(mentions, key=lambda item: item.start()):
            if any(start <= match.start() < end for start, end in spans):
                continue
            line = locate(match.start())
            around = window(text, match.start(), match.end())
            for check, rule, pattern, why in RULES:
                if pattern.search(around):
                    self.add(line, "high", check, rule, where, snippet(text, match.start(), match.end()), why)
                    break
            else:
                severity, check, rule, why = ("info", 9, "text inside a link to your own page", "Fine as a label on a link to your own page.") if allowed else default
                self.add(line, severity, check, rule, where, snippet(text, match.start(), match.end()), why)


PLAIN_VISIBLE = ("medium", 10, "LinkedIn named in visible copy", "Artisan removed all mentions from its site. Decide if this one is needed.")
PLAIN_HIDDEN = ("medium", 10, "LinkedIn named in a hidden place", "Hidden places count too. Visitors and crawlers can read them.")
PLAIN_PROMINENT = ("medium", 3, "LinkedIn named in a page title or main heading", "LinkedIn's guidelines say not to make its name the most prominent feature.")
PLAIN_CODE = ("low", 10, "LinkedIn named in code or config", "Often harmless, such as a social link setting. Check that it never shows as copy.")


class PageParser(HTMLParser):
    def __init__(self, collector: Collector) -> None:
        super().__init__(convert_charrefs=True)
        self.out = collector
        self.chunks: List[Tuple[str, int]] = []
        self.allowed = False
        self.where = "visible text"

    # Joining the text of one block means "than <em>LinkedIn</em>" is read as one sentence.
    def flush(self) -> None:
        if not self.chunks:
            return
        text = "".join(chunk for chunk, _ in self.chunks)
        chunks = list(self.chunks)
        self.chunks = []

        def locate(offset: int) -> int:
            seen = 0
            for chunk, line in chunks:
                if offset < seen + len(chunk):
                    return line + chunk[:offset - seen].count("\n")
                seen += len(chunk)
            return chunks[-1][1]

        default = PLAIN_PROMINENT if self.where in ("page title", "main heading") else PLAIN_VISIBLE
        self.out.segment(text, self.where, locate, self.allowed, default)

    def _is_allowed_link(self, href: str) -> bool:
        parsed = urlsplit(href if "://" in href else f"https://{href}")
        return bool(LINKEDIN_HOST.search(parsed.hostname or "") and ALLOWED_PATH.match(parsed.path or "/"))

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        line = self.getpos()[0]
        if tag in BLOCK_TAGS or tag == "a":
            self.flush()
        if tag == "title":
            self.where = "page title"
        elif tag == "h1":
            self.where = "main heading"
        if tag == "a":
            href = dict(attrs).get("href") or ""
            self.allowed = bool(href) and self._is_allowed_link(href)
        self._attributes(tag, attrs, line)

    def handle_startendtag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        self.handle_starttag(tag, attrs)

    def _attributes(self, tag: str, attrs: List[Tuple[str, Optional[str]]], line: int) -> None:
        locate: Locate = lambda _offset: line
        for name, value in attrs:
            if not value or not (BRAND.search(value) or BRAND_CASED.search(value)):
                continue
            name = name.lower()
            if name in URL_ATTRS:
                for part in value.split(",") if name == "srcset" else [value]:
                    part = part.strip().split(" ")[0]
                    if BRAND.search(part):
                        self.out.token(part, f"{name} attribute", line, self.allowed)
            elif name in ("class", "id"):
                if ICON_CLASS.search(value):
                    if self.allowed:
                        self.out.add(line, "info", 4, "icon inside a link to your own page", f"{name} attribute", value,
                                     "The [in] Logo may be a hyperlink to your profile or page.")
                    else:
                        self.out.add(line, "high", 4, "LinkedIn icon outside a link to your own page", f"{name} attribute", value,
                                     "The [in] Logo has narrow allowed uses. See check 4.")
                else:
                    self.out.add(line, "low", 10, "LinkedIn named in a class or id", f"{name} attribute", value,
                                 "Usually harmless. Check that nothing visible depends on it.")
            elif tag == "meta" and name == "content":
                self.out.segment(value, "meta tag", locate, False, PLAIN_HIDDEN)
            elif name in TEXT_ATTRS:
                self.out.segment(value, f"{name} attribute", locate, self.allowed, PLAIN_HIDDEN)
            else:
                self.out.segment(value, f"{name} attribute", locate, False, PLAIN_CODE)

    def handle_endtag(self, tag: str) -> None:
        if tag in BLOCK_TAGS or tag == "a":
            self.flush()
        if tag in ("title", "h1"):
            self.where = "visible text"
        if tag == "a":
            self.allowed = False

    def handle_data(self, data: str) -> None:
        if self.cdata_elem in ("script", "style"):
            start = self.getpos()[0]
            for index, text in enumerate(data.splitlines()):
                self.out.segment(text, self.cdata_elem, _fixed(start + index), False, PLAIN_CODE)
            return
        self.chunks.append((data, self.getpos()[0]))

    def handle_comment(self, data: str) -> None:
        start = self.getpos()[0]
        for index, text in enumerate(data.splitlines()):
            self.out.segment(text, "html comment", _fixed(start + index), False, PLAIN_HIDDEN)


def _fixed(line: int) -> Locate:
    return lambda _offset: line


def scan_html(text: str, label: str) -> List[Finding]:
    collector = Collector(label)
    parser = PageParser(collector)
    parser.feed(text)
    parser.close()
    parser.flush()
    return collector.findings


def scan_lines(text: str, label: str, where: str, default: Tuple[str, int, str, str]) -> List[Finding]:
    collector = Collector(label)
    for number, line in enumerate(text.splitlines(), 1):
        collector.segment(line, where, _fixed(number), False, default)
    return collector.findings


def scan_file_name(relative: pathlib.PurePath, label: str) -> List[Finding]:
    if not BRAND.search(str(relative)):
        return []
    collector = Collector(label)
    if relative.suffix.lower() in IMAGE_SUFFIXES:
        collector.add(1, "high", 4, "image file named after LinkedIn", "file name", str(relative),
                      "Open it. If it shows a LinkedIn logo, see check 4.")
    else:
        collector.add(1, "high", 2, "LinkedIn in a file name that may become a URL", "file name", str(relative),
                      "On most sites a file name becomes part of the page address.")
    return collector.findings


def read_text(path: pathlib.Path) -> Optional[str]:
    raw = path.read_bytes()
    if b"\0" in raw[:4096]:
        return None
    return raw.decode("utf-8", errors="replace")


def scan_path(target: pathlib.Path) -> Tuple[List[Finding], int, List[str]]:
    findings: List[Finding] = []
    scanned = 0
    not_read: List[str] = []
    files = [target] if target.is_file() else sorted(p for p in target.rglob("*") if p.is_file())
    base = target.parent if target.is_file() else target
    for path in files:
        relative = path.relative_to(base)
        if any(part in SKIP_DIRS for part in relative.parts) or path.name == ".DS_Store":
            continue
        label = str(relative)
        findings.extend(scan_file_name(relative, label))
        suffix = path.suffix.lower()
        known = suffix in HTML_SUFFIXES | PROSE_SUFFIXES | CODE_SUFFIXES
        if suffix in UNREADABLE_SUFFIXES:
            not_read.append(f"{label} (open it and search by hand)")
            continue
        if not known:
            continue
        if path.stat().st_size > MAX_BYTES:
            not_read.append(f"{label} (larger than {MAX_BYTES} bytes)")
            continue
        text = read_text(path)
        if text is None:
            not_read.append(f"{label} (looks binary)")
            continue
        scanned += 1
        if suffix in HTML_SUFFIXES:
            findings.extend(scan_html(text, label))
        elif suffix in PROSE_SUFFIXES:
            findings.extend(scan_lines(text, label, "visible text", PLAIN_VISIBLE))
        else:
            findings.extend(scan_lines(text, label, "code or data file", PLAIN_CODE))
    return findings, scanned, not_read


def counts(findings: List[Finding]) -> Dict[str, int]:
    tally = {name: 0 for name in SEVERITY_ORDER}
    for item in findings:
        tally[item.severity] += 1
    return tally


def print_text(findings: List[Finding], scanned: int, not_read: List[str]) -> None:
    ordered = sorted(findings, key=lambda f: (-SEVERITY_ORDER[f.severity], f.file, f.line))
    for item in ordered:
        print(f"{item.severity.upper():6} {item.file}:{item.line}  [check {item.check}] {item.rule} ({item.where})")
        print(f"       text: {item.text}")
        print(f"       why:  {item.why}")
    tally = counts(findings)
    print()
    print(f"Files read: {scanned}. High {tally['high']}, medium {tally['medium']}, low {tally['low']}, info {tally['info']}.")
    if not_read:
        print("Not read, check these by hand:")
        for name in not_read:
            print(f"  {name}")
    print("Wording fixes: guides/WEBSITE-WORDING-FIXES.md. The check numbers are in the checks folder.")
    print("A clean result only means no mention was found in these files. It is not a promise and not legal advice.")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Scan a website folder or pasted HTML for LinkedIn name and brand mentions.")
    parser.add_argument("path", nargs="?", help="a folder or a single file")
    parser.add_argument("--stdin", action="store_true", help="read pasted HTML from standard input")
    parser.add_argument("--html", help="HTML passed directly as text")
    parser.add_argument("--json", action="store_true", help="print the results as JSON")
    parser.add_argument("--fail-on", choices=["high", "medium", "low", "never"], default="high",
                        help="lowest severity that makes the exit code 1 (default: high)")
    args = parser.parse_args(argv)

    if sum(bool(item) for item in (args.path, args.stdin, args.html)) != 1:
        print("Give exactly one input: a path, --stdin, or --html. See --help.", file=sys.stderr)
        return 2
    if args.path:
        target = pathlib.Path(args.path)
        if not target.exists():
            print(f"Could not find {args.path}. Check the path and try again.", file=sys.stderr)
            return 2
        findings, scanned, not_read = scan_path(target)
    else:
        pasted = sys.stdin.read() if args.stdin else args.html
        if not pasted or not pasted.strip():
            print("The pasted HTML was empty. Paste your page and try again.", file=sys.stderr)
            return 2
        findings, scanned, not_read = scan_html(pasted, "pasted-html"), 1, []

    if args.json:
        print(json.dumps({
            "scanned_files": scanned,
            "counts": counts(findings),
            "findings": [asdict(item) for item in findings],
            "not_read": not_read,
        }, indent=2))
    else:
        print_text(findings, scanned, not_read)

    if args.fail_on == "never":
        return 0
    limit = SEVERITY_ORDER[args.fail_on]
    return 1 if any(SEVERITY_ORDER[item.severity] >= limit for item in findings) else 0


if __name__ == "__main__":
    sys.exit(main())

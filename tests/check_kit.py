"""Checks that the Outreach Safety Kit is complete, honest and working.

Standard library only, no network, no key. Run from anywhere:

    python3 tests/check_kit.py

Exit code 0 means every check passed. Exit code 1 lists each problem found.
"""

from __future__ import annotations

import ast
import csv
import io
import json
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import kitlib  # noqa: E402

EXPECTED_CHECKS = 30
EXPECTED_PER_GROUP = 10
EXPECTED_QUESTIONS = 30
EXPECTED_WORDING_PAIRS = 24

REQUIRED_FILES = [
    "README.md",
    "QUICK-START-PROMPT.md",
    "SAFETY-AND-LIMITS.md",
    "SOURCES.md",
    "CHANGELOG.md",
    "LICENSE",
    "CLAUDE.md",
    "AGENTS.md",
    ".gitignore",
    ".github/workflows/check.yml",
    ".claude/skills/linkedin-safety-audit/SKILL.md",
    ".claude/commands/linkedin-audit.md",
    "checks/README.md",
    "guides/VENDOR-QUESTIONNAIRE.md",
    "guides/WEBSITE-WORDING-FIXES.md",
    "guides/IF-YOUR-ACCOUNT-IS-RESTRICTED.md",
    "guides/WHAT-HAPPENED-TO-ARTISAN.md",
    "audit/AUDIT-TEMPLATE.csv",
    "audit/HOW-TO-SCORE.md",
    "tools/scan_site.py",
    "tools/lead_list_check.py",
    "tools/score_audit.py",
    "samples/README.md",
]

STDLIB_ALLOWED = {
    "__future__", "argparse", "ast", "csv", "dataclasses", "datetime", "html", "io", "json",
    "pathlib", "re", "subprocess", "sys", "tempfile", "typing", "urllib", "kitlib",
}

BANNED_DASHES = {
    chr(0x2014): "an em dash",
    chr(0x2013): "an en dash",
    chr(0x2012): "a figure dash",
    chr(0x2015): "a horizontal bar",
    chr(0x2212): "a minus sign",
    chr(0x2010): "a unicode hyphen",
    chr(0x2011): "a non breaking hyphen",
}

# Built from parts so this file does not match itself.
SECRET_PATTERNS = [
    ("API key", re.compile("s" + r"k-[A-Za-z0-9_\-]{20,}")),
    ("GitHub token", re.compile("gh" + r"[pousr]_[A-Za-z0-9]{30,}")),
    ("AWS access key", re.compile("AK" + r"IA[0-9A-Z]{16}")),
    ("Slack token", re.compile("xo" + r"x[abpr]-[A-Za-z0-9\-]{10,}")),
    ("Private key block", re.compile("-----BEGIN " + r"[A-Z ]*PRIVATE KEY-----")),
    ("Assigned secret", re.compile(r"(?i)(api[_ ]?key|secret|token|password)\s*[:=]\s*['\"][A-Za-z0-9_\-]{12,}['\"]")),
]
FORBIDDEN_WORDS = ["send" + "ora", "/Us" + "ers/", "co-auth" + "ored", "generated with cla" + "ude"]
EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
ALLOWED_EMAIL = ("example.com", "example.org", "example.net", "example.test")

# A claimed volume of LinkedIn activity. LinkedIn publishes no safe number, so none may appear.
SAFE_NUMBER = re.compile(
    r"(?i)\b\d[\d,]*\s*(?:to\s*\d+\s*)?(?:connection requests?|connection invites?|invites?|invitations?|"
    r"messages?|profile views?|actions?)\s*(?:a|per|each|every)\s*(?:day|week)\b"
)
INVENTED_STAT = re.compile(r"(?i)\b(ban rate|\d+\s*(?:%|percent)\s+of\s+(?:accounts|users|founders|startups))\b")

TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".txt", ".json", ".csv", ".html", ""}
SKIP_DIRS = {".git", "__pycache__"}

errors = []


def fail(message):
    errors.append(message)


def text_files():
    found = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        parts = path.relative_to(ROOT).parts
        if any(part in SKIP_DIRS for part in parts):
            continue
        if parts[:2] == ("audit", "out"):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            found.append(path)
    return found


def normalise(text):
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip()


def run(tool, *args, stdin=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "tools" / tool), *args],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=60,
    )


def check_files():
    for name in REQUIRED_FILES:
        if not (ROOT / name).exists():
            fail(f"missing {name}")


def check_thirty(checks):
    if len(checks) != EXPECTED_CHECKS:
        fail(f"expected exactly {EXPECTED_CHECKS} checks, found {len(checks)}")
    numbers = [c.number for c in checks]
    if numbers != list(range(1, EXPECTED_CHECKS + 1)):
        fail(f"checks must be numbered 1 to {EXPECTED_CHECKS} in order, found {numbers}")
    titles = [c.title for c in checks]
    if len(set(titles)) != len(titles):
        fail("two checks share a title")
    for group, _ in kitlib.GROUPS:
        count = len([c for c in checks if c.group == group])
        if count != EXPECTED_PER_GROUP:
            fail(f"group '{group}': expected {EXPECTED_PER_GROUP} checks, found {count}")


def check_each(checks, sources_text):
    sources_norm = normalise(sources_text)
    for c in checks:
        label = f"check {c.number}"
        if c.priority not in kitlib.PRIORITIES:
            fail(f"{label}: priority must be one of {kitlib.PRIORITIES}, found '{c.priority}'")
        if c.based_on not in kitlib.BASES:
            fail(f"{label}: 'Based on' must be one of {kitlib.BASES}, found '{c.based_on}'")
        for name in kitlib.FIELDS:
            body = c.sections.get(name, "")
            if len(body) < 40:
                fail(f"{label}: section '{name}' is missing or too short")
        test = c.sections.get("Pass or fail test", "")
        if "**Pass:**" not in test or "**Fail:**" not in test:
            fail(f"{label}: needs both a **Pass:** and a **Fail:** line")
        source = c.sections.get("Source", "")
        urls = re.findall(r"https?://[^\s)>]+", source)
        if not urls:
            fail(f"{label}: source has no link")
        if c.based_on == "LinkedIn rule" and not any("linkedin.com" in u for u in urls):
            fail(f"{label}: a LinkedIn rule must link one of LinkedIn's own pages")
        if c.based_on == "LinkedIn rule" and not re.search(r"^\s*>\s", source, re.M):
            fail(f"{label}: a LinkedIn rule must quote LinkedIn's own words")
        for url in urls:
            if url.rstrip(".,") not in sources_text:
                fail(f"{label}: link not listed in SOURCES.md: {url}")
        for line in source.splitlines():
            stripped = line.strip()
            if stripped.startswith("> ") and normalise(stripped[2:]) not in sources_norm:
                fail(f"{label}: quote not found in SOURCES.md: {stripped[2:60]}")


def check_template(checks):
    path = ROOT / "audit" / "AUDIT-TEMPLATE.csv"
    if not path.exists():
        return
    rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
    if len(rows) != EXPECTED_CHECKS:
        fail(f"audit template: expected {EXPECTED_CHECKS} rows, found {len(rows)}")
    for row, c in zip(rows, checks):
        if row["check"] != str(c.number) or row["title"] != c.title or row["priority"] != c.priority:
            fail(f"audit template row {row['check']} does not match check {c.number}")
        if row["status"].strip():
            fail(f"audit template row {row['check']} should have an empty status")
    fresh = run("score_audit.py", "new", "--out", "-")
    if fresh.returncode != 0 or fresh.stdout.replace("\r\n", "\n") != path.read_text(encoding="utf-8").replace("\r\n", "\n"):
        fail("audit template differs from `score_audit.py new` output")


def count_guides():
    questions = wording = 0
    path = ROOT / "guides" / "VENDOR-QUESTIONNAIRE.md"
    if path.exists():
        questions = len(re.findall(r"^### Q\d+\.", path.read_text(encoding="utf-8"), re.M))
    path = ROOT / "guides" / "WEBSITE-WORDING-FIXES.md"
    if path.exists():
        wording = len(re.findall(r"^### Example \d+:", path.read_text(encoding="utf-8"), re.M))
    return questions, wording


def check_counts(checks):
    questions, wording = count_guides()
    if questions != EXPECTED_QUESTIONS:
        fail(f"vendor questionnaire: expected {EXPECTED_QUESTIONS} questions, found {questions}")
    if wording != EXPECTED_WORDING_PAIRS:
        fail(f"wording guide: expected {EXPECTED_WORDING_PAIRS} before and after examples, found {wording}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
    for phrase in (f"{len(checks)} checks", f"{questions} question", f"{wording} before and after"):
        if phrase not in readme:
            fail(f"README.md does not state the real count: '{phrase}'")
    index = ROOT / "checks" / "README.md"
    if index.exists():
        text = index.read_text(encoding="utf-8")
        for c in checks:
            if f"| {c.number} |" not in text or c.title not in text:
                fail(f"checks/README.md does not list check {c.number}: {c.title}")


def check_scanner():
    risky = run("scan_site.py", str(ROOT / "samples/site-risky"), "--json")
    if risky.returncode != 1:
        fail(f"scan_site.py on the risky sample should exit 1, got {risky.returncode}: {risky.stderr[:200]}")
        return
    report = json.loads(risky.stdout)
    found = {(pathlib.PurePath(f["file"]).name, f["check"]) for f in report["findings"] if f["severity"] == "high"}
    expected_path = ROOT / "samples" / "site-risky-expected.json"
    expected = json.loads(expected_path.read_text(encoding="utf-8"))["must_find_high"]
    for item in expected:
        if (item["file"], item["check"]) not in found:
            fail(f"scanner missed a planted problem: {item['file']} check {item['check']}")
    covered = {f["check"] for f in report["findings"]}
    for number in (1, 2, 3, 4, 5, 6, 7, 9, 10):
        if number not in covered:
            fail(f"scanner produced no finding for check {number} on the risky sample")

    clean = run("scan_site.py", str(ROOT / "samples/site-clean"), "--json")
    if clean.returncode != 0:
        fail(f"scan_site.py on the clean sample should exit 0, got {clean.returncode}")
    else:
        rep = json.loads(clean.stdout)
        bad = [f for f in rep["findings"] if f["severity"] in ("high", "medium")]
        if bad:
            fail(f"clean sample has high or medium findings: {bad[:2]}")
        if not any(f["severity"] == "info" for f in rep["findings"]):
            fail("clean sample should show its allowed company page link as info")

    cases = [
        # (pasted HTML, expected check or None, expected severity or None)
        ('<p>Fresher contacts than LinkedIn.</p>', 1, "high"),
        ('<p>Fresher <b>contacts</b> than <em>LinkedIn</em>.</p>', 1, "high"),
        ('<p>Official LinkedIn partner</p>', 5, "high"),
        ('<p>We pull data from LinkedIn every night.</p>', 6, "high"),
        ('<p>Undetectable LinkedIn automation.</p>', 7, "high"),
        ('<a href="https://linkedin-leads.example.com/">x</a>', 2, "high"),
        ('<a href="https://www.linkedin.com/search/results/people/">x</a>', 9, "medium"),
        ('<img src="/img/linkedin-logo.png" alt="">', 4, "high"),
        ('<meta name="keywords" content="sdr, linkedin scraper">', 6, "high"),
        ('<img src="a.png" alt="our linkedin lead list">', 6, "high"),
        ('<!-- compared to LinkedIn -->', 1, "high"),
        ('<a href="mailto:linkedin@example.com">x</a>', 3, "high"),
        ('<p>Export your Sales Navigator lists here.</p>', 6, "high"),
    ]
    for html_text, want_check, want_sev in cases:
        out = run("scan_site.py", "--stdin", "--json", "--fail-on", "never", stdin=html_text)
        if out.returncode != 0:
            fail(f"--stdin failed on {html_text}: {out.stderr[:200]}")
            continue
        got = {(f["check"], f["severity"]) for f in json.loads(out.stdout)["findings"]}
        if (want_check, want_sev) not in got:
            fail(f"scanner: {html_text} expected check {want_check} {want_sev}, got {sorted(got)}")

    negatives = [
        "<p>Your CRM is linked in real time to your inbox.</p>",
        "<p>class LinkedList { } and a linked item.</p>",
        '<a href="https://example.com/about">About us</a>',
    ]
    for html_text in negatives:
        out = run("scan_site.py", "--stdin", "--json", "--fail-on", "never", stdin=html_text)
        if json.loads(out.stdout)["findings"]:
            fail(f"scanner false alarm on: {html_text}")

    allowed = '<a href="https://www.linkedin.com/company/example-co/"><img src="/icons/linkedin.svg" alt="LinkedIn"></a>'
    out = run("scan_site.py", "--stdin", "--json", "--fail-on", "never", stdin=allowed)
    severities = {f["severity"] for f in json.loads(out.stdout)["findings"]}
    if severities != {"info"}:
        fail(f"a linked company page icon should be info only, got {severities}")

    with tempfile.TemporaryDirectory() as tmp:
        folder = pathlib.Path(tmp)
        (folder / "linkedin-banner.png").write_bytes(b"\x89PNG\r\n\x00\x00")
        out = run("scan_site.py", tmp, "--json", "--fail-on", "never")
        rep = json.loads(out.stdout)
        if not any(f["check"] == 4 and f["severity"] == "high" for f in rep["findings"]):
            fail("scanner should flag a file named after the logo")
        (folder / "deck.pdf").write_bytes(b"%PDF-1.7\x00\x00")
        out = run("scan_site.py", tmp, "--json", "--fail-on", "never")
        if "deck.pdf" not in " ".join(json.loads(out.stdout)["not_read"]):
            fail("scanner must list files it could not read instead of skipping them silently")

    missing = run("scan_site.py", "/no/such/folder/anywhere")
    if missing.returncode != 2 or "Traceback" in missing.stderr:
        fail("scanner should exit 2 with a plain message on a missing folder")
    empty = run("scan_site.py", "--stdin", stdin="")
    if empty.returncode != 2:
        fail("scanner should exit 2 on empty pasted input")


def check_lead_tool():
    risky = run("lead_list_check.py", str(ROOT / "samples/lead-lists/list-risky.csv"), "--json")
    if risky.returncode != 1:
        fail(f"lead_list_check.py on the risky list should exit 1, got {risky.returncode}: {risky.stderr[:200]}")
    else:
        rep = json.loads(risky.stdout)
        if not rep["files"][0]["high"]:
            fail("risky lead list should raise a high signal")
        if "@" in risky.stdout:
            fail("lead_list_check.py must not print cell values such as email addresses")
    clean = run("lead_list_check.py", str(ROOT / "samples/lead-lists/list-clean.csv"), "--json")
    if clean.returncode != 0:
        fail(f"lead_list_check.py on the clean list should exit 0, got {clean.returncode}")
    missing = run("lead_list_check.py", "/no/such/file.csv")
    if missing.returncode != 2 or "Traceback" in missing.stderr:
        fail("lead_list_check.py should exit 2 with a plain message on a missing file")


def check_score_tool(checks):
    sample = ROOT / "samples/audit/filled-audit.csv"
    out = run("score_audit.py", "score", str(sample), "--json")
    if out.returncode != 1:
        fail(f"score_audit.py on the sample should exit 1 (open fix first items), got {out.returncode}: {out.stderr[:200]}")
        return
    rep = json.loads(out.stdout)
    rows = list(csv.DictReader(sample.open(encoding="utf-8", newline="")))
    points = {"pass": 2, "partial": 1, "fail": 0}
    earned = sum(points[r["status"].lower()] for r in rows if r["status"].lower() in points)
    possible = 2 * len([r for r in rows if r["status"].lower() in points])
    if rep["earned"] != earned or rep["possible"] != possible:
        fail(f"score mismatch: tool {rep['earned']}/{rep['possible']}, hand count {earned}/{possible}")
    if not rep["fix_first_open"]:
        fail("sample audit should list open fix first items")

    blank = run("score_audit.py", "score", str(ROOT / "audit/AUDIT-TEMPLATE.csv"), "--json")
    rep = json.loads(blank.stdout)
    if rep["earned"] != 0 or len(rep["not_answered"]) != EXPECTED_CHECKS or blank.returncode != 1:
        fail("a blank audit must score 0, list every check as not answered and exit 1")

    if "Fix first" not in rep["verdict"]:
        fail("an incomplete audit must still say how many Fix first items are open")

    buf = io.StringIO()
    rows_all = list(csv.DictReader((ROOT / "audit/AUDIT-TEMPLATE.csv").open(encoding="utf-8", newline="")))
    writer = csv.DictWriter(buf, fieldnames=list(rows_all[0].keys()))
    writer.writeheader()
    for row in rows_all:
        writer.writerow({**row, "status": "maybe"})
    with tempfile.TemporaryDirectory() as tmp:
        bad = pathlib.Path(tmp) / "bad.csv"
        bad.write_text(buf.getvalue(), encoding="utf-8")
        out = run("score_audit.py", "score", str(bad))
        if out.returncode != 2 or "Traceback" in out.stderr:
            fail("score_audit.py should exit 2 with a plain message on an unknown status")
        report = pathlib.Path(tmp) / "report.md"
        out = run("score_audit.py", "score", str(sample), "--out", str(report))
        if not report.exists() or "not legal advice" not in report.read_text(encoding="utf-8").lower():
            fail("score_audit.py --out must write a report that says it is not legal advice")


def check_stdlib_only():
    for path in list((ROOT / "tools").glob("*.py")) + list((ROOT / "tests").glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module.split(".")[0]]
            for name in names:
                if name not in STDLIB_ALLOWED:
                    fail(f"{path.relative_to(ROOT)}: imports '{name}', tools must be standard library only")


def check_samples():
    folder = ROOT / "samples"
    for path in sorted(folder.rglob("*")):
        if path.is_file() and path.name != ".DS_Store" and "__pycache__" not in path.parts:
            if "synthetic" not in path.read_text(encoding="utf-8").lower():
                fail(f"{path.relative_to(ROOT)}: sample must be labelled synthetic")


def check_prompts():
    prompt = (ROOT / "QUICK-START-PROMPT.md").read_text(encoding="utf-8")
    if "```text" not in prompt:
        fail("QUICK-START-PROMPT.md has no paste in prompt block")
    skill = (ROOT / ".claude/skills/linkedin-safety-audit/SKILL.md").read_text(encoding="utf-8")
    if not re.match(r"---\nname: linkedin-safety-audit\ndescription: .{40,}\n---", skill):
        fail("skill needs frontmatter with a name and a real description")
    command = (ROOT / ".claude/commands/linkedin-audit.md").read_text(encoding="utf-8")
    if not command.startswith("---\ndescription:"):
        fail("command needs frontmatter with a description")
    for name, text in (("prompt", prompt), ("skill", skill)):
        for tool in ("scan_site.py", "lead_list_check.py", "score_audit.py"):
            if tool not in text:
                fail(f"{name} does not use {tool}")


def check_safety_doc():
    text = (ROOT / "SAFETY-AND-LIMITS.md").read_text(encoding="utf-8").lower()
    for phrase in ("not legal advice", "does not publish", "safe list", "not affiliated"):
        if phrase not in text:
            fail(f"SAFETY-AND-LIMITS.md must say '{phrase}'")
    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    for phrase in ("not legal advice", "not affiliated", "synthetic"):
        if phrase not in readme:
            fail(f"README.md must say '{phrase}'")


def check_attribution():
    case = (ROOT / "guides/WHAT-HAPPENED-TO-ARTISAN.md").read_text(encoding="utf-8")
    if "TechCrunch" not in case or "CEO" not in case:
        fail("the Artisan guide must attribute the reasons to the CEO's account to TechCrunch")
    for path in text_files():
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        if "HeyReach" in text and "self reported" not in text.lower():
            fail(f"{path.relative_to(ROOT)}: HeyReach is named without saying it is self reported")


def check_links():
    for path in text_files():
        if path.suffix != ".md":
            continue
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            if not (path.parent / target.split("#")[0]).resolve().exists():
                fail(f"{path.relative_to(ROOT)}: broken link to '{target}'")


def check_clean_text():
    for path in text_files():
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        for word in FORBIDDEN_WORDS:
            if word in lower:
                fail(f"{rel}: contains a forbidden word or path ({word[:4]}...)")
        is_test = rel.parts[0] == "tests"
        for lineno, line in enumerate(text.splitlines(), 1):
            for char, name in BANNED_DASHES.items():
                if char in line:
                    fail(f"{rel}:{lineno}: contains {name}")
            if path.suffix == ".md" and " - " in line.lstrip("- ").strip():
                fail(f"{rel}:{lineno}: a spaced hyphen is used as a dash")
            for name, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    fail(f"{rel}:{lineno}: looks like a {name}")
            for email in EMAIL.findall(line):
                if not email.lower().endswith(ALLOWED_EMAIL):
                    fail(f"{rel}:{lineno}: contains an email address ({email})")
            if not is_test and rel.parts[0] != "samples" and SAFE_NUMBER.search(line):
                fail(f"{rel}:{lineno}: states a volume of activity, LinkedIn publishes no safe number")
            if not is_test and INVENTED_STAT.search(line):
                fail(f"{rel}:{lineno}: looks like an invented statistic")
            if "github.com/" in line and "/rele" + "ases" in line:
                fail(f"{rel}:{lineno}: GitHub links must be the repo home page")


def main():
    check_files()
    if any(e.startswith("missing") for e in errors):
        print(f"FAILED with {len(errors)} problem(s):")
        for err in errors:
            print(f"  {err}")
        return 1
    checks = kitlib.load_checks(ROOT)
    sources = (ROOT / "SOURCES.md").read_text(encoding="utf-8")
    check_thirty(checks)
    check_each(checks, sources)
    check_template(checks)
    check_counts(checks)
    check_scanner()
    check_lead_tool()
    check_score_tool(checks)
    check_stdlib_only()
    check_samples()
    check_prompts()
    check_safety_doc()
    check_attribution()
    check_links()
    check_clean_text()

    questions, wording = count_guides()
    print(f"Checks: {len(checks)} ({', '.join(f'{g} {len([c for c in checks if c.group == g])}' for g, _ in kitlib.GROUPS)})")
    print(f"Fix first checks: {len([c for c in checks if c.priority == 'Fix first'])}")
    print(f"Vendor questions: {questions}")
    print(f"Before and after wording examples: {wording}")
    print(f"Text files scanned: {len(text_files())}")
    print("Tools exercised: scan_site.py, lead_list_check.py, score_audit.py")
    if errors:
        print(f"\nFAILED with {len(errors)} problem(s):")
        for err in errors:
            print(f"  {err}")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

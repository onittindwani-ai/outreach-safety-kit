"""Create a blank audit sheet and score a filled one.

Usage:
    python3 tools/score_audit.py new --out audit/out/my-audit.csv
    python3 tools/score_audit.py score audit/out/my-audit.csv
    python3 tools/score_audit.py score audit/out/my-audit.csv --out audit/out/report.md

Scoring: pass is 2 points, partial is 1, fail is 0, na leaves the check out of the
total. A blank status is reported as not answered and earns nothing.

The score only adds up your own answers. It does not predict what LinkedIn will
do and it is not legal advice.

Exit codes: 0 every check answered and no Fix first item open,
1 something is still open or unanswered, 2 the sheet could not be read.
"""

from __future__ import annotations

import argparse
import csv
import datetime
import json
import pathlib
import sys
from typing import Dict, List, Optional

import kitlib

COLUMNS = ["check", "group", "title", "priority", "status", "evidence", "owner", "due"]
POINTS = {"pass": 2, "partial": 1, "fail": 0}
VALID = set(POINTS) | {"na", ""}


class SheetError(Exception):
    pass


def new_sheet(out: str, force: bool) -> int:
    checks = kitlib.load_checks()
    if out == "-":
        handle = sys.stdout
    else:
        path = pathlib.Path(out)
        if path.exists() and not force:
            print(f"{out} already exists. Use --force to replace it.", file=sys.stderr)
            return 2
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = path.open("w", encoding="utf-8", newline="")
    writer = csv.writer(handle, lineterminator="\n")
    writer.writerow(COLUMNS)
    for check in checks:
        writer.writerow([check.number, check.group, check.title, check.priority, "", "", "", ""])
    if out != "-":
        handle.close()
        print(f"Wrote a blank audit with {len(checks)} checks to {out}")
    return 0


def read_sheet(path: pathlib.Path) -> List[Dict[str, str]]:
    if not path.is_file():
        raise SheetError(f"Could not find the file {path}. Check the path and try again.")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = [name for name in COLUMNS if name not in (reader.fieldnames or [])]
        if missing:
            raise SheetError(f"The sheet is missing these columns: {', '.join(missing)}.")
        rows = list(reader)
    numbers = sorted(int(row["check"]) for row in rows if row["check"].strip().isdigit())
    expected = [check.number for check in kitlib.load_checks()]
    if numbers != expected:
        raise SheetError(f"The sheet must have one row for each of the {len(expected)} checks. Make a fresh one with `new`.")
    for row in rows:
        status = row["status"].strip().lower()
        if status not in VALID:
            raise SheetError(f"Check {row['check']} has status '{row['status']}'. Use pass, partial, fail or na.")
    return sorted(rows, key=lambda row: int(row["check"]))


def score(rows: List[Dict[str, str]]) -> Dict[str, object]:
    groups: Dict[str, Dict[str, int]] = {}
    fix_first: List[Dict[str, str]] = []
    other_open: List[Dict[str, str]] = []
    unanswered: List[int] = []
    earned = possible = 0
    for row in rows:
        status = row["status"].strip().lower()
        group = groups.setdefault(row["group"], {"earned": 0, "possible": 0})
        if status == "":
            unanswered.append(int(row["check"]))
            group["possible"] += 2
            possible += 2
            continue
        if status == "na":
            continue
        group["earned"] += POINTS[status]
        group["possible"] += 2
        earned += POINTS[status]
        possible += 2
        if status != "pass":
            bucket = fix_first if row["priority"] == "Fix first" else other_open
            bucket.append({"check": row["check"], "title": row["title"], "status": status, "owner": row["owner"], "due": row["due"]})
    if unanswered:
        verdict = f"INCOMPLETE: {len(unanswered)} check(s) not answered, {len(fix_first)} Fix first item(s) open so far"
    elif fix_first:
        verdict = "FIX FIRST ITEMS OPEN"
    elif other_open:
        verdict = "NO FIX FIRST ITEMS OPEN: finish the remaining items"
    else:
        verdict = "EVERY ANSWERED CHECK PASSES, on your own evidence"
    percent = round(100 * earned / possible) if possible else 0
    return {
        "earned": earned,
        "possible": possible,
        "percent": percent,
        "groups": groups,
        "fix_first_open": fix_first,
        "other_open": other_open,
        "not_answered": unanswered,
        "verdict": verdict,
    }


def report_text(result: Dict[str, object], rows: List[Dict[str, str]], date: str) -> str:
    lines = [
        "# LinkedIn safety audit report",
        "",
        f"Date: {date}",
        "",
        f"**Result: {result['verdict']}**",
        "",
        f"Score: {result['earned']} of {result['possible']} points ({result['percent']} percent).",
        "",
        "This report is not legal advice. LinkedIn does not publish a safe list, so no score here can promise anything. "
        "The score only adds up the answers written in this audit.",
        "",
        "## Score by group",
        "",
        "| Group | Points |",
        "| --- | --- |",
    ]
    for name, data in result["groups"].items():
        lines.append(f"| {name} | {data['earned']} of {data['possible']} |")
    lines += ["", "## Fix first", ""]
    if result["fix_first_open"]:
        lines += ["| Check | Title | Status | Owner | Due |", "| --- | --- | --- | --- | --- |"]
        for item in result["fix_first_open"]:
            lines.append(f"| {item['check']} | {item['title']} | {item['status']} | {item['owner']} | {item['due']} |")
    else:
        lines.append("No Fix first item is open.")
    lines += ["", "## Other open items", ""]
    if result["other_open"]:
        lines += ["| Check | Title | Status | Owner | Due |", "| --- | --- | --- | --- | --- |"]
        for item in result["other_open"]:
            lines.append(f"| {item['check']} | {item['title']} | {item['status']} | {item['owner']} | {item['due']} |")
    else:
        lines.append("None.")
    if result["not_answered"]:
        lines += ["", "## Not answered", "", "| Check | Title | Priority |", "| --- | --- | --- |"]
        for row in rows:
            if int(row["check"]) in result["not_answered"]:
                lines.append(f"| {row['check']} | {row['title']} | {row['priority']} |")
    lines += ["", "## All 30 answers", "", "| Check | Title | Priority | Status | Evidence |", "| --- | --- | --- | --- | --- |"]
    for row in rows:
        evidence = row["evidence"].replace("|", "/").replace("\n", " ")
        lines.append(f"| {row['check']} | {row['title']} | {row['priority']} | {row['status'] or 'not answered'} | {evidence} |")
    return "\n".join(lines) + "\n"


def print_summary(result: Dict[str, object]) -> None:
    print(result["verdict"])
    print(f"Score: {result['earned']} of {result['possible']} points ({result['percent']} percent)")
    for name, data in result["groups"].items():
        print(f"  {name}: {data['earned']} of {data['possible']}")
    if result["fix_first_open"]:
        print("Fix first:")
        for item in result["fix_first_open"]:
            print(f"  Check {item['check']}: {item['title']} ({item['status']})")
    if result["not_answered"]:
        print("Not answered: " + ", ".join(str(n) for n in result["not_answered"]))
    print("This score only adds up your own answers. It is not legal advice and does not predict what LinkedIn will do.")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Create or score the 30 check audit sheet.")
    sub = parser.add_subparsers(dest="command", required=True)
    make = sub.add_parser("new", help="write a blank audit sheet")
    make.add_argument("--out", required=True, help="file to write, or - for the screen")
    make.add_argument("--force", action="store_true", help="replace an existing file")
    grade = sub.add_parser("score", help="score a filled audit sheet")
    grade.add_argument("sheet", help="the filled CSV file")
    grade.add_argument("--out", help="also write a Markdown report to this file")
    grade.add_argument("--date", default=datetime.date.today().isoformat(), help="date printed on the report")
    grade.add_argument("--json", action="store_true", help="print the result as JSON")
    args = parser.parse_args(argv)

    if args.command == "new":
        return new_sheet(args.out, args.force)
    try:
        rows = read_sheet(pathlib.Path(args.sheet))
    except SheetError as error:
        print(str(error), file=sys.stderr)
        return 2
    result = score(rows)
    if args.out:
        out = pathlib.Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report_text(result, rows, args.date), encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_summary(result)
        if args.out:
            print(f"Report written to {args.out}")
    return 0 if not result["not_answered"] and not result["fix_first_open"] else 1


if __name__ == "__main__":
    sys.exit(main())

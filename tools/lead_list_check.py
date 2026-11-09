"""Look at lead list CSV files for signs the data may trace back to LinkedIn.

Usage:
    python3 tools/lead_list_check.py path/to/list.csv
    python3 tools/lead_list_check.py list-a.csv list-b.csv --json

What it does: reads column names and counts how many cells hold a LinkedIn link
or a suspicious source value. It also tells you when a list has no record of
where it came from.

What it does not do: it never prints names, emails or any other cell value, and
it never sends the file anywhere. A signal is a reason to ask your vendor, not
proof of scraping. No signal is not proof the list is clean. Not legal advice.

Exit codes: 0 no high signals, 1 at least one high signal, 2 a file could not be read.
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
import sys
from typing import Dict, List, Optional

HIGH_COLUMN = re.compile(r"linkedin|sales_?nav|salesnav|lead_?urn|vmid|public_?identifier|\bli_(url|profile|id)\b", re.I)
MEDIUM_COLUMN = re.compile(r"^(headline|summary|about|connections?|connection_count|followers?|skills|recommendations|open_to_work|profile_url)$", re.I)
SOURCE_COLUMN = re.compile(r"^(data_)?(source|origin|provider|vendor)(_name)?$", re.I)
DATE_COLUMN = re.compile(r"(acquired|collected|sourced|purchased|source_date|verified)(_at|_on|_date)?", re.I)
OPT_OUT_COLUMN = re.compile(r"opt_?out|unsubscrib|do_?not_?contact|suppress", re.I)
LINKEDIN_CELL = re.compile(r"linkedin\.com/|lnkd\.in/", re.I)
SOURCE_VALUE = re.compile(r"linkedin|sales\s*nav|scrap|phantom|chrome\s*ext|extension|crawl", re.I)


def check_file(path: pathlib.Path) -> Dict[str, object]:
    high: List[str] = []
    medium: List[str] = []
    notes: List[str] = []
    with path.open(encoding="utf-8-sig", errors="replace", newline="") as handle:
        reader = csv.reader(handle)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError("the file is empty") from None
        cleaned = [name.strip().replace(" ", "_") for name in header]
        for name in cleaned:
            if HIGH_COLUMN.search(name):
                high.append(f"column '{name}' names LinkedIn or one of its identifiers")
            elif MEDIUM_COLUMN.match(name):
                medium.append(f"column '{name}' is a field LinkedIn profiles commonly show")
        source_index = [i for i, name in enumerate(cleaned) if SOURCE_COLUMN.match(name)]
        link_cells: Dict[str, int] = {}
        source_hits = 0
        rows = 0
        for row in reader:
            rows += 1
            for index, value in enumerate(row[:len(cleaned)]):
                if LINKEDIN_CELL.search(value):
                    link_cells[cleaned[index]] = link_cells.get(cleaned[index], 0) + 1
                if index in source_index and SOURCE_VALUE.search(value):
                    source_hits += 1
    for name, count in sorted(link_cells.items()):
        high.append(f"column '{name}' has {count} cell(s) holding a LinkedIn link")
    if source_hits:
        high.append(f"{source_hits} row(s) name LinkedIn, scraping or a browser extension as the source")
    if not source_index:
        notes.append("no source column, so you cannot show where each record came from (check 16)")
    if not any(DATE_COLUMN.search(name) for name in cleaned):
        notes.append("no date column, so you cannot show when each record was obtained (check 16)")
    if not any(OPT_OUT_COLUMN.search(name) for name in cleaned):
        notes.append("no opt out or suppression column (check 19)")
    return {"file": str(path), "rows": rows, "high": high, "medium": medium, "notes": notes}


def print_text(results: List[Dict[str, object]]) -> None:
    for item in results:
        verdict = "NEEDS REVIEW" if item["high"] else "NO HIGH SIGNALS"
        print(f"{item['file']}: {item['rows']} rows, {verdict}")
        for label in ("high", "medium", "notes"):
            for line in item[label]:
                print(f"  {label.upper():6} {line}")
    print()
    print("A signal is a reason to ask your vendor, not proof of scraping. No signal is not proof the list is clean.")
    print("Next step: guides/VENDOR-QUESTIONNAIRE.md. Not legal advice.")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Check lead list CSV files for LinkedIn signals.")
    parser.add_argument("paths", nargs="+", help="one or more CSV files")
    parser.add_argument("--json", action="store_true", help="print the results as JSON")
    args = parser.parse_args(argv)

    results: List[Dict[str, object]] = []
    for name in args.paths:
        path = pathlib.Path(name)
        if not path.is_file():
            print(f"Could not find the file {name}. Check the path and try again.", file=sys.stderr)
            return 2
        try:
            results.append(check_file(path))
        except (ValueError, csv.Error) as error:
            print(f"Could not read {name} as a CSV file: {error}", file=sys.stderr)
            return 2

    if args.json:
        print(json.dumps({"files": results}, indent=2))
    else:
        print_text(results)
    return 1 if any(item["high"] for item in results) else 0


if __name__ == "__main__":
    sys.exit(main())

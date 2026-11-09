---
description: Run the 30 check LinkedIn safety audit and write a scored report
---

Use the `linkedin-safety-audit` skill to walk me through the audit.

Start with `python3 tests/check_kit.py`, then create `audit/out/my-audit.csv` and go through the website, data and outreach groups in order. Run the scanner and the lead list tool where they apply. Finish with `python3 tools/score_audit.py score audit/out/my-audit.csv --out audit/out/report.md`.

Never log in to LinkedIn, never send anything, and never change my files until I have seen the findings and said yes.

$ARGUMENTS

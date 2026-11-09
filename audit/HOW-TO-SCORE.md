# How to score your audit

Make your own copy of the sheet so the blank one stays clean. The folder `audit/out/` is ignored by git.

```bash
python3 tools/score_audit.py new --out audit/out/my-audit.csv
```

For each of the 30 checks fill in four columns:

| Column | What to write |
| --- | --- |
| `status` | `pass`, `partial`, `fail` or `na` |
| `evidence` | What you looked at. A file, a saved reply, a scan date. "We think so" is not evidence |
| `owner` | The one person responsible |
| `due` | The date it will be fixed, if it is not a pass |

Then score it:

```bash
python3 tools/score_audit.py score audit/out/my-audit.csv --out audit/out/report.md
```

## The points

| Status | Points | When to use it |
| --- | --- | --- |
| pass | 2 | The pass test is met everywhere, and you have evidence |
| partial | 1 | It passes in some places, or the fix has started and is not finished |
| fail | 0 | The fail test is met |
| na | left out | The check truly does not apply. Write why in the evidence column |
| blank | 0 | Reported as not answered |

## How to read the result

| Result | Meaning |
| --- | --- |
| INCOMPLETE | At least one check is not answered. It still tells you how many Fix first items are open so far |
| FIX FIRST ITEMS OPEN | At least one Fix first check is partial or fail. Your score does not matter until these are closed |
| NO FIX FIRST ITEMS OPEN | The Fix first checks pass. Work through the rest |
| EVERY ANSWERED CHECK PASSES | Every answer you wrote passes. It is still your own assessment |

The Fix first and Fix soon labels are this kit's own judgement about what to do first. LinkedIn does not rank its rules.

## What the score is not

The score only adds up your own answers. It is not a measure of how likely LinkedIn is to act, because nobody outside LinkedIn knows that. A perfect score is not a guarantee. This is not legal advice. Run the audit again after any big change to your site, your vendors or your tools.

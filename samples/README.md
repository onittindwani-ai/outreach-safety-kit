# Sample data

Everything in this folder is synthetic. ExampleCo, every person, every email address, every vendor and every number here is made up for practice and for the kit's own tests. None of it is a real customer, a real vendor or real lead data, and none of it describes a real company.

| Path | What it is |
| --- | --- |
| `site-risky/` | A made up website with planted problems. The scanner should find them |
| `site-clean/` | A made up website with only a link to its own company page |
| `site-risky-expected.json` | The planted problems the kit's own test expects the scanner to find |
| `lead-lists/list-risky.csv` | A made up lead list that shows signs of LinkedIn sourcing |
| `lead-lists/list-clean.csv` | A made up lead list with a source, a date and an opt out column |
| `vendor-answers/` | Made up replies to the vendor questionnaire, one clear and one evasive |
| `audit/filled-audit.csv` | A made up completed audit |
| `audit/sample-report.md` | The report the score tool produces from that audit |

Try them:

```bash
python3 tools/scan_site.py samples/site-risky
python3 tools/scan_site.py samples/site-clean
python3 tools/lead_list_check.py samples/lead-lists/list-risky.csv
python3 tools/score_audit.py score samples/audit/filled-audit.csv
```

The risky site is meant to be hard. It hides problems in meta tags, alt text, comments, a file name and text broken across tags. It also has a plain sentence using the words "linked in", which must not be flagged.

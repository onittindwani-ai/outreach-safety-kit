# Outreach Safety Kit

If you came here from the Reel, this is the LinkedIn safety checklist it mentions. This is an independent resource and is not affiliated with or endorsed by LinkedIn.

**30 checks for AI SDR founders, covering your website, your data vendors and your outreach, with the tools to run them.**

If you are building or starting an AI SDR (AI sales development rep) business, your website, your data vendors and your outreach can each put your LinkedIn presence at risk. In December 2025, LinkedIn banned the AI SDR startup Artisan. According to what its CEO told TechCrunch, the two issues were LinkedIn's name on Artisan's website and an allegation that its data brokers had scraped LinkedIn without permission.

This kit helps you check for the same issues in your own business. It is an independent kit, not affiliated with or endorsed by LinkedIn. It is not legal advice, and it cannot promise you will not be restricted. Please read [SAFETY-AND-LIMITS.md](SAFETY-AND-LIMITS.md).

## Quick start

Open Claude Code or Codex, then paste the prompt in [QUICK-START-PROMPT.md](QUICK-START-PROMPT.md). It walks you through every check and writes a scored report on your machine.

Prefer to run it yourself? You need Python 3.9 or newer and nothing else.

```bash
python3 tests/check_kit.py                     # confirm the kit works
python3 tools/scan_site.py path/to/your/site   # find LinkedIn mentions in your site
python3 tools/lead_list_check.py your-list.csv # look for signs of LinkedIn sourcing
python3 tools/score_audit.py new --out audit/out/my-audit.csv
```

## What is inside

| Part | Path | What it does |
| --- | --- | --- |
| 30 checks in 3 groups | [checks/](checks/README.md) | What to look at, how to check it, the pass or fail test, the fix and the source for each |
| Website and marketing pages | [checks 1 to 10](checks/1-website-and-marketing-pages.md) | LinkedIn's name, logos, partner claims, hidden mentions |
| Data vendors and lead lists | [checks 11 to 20](checks/2-data-vendors-and-lead-lists.md) | Where your data really comes from, and how to prove it |
| Outreach and automation | [checks 21 to 30](checks/3-outreach-and-automation.md) | Tools, logins, personas, limits, your own product |
| Vendor questionnaire | [guides/VENDOR-QUESTIONNAIRE.md](guides/VENDOR-QUESTIONNAIRE.md) | A 30 question due diligence form for data brokers, with contract wording to discuss with your lawyer |
| Website wording fixes | [guides/WEBSITE-WORDING-FIXES.md](guides/WEBSITE-WORDING-FIXES.md) | 24 before and after examples, all synthetic |
| If you are restricted | [guides/IF-YOUR-ACCOUNT-IS-RESTRICTED.md](guides/IF-YOUR-ACCOUNT-IS-RESTRICTED.md) | What to do first, what not to do, and a draft you can edit |
| The Artisan case | [guides/WHAT-HAPPENED-TO-ARTISAN.md](guides/WHAT-HAPPENED-TO-ARTISAN.md) | What was reported, and what was not |
| Site scanner | [tools/scan_site.py](tools/scan_site.py) | Scans a folder or pasted HTML for name and brand mentions, and points each to a check |
| Lead list checker | [tools/lead_list_check.py](tools/lead_list_check.py) | Reads a CSV for LinkedIn signals, without printing personal data |
| Audit and scoring | [audit/](audit/HOW-TO-SCORE.md) and [tools/score_audit.py](tools/score_audit.py) | A blank 30 row sheet, and a report with your score and your Fix first list |
| Claude Code skill and command | [.claude/](.claude/skills/linkedin-safety-audit/SKILL.md) | `/linkedin-audit` walks you through the audit |
| Sample data | [samples/](samples/README.md) | A risky site, a clean site, lead lists, vendor replies and a filled audit, all synthetic |
| Tests | [tests/check_kit.py](tests/check_kit.py) | Proves the count of 30, the quotes, and the tools |

Every LinkedIn rule in this kit quotes or links LinkedIn's own pages, and they are all in [SOURCES.md](SOURCES.md).

## Plain words

- **AI SDR:** an AI agent that does a sales development rep's job of finding and contacting prospects.
- **Data broker:** a company that sells lists of people and their contact details.
- **Scraping:** using software to copy information from a website in bulk.
- **Restricted:** LinkedIn has limited or closed your access to your account.

## Honest limits

- This is not legal advice.
- LinkedIn does not publish a list of safe tools or a safe daily number. This kit gives neither, and anyone who gives you one is guessing or selling.
- Passing every check does not stop LinkedIn from acting. The score only adds up your own answers.
- The scanner finds words in files. It cannot see logos in images, your ads or your live site.
- The Artisan reasons are its CEO's account to TechCrunch. LinkedIn did not immediately respond to that report.
- All sample data is synthetic. Your real site and lists will be messier.
- Sources were read on 2026-11-09 and can change.

LinkedIn is a registered trademark of LinkedIn Corporation and its affiliates in the United States and/or other countries. This kit is not affiliated with, sponsored by or endorsed by LinkedIn.

MIT licence. See [LICENSE](LICENSE).

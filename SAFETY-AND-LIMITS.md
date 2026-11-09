# Safety and limits

Please read this before you rely on the kit.

## This is not legal advice

This kit is a practical checklist written by a founder for founders. It is not legal advice, and using it does not create any relationship with a lawyer. Terms, trademarks, privacy law and email law depend on your facts and your country. Before you act on anything that matters, talk to a lawyer who knows your situation.

## LinkedIn does not publish a safe list

On the pages read for this kit, LinkedIn does not publish a safe list of outreach tools, and it does not publish a safe daily or weekly number of invitations, messages or profile views. This kit does not give you one either, because any number would be made up. The numbers you see online come from vendors and bloggers, and some of them sell the tools.

Passing all 30 checks does not make you safe from a restriction. LinkedIn can restrict an account under its own terms and it decides what counts as a breach. No score here predicts what LinkedIn will do.

## Independent kit

This kit is independent. It is not affiliated with, made by, sponsored by or endorsed by LinkedIn Corporation or Microsoft. LinkedIn is a registered trademark of LinkedIn Corporation and its affiliates in the United States and/or other countries. The name of this kit describes what it checks.

LinkedIn's own guidelines limit how its name can be used in names and web addresses, and checks 2 and 3 cover that. Please do not copy this kit's name as a pattern for your own company or product.

## What the Artisan story is and is not

The reasons given for the Artisan case are the account of its CEO to TechCrunch. The report says LinkedIn did not immediately respond. The kit does not claim to know LinkedIn's actual reasons, and it does not say that Artisan or any data broker did anything wrong. The allegation about data brokers is reported as an allegation.

## What the tools can and cannot see

| Tool | It can | It cannot |
| --- | --- | --- |
| `scan_site.py` | Find the words and addresses in files you give it | See logos inside images, read PDFs, or look at your live site or your ads |
| `lead_list_check.py` | Spot columns and links that suggest a LinkedIn origin | Prove a list was or was not scraped |
| `score_audit.py` | Add up the answers you wrote | Tell whether your answers are true |

A clean result means nothing was found in what was checked. Treat it that way.

The Fix first and Fix soon labels are this kit's own judgement. The scanner's rules are pattern matches, so expect both false alarms and misses.

## Your data stays with you

The tools run on your computer and make no network calls. They send nothing anywhere. `lead_list_check.py` does not print cell values. Put your own audit files in `audit/out/`, which git ignores. If you run the kit through an AI assistant, whatever you show the assistant goes to that assistant's provider, so check their terms before you share a real lead list.

## The rules the kit follows

- It never logs in to LinkedIn and never asks for a LinkedIn password or cookie.
- It never automates activity on LinkedIn and will not help you scrape it.
- It never sends a message, email or appeal for you.
- It contains no real customer data. All samples are synthetic.

## Sources can go stale

Everything was read on 2026-11-09. LinkedIn can change its terms, its guidelines and its help pages at any time. Open the page in [SOURCES.md](SOURCES.md) before you rely on a quote. If what you read on LinkedIn differs from this kit, LinkedIn's page is the one that counts.

## What was tested

`tests/check_kit.py` runs the tools on the synthetic samples and on planted test cases, and checks the counts, the quotes and the links. It has not been tested against your website or your data, and it does not check live web pages.

# Group 2: Your data vendors and lead lists (checks 11 to 20)

Artisan's CEO told TechCrunch that LinkedIn alleged Artisan was using data brokers who had scraped the site without permission. LinkedIn's User Agreement covers information obtained "through third parties", so buying a list does not by itself put you in the clear.

Send [the vendor questionnaire](../guides/VENDOR-QUESTIONNAIRE.md) to each vendor. You can score this group before the replies arrive: a vendor that has not answered counts as a fail on check 12 until it does. Check your own lists with:

```bash
python3 tools/lead_list_check.py path/to/your-list.csv
```

The tool reads column names and counts. It never prints names or emails. A signal is a reason to ask your vendor, not proof of scraping.

## Check 11: A written map of every data source

**Priority:** Fix first
**Based on:** Operating practice

### What to look at

Every place a lead record enters your business: brokers, enrichment tools and each step of a waterfall, purchased lists, freelancers, browser extensions your team uses, and lists a customer uploads.

### How to check it

Open your billing history and your CRM import log, and ask each person who touches leads what they use. Write one row per source in your audit evidence: name, what it supplies, who owns the relationship.

### Pass or fail test

- **Pass:** a written list covers every source, and someone owns keeping it current.
- **Fail:** there is no list, or sources turn up that nobody had written down.

### The fix

Build the list today from billing, import logs and the team. Any source nobody can explain stops being used until checks 12 to 15 are done for it.

### Source

- [TechCrunch, the CEO's account of the Artisan case](https://techcrunch.com/2026/01/07/yes-linkedin-banned-ai-agent-startup-artisan-but-now-its-back/):
  > The CEO also got a crash course in third-party vendor verification, ensuring that his data partners were operating in compliance with LinkedIn’s policies.

## Check 12: A written answer on where each vendor's data comes from

**Priority:** Fix first
**Based on:** LinkedIn rule

### What to look at

Each vendor's written answer to one direct question: was any of this data obtained from LinkedIn, by you or by anyone who supplied you, by scraping, browser extensions, or automated collection?

### How to check it

Send the [questionnaire](../guides/VENDOR-QUESTIONNAIRE.md). Save the reply. A sales call is not an answer. Vague wording such as "public web sources" with no detail counts as no answer.

### Pass or fail test

- **Pass:** every vendor has given a specific written answer, and it says no.
- **Fail:** a vendor says yes, refuses, stays vague, or has not replied.

### The fix

Stop buying from that vendor, and set aside the records it supplied until you get a clear answer. Tell a lawyer before you delete or keep them, if a dispute is possible.

### Source

- [LinkedIn User Agreement, section 8.2](https://www.linkedin.com/legal/user-agreement):
  > Copy, use, display or distribute any information (including content) obtained from the Services, whether directly or through third parties (such as search tools or data aggregators or brokers), without the consent of the content owner (such as LinkedIn for content it owns);
- [LinkedIn Crawling Terms](https://www.linkedin.com/legal/crawling-terms):
  > Automated Crawling & Indexing without the express permission of LinkedIn is strictly prohibited.

## Check 13: Field fingerprints in your lists

**Priority:** Fix first
**Based on:** LinkedIn rule

### What to look at

Columns that point back at LinkedIn: profile links, member identifiers, Sales Navigator fields, or profile headline and summary fields that match LinkedIn word for word.

### How to check it

Run `lead_list_check.py` on each list. Then take a few records and compare the headline text with the person's public profile by eye, one at a time, by hand.

### Pass or fail test

- **Pass:** the tool shows no high signals, and the vendor's answer in check 12 explains any field that looks similar.
- **Fail:** the tool shows high signals you cannot explain.

### The fix

Ask the vendor to explain those fields in writing. Until it does, take the list out of use. Do not simply delete the column and carry on, because the source has not changed.

### Source

- [LinkedIn User Agreement, section 8.2](https://www.linkedin.com/legal/user-agreement):
  > Develop, support or use software, devices, scripts, robots or any other means or processes (such as crawlers, browser plugins and add-ons or any other technology) to scrape or copy the Services, including profiles and other data from the Services;

## Check 14: What your vendor says about itself

**Priority:** Fix first
**Based on:** LinkedIn rule

### What to look at

The vendor's own website, docs and sales emails. If it advertises LinkedIn data, a Chrome extension for LinkedIn, or LinkedIn enrichment, take that as a direct answer.

### How to check it

Save the vendor's page as HTML and run `python3 tools/scan_site.py saved-page.html`. Read its help docs and pricing page. Compare what you find with its written answer from check 12.

### Pass or fail test

- **Pass:** the vendor's public claims match its written answer, and neither points to LinkedIn.
- **Fail:** it markets LinkedIn data or tooling, or its marketing contradicts its answer.

### The fix

Treat a contradiction as a failed check 12. Ask the vendor to explain in writing, or move to another vendor.

### Source

- [LinkedIn Help, automated activity](https://www.linkedin.com/help/linkedin/answer/a1340567):
  > Third-party software that automates tasks could potentially export or scrape data from LinkedIn and affects authenticity; at times, without your consent.
- [LinkedIn Professional Community Policies](https://www.linkedin.com/legal/professional-community-policies):
  > We don't allow content that promotes or distributes fake educational and/or professional certifications, sale of scraped data, proxy test-taking, or instructions on creating forged official documents.

## Check 15: Contract terms that back up the answers

**Priority:** Fix soon
**Based on:** Operating practice

### What to look at

Your contract with each vendor. Does it promise the data was lawfully obtained and not taken from platforms in breach of their terms, and does it say what happens if that turns out to be wrong?

### How to check it

Read the data warranties, indemnity and termination sections. If there is only a click through page, read that. Ask your lawyer to review anything you are unsure about.

### Pass or fail test

- **Pass:** the contract has a warranty on data origin, a duty to tell you of a problem, and a way for you to leave.
- **Fail:** the contract is silent on where the data comes from, or disclaims it completely.

### The fix

Ask for an addendum. Sample wording to discuss with your lawyer is in the questionnaire guide. A vendor that will not put its answer in writing has told you something useful.

### Source

- [FTC, CAN-SPAM guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business), on not being able to hand your duties to someone else (an email law, used here as the same principle):
  > you can’t contract away your legal responsibility to comply with the law.
- [TechCrunch, the CEO's account of the Artisan case](https://techcrunch.com/2026/01/07/yes-linkedin-banned-ai-agent-startup-artisan-but-now-its-back/):
  > The CEO also got a crash course in third-party vendor verification, ensuring that his data partners were operating in compliance with LinkedIn’s policies.

## Check 16: Where each record came from and when

**Priority:** Fix soon
**Based on:** Law

### What to look at

Whether each lead record stores its source and the date you got it, so you can answer a person who asks, and so you can pull one vendor's records out if you have to.

### How to check it

Open your CRM and look at a few records. Run `lead_list_check.py`, which notes when a list has no source or date column.

### Pass or fail test

- **Pass:** you can pick any record and say which vendor supplied it and when.
- **Fail:** you cannot, or the field is often empty.

### The fix

Add source and acquired date fields, and make imports fill them. For older records, tag them by import batch.

### Source

- [GDPR Article 14](https://gdpr-info.eu/art-14-gdpr/), one of the things to tell people where it applies:
  > from which source the personal data originate, and if applicable, whether it came from publicly accessible sources;

## Check 17: Data broker registration

**Priority:** Fix soon
**Based on:** Law

### What to look at

Whether a vendor that sells personal data about people it has no direct relationship with is registered where it needs to be. California keeps a public registry.

### How to check it

Search the registry linked from the California page below for the vendor's legal name, if it handles data about Californians. Ask your lawyer which other places apply to you. Mark this check na only if your lawyer confirms it does not apply.

### Pass or fail test

- **Pass:** the vendor is registered where it must be, or you have confirmed it does not need to be.
- **Fail:** it should be registered, is not, and has no explanation.

### The fix

Ask the vendor why it is not listed. If the answer does not hold up, replace it.

### Source

- [California Privacy Protection Agency, data brokers](https://cppa.ca.gov/data_brokers/):
  > To fall under the definition of data broker, a business must knowingly collect and sell to “third parties the personal information of a consumer with whom the business does not have a direct relationship.”

## Check 18: Your right to contact the people on the list

**Priority:** Fix soon
**Based on:** Law

### What to look at

The legal basis for contacting people, where they are, and whether you tell them what the law requires. The rules differ by country and by channel.

### How to check it

List which countries your leads are in. For people covered by GDPR, check that your first message or the page it links to gives the required information, including where you got their data. Have a lawyer confirm this.

### Pass or fail test

- **Pass:** a lawyer or a written policy covers each region you contact, and your messages follow it.
- **Fail:** you contact people in a region without knowing what applies there.

### The fix

Pause that region until a lawyer has confirmed the basis and the notice wording.

### Source

- [GDPR Article 14](https://gdpr-info.eu/art-14-gdpr/), on when to give that information:
  > if the personal data are to be used for communication with the data subject, at the latest at the time of the first communication to that data subject;

## Check 19: Opt outs that reach every list

**Priority:** Fix first
**Based on:** Law

### What to look at

What happens when a person says stop. Does the request reach every tool, every list and every future import, including lists bought later?

### How to check it

Pick one made up test contact of your own. Opt it out, then import a list containing it and see whether it comes back. Read your written process for how fast you act.

### Pass or fail test

- **Pass:** one opt out blocks that person across every tool and survives new imports.
- **Fail:** an opt out stops at one tool, or a new import brings the person back.

### The fix

Keep one suppression list, check every import against it, and pass deletion requests to your vendors.

### Source

- [FTC, CAN-SPAM guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business):
  > You must honor a recipient’s opt-out request within 10 business days.
  > Once people have told you they don’t want to receive more messages from you, you can’t sell or transfer their email addresses, even in the form of a mailing list.
- [GDPR Article 21](https://gdpr-info.eu/art-21-gdpr/):
  > Where the data subject objects to processing for direct marketing purposes, the personal data shall no longer be processed for such purposes.

## Check 20: Reselling or showing LinkedIn data to your customers

**Priority:** Fix first
**Based on:** LinkedIn rule

### What to look at

Whether your product shows customers profile data, exports it, or feeds it to your AI agents as a feature. An AI SDR product that hands data to customers is reselling it, whoever collected it first.

### How to check it

Trace one lead from source to your customer's screen. Note every field shown and where each came from. Compare with the source map from check 11.

### Pass or fail test

- **Pass:** no field you show or export traces to LinkedIn.
- **Fail:** any field does, or you cannot tell.

### The fix

Remove those fields from the product and from anything your agents use, and replace the source.

### Source

- [LinkedIn User Agreement, section 8.2](https://www.linkedin.com/legal/user-agreement):
  > Rent, lease, loan, trade, sell/re-sell or otherwise monetize the Services or related data or access to the same, without LinkedIn’s consent;
- [LinkedIn Crawling Terms](https://www.linkedin.com/legal/crawling-terms):
  > You agree that you will not rent, lease, loan, trade, or sell any data collected through Automated Crawling & Indexing.

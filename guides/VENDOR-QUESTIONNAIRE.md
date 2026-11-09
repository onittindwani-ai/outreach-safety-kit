# Vendor due diligence questionnaire for data brokers

Use this before you buy a lead list, and for every vendor you already use. It supports checks 11 to 20.

Artisan's CEO told TechCrunch that its fix included verifying its data partners. These 30 questions are one practical way to do that. They are our suggestion, not a form LinkedIn provides.

## How to use it

1. Copy the email below and send it with the questions. You send it, nothing in this kit sends anything.
2. Ask for written answers from someone who can commit the company. A sales call does not count.
3. Save the reply with the date. Your evidence column in the audit points to it.
4. Mark each answer **Clear**, **Vague** or **Red flag** using the notes under each question.

| Result | What to do |
| --- | --- |
| Any Red flag on Q12 to Q19 | Stop using this vendor's data until it is resolved in writing |
| Three or more Vague answers | Ask again once with the exact question. If it stays vague, replace the vendor |
| No reply after two requests | Treat it as a failed check 12 |
| All Clear | Record it, and ask again each year or when the vendor changes suppliers |

Clear answers are still only what the vendor told you. They reduce your risk and prove nothing on their own. This is not legal advice.

## Email to send

```text
Subject: Data origin questions for our vendor review

Hi [NAME],

We are reviewing every data supplier we use. Please answer the attached
questions in writing, and have someone who can commit [VENDOR] confirm them.

The most important one is Q12: was any data you supply to us obtained from
LinkedIn, by you or anyone who supplied you, by scraping, browser extensions
or other automated collection?

Please reply by [DATE]. We will pause new purchases until we have your answers.

Thanks,
[YOUR NAME]
```

## A. Who you are

### Q1. What is your full legal company name, country of registration and registered address?

Clear: a legal entity you can look up. Red flag: only a brand name or a free email contact.

### Q2. Who is responsible for data protection at your company, and how do we contact them?

Clear: a named role and a working address. Vague: a general support inbox.

### Q3. Do you sell personal data about people you have no direct relationship with, and are you registered as a data broker anywhere?

Clear: names each registry, which you can check. Red flag: says it does not apply while selling contact lists. See check 17.

### Q4. Has any platform, regulator or court told you to stop collecting or selling data in the last 3 years?

Clear: no, or a full account of what happened and what changed. Red flag: refuses to answer.

## B. How your data is collected

### Q5. List every method you use to collect the data you supply to us.

Clear: a specific list, such as licensed files, company websites, or people who opted in. Vague: "proprietary methods" or "public web sources" with no detail.

### Q6. For the fields you supply to us, which come from which method?

Clear: a field by field table. Vague: one sentence covering everything.

### Q7. Do you use crawlers, bots or scrapers? On which websites?

Clear: names the sites, and they do not include LinkedIn. Red flag: will not name them.

### Q8. Do you collect data through browser extensions or software installed by your users?

Clear: no. Red flag: yes, and the extension runs on LinkedIn pages, which also feeds Q13.

### Q9. Do you obtain data from contributors who share their contacts or email inboxes?

Clear: no, or it explains consent clearly. Vague: "community data" with no explanation.

### Q10. How do you record where each record came from and when?

Clear: source and date stored for each record, and available to you. Red flag: not recorded. See check 16.

### Q11. How often is each record checked, and what happens to records that fail?

Clear: a stated process. Vague: "constantly refreshed".

## C. LinkedIn specifically

### Q12. Was any data you supply to us obtained from LinkedIn, by you or anyone who supplied you, by scraping, browser extensions or other automated collection?

Clear: a plain, signed no. Red flag: yes, or any answer that avoids the question.

### Q13. Do you or your suppliers use logged in LinkedIn accounts, session cookies or rented accounts to collect data?

Clear: no. Red flag: yes.

### Q14. Do any fields come from LinkedIn profiles, such as headline, summary, job history or profile link?

Clear: no, or each field has a documented lawful source you can inspect. Red flag: "it's public information", since being public is not what LinkedIn's terms turn on.

### Q15. Do you have LinkedIn's written permission for any part of your data collection? If yes, please share it.

Clear: no permission needed because no LinkedIn data is used, or a real agreement you can read. Red flag: claims permission and cannot show it.

### Q16. Do you market or offer any LinkedIn data, LinkedIn enrichment or a LinkedIn extension to any customer?

Clear: no. Red flag: yes, even if not to you. See check 14.

### Q17. Has LinkedIn ever contacted you about scraping, your accounts, or use of its name?

Clear: no, or a full account. Red flag: refuses to answer.

### Q18. Do you hold LinkedIn profile links in your database, and if so how did you get them?

Clear: no, or a documented source other than LinkedIn. Vague: "from around the web".

### Q19. If LinkedIn data were found in what you supplied us, what would you do and how quickly?

Clear: a written commitment to tell you, stop, and help you remove it. Red flag: "that can't happen".

## D. Your suppliers

### Q20. Do you buy or license data from other companies? Please list them.

Clear: a list you can run this same questionnaire on. Vague: "trusted partners".

### Q21. Do your contracts with those suppliers forbid data taken in breach of a platform's terms?

Clear: yes, and it can show the clause. Vague: yes, with no detail.

### Q22. How do you check that your suppliers are telling you the truth?

Clear: a described audit or sampling process. Red flag: no check at all.

## E. Law and privacy

### Q23. Which laws do you consider apply to this data, and what is your legal basis in each region?

Clear: names regions and bases, reviewed by counsel. Red flag: "not our responsibility".

### Q24. How do you handle a person's request to delete or stop using their data?

Clear: a published process with a stated timeframe. Red flag: no process.

### Q25. How will you tell us when someone opts out or asks for deletion, so we can act too?

Clear: a feed or a regular file. Vague: "contact support". See check 19.

### Q26. Where is the data stored and which countries is it transferred to?

Clear: named countries and safeguards. Vague: "the cloud".

## F. Contract and proof

### Q27. Will you warrant in our contract that the data was lawfully obtained and not taken in breach of any platform's terms?

Clear: yes. Red flag: no. See check 15.

### Q28. Will you indemnify us if that warranty turns out to be wrong?

Clear: yes, or a reasoned limit. Vague: silence on the point.

### Q29. Will you let us review a sample of records with the source shown for each?

Clear: yes. Red flag: no.

### Q30. Who at your company confirms these answers are true? Please give their name, title and the date.

Clear: a named officer and a date. Red flag: unsigned.

## Contract wording to discuss with your lawyer

This is a starting point for a conversation, not legal drafting.

```text
Vendor warrants that all data supplied under this agreement was collected and
supplied lawfully and was not obtained, directly or through any third party,
in breach of the terms of any website or platform, including by scraping or
other automated collection. Vendor will notify Customer without delay if it
learns of any breach of this warranty, will cease supplying the affected data,
and will assist Customer in identifying and removing it.
```

A worked example of a clear reply and an evasive reply is in [samples/vendor-answers](../samples/vendor-answers/vendor-a-clear.md). Both are synthetic.

# Group 1: Your website and marketing pages (checks 1 to 10)

Start here. Artisan's CEO told TechCrunch that LinkedIn objected to LinkedIn's name on Artisan's website. This group is also the fastest to fix, because the words are yours to change.

Run the scanner once before you begin, then use its check numbers to work through this page:

```bash
python3 tools/scan_site.py path/to/your/website/folder
```

No folder? Open a page in your browser, choose View Source, copy all of it, and run `python3 tools/scan_site.py --stdin`, then paste, then press Ctrl+D.

Mark each check pass, partial, fail or na in your audit sheet. Partial means it passes in some places but not all, or the fix has started and is not finished.

## Check 1: Comparison copy that names LinkedIn

**Priority:** Fix first
**Based on:** LinkedIn rule

### What to look at

Every sentence that compares your product, your data or your results with LinkedIn: comparison pages, pricing tables, feature grids, sales decks, and lines such as "fresher than" or "more accurate than".

### How to check it

Run the scanner and read every finding tagged `[check 1]`. Then open your comparison, pricing and features pages and read them by eye, because a table can split a comparison across cells.

### Pass or fail test

- **Pass:** no page, table, deck or ad compares you with LinkedIn by name.
- **Fail:** any page does, even a single row in a feature table.

### The fix

Delete the comparison, or compare against the job instead of the company. "Contacts checked every 30 days" says what you do without naming anyone. Worked examples are in [the wording guide](../guides/WEBSITE-WORDING-FIXES.md). Artisan's fix, per its CEO, was to remove every mention from its site.

### Source

- [LinkedIn User Agreement, section 8.2](https://www.linkedin.com/legal/user-agreement):
  > using the word “LinkedIn” or our logos in any business name, email, or URL except as provided in the Brand Guidelines;
- [LinkedIn Brand Guidelines](https://brand.linkedin.com/policies):
  > You may not use our Brand, including our name, logos, or any elements that are identical to, incorporate, or closely resemble our Brand, in any way that could cause confusion about the source, sponsorship, or affiliation of your product, service, or account.
- [TechCrunch, the CEO's account of the Artisan case](https://techcrunch.com/2026/01/07/yes-linkedin-banned-ai-agent-startup-artisan-but-now-its-back/):
  > It was using the name to compare some of its data features to LinkedIn’s.

## Check 2: LinkedIn in your domain or page addresses

**Priority:** Fix first
**Based on:** LinkedIn rule

### What to look at

Your domains, subdomains and page addresses: anything like a `linkedin-outreach` page or a `linkedin.yourcompany.example` subdomain. Include landing pages built for ads and pages you forgot.

### How to check it

Read scanner findings tagged `[check 2]`. Then search your sitemap and your domain registrar's list for the word. File names count, because on most sites a file name becomes the page address.

### Pass or fail test

- **Pass:** no domain, subdomain or page address contains the word.
- **Fail:** any one does, including a redirect you still own.

### The fix

Move the page to an address that describes the job, such as `/social-outreach`, and redirect the old address. Stop renewing any domain that contains the name, after checking with your lawyer what to do with it.

### Source

- [LinkedIn Brand Guidelines, business usage](https://brand.linkedin.com/business-books-and-media-usage):
  > Don’t register or use a domain name that includes Linkedin in any part of the domain name.
- [LinkedIn User Agreement, section 8.2](https://www.linkedin.com/legal/user-agreement):
  > using the word “LinkedIn” or our logos in any business name, email, or URL except as provided in the Brand Guidelines;

## Check 3: LinkedIn in your business, product, handle or email names

**Priority:** Fix first
**Based on:** LinkedIn rule

### What to look at

Company name, product and plan names, social handles, email addresses such as a `linkedin@` inbox, page titles and main headings. Also look at whether the word is the biggest thing on the page.

### How to check it

Read scanner findings tagged `[check 3]`. Then list your product names, plan names, social handles and shared inboxes, and search that list for the word. The word InMail and the name Sales Navigator are LinkedIn marks too.

### Pass or fail test

- **Pass:** no name you own contains the word or a close variation, and no page makes it the most prominent feature.
- **Fail:** any name contains it, or a page headline is built around it.

### The fix

Rename the plan, handle or inbox. Rewrite the headline around the result you deliver. Keep any necessary mention small, plain and descriptive.

### Source

- [LinkedIn User Agreement, section 8.2](https://www.linkedin.com/legal/user-agreement):
  > using the word “LinkedIn” or our logos in any business name, email, or URL except as provided in the Brand Guidelines;
- [LinkedIn Brand Guidelines, business usage](https://brand.linkedin.com/business-books-and-media-usage):
  > Don’t adopt names that are confusingly similar to the Brand.
  > Don’t make the words “LinkedIn” or “in” the most prominent feature of your business or materials related to your business.
  > Don’t use the LinkedIn® trademark, Linkedin Logo, or [in] Logo in your social media account name, handle, or in social media posts other than in a descriptive manner to describe the services that you offer.

## Check 4: LinkedIn logos

**Priority:** Fix first
**Based on:** LinkedIn rule

### What to look at

The full LinkedIn Logo and the small [in] Logo, anywhere: logo walls, "integrations" grids, hero images, decks, and icon fonts. Download folders named after the logo count too.

### How to check it

Read scanner findings tagged `[check 4]`. Then look at your home page, integrations page and sales deck by eye, because a logo baked into a larger image cannot be found by a text scan.

### Pass or fail test

- **Pass:** the full LinkedIn Logo appears nowhere unless you hold a licence, and the [in] Logo appears only in an allowed use, such as a small icon linking to your own company page.
- **Fail:** either logo appears on a logo wall, an integrations grid, a hero image or any feature section.

### The fix

Remove it, or replace a logo wall with plain words describing the category, such as "social networks". Keep only the footer icon that links to your own page, using LinkedIn's own file.

### Source

- [LinkedIn Brand Guidelines, LinkedIn Logo](https://brand.linkedin.com/linkedin-logo):
  > LinkedIn does not allow anyone to use the LinkedIn Logo, unless they already have an existing relationship with LinkedIn and a Brand or Trademark License.
- [LinkedIn Brand Guidelines, [in] Logo](https://brand.linkedin.com/in-logo):
  > As a hyperlink to your LinkedIn profile, company page, and/or group page.
  > Use the [in] Logo in a manner that implies affiliation with or endorsement by LinkedIn.

## Check 5: Partner, endorsed or certified claims

**Priority:** Fix first
**Based on:** LinkedIn rule

### What to look at

Any wording that suggests a relationship: partner, official, approved, certified, integrated, works with, built on, powered by, and badges that look like official marks.

### How to check it

Read scanner findings tagged `[check 5]`. Then ask one question of each one: do you hold a written agreement from LinkedIn that allows this exact wording? If nobody can produce it, the answer is no.

### Pass or fail test

- **Pass:** nothing implies a relationship, or you can produce LinkedIn's written consent for the exact wording.
- **Fail:** any claim of partnership, approval or certification without that written consent.

### The fix

Remove the claim. If you must describe a real and permitted connection, say only what is true, and add a plain line saying you are not affiliated with or endorsed by LinkedIn.

### Source

- [LinkedIn User Agreement, section 8.2](https://www.linkedin.com/legal/user-agreement):
  > Imply or state that you are affiliated with or endorsed by LinkedIn without our express consent (e.g., representing yourself as an accredited LinkedIn trainer);
- [LinkedIn Brand Guidelines, business usage](https://brand.linkedin.com/business-books-and-media-usage):
  > Don’t use the Brand in a way that implies sponsorship, affiliation with or endorsement by LinkedIn of your products or services.

## Check 6: Copy saying your data comes from LinkedIn

**Priority:** Fix first
**Based on:** LinkedIn rule

### What to look at

Marketing lines, help articles and sales scripts that say or suggest your contacts, profiles or enrichment come from LinkedIn. "LinkedIn data", "profiles from LinkedIn" and "export your Sales Navigator list" are typical.

### How to check it

Read scanner findings tagged `[check 6]`. Then search your help centre and sales scripts, and ask your sales team what they tell prospects when asked where the data comes from.

### Pass or fail test

- **Pass:** nothing you publish or say suggests your data comes from LinkedIn, and that matches what checks 11 to 14 found.
- **Fail:** any line says or suggests it.

### The fix

If the claim is untrue, delete it. If it is true, deleting the sentence does not fix the problem: stop and work through group 2 first, because the data itself is the issue.

### Source

- [LinkedIn User Agreement, section 8.2](https://www.linkedin.com/legal/user-agreement):
  > Copy, use, display or distribute any information (including content) obtained from the Services, whether directly or through third parties (such as search tools or data aggregators or brokers), without the consent of the content owner (such as LinkedIn for content it owns);
- [LinkedIn Professional Community Policies](https://www.linkedin.com/legal/professional-community-policies):
  > We don't allow content that promotes or distributes fake educational and/or professional certifications, sale of scraped data, proxy test-taking, or instructions on creating forged official documents.

## Check 7: Copy promising safe automation or beaten limits

**Priority:** Fix first
**Based on:** LinkedIn rule

### What to look at

Sales lines such as undetectable, bypass limits, avoid bans, ban proof, stealth, or safe automation, on your site, in ads, in onboarding emails and in help docs.

### How to check it

Read scanner findings tagged `[check 7]`. Then search your ad accounts and email sequences for the same words.

### Pass or fail test

- **Pass:** you make no promise about avoiding detection, bans or limits.
- **Fail:** any such promise appears anywhere.

### The fix

Remove it, then fix the product behind it if the promise was true (see checks 22 and 27). LinkedIn publishes no safe volume, so no honest company can promise one.

### Source

- [LinkedIn User Agreement, section 8.2](https://www.linkedin.com/legal/user-agreement):
  > Override any security feature or bypass or circumvent any access controls or use limits of the Services (such as search results, profiles, or videos);
- [LinkedIn Help, prohibited software and extensions](https://www.linkedin.com/help/linkedin/answer/a1341387):
  > we don't permit the use of any third party software, including "crawlers", bots, browser plug-ins, or browser extensions that scrape, modify the appearance of, or automate activity on LinkedIn's website.

## Check 8: Copying LinkedIn's look, or showing its screens

**Priority:** Fix soon
**Based on:** LinkedIn rule

### What to look at

Pages, demos and mock ups that imitate LinkedIn's design, colours, type or layout. Product screenshots and demo videos showing LinkedIn pages. Fake profile cards used to sell your product.

### How to check it

Look through your site, demo video and deck by eye. A text scanner cannot see this. Ask someone who has not seen the design: does any part of this look like LinkedIn?

### Pass or fail test

- **Pass:** nothing could be mistaken for LinkedIn's site, and no LinkedIn screen appears in your marketing.
- **Fail:** a page imitates its look, or your demo shows LinkedIn screens as part of your product.

### The fix

Redraw the card in your own design with made up data, and label the data as an example. Cut LinkedIn screens from demos.

### Source

- [LinkedIn Brand Guidelines, business usage](https://brand.linkedin.com/business-books-and-media-usage):
  > Don’t copy or imitate LinkedIn’s website design, typeface, colors, graphics, or imagery.
- [LinkedIn User Agreement, section 8.2](https://www.linkedin.com/legal/user-agreement):
  > Engage in “framing”, “mirroring”, or otherwise simulating the appearance or function of the Services;

## Check 9: Deep links into LinkedIn

**Priority:** Fix soon
**Based on:** LinkedIn rule

### What to look at

Links from your site or product that point inside LinkedIn: search results, Sales Navigator pages, specific people's profiles used as examples, and any embedded frame.

### How to check it

Read scanner findings tagged `[check 9]`. Findings marked `info` are plain links to a profile, company page or group: confirm they are yours. Findings marked `medium` point somewhere else on LinkedIn.

### Pass or fail test

- **Pass:** your only links into LinkedIn promote your own profile, page or Group.
- **Fail:** any link points to search results, other people's profiles or other inner pages, or you embed LinkedIn in a frame.

### The fix

Remove those links. Keep one link to your own company page.

### Source

- [LinkedIn User Agreement, section 8.2](https://www.linkedin.com/legal/user-agreement):
  > Deep-link to our Services for any purpose other than to promote your profile or a Group on our Services, without LinkedIn’s consent;

## Check 10: Hidden mentions

**Priority:** Fix soon
**Based on:** LinkedIn rule

### What to look at

Everything a visitor does not read but a crawler or a curious person can: meta tags, image alt text, HTML comments, structured data, SEO landing pages, old blog posts, help docs, changelogs, PDFs, ad copy and app store listings.

### How to check it

Read every scanner finding whose location is a meta tag, an attribute, a comment, a script or a file name, whatever check number it carries, plus everything tagged `[check 10]`. Open every file listed under "Not read". Then search your blog, help centre, ad accounts and app store listings for the word. Search for your own domain plus the word in a search engine.

### Pass or fail test

- **Pass:** every remaining mention is one you chose to keep, and you can say why it is allowed.
- **Fail:** mentions remain that nobody has reviewed.

### The fix

Remove what you do not need. Artisan's fix, per its CEO, was all mentions. If you keep a descriptive mention, write it in plain characters with the ® symbol, and say you are separate from LinkedIn.

### Source

- [LinkedIn Brand Guidelines, business usage](https://brand.linkedin.com/business-books-and-media-usage):
  > You may use the LinkedIn trademark in standard characters with no stylization accompanied with the ® symbol to describe the services that you offer: LinkedIn®
- [LinkedIn Brand Guidelines](https://brand.linkedin.com/policies):
  > We may request that you stop the use of our Brand both on and off the LinkedIn platform
  > make clear that your use is separate from the LinkedIn Brand, and ensure that you do not copy or imitate the LinkedIn platform’s overall look and feel.
- [TechCrunch, the CEO's account of the Artisan case](https://techcrunch.com/2026/01/07/yes-linkedin-banned-ai-agent-startup-artisan-but-now-its-back/):
  > To appease LinkedIn, Artisan removed all mentions of LinkedIn from its website.

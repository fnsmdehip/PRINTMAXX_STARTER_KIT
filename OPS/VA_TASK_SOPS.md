# VA Task Standard Operating Procedures

**26 delegatable tasks. Each SOP written so someone with zero context can execute.**

Hire from OnlineJobs.ph ($3-6/hr) or Fiverr (per-task). See `OPS/VA_HIRING_SYSTEM.md` for job postings and management. See `OPS/VA_TRAINING/` for niche-specific training docs.

**Pay structure:** $5/hr base + performance bonuses. Pay weekly via Wise or PayPal.

**Tooling note:** All tasks reference specific tools. If a VA doesn't have access, provision it before assigning the task. Most tools have team/seat pricing. Budget $50-100/mo for VA tool access.

---

## Quick reference

| # | Task | Frequency | Time/exec | Skill |
|---|------|-----------|-----------|-------|
| 1 | Social media posting | Daily | 30-45 min | Basic |
| 2 | Comment engagement | Daily | 45-60 min | Intermediate |
| 3 | Content repurposing | Daily | 60-90 min | Intermediate |
| 4 | Hashtag research | Weekly | 45-60 min | Basic |
| 5 | Competitor monitoring | Daily | 30-45 min | Basic |
| 6 | UGC collection | Daily | 30 min | Basic |
| 7 | Newsletter curation | Weekly | 60-90 min | Intermediate |
| 8 | Reddit engagement | Daily | 45-60 min | Advanced |
| 9 | Cold email list building | Daily | 60-90 min | Intermediate |
| 10 | LinkedIn connections | Daily | 30-45 min | Basic |
| 11 | Lead qualification | As-needed | 15-20 min/lead | Intermediate |
| 12 | CRM data entry | Daily | 20-30 min | Basic |
| 13 | Local business prospecting | Weekly | 2-3 hrs | Intermediate |
| 14 | Review mining | Weekly | 60-90 min | Intermediate |
| 15 | Daily alpha scan | Daily | 45-60 min | Intermediate |
| 16 | Product research | Weekly | 2-3 hrs | Intermediate |
| 17 | App Store research | Weekly | 60-90 min | Intermediate |
| 18 | Price monitoring | Weekly | 30-45 min | Basic |
| 19 | Trend spotting | Daily | 30-45 min | Intermediate |
| 20 | Customer support | Daily | 30-60 min | Basic |
| 21 | Order fulfillment tracking | Daily | 15-30 min | Basic |
| 22 | Invoice and expense logging | Weekly | 30-45 min | Basic |
| 23 | Weekly metrics reporting | Weekly | 60-90 min | Intermediate |
| 24 | Basic image editing | As-needed | 15-30 min/batch | Basic |
| 25 | Video clipping | As-needed | 30-60 min/video | Intermediate |
| 26 | Thumbnail creation | As-needed | 15-20 min/thumb | Basic |

**Total daily VA time (all tasks):** ~6-8 hours. Split across 2 VAs or 1 full-time.

---

## Content Operations (SOPs 1-8)

---

### SOP 1: Daily social media posting

**Frequency:** Daily
**Time:** 30-45 minutes
**Skill level:** Basic
**Tools:** Buffer or Publer, Google Sheets (content calendar), Canva (image resizing)

#### Steps

1. Open the content calendar at `LEDGER/CONTENT_CALENDAR_30DAY.csv` (shared via Google Sheets). Find today's date row.
2. For each scheduled post, copy the text from the "copy" column.
3. Open Buffer (or Publer). Select the correct account profile that matches the "account" column in the calendar.
4. Paste the copy into the compose window. Do NOT edit the text unless there's an obvious typo (misspelling, broken link).
5. If the post has an image listed in the "media" column, download it from the shared Google Drive folder and attach it.
6. If the post requires an image resize (different dimensions per platform), open Canva, use the "Resize" feature, and export at the correct size: X/Twitter = 1200x675, Instagram = 1080x1080, LinkedIn = 1200x627, TikTok = 1080x1920.
7. Set the scheduled time from the "time" column. If no time is specified, use these defaults: X = 8:15 AM EST, IG = 12:30 PM EST, LinkedIn = 7:45 AM EST, TikTok = 6:00 PM EST.
8. Double-check: correct account, correct copy, correct media, correct time. Hit "Schedule."
9. In the content calendar, change the "status" column for that row from "SCHEDULED" to "QUEUED_IN_BUFFER."
10. After all posts are queued, send a Slack/Telegram message to the team channel: "Day [date] posts queued: [X] posts across [Y] platforms."

#### Quality checklist
- [ ] Every post from today's calendar row is in Buffer
- [ ] Images are correct dimensions per platform
- [ ] No broken links (click every link before scheduling)
- [ ] Hashtags included where the calendar specifies them
- [ ] Times match the calendar or use default schedule
- [ ] Calendar status updated to QUEUED_IN_BUFFER

#### Common mistakes
- Posting to wrong account (e.g., fitness content on faith account). Always check the "account" column.
- Scheduling in wrong timezone. Buffer should be set to EST. Confirm in Settings > Timezone.
- Forgetting to attach media. Posts with images get 2-3x more engagement. Never post text-only if an image is specified.
- Editing copy beyond typo fixes. Do not rewrite or "improve" posts. Post exactly as written.

#### Escalation triggers
- Calendar row is empty or has conflicting data. Flag in Slack, do not guess.
- Media file is missing from Drive. Flag, skip that post, continue with others.
- Buffer shows an account disconnected. Flag immediately. Do not try to reconnect yourself.
- Post contains a link to a page that returns a 404. Flag, do not publish.

---

### SOP 2: Comment engagement

**Frequency:** Daily
**Time:** 45-60 minutes
**Skill level:** Intermediate
**Tools:** Native platform apps (X, IG, TikTok, LinkedIn), Google Sheets (engagement tracker)

#### Steps

1. Open the engagement tracker (Google Sheet labeled "ENGAGEMENT_TRACKER"). Check the "target accounts" tab for the list of 20-30 accounts you should engage with daily.
2. Start with X/Twitter. Open each target account's profile. Find their most recent post (within last 24 hours).
3. Leave a genuine reply. Rules: (a) Reference something specific in their post. (b) Add value, ask a question, or share a related experience. (c) Keep it under 280 characters. (d) Never use generic replies like "Great post!" or single emojis.
4. Like their post after replying. If the post is a thread, like at least the first 2 tweets.
5. Log the engagement in the tracker: Date, Platform, Target Account, Post URL, Your Reply Text, Likes on Your Reply (check back next day).
6. Repeat for Instagram. Go to target accounts, leave a comment on their most recent Reel or carousel. Comments should be 2-3 sentences minimum on IG (short comments get buried).
7. Repeat for LinkedIn. Comment on target accounts' posts. LinkedIn rewards long comments (50+ words). Add a personal take or data point.
8. Respond to comments on OUR posts. Open each of our accounts. Check notifications. Reply to every comment within 24 hours. Use conversational tone, ask follow-up questions to keep threads going.
9. Check DMs on all platforms. Respond to non-spam DMs. If someone asks about pricing, services, or wants to collaborate, flag for human review.
10. Update the engagement tracker with total engagements for the day: [X] replies sent, [Y] comments on our posts answered, [Z] DMs handled.

#### Quality checklist
- [ ] Minimum 20 outbound engagements across platforms
- [ ] Every reply references something specific from the original post
- [ ] Zero generic comments ("Great post!", fire emojis, etc.)
- [ ] All comments on our posts answered within 24 hours
- [ ] DMs checked and responded to
- [ ] Engagement tracker updated

#### Common mistakes
- Generic replies. "Love this!" does nothing. Reference the specific content. Example: "The point about cold email subject lines being under 6 words matches what I've seen. Have you tested emoji in subject lines?"
- Engaging with bots or spam accounts. Check if the account is real before engaging (has real posts, consistent posting history, real followers).
- Over-promoting in replies. Never link to our products/services in comment replies unless directly asked. Provide value only.
- Skipping platforms. Engage on ALL platforms listed, not just the ones you prefer.

#### Escalation triggers
- Someone asks for pricing, proposals, or partnership details. Screenshot the message, flag in Slack.
- Negative comments about our brand or products. Do not reply. Screenshot and flag immediately.
- An account with 50K+ followers engages with us. Flag so we can respond personally.
- DM contains a business opportunity or collaboration request. Forward to team.

---

### SOP 3: Content repurposing

**Frequency:** Daily
**Time:** 60-90 minutes
**Skill level:** Intermediate
**Tools:** Google Docs (source content), Canva, CapCut (video), Google Sheets (repurposing tracker)

#### Steps

1. Open the repurposing tracker (Google Sheet). Find the next "source content" row with status "NOT_REPURPOSED."
2. Read the source content completely. It could be a blog post, a long tweet thread, a newsletter issue, or a video transcript.
3. Create 5+ variants from the source. Follow this formula:
   - **Variant 1: X/Twitter post.** Extract the single most interesting stat, claim, or insight. Write it as a standalone tweet (under 280 chars). Add a hook line at the start.
   - **Variant 2: X/Twitter thread.** Break the content into 5-7 tweet-sized chunks. First tweet is the hook. Last tweet is a CTA or summary. Number them (1/7, 2/7, etc.).
   - **Variant 3: Instagram carousel.** Pull 5-8 key points. Write each as a short slide (1-2 sentences). First slide = hook/title. Last slide = CTA. Use Canva carousel template.
   - **Variant 4: LinkedIn post.** Rewrite as a first-person narrative. Start with a bold statement or personal experience. Include line breaks every 1-2 sentences (LinkedIn rewards whitespace). 150-300 words.
   - **Variant 5: Short-form video script.** Write a 30-60 second script. Format: Hook (first 3 seconds) > Problem > Solution > CTA. Include suggested B-roll or text overlay notes.
   - **Variant 6 (if applicable): Newsletter blurb.** Write a 2-3 paragraph summary with a "read more" link.
4. Save each variant in the shared Google Drive folder: `/Content/Repurposed/[DATE]/`
5. Name files: `[DATE]_[PLATFORM]_[SOURCE_TITLE_SHORT].txt` (e.g., `20260206_twitter_thread_cold_email_framework.txt`)
6. Update the repurposing tracker: change status to "REPURPOSED," add links to each variant file, note which platforms are covered.
7. Add the variants to the content calendar for scheduling (or flag them for the posting VA).

#### Quality checklist
- [ ] Minimum 5 variants created per source
- [ ] Each variant is platform-native (not just copy-pasted across platforms)
- [ ] X posts are under 280 characters
- [ ] IG carousel has Canva file saved
- [ ] LinkedIn post has proper line breaks
- [ ] Video script has hook, problem, solution, CTA structure
- [ ] All files named correctly and saved in right folder
- [ ] Tracker updated

#### Common mistakes
- Copy-pasting the same text to all platforms. Each platform needs native formatting. A LinkedIn post that reads like a tweet looks lazy.
- Missing the hook. The first line/slide/second of every variant must grab attention. Never start with "In this post I'll discuss..."
- Making carousels too text-heavy. Max 2 sentences per slide. Use large font.
- Forgetting CTAs. Every variant needs a clear next step (follow, link in bio, reply, subscribe).

#### Escalation triggers
- Source content contains claims you can't verify (revenue numbers, health claims). Flag for review before repurposing.
- Source content mentions competitors by name. Flag to confirm we want to reference them.
- You're unsure if content needs a disclosure (affiliate link, sponsored, AI-generated). Flag.

---

### SOP 4: Hashtag research

**Frequency:** Weekly (every Monday)
**Time:** 45-60 minutes
**Skill level:** Basic
**Tools:** RiteTag, Hashtagify, native platform search, Google Sheets (hashtag tracker)

#### Steps

1. Open the hashtag tracker (Google Sheet). Check which niches need updated hashtags this week (rotate through all niches over the month).
2. For X/Twitter: Search each niche keyword in the X search bar. Click "Latest" tab. Note which hashtags appear in posts with 100+ likes. Record the top 10.
3. For Instagram: Open the Instagram search. Type each niche keyword. Check "Tags" results. Record hashtags with 10K-500K posts (avoid over 1M = too competitive, under 10K = too dead).
4. For TikTok: Search niche keywords. Check "Hashtags" tab. Record hashtags with growing view counts (look for upward trends, not just high totals).
5. For LinkedIn: LinkedIn doesn't show hashtag volume. Search niche keywords, check which hashtags appear on posts with 50+ reactions. Record top 5 per niche.
6. Use RiteTag (free browser extension): paste one of our recent posts and see which hashtags it recommends. Add any new ones to the list.
7. Categorize all hashtags in the tracker into three groups:
   - **Primary (3-5):** High-volume, directly relevant. Use on every post.
   - **Secondary (5-10):** Medium-volume, niche-specific. Rotate through these.
   - **Long-tail (5-10):** Low-volume, ultra-specific. Use 2-3 per post for discoverability.
8. For each hashtag, log: Platform, Hashtag, Category (Primary/Secondary/Long-tail), Estimated Volume, Date Researched, Notes.
9. Remove any hashtags from the "active" list that have been flagged, shadowbanned, or are no longer trending.
10. Share updated hashtag sets with the posting VA and content repurposing VA.

#### Quality checklist
- [ ] At least 20 hashtags per niche per platform
- [ ] Categorized into Primary, Secondary, Long-tail
- [ ] No banned or shadowbanned hashtags (test by searching the hashtag - if zero results show, it's banned)
- [ ] Volume estimates recorded
- [ ] Previous week's dead hashtags removed
- [ ] Updated sets shared with posting VA

#### Common mistakes
- Using only high-volume hashtags. Posts get buried in 1M+ hashtag feeds. Mix sizes.
- Using banned hashtags. Instagram especially bans common hashtags without warning. Always test search them first.
- Using the same hashtag set every post. Platforms flag this as spam. Rotate Secondary and Long-tail groups.
- Forgetting LinkedIn. LinkedIn hashtags matter for discovery but most people skip them.

#### Escalation triggers
- A hashtag in our active set has been banned (search returns zero results). Remove immediately and flag.
- A trending hashtag is relevant to our niche but could be controversial. Flag before using.

---

### SOP 5: Competitor monitoring

**Frequency:** Daily
**Time:** 30-45 minutes
**Skill level:** Basic
**Tools:** Visualping (or manual browser), Google Sheets (competitor tracker), screenshot tool

#### Steps

1. Open the competitor tracker (Google Sheet). It lists 10 competitor accounts/websites per niche, with columns for: Name, Platform, URL, Last Checked, Changes Noted.
2. For each social media competitor: Open their profile. Check for new posts in the last 24 hours.
3. For each new post, log: Date, Platform, Post Type (image/video/carousel/text), Topic, Engagement (likes, comments, shares), Link to Post.
4. Flag any post with unusually high engagement (3x+ their average). Copy the post text and screenshot it. Save to `/Research/Competitor_Intel/[DATE]/`.
5. For each website competitor: Open their site. Check for: new blog posts, new products/features, pricing changes, new landing pages, new lead magnets.
6. Log any changes: Date, Competitor, What Changed, URL, Screenshot Saved (Y/N).
7. Check competitor email lists (you should be subscribed to all 10). Screenshot any new emails received. Log: Date, Competitor, Subject Line, Offer/CTA, Screenshot File.
8. If using Visualping: Check alerts dashboard. Any new change alerts, log them in the tracker and take screenshots.
9. At end of daily check, write a 2-3 sentence summary in the tracker: "Summary [DATE]: [Competitor X] launched new pricing page. [Competitor Y] viral post about [topic] got 5K likes. No major changes from others."
10. If you spot a significant competitive move (new product launch, major pivot, funding announcement), flag immediately in Slack.

#### Quality checklist
- [ ] All 10 competitors checked today
- [ ] New posts logged with engagement numbers
- [ ] High-engagement posts screenshotted and saved
- [ ] Website changes documented
- [ ] Competitor emails logged
- [ ] Daily summary written
- [ ] Significant moves flagged in Slack

#### Common mistakes
- Only checking social media, ignoring websites. Product/pricing changes on websites are often more valuable intel than social posts.
- Not saving screenshots. Competitors delete posts, change pricing, remove landing pages. Always screenshot.
- Logging without analysis. Don't just record "new post." Note what's different about it (new format, new angle, new offer).
- Checking the same competitor first every day. Rotate your starting order to avoid neglecting the bottom of the list.

#### Escalation triggers
- Competitor launches a product directly competing with something we're building. Flag immediately.
- Competitor drops pricing significantly (20%+). Flag for strategic review.
- Competitor goes viral (post with 10x their normal engagement). Screenshot everything and flag.
- Competitor's website goes down or domain expires. Potential acquisition opportunity. Flag.

---

### SOP 6: UGC collection

**Frequency:** Daily
**Time:** 30 minutes
**Skill level:** Basic
**Tools:** Native platform apps, Google Drive (UGC folder), Google Sheets (UGC tracker)

#### Steps

1. Search for mentions of our brand name, product names, and relevant keywords on X, Instagram, TikTok, Reddit.
2. On X: Search for "@[our_handle]" and "[brand name]" in the search bar. Check "Latest" tab.
3. On Instagram: Check tagged photos/reels (the tag icon on our profile). Search our brand hashtag.
4. On TikTok: Search our brand name and product names. Check the "Videos" tab.
5. On Reddit: Search our brand name and product names across relevant subreddits.
6. For each piece of UGC found:
   - Screenshot or screen record it
   - Save to Google Drive: `/Content/UGC/[PLATFORM]/[DATE]_[USERNAME].png`
   - Log in UGC tracker: Date, Platform, Creator Username, Follower Count, Content Type (photo/video/text), Sentiment (positive/neutral/negative), URL, Screenshot Saved, Permission Status
7. For positive UGC with 100+ followers: Send a DM or reply thanking them and asking permission to repost. Use this template: "hey! love this. mind if we share it on our page? we'll tag you of course"
8. For negative UGC: Do NOT reply. Screenshot and flag in Slack immediately.
9. Mark permission status in tracker: REQUESTED, GRANTED, DENIED, NO_RESPONSE.
10. UGC with permission granted gets moved to `/Content/UGC/APPROVED/` and added to the content calendar for reposting.

#### Quality checklist
- [ ] All platforms searched (X, IG, TikTok, Reddit)
- [ ] Every piece of UGC logged in tracker
- [ ] Screenshots saved in correct folder
- [ ] Permission requested for repostable content
- [ ] Negative UGC flagged (never replied to)
- [ ] Tracker updated with permission status

#### Common mistakes
- Reposting without permission. Always ask first. Even a simple DM counts. Never repost without explicit "yes."
- Responding to negative UGC. Flag it. Let the team handle negative feedback.
- Missing platform-specific searches. People mention brands differently on each platform (@ on Twitter, # on Instagram, etc.).
- Not noting follower count. UGC from a creator with 50K followers is worth more attention than one from 50 followers.

#### Escalation triggers
- Negative UGC from someone with 10K+ followers. Flag immediately.
- UGC that contains misinformation about our product. Flag.
- Influencer voluntarily promoting us (potential partnership). Flag for outreach.
- UGC that could be used in paid ads (high quality, authentic). Flag for marketing team.

---

### SOP 7: Newsletter curation

**Frequency:** Weekly (every Wednesday for Friday send)
**Time:** 60-90 minutes
**Skill level:** Intermediate
**Tools:** Feedly or Pocket (RSS reader), Google Docs (newsletter draft), Google Sheets (newsletter tracker)

#### Steps

1. Open Feedly (or Pocket). Review saved articles from the past 7 days across all subscribed feeds.
2. Select 5-7 stories/links that meet these criteria:
   - Relevant to our newsletter's niche (check the niche definition doc)
   - Published within the last 7 days
   - Not behind a hard paywall
   - Has a clear takeaway or actionable insight
3. For each selected story, write a blurb (3-5 sentences):
   - Sentence 1: What happened or what the article says (the news).
   - Sentence 2-3: Why it matters to our readers (the context).
   - Sentence 4-5: What readers should do about it (the action).
4. Find 1-2 relevant stats or data points from the week. Source them properly (link to original source, not a blog quoting another blog).
5. Write a 2-3 paragraph editor's note for the intro. Rules: be conversational, share a personal take or observation, tie it to the issue's theme. Do NOT write "Welcome to this week's newsletter."
6. Compile everything into the newsletter draft template in Google Docs:
   - Editor's note (top)
   - 5-7 curated stories with blurbs
   - 1-2 stats of the week
   - CTA section (what we're promoting this week, as specified in the marketing calendar)
   - Footer (unsubscribe link, social links - already templated, don't edit)
7. Add all source links and verify every link works (click each one).
8. Save the draft and update the newsletter tracker: Issue Number, Date Drafted, Theme, Number of Stories, Draft Link, Status = "DRAFT_READY."
9. Notify the team in Slack: "Newsletter #[number] draft ready for review: [link to Google Doc]."

#### Quality checklist
- [ ] 5-7 stories, all from last 7 days
- [ ] Each story has a 3-5 sentence blurb
- [ ] Editor's note is personal and conversational (not "Welcome to...")
- [ ] All links verified and working
- [ ] Stats sourced from original data (not secondary sources)
- [ ] CTA matches this week's marketing calendar
- [ ] Draft saved and team notified

#### Common mistakes
- Including stories older than 7 days. Newsletter should feel current.
- Writing blurbs that just summarize the article. Readers want YOUR take on why it matters.
- Using secondary sources for stats ("according to a TechCrunch article that cited a Gartner report"). Find the Gartner report.
- Forgetting to check links. Dead links in a newsletter destroy credibility.
- Writing the editor's note last (and rushing it). The intro is the most read section. Write it first.

#### Escalation triggers
- Slow news week with fewer than 3 qualifying stories. Flag and ask if we should skip this week or pivot to a different angle.
- A story involves our competitors directly. Flag for review before including.
- Curated content conflicts with our product messaging. Flag.

---

### SOP 8: Reddit engagement

**Frequency:** Daily
**Time:** 45-60 minutes
**Skill level:** Advanced
**Tools:** Reddit (browser, not app), Google Sheets (Reddit engagement tracker), `LEDGER/RESEARCH_SUBREDDITS.csv` for subreddit list

#### Steps

1. Open the Reddit engagement tracker. Check today's target subreddits (rotate through 5 per day from the full list of 41).
2. For each subreddit: Sort by "Hot" and "New." Read the top 5 hot posts and top 10 new posts.
3. Find 2-3 posts per subreddit where you can add genuine value. These must be:
   - Questions where you have real expertise/data to share
   - Discussions where a different perspective adds value
   - Show-and-tell posts where constructive feedback is helpful
4. Write substantive comments (50-200 words). Rules:
   - Lead with the answer or your main point (not "Great question!")
   - Include specific details, numbers, or examples
   - Never link to our products unless the post specifically asks for recommendations in that category AND subreddit rules allow it
   - Match the subreddit's tone (r/Entrepreneur is more formal than r/SideProject)
5. Upvote posts and comments that genuinely deserve it. Do NOT mass-upvote.
6. Check for replies to your previous comments (last 48 hours). Respond to questions or pushback thoughtfully.
7. Log each engagement: Date, Subreddit, Post Title, Your Comment (first 50 chars), Upvotes on Your Comment (check next day), Link to Comment.
8. If a post's discussion reveals a pain point, product idea, or tactic relevant to our business, log it separately in the "Reddit Alpha" column.
9. Post 1 original valuable post per week (not daily). It should share genuine knowledge, a case study, or helpful resource. Never post promotional content disguised as value.
10. Check Reddit modmail and post removals. If any of your comments/posts were removed, note the reason and adjust approach for that subreddit.

#### Quality checklist
- [ ] 5 subreddits engaged (rotated from master list)
- [ ] 10-15 substantive comments posted
- [ ] Zero promotional or self-linking comments (unless explicitly relevant and allowed)
- [ ] Previous replies responded to
- [ ] Engagement tracker updated
- [ ] Any alpha findings logged separately
- [ ] Weekly original post published (if it's posting day)

#### Common mistakes
- Self-promoting. Reddit communities will ban you. Provide value for months before ever mentioning your product.
- Short, low-effort comments. "This is great!" or "Thanks for sharing" comments get downvoted and damage karma.
- Ignoring subreddit rules. Every subreddit has specific rules in the sidebar. Read them before your first post.
- Using the same comment across subreddits. Moderators cross-check. Always write unique comments.
- Engaging in arguments. If someone pushes back aggressively, reply once with facts and data, then disengage.

#### Escalation triggers
- A post directly asks about our product category and has 50+ upvotes. Flag for a strategic response (human crafted).
- A post contains negative feedback about our product. Flag immediately. Do not respond.
- You discover a potential partnership opportunity (moderator of a relevant subreddit, organizer of an AMA). Flag.
- A subreddit bans our account. Flag immediately with the reason given.

---

## Lead Generation (SOPs 9-14)

---

### SOP 9: Cold email list building

**Frequency:** Daily
**Time:** 60-90 minutes
**Skill level:** Intermediate
**Tools:** Apollo.io (or Hunter.io), Google Sheets (prospect list), LinkedIn (for verification)

#### Steps

1. Open the prospect list (Google Sheet). Check the "target criteria" tab for current ICP (Ideal Customer Profile): industry, company size, job title, geography.
2. Log into Apollo.io. Set filters to match the ICP:
   - Job Title: [as specified, e.g., "Marketing Director," "Head of Growth"]
   - Company Size: [as specified, e.g., 11-50 employees]
   - Industry: [as specified]
   - Location: [as specified, e.g., United States]
3. Export 30-50 prospects per day. Do NOT exceed 50 to maintain quality.
4. For each prospect, verify the email. Apollo marks emails as "verified" or "guessed." Only keep "verified" emails (green check). Delete "guessed" unless you can verify through another source.
5. For each verified prospect, quickly check their LinkedIn profile (10-15 seconds each):
   - Are they still at that company? (Check "Experience" section for current role)
   - Do they seem like a real person? (Profile photo, activity, connections)
   - Any recent posts about problems we solve?
6. For prospects that pass verification, add to the prospect list with these columns: First Name, Last Name, Email, Company, Title, Company Size, LinkedIn URL, Date Added, Source (Apollo), Personalization Note.
7. The "Personalization Note" is critical. Write 1 sentence about something specific to them: recent post, company news, mutual connection, relevant company detail. This goes into the cold email template.
8. Mark the prospect as "READY_FOR_OUTREACH" in the status column.
9. At end of session, update the tracker: [X] prospects researched, [Y] verified and added, [Z] rejected (with reasons).
10. Never add someone who is already in the prospect list (check for duplicate emails before adding).

#### Quality checklist
- [ ] 30-50 prospects researched
- [ ] Only verified emails kept
- [ ] LinkedIn profiles checked for currency
- [ ] Personalization note written for each
- [ ] No duplicates in list
- [ ] Daily count logged in tracker

#### Common mistakes
- Adding unverified emails. Bounced emails destroy sender reputation. Only verified.
- Skipping personalization notes. Generic cold emails get 1% reply rate. Personalized get 5-15%. The note is not optional.
- Adding people who left the company. Always check LinkedIn for current role.
- Exceeding daily limits. Apollo has export limits. Stay within them to avoid account flags.
- Duplicating prospects. Always search the existing list for the email before adding.

#### Escalation triggers
- Apollo account gets flagged or limited. Stop immediately, flag in Slack.
- You discover a prospect that's a perfect fit (C-suite at a target company). Flag for personalized outreach from the team.
- ICP criteria seem too narrow (finding fewer than 10 quality prospects per day). Flag for criteria review.

---

### SOP 10: LinkedIn connection requests

**Frequency:** Daily
**Time:** 30-45 minutes
**Skill level:** Basic
**Tools:** LinkedIn (browser), Google Sheets (connection tracker)

#### Steps

1. Open the connection tracker (Google Sheet). Check today's target: 20-30 connection requests.
2. Log into LinkedIn. Go to "My Network" > "People you may know" or use Search with the current ICP filters.
3. For each target, review their profile for 15-20 seconds:
   - Current role matches ICP
   - Active on LinkedIn (posted or engaged within last 30 days)
   - Not already connected or pending
4. Send a connection request WITH a personalized note (300 character limit). Use this framework:
   - Line 1: Reference something specific (their role, a post they made, mutual connection)
   - Line 2: Why you're connecting (shared interest, value you can provide)
   - Line 3: No pitch. Never pitch in the connection request.
5. Example note: "Hey [Name] - saw your post about cold email deliverability last week. Working on similar problems for SaaS companies. Would love to connect and exchange notes."
6. Log each request: Date, Name, Title, Company, Note Sent, Status (SENT/ACCEPTED/IGNORED).
7. Check yesterday's requests. Update status for any that were accepted.
8. For newly accepted connections, send a thank-you message within 24 hours. Template: "Thanks for connecting, [Name]. If you ever want to chat about [their area of expertise], happy to jump on a quick call."
9. Do NOT send more than 30 requests per day. LinkedIn limits are strict. 20-25 is the safe zone.
10. If your connection acceptance rate drops below 25%, flag it. Your targeting or notes may need adjustment.

#### Quality checklist
- [ ] 20-30 requests sent with personalized notes
- [ ] Zero generic "I'd like to add you to my network" messages
- [ ] Yesterday's acceptances followed up
- [ ] Tracker updated with all sends and status changes
- [ ] Daily count within LinkedIn limits (max 30)

#### Common mistakes
- Sending blank connection requests. Always include a note. Acceptance rate is 2x higher with notes.
- Pitching in the connection request. Never sell in the request. Build relationship first.
- Exceeding daily limits. LinkedIn will restrict your account. Stay under 30.
- Connecting with irrelevant people. Every connection should match the ICP.
- Not following up on acceptances. The follow-up message is where relationships start.

#### Escalation triggers
- LinkedIn account gets restricted (can't send requests). Stop immediately. Flag.
- Someone responds with strong interest in our services. Forward the conversation.
- Connection acceptance rate drops below 20% for 3 consecutive days. Flag for targeting review.

---

### SOP 11: Lead qualification

**Frequency:** As-needed (when new inbound leads arrive)
**Time:** 15-20 minutes per lead
**Skill level:** Intermediate
**Tools:** Google Sheets (lead tracker), LinkedIn, company website, Crunchbase (free)

#### Steps

1. New lead arrives (form submission, email reply, DM). Open their record in the lead tracker.
2. Research the person (5 minutes):
   - LinkedIn profile: current role, company size, how long in role, relevant experience
   - Company website: what they do, how big they are, do they have the problem we solve
   - Crunchbase (if B2B): funding stage, employee count, revenue estimate
3. Score the lead using the BANT framework:
   - **Budget:** Can they afford our offering? (Check company size, funding, role seniority)
   - **Authority:** Are they the decision-maker? (Check if their title includes Director, VP, Head of, Owner, Founder)
   - **Need:** Do they have the problem we solve? (Check their website, recent posts, form submission notes)
   - **Timeline:** Are they likely buying soon? (Check if they mentioned urgency, deadlines, current pain)
4. Assign a score: HOT (3-4 BANT criteria met), WARM (2 criteria), COLD (0-1 criteria).
5. Write a 2-3 sentence qualification summary: "John Smith, Marketing Director at Acme Corp (50 employees, Series A). Company blog shows they're scaling content marketing. HOT - has budget, authority, and clear need."
6. Update lead tracker: Name, Company, Score (HOT/WARM/COLD), Qualification Summary, Next Action (e.g., "Send case study" or "Schedule call").
7. For HOT leads: Flag in Slack immediately for fast follow-up.
8. For WARM leads: Add to nurture sequence (email drip).
9. For COLD leads: Add to long-term newsletter list.

#### Quality checklist
- [ ] LinkedIn profile researched
- [ ] Company website checked
- [ ] BANT score assigned
- [ ] Qualification summary written
- [ ] Lead tracker updated
- [ ] HOT leads flagged immediately

#### Common mistakes
- Scoring based on gut feel instead of BANT criteria. Use the framework every time.
- Spending too long on one lead. 15-20 minutes max. If you can't find enough info, mark as WARM and move on.
- Marking everyone as WARM to avoid decisions. Be honest. COLD leads are fine, they just go to a different sequence.
- Not flagging HOT leads immediately. Speed-to-response is the #1 predictor of conversion. HOT leads need contact within 1 hour.

#### Escalation triggers
- HOT lead from a company with 500+ employees or known brand. Flag for personal outreach from founder.
- Lead mentions a competitor by name. Flag for competitive positioning.
- Lead's form submission indicates urgent timeline ("need this by next week"). Flag immediately.

---

### SOP 12: CRM data entry

**Frequency:** Daily (end of day)
**Time:** 20-30 minutes
**Skill level:** Basic
**Tools:** Google Sheets (CRM), email client (to check correspondence)

#### Steps

1. Open the CRM (Google Sheet). Go to the "Pipeline" tab.
2. Check all communication channels for new interactions from today: email inbox, LinkedIn messages, X DMs, Instagram DMs, form submissions.
3. For each new interaction:
   - If the person is already in the CRM, update their row: Last Contact Date, Last Action (e.g., "Replied to email, asked about pricing"), Next Action, Pipeline Stage.
   - If the person is new, create a new row: Name, Email, Company, Source (where they came from), Date Added, First Interaction Summary.
4. Update pipeline stages as needed:
   - AWARENESS: They know about us (subscribed, followed)
   - INTEREST: They engaged (replied, commented, clicked)
   - CONSIDERATION: They asked about pricing or specifics
   - DECISION: They requested a proposal or trial
   - CLOSED_WON: They paid
   - CLOSED_LOST: They declined or went silent (30+ days no response)
5. Check for stale leads: anyone in INTEREST or CONSIDERATION for more than 14 days without a next action. Add a follow-up action.
6. Log the daily summary at the bottom of the "Activity Log" tab: Date, New Leads Added, Interactions Logged, Pipeline Stage Changes, Notes.
7. Verify no duplicate entries (search for email before creating a new row).

#### Quality checklist
- [ ] All today's interactions logged
- [ ] Pipeline stages current
- [ ] Stale leads identified and flagged for follow-up
- [ ] No duplicate entries
- [ ] Activity log updated

#### Common mistakes
- Forgetting to check all channels. People might DM on Instagram but email on a different day. Check everything.
- Not updating pipeline stages. A lead who asked for pricing is not still in "AWARENESS."
- Creating duplicate entries. Always search by email before adding a new row.
- Leaving "Next Action" blank. Every lead in an active stage needs a next action.

#### Escalation triggers
- Lead in DECISION stage for 3+ days without a response from us. Flag immediately.
- More than 5 new leads in a single day (unusual spike). Flag to understand source.
- Lead asks to be removed from our communications. Flag and remove from all lists immediately (compliance).

---

### SOP 13: Local business prospecting

**Frequency:** Weekly
**Time:** 2-3 hours
**Skill level:** Intermediate
**Tools:** Google Maps, Google Search, Google Sheets (prospect tracker), Wappalyzer (browser extension)

#### Steps

1. Open the prospect tracker. Check this week's target: industry vertical and geographic area (e.g., "Dentists in Austin, TX" or "Gyms in Miami, FL").
2. Open Google Maps. Search for "[business type] in [city]."
3. For each business in the results (work through 30-50 per session):
   - Click their listing. Note: Name, Address, Phone, Rating, Number of Reviews, Website URL.
   - Open their website (if they have one). Check:
     - Is it mobile-responsive? (Resize your browser window to phone size)
     - Does it look modern or outdated? (Built in the last 2 years vs. obviously old)
     - Does it load fast? (If it takes more than 3 seconds, note it)
     - Do they have online booking/scheduling?
     - Are they running Google Ads? (Check if their listing has an "Ad" label)
   - If they have NO website, mark them as "NO_WEBSITE" in the tracker. These are high-priority prospects.
4. Use Wappalyzer extension to check their tech stack: What CMS? (WordPress, Wix, Squarespace, custom). What analytics? What marketing tools?
5. Check their social media presence: do they have Instagram, Facebook, TikTok? How active? Last post date? Follower count?
6. Assign a prospect score:
   - **A (Hot):** No website OR terrible website + good Google reviews (they have a real business but bad digital presence)
   - **B (Warm):** Decent website but missing key features (no booking, no blog, no SEO)
   - **C (Cold):** Good website, active social, clearly has marketing handled
7. Log in tracker: Business Name, Address, Phone, Website, CMS, Rating, Reviews, Social Presence, Score (A/B/C), Notes, Contact Email (if findable).
8. For Score A and B businesses, try to find a decision-maker email:
   - Check website "About" or "Contact" page
   - Check LinkedIn for the owner/manager
   - Use Hunter.io domain search
9. Mark prospects with verified emails as "READY_FOR_OUTREACH."
10. Weekly summary: [X] businesses researched, [Y] Score A, [Z] Score B, [W] ready for outreach.

#### Quality checklist
- [ ] 30-50 businesses researched
- [ ] Each scored A/B/C with justification
- [ ] Websites checked for mobile, speed, booking, modernity
- [ ] Social media presence noted
- [ ] Contact emails found for A and B prospects
- [ ] Tracker fully updated
- [ ] Weekly summary written

#### Common mistakes
- Only checking the first page of Google Maps results. Go through at least 3 pages.
- Not actually visiting the website. Don't just note if it exists. Check its quality.
- Scoring too generously. A business with a decent Wix site and active Instagram is a C, not a B.
- Skipping the social media check. A business with no social media is often a better prospect than one with no website.
- Not finding the email. LinkedIn + Hunter.io finds emails for 60-70% of local businesses. Do the extra step.

#### Escalation triggers
- You find a cluster of 5+ Score A businesses in one area (indicates an underserved market). Flag for geographic targeting.
- A business has terrible reviews AND a bad website. They may be struggling, approach carefully. Flag.
- You find a business actively looking for a web developer (job posting, Facebook post). Flag for immediate outreach.

---

### SOP 14: Review mining

**Frequency:** Weekly
**Time:** 60-90 minutes
**Skill level:** Intermediate
**Tools:** App Store, Google Play, G2, Trustpilot, Google Sheets (pain points tracker)

#### Steps

1. Open the pain points tracker (Google Sheet). Check which competitors are scheduled for review mining this week (rotate through all competitors monthly).
2. For app competitors: Go to their App Store and Google Play listings. Sort reviews by "Most Recent."
3. Read through the last 50 reviews (both 1-star and 5-star are valuable).
4. For each review, extract:
   - **Pain points** (1-3 star reviews): What specific complaint? Categorize: UX issue, missing feature, pricing complaint, reliability problem, support problem.
   - **Love points** (4-5 star reviews): What specific praise? Categorize: feature praise, ease of use, value for money, support quality.
5. For SaaS/service competitors: Go to G2, Trustpilot, Capterra. Repeat the same process.
6. For each pain point, log: Competitor Name, Source (App Store/G2/etc), Star Rating, Category, Exact Quote, Date, Our Opportunity (how we could solve this).
7. After mining all reviews, group pain points by category. Count frequency:
   - If 10+ reviews mention the same issue, mark it as "HIGH_FREQUENCY."
   - If 5-9 reviews, mark "MEDIUM_FREQUENCY."
   - If 1-4 reviews, mark "LOW_FREQUENCY."
8. For HIGH_FREQUENCY pain points, write a 1-2 sentence opportunity brief: "15 users complained about [competitor]'s lack of offline mode. We could differentiate by offering offline-first functionality."
9. Update the pain points tracker with all findings.
10. Write a weekly summary: Top 3 pain points found, Top 3 love points (what competitors do well), recommendations.

#### Quality checklist
- [ ] 50+ reviews read per competitor
- [ ] Pain points categorized and counted
- [ ] Exact quotes saved (not paraphrased)
- [ ] Frequency tags assigned
- [ ] Opportunity briefs written for HIGH_FREQUENCY issues
- [ ] Weekly summary completed

#### Common mistakes
- Only reading 1-star reviews. 5-star reviews tell you what competitors do RIGHT (and what you must match).
- Paraphrasing instead of quoting. Use the customer's exact words. Their language is what resonates in your marketing copy.
- Ignoring review date. A complaint from 2 years ago may be fixed. Focus on reviews from the last 6 months.
- Not counting frequency. One complaint is an anecdote. 15 complaints are a market opportunity.

#### Escalation triggers
- A HIGH_FREQUENCY pain point directly aligns with a feature we already have. Flag for marketing content (comparison page, ad copy).
- Reviews mention our product by name as an alternative. Flag immediately (positive or negative).
- A competitor's recent reviews show a sharp decline in ratings. Flag (possible opportunity to capture churning users).

---

## Research (SOPs 15-19)

---

### SOP 15: Daily alpha scan

**Frequency:** Daily
**Time:** 45-60 minutes
**Skill level:** Intermediate
**Tools:** X/Twitter, Reddit, Google Sheets (alpha tracker), `LEDGER/HIGH_SIGNAL_SOURCES.csv` for account list

#### Steps

1. Open X/Twitter. Check the 10 accounts listed in today's rotation from `HIGH_SIGNAL_SOURCES.csv`. Read their posts from the last 24 hours.
2. For each account, look for:
   - Specific revenue numbers or growth metrics
   - New tools, platforms, or APIs mentioned
   - Tactics with step-by-step breakdowns
   - Failed experiments with lessons learned
   - Industry shifts or algorithm changes
3. If you find something actionable, log it in the alpha tracker: Date, Source (@handle), Category (APP_FACTORY/CONTENT_FORMAT/OUTBOUND/GROWTH_HACK/TOOL_ALPHA/MONETIZATION), Summary (2-3 sentences), Specific Numbers (if any), Link, Status = PENDING_REVIEW.
4. Switch to Reddit. Check 5 target subreddits (rotate daily). Sort by "Hot" and "Top - Past 24 Hours."
5. Look for posts with 50+ upvotes that contain:
   - Real revenue/traffic numbers (not "I made a lot of money")
   - Detailed breakdowns of what worked
   - Tool comparisons with data
   - Failure post-mortems
6. Log any findings in the alpha tracker with the same format.
7. Quick scan Google Trends (trending searches) and Product Hunt (today's launches) for 5 minutes each. Log anything relevant.
8. Apply the bot detection check (from `alpha-review.md`): For any finding with big numbers, check engagement ratio, comment quality, account age. Mark suspicious findings with "ENGAGEMENT_SUSPICIOUS" note.
9. Daily summary in the tracker: "Scanned [X] accounts, [Y] subreddits. Found [Z] entries. Top finding: [brief description]."
10. Any finding that could generate immediate revenue or is time-sensitive should be flagged in Slack with "URGENT ALPHA" prefix.

#### Quality checklist
- [ ] 10 Twitter accounts checked
- [ ] 5 subreddits scanned
- [ ] Google Trends and Product Hunt quick-scanned
- [ ] All findings logged with proper format
- [ ] Bot detection applied to big claims
- [ ] Daily summary written
- [ ] Time-sensitive findings flagged

#### Common mistakes
- Logging vague hype as alpha. "AI is changing everything" is not alpha. "$47K MRR from AI voice cloning tutorials with 23% conversion rate" is alpha.
- Trusting screenshots without skepticism. Revenue screenshots are trivially fakeable. Note "UNVERIFIED" for screenshot-only proof.
- Skipping the thread/replies. The real alpha is often in the self-reply thread, not the main post.
- Only checking text posts. Check images, videos, and linked articles too.

#### Escalation triggers
- Discovery of a tactic we can implement immediately with existing tools. Flag as "SAME_DAY_ACTIONABLE."
- A major platform announces algorithm or policy changes. Flag immediately.
- A competitor or someone in our space goes viral. Flag for analysis.
- A new tool or API is launched that could save significant time/money. Flag with pricing and URL.

---

### SOP 16: Product research

**Frequency:** Weekly
**Time:** 2-3 hours
**Skill level:** Intermediate
**Tools:** TikTok, Amazon (BSR), Etsy, Google Sheets (product research tracker), Helium10 (if available)

#### Steps

1. Open the product research tracker. Check this week's focus: TikTok Shop trending, POD (Print on Demand) opportunities, or dropshipping/arbitrage.
2. **TikTok Shop research:**
   - Open TikTok. Go to Shop tab or search "TikTok Shop" trending.
   - Browse "Best Sellers" and "Trending" categories.
   - For each interesting product, note: Product name, Price, Sales volume (if visible), Number of videos, Top video view count, Commission rate (for affiliates).
   - Look for products with high video views but low seller count (opportunity gap).
3. **Amazon BSR research:**
   - Pick 3 categories from the rotation list.
   - Check Best Sellers, New Releases, and Movers & Shakers.
   - For products in the top 50, note: Product name, Price, BSR rank, Rating, Number of reviews, Monthly sales estimate (use Helium10 if available).
   - Look for products with high demand but few reviews (new or underserved market).
4. **POD/Etsy research:**
   - Search trending themes and niches on Etsy.
   - Check which designs/products are in "Trending" and "Editor's Picks."
   - Note: Design theme, Price range, Number of sales, Number of competing listings.
5. For each promising product, do a quick viability check:
   - Can we source or create this? (POD, wholesale, digital)
   - Estimated margin (sell price - cost - fees - shipping)
   - Competition level (Low: <50 sellers, Medium: 50-200, High: 200+)
   - Trend direction (rising, stable, declining - check Google Trends for the keyword)
6. Score products: A (margins 40%+, low competition, rising trend), B (margins 25-40%, medium competition), C (margins under 25% or high competition).
7. Log everything in the tracker: Date, Platform, Product, Category, Price Range, Estimated Margin, Competition Level, Trend Direction, Score, Notes.
8. For Score A products, write a 1-paragraph opportunity brief.
9. Weekly summary: [X] products researched, [Y] Score A opportunities, top recommendations.

#### Quality checklist
- [ ] All assigned platforms researched
- [ ] Products scored A/B/C
- [ ] Margins estimated (not guessed)
- [ ] Competition level assessed
- [ ] Google Trends checked for each top product
- [ ] Tracker updated
- [ ] Weekly summary written

#### Common mistakes
- Chasing fad products without checking trend direction. A product trending DOWN is not an opportunity, it's a trap.
- Overestimating margins. Always include ALL costs: product cost, platform fees, shipping, returns, packaging.
- Ignoring competition level. A great product with 500 competitors is a bad product.
- Not checking if we can actually source/create the product. Research means nothing if we can't execute.

#### Escalation triggers
- Score A product that aligns with our existing niches. Flag for immediate action.
- A product category showing explosive growth (10x+ in Google Trends). Flag.
- A successful product that we could create a better version of. Flag with improvement ideas.

---

### SOP 17: App Store research

**Frequency:** Weekly
**Time:** 60-90 minutes
**Skill level:** Intermediate
**Tools:** App Store, Google Play, Sensor Tower (free tier) or AppFigures, Google Sheets (app tracker)

#### Steps

1. Open the app tracker (Google Sheet). Check this week's competitor apps to monitor (10 per week, rotating).
2. For each app:
   - App Store: Note current rating, number of ratings this week (vs. last week), rank in category, last update date, what's new text.
   - Google Play: Note rating, installs (range), rank, last update, what's new.
3. Check the "What's New" section for feature updates. Log any new features.
4. Read the 10 most recent reviews (both 1-star and 5-star). Note common themes. (Cross-reference with SOP 14 if same app.)
5. Check if the app has changed pricing (subscription tiers, free trial length, one-time purchases). Log any changes.
6. Search the App Store for our target keywords (5-10 keywords). Note which apps appear in top 10 results. Track position changes week over week.
7. Check for new competitor apps that weren't on our radar. Search category pages and "Apps We Love" features.
8. For our own apps (if live): Check ranking, rating, downloads, keyword positions. Log all metrics.
9. Update the tracker: App Name, Platform, Rating, Rating Change, Rank, Rank Change, New Features, Pricing Changes, Notable Reviews.
10. Weekly summary: Ranking changes, new competitor apps, feature launches, pricing moves, keyword position changes.

#### Quality checklist
- [ ] All 10 competitor apps checked
- [ ] Ratings and ranking changes logged
- [ ] New features documented
- [ ] Pricing changes noted
- [ ] Recent reviews read and themes extracted
- [ ] Keyword rankings tracked
- [ ] New competitor apps identified
- [ ] Our own apps' metrics logged

#### Common mistakes
- Only checking one platform (App Store but not Play Store). Always check both.
- Not tracking week-over-week changes. Raw numbers are less useful than trends.
- Missing pricing changes. Competitors test pricing constantly. A price drop could signal a new strategy.
- Ignoring "last updated" date. An app that hasn't been updated in 6+ months may be abandoned (opportunity to capture their users).

#### Escalation triggers
- Competitor launches a feature that directly competes with our core offering. Flag immediately.
- Our app's rating drops below 4.0. Flag with review analysis.
- A new app enters our category with significant funding or marketing push. Flag.
- A keyword we target drops in ranking significantly (5+ positions). Flag.

---

### SOP 18: Price monitoring

**Frequency:** Weekly (Wednesday)
**Time:** 30-45 minutes
**Skill level:** Basic
**Tools:** Visualping (or manual), competitor websites, Google Sheets (pricing tracker)

#### Steps

1. Open the pricing tracker (Google Sheet). It lists competitor pricing pages, product prices, and subscription tiers.
2. Visit each competitor's pricing page (10-15 competitors).
3. Compare current pricing to last week's entry:
   - Any tier prices changed? (Up or down)
   - Any new tiers added or removed?
   - Free trial length changed?
   - Any new add-ons or upsells?
   - Annual vs monthly pricing changes?
   - Any special offers or discounts visible?
4. Log changes: Competitor, Date, What Changed, Old Price, New Price, Notes.
5. If Visualping is set up: Check the alerts dashboard. Confirm any alerts match what you see on the page. Sometimes Visualping catches changes in page layout, not pricing. Verify.
6. Screenshot any pricing page that changed. Save to `/Research/Pricing/[COMPETITOR]_[DATE].png`.
7. For products we sell on marketplaces (Gumroad, Whop, etc.), check if competitors have launched similar products. Note their pricing.
8. If a competitor drops pricing by 20%+ or launches a significant new discount, flag immediately.
9. Update tracker with "No Changes" for competitors with stable pricing (still document that you checked).
10. Weekly summary: [X] competitors checked, [Y] pricing changes detected, notable: [brief description of biggest change].

#### Quality checklist
- [ ] All competitors' pricing pages visited
- [ ] Changes logged with old vs new prices
- [ ] Screenshots saved for any changes
- [ ] Visualping alerts verified
- [ ] Marketplace pricing checked
- [ ] Weekly summary written

#### Common mistakes
- Only checking the main pricing page. Some products have add-on pricing, usage-based pricing, or enterprise pricing on separate pages.
- Not noting "no changes." If you don't record that you checked, there's no proof you did.
- Forgetting to check annual pricing. Competitors often change annual discounts without changing monthly prices.
- Confusing promotional pricing with permanent changes. Note if a price change appears to be a limited-time offer.

#### Escalation triggers
- Competitor drops price by 20%+ (potential price war). Flag.
- Competitor launches a free tier that competes with our paid product. Flag.
- Competitor significantly increases prices (potential opportunity to capture price-sensitive customers). Flag.

---

### SOP 19: Trend spotting

**Frequency:** Daily
**Time:** 30-45 minutes
**Skill level:** Intermediate
**Tools:** Google Trends, TikTok Discover, Reddit Popular, Twitter Trending, Google Sheets (trend tracker)

#### Steps

1. Open Google Trends. Check:
   - "Trending Searches" (Real-time): Note any trends relevant to our niches.
   - Search our core keywords (5-10): Check if interest is rising, stable, or declining over the past 7 days.
   - Check "Related Queries" for each keyword: Note any new breakout queries (labeled "Breakout" = 5000%+ increase).
2. Open TikTok. Check the Discover/For You page:
   - Note trending sounds and hashtags in our niches.
   - Look for content formats getting high engagement (before-after, storytelling, tutorial, etc.).
   - Note any new creators in our space gaining rapid followers.
3. Check Reddit Popular and Trending subreddits:
   - Any new subreddits growing rapidly that relate to our niches?
   - Any memes or cultural moments we should comment on?
4. Check X/Twitter Trending:
   - Any hashtags or topics relevant to our niches?
   - Note the conversation (what's the sentiment? is it negative or positive?).
5. For each trend spotted, log: Date, Platform, Trend Description, Relevance to Our Niches (1-5 scale), Potential Content Angle, Time Sensitivity (can we ride this trend today, this week, or is it long-term?).
6. For high-relevance, time-sensitive trends: Draft a quick content idea (1-2 sentences) and flag in Slack.
7. For long-term trends: Add to the "Long-Term Trends" tab in the tracker for strategic review.
8. Cross-reference: Does this trend match any alpha we've already logged? Note connections.
9. Daily summary: Top 3 trends spotted, relevance, recommended action.

#### Quality checklist
- [ ] Google Trends checked (trending + our keywords + related queries)
- [ ] TikTok Discover scanned
- [ ] Reddit Popular checked
- [ ] X Trending checked
- [ ] All trends logged with relevance score
- [ ] Time-sensitive trends flagged in Slack
- [ ] Daily summary written

#### Common mistakes
- Spotting trends too late. If everyone is already talking about it, we missed the wave. Focus on "Breakout" queries and emerging trends.
- Forcing irrelevant trends. Not every trend is relevant. A 1-2 relevance score means skip it.
- Not acting on time-sensitive trends. If a trend is hot today, flagging it for "next week's content calendar" is too late. Flag immediately.
- Only checking one platform. Trends often start on TikTok, spread to X, then hit mainstream. Check all platforms.

#### Escalation triggers
- A breakout trend directly related to our niche (5/5 relevance). Flag immediately with content angle.
- A negative trend about our industry (e.g., "X industry is a scam" trending). Flag for crisis response review.
- A new platform or feature launch trending (e.g., new social media app, new monetization feature). Flag for first-mover evaluation.

---

## Operations (SOPs 20-23)

---

### SOP 20: Customer support

**Frequency:** Daily (2-3 times per day)
**Time:** 30-60 minutes total
**Skill level:** Basic
**Tools:** Email client, social media DMs, Google Sheets (support tracker), `OPS/SUPPORT/` (templates and playbooks)

#### Steps

1. Check all support channels. Order of priority: Email > X DMs > IG DMs > Reddit mentions > Comment replies.
2. For each incoming message, categorize:
   - **FAQ:** Question already answered in our FAQ. Use the canned response from `OPS/SUPPORT/FAQ_MASTER.md`.
   - **Technical Issue:** App crash, feature not working, login problem. Use troubleshooting guide from `OPS/SUPPORT/troubleshooting_guides/`.
   - **Billing/Payment:** Subscription question, refund request, payment failed. Use template from `OPS/SUPPORT/canned_responses/billing_issues.md`.
   - **Feature Request:** User wants something we don't have. Log it, thank them, use feature request template.
   - **Escalation:** Angry customer, legal threat, complex issue. Flag immediately, do NOT respond.
3. Respond using the appropriate template. Personalize it: use their name, reference their specific issue, don't just copy-paste the template verbatim.
4. Response time targets: First reply within 4 hours. Resolution within 24 hours for FAQ/simple issues. 48 hours for technical issues.
5. Log every interaction: Date, Channel, Customer Name/Handle, Category, Summary, Response Sent, Resolution Status (OPEN/RESOLVED/ESCALATED), Resolution Time.
6. For resolved issues, ask for feedback: "Is there anything else I can help with?" If they're satisfied, ask if they'd be willing to leave a review.
7. For unresolved issues, set a follow-up reminder for the next day.
8. End-of-day summary: [X] tickets received, [Y] resolved, [Z] escalated, average response time.

#### Quality checklist
- [ ] All channels checked (email, DMs, comments)
- [ ] Response time under 4 hours for first reply
- [ ] Templates personalized (not copy-pasted verbatim)
- [ ] Every interaction logged in tracker
- [ ] Unresolved issues have follow-up reminders
- [ ] Escalations flagged immediately
- [ ] End-of-day summary written

#### Common mistakes
- Copy-pasting templates without personalizing. Customers can tell. Use their name and reference their issue.
- Responding to escalation cases. If someone is angry or threatening legal action, do not respond. Flag immediately.
- Ignoring social media DMs. DMs are support channels too. Check them.
- Promising things you can't deliver ("I'll have the developer fix this by tomorrow"). Only promise what's in the template. For anything else, say "I'll pass this to the team and get back to you."

#### Escalation triggers
- Customer threatens to leave a negative review or report us. Flag immediately.
- Customer requests a refund. Flag (VA should not process refunds without approval).
- Customer reports a security issue or data breach. Flag immediately.
- Customer is a large account or influencer. Flag for personal response.
- Any legal language in the message. Flag immediately.

---

### SOP 21: Order fulfillment tracking

**Frequency:** Daily
**Time:** 15-30 minutes
**Skill level:** Basic
**Tools:** POD supplier dashboard (Printful/Printify), dropship supplier dashboard, Google Sheets (order tracker)

#### Steps

1. Log into each supplier dashboard. Check for new orders, in-progress orders, and shipped orders.
2. For new orders: Verify order details match what the customer purchased (correct product, size, color, shipping address). If anything looks wrong, flag immediately.
3. For in-progress orders: Check estimated completion date. If it's past the estimated date, note it in the tracker.
4. For shipped orders: Record tracking number and carrier in the order tracker. If the customer hasn't been notified automatically, send them the tracking info.
5. Check for failed orders (payment issues, out of stock, address problems). For each failed order:
   - Payment failed: Flag for re-billing or customer outreach.
   - Out of stock: Check if a substitute is available. Flag for customer contact.
   - Address problem: Flag for customer contact to verify address.
6. Check delivery status of previously shipped orders. Mark delivered orders as "DELIVERED" in the tracker.
7. Check for returns or complaints related to delivered orders. Log any issues.
8. Update the order tracker: Order ID, Customer, Product, Status (NEW/IN_PROGRESS/SHIPPED/DELIVERED/FAILED), Supplier, Tracking Number, Notes.
9. Flag any order that is 3+ days past expected delivery date.
10. Daily summary: [X] new orders, [Y] shipped, [Z] delivered, [W] issues flagged.

#### Quality checklist
- [ ] All supplier dashboards checked
- [ ] New orders verified
- [ ] Overdue orders flagged
- [ ] Tracking numbers recorded
- [ ] Failed orders identified and flagged
- [ ] Delivered orders marked
- [ ] Daily summary written

#### Common mistakes
- Forgetting to check all supplier dashboards. If we use 3 POD suppliers, check all 3.
- Not flagging overdue orders early. A 1-day delay is normal. 3+ days requires action.
- Missing failed orders. Some suppliers don't send notifications for failed orders. Check manually.
- Not recording tracking numbers. Customers will ask for tracking. It needs to be in the tracker.

#### Escalation triggers
- Order is 5+ days past expected delivery with no tracking update. Flag for supplier contact.
- Customer reports receiving wrong product. Flag immediately.
- Multiple failed orders from the same supplier (potential supplier issue). Flag.
- Customer requests express shipping after placing a standard order. Flag for pricing.

---

### SOP 22: Invoice and expense logging

**Frequency:** Weekly (every Friday)
**Time:** 30-45 minutes
**Skill level:** Basic
**Tools:** Bank/credit card statements, PayPal/Stripe dashboards, Google Sheets (`FINANCIALS/EXPENSE_TRACKER.csv`)

#### Steps

1. Open the expense tracker. Check the last entry date to know where to start.
2. Go through each payment source for new transactions since last entry:
   - Bank account statement
   - Credit card statement
   - PayPal transactions
   - Stripe dashboard (for tool subscriptions)
   - Any other payment platforms (Wise, etc.)
3. For each business expense, log: Date, Description, Category, Amount, Payment Method, Vendor, Receipt (Y/N), Tax Deductible (Y/N), Notes.
4. Categories to use (match existing tracker format): TOOLS (software subscriptions), ADVERTISING (paid ads), FREELANCERS (VA, designers), HOSTING (servers, domains), CONTENT (stock photos, music), LEGAL (compliance, filings), OTHER.
5. Download or screenshot receipts for every expense. Save to `/FINANCIALS/receipts/[YEAR]/[MONTH]/[VENDOR]_[DATE].pdf`.
6. For recurring subscriptions: Verify the amount matches last month. If it changed, note it.
7. Check for unknown charges. If you see a charge you don't recognize, flag it immediately.
8. Update totals at the bottom of the tracker: Total This Week, Total This Month, Running Monthly Total by Category.
9. Check revenue tracker (`FINANCIALS/REVENUE_TRACKER.csv`) for any new revenue that needs logging. Add new entries.
10. Weekly summary: Total expenses this week: $[X]. Categories breakdown. Any anomalies.

#### Quality checklist
- [ ] All payment sources checked
- [ ] Every expense logged with correct category
- [ ] Receipts saved for each expense
- [ ] Recurring subscriptions verified
- [ ] Revenue tracker updated if applicable
- [ ] Totals updated
- [ ] No unknown charges (or all flagged)

#### Common mistakes
- Forgetting a payment source. Check ALL of them, not just the main bank account.
- Wrong categorization. A Facebook Ad is ADVERTISING, not TOOLS. Be precise.
- Not saving receipts. Receipts are needed for tax deductions. No receipt = no deduction.
- Logging personal expenses as business. Only log business expenses. When in doubt, skip it and flag.

#### Escalation triggers
- Unknown charge on any account. Flag immediately.
- Expenses exceeding budget threshold (set in tracker). Flag when monthly total exceeds limit.
- Subscription price increased without notice. Flag for evaluation (keep or cancel).
- Duplicate charges. Flag for refund request.

---

### SOP 23: Weekly metrics reporting

**Frequency:** Weekly (every Monday for previous week)
**Time:** 60-90 minutes
**Skill level:** Intermediate
**Tools:** Google Analytics, social media analytics (native), email analytics (Beehiiv), Google Sheets (metrics dashboard)

#### Steps

1. Open the metrics dashboard (Google Sheet). Create a new row for the reporting week.
2. **Website metrics** (Google Analytics):
   - Total sessions, unique users
   - Top 5 pages by traffic
   - Bounce rate
   - Average session duration
   - Traffic sources breakdown (organic, social, direct, referral, paid)
   - Goal completions (leads captured, signups, etc.)
3. **Social media metrics** (native analytics for each platform):
   - Follower count (and change from last week)
   - Total impressions
   - Total engagements (likes, comments, shares)
   - Engagement rate (engagements / impressions)
   - Top performing post (link + metrics)
   - Profile visits
4. **Email metrics** (Beehiiv or email platform):
   - Total subscribers (and change from last week)
   - Open rate
   - Click rate
   - Unsubscribe rate
   - Top clicked link
5. **Revenue metrics** (Stripe, Gumroad, Whop, etc.):
   - Total revenue this week
   - Number of transactions
   - Average order value
   - New vs returning customers
   - Revenue by product/method
6. **Lead generation metrics:**
   - New leads captured
   - Lead source breakdown
   - Conversion rate (leads to customers)
   - Pipeline value (total potential revenue from active leads)
7. Calculate week-over-week changes for all key metrics. Use formula: ((This Week - Last Week) / Last Week) x 100.
8. Flag any metric that changed by more than 20% (positive or negative) with a note explaining possible cause.
9. Create a "Highlights and Concerns" section:
   - Top 3 wins this week (metrics that improved)
   - Top 3 concerns (metrics that declined or underperformed)
10. Share the completed report in Slack and tag the team.

#### Quality checklist
- [ ] Website metrics logged (sessions, users, bounce rate, sources)
- [ ] Social media metrics logged (per platform)
- [ ] Email metrics logged
- [ ] Revenue metrics logged
- [ ] Lead gen metrics logged
- [ ] Week-over-week changes calculated
- [ ] 20%+ changes flagged and explained
- [ ] Highlights and Concerns section written
- [ ] Report shared in Slack

#### Common mistakes
- Comparing wrong date ranges. Always compare Monday-Sunday to the previous Monday-Sunday.
- Missing a platform. If we're on 4 social platforms, report on all 4.
- Not calculating week-over-week changes. Raw numbers without context are not useful.
- Reporting vanity metrics only. Follower count without engagement rate is meaningless. Always pair vanity metrics with action metrics.
- Not explaining changes. A 30% drop in traffic means nothing without "Possible cause: Google algorithm update on Tuesday."

#### Escalation triggers
- Revenue drops 20%+ week-over-week. Flag immediately.
- Email unsubscribe rate exceeds 2%. Flag for content review.
- Website traffic drops 30%+ (possible SEO penalty or technical issue). Flag immediately.
- Social account reaches a milestone (10K, 50K, 100K followers). Flag for celebration content.

---

## Creative (SOPs 24-26)

---

### SOP 24: Basic image editing

**Frequency:** As-needed
**Time:** 15-30 minutes per batch
**Skill level:** Basic
**Tools:** Canva (free tier), Google Drive (source images), Google Sheets (asset tracker)

#### Steps

1. Check the asset request queue (Google Sheet or Slack channel). Each request specifies: source image, desired output (resize, text overlay, color adjustment), platform (determines dimensions).
2. Open Canva. Use the correct template size:
   - X/Twitter post: 1200 x 675 px
   - Instagram post: 1080 x 1080 px
   - Instagram Story/Reel: 1080 x 1920 px
   - LinkedIn post: 1200 x 627 px
   - YouTube thumbnail: 1280 x 720 px
   - Facebook post: 1200 x 630 px
3. Import the source image into the template.
4. For resizing: Adjust the image to fit the template. Use "Fit" not "Fill" if the aspect ratio is different (add background color to fill gaps).
5. For text overlay: Use the brand font (specified in brand guidelines). Text must be:
   - Large enough to read on mobile (minimum 24pt for body, 48pt for headlines)
   - High contrast against the background (use a semi-transparent overlay if needed)
   - No more than 10 words per image
6. For creating variants: Make 3 versions of each image with different:
   - Background colors (use brand palette)
   - Text positions (top, center, bottom)
   - Font sizes or styles
7. Export all images as PNG (for social posts) or JPG (for web, if file size matters). Use highest quality setting.
8. Name files: `[DATE]_[PLATFORM]_[DESCRIPTION]_v[1/2/3].png` (e.g., `20260206_instagram_cold_email_tips_v1.png`)
9. Upload to Google Drive: `/Content/Assets/[PLATFORM]/[MONTH]/`
10. Update the asset tracker: Request ID, Date Completed, Files Created (with Drive links), Notes.

#### Quality checklist
- [ ] Correct dimensions for target platform
- [ ] Text is readable on mobile (screenshot and zoom to check)
- [ ] Brand colors and fonts used
- [ ] Multiple variants created
- [ ] Files named correctly
- [ ] Uploaded to correct Drive folder
- [ ] Asset tracker updated

#### Common mistakes
- Wrong dimensions. An Instagram post at Twitter dimensions looks terrible. Always check.
- Text too small. If you can't read it on your phone at arm's length, it's too small.
- Ignoring brand colors. Don't use random colors. Stick to the palette.
- Saving at low quality. Always use highest export quality.
- Forgetting to create variants. 3 variants allows A/B testing.

#### Escalation triggers
- Request requires advanced editing (photo manipulation, custom illustration). Flag for designer.
- Brand guidelines are unclear for this type of image. Flag for clarification.
- Source image is low resolution and can't be resized without looking bad. Flag.

---

### SOP 25: Video clipping

**Frequency:** As-needed
**Time:** 30-60 minutes per long video
**Skill level:** Intermediate
**Tools:** CapCut (free), Google Drive (source videos), Google Sheets (clip tracker)

#### Steps

1. Download the source video from Google Drive or the link provided. Note the total length.
2. Watch the full video at 1.5x speed. Mark timestamps of "clip-worthy" moments:
   - Strong opening hooks (first 3 seconds that grab attention)
   - Key insights or takeaways (specific advice, numbers, stories)
   - Emotional peaks (laughter, surprise, conviction)
   - Quotable one-liners
   - Before/after reveals or demonstrations
3. For each clip-worthy moment, note: Start Time, End Time, Topic, Hook (first line), Why It's Good.
4. Open CapCut. Import the source video.
5. For each clip, cut the segment. Target lengths:
   - TikTok/Reels/Shorts: 15-60 seconds (30-45 is sweet spot)
   - X/Twitter video: 30-120 seconds
   - LinkedIn: 30-90 seconds
6. Add captions to every clip. In CapCut:
   - Use Auto Captions feature
   - Review and correct any transcription errors
   - Style: white text with black outline or background, centered bottom third
   - Font size: readable on mobile
7. Add a hook text overlay in the first 2-3 seconds of each clip (the topic or a teaser question).
8. Export each clip at highest quality. Format: MP4, 1080x1920 (vertical) for TikTok/Reels/Shorts, 1920x1080 (horizontal) for YouTube/LinkedIn.
9. Name files: `[DATE]_[PLATFORM]_[TOPIC_SHORT]_clip[N].mp4`
10. Upload to Google Drive: `/Content/Video_Clips/[SOURCE_VIDEO_NAME]/`
11. Update clip tracker: Source Video, Clip Number, Start-End Time, Topic, Platform, Duration, File Link, Status (READY/POSTED).
12. Aim for 5-8 clips per long-form video (30-60 min source).

#### Quality checklist
- [ ] Full video watched and timestamps marked
- [ ] 5-8 clips created per long-form source
- [ ] Each clip has a strong opening hook (first 3 seconds)
- [ ] Captions added and verified for accuracy
- [ ] Hook text overlay in first 2-3 seconds
- [ ] Correct dimensions per platform
- [ ] Files named and organized in Drive
- [ ] Clip tracker updated

#### Common mistakes
- Clips starting without a hook. The first 3 seconds determine if people watch. Every clip must start with something attention-grabbing.
- Captions with errors. Auto-captions are 80-90% accurate. You MUST review and correct them.
- Clips too long. For short-form platforms, under 60 seconds. Ruthlessly cut anything that doesn't add value.
- Wrong aspect ratio. Vertical (9:16) for TikTok/Reels/Shorts. Horizontal (16:9) for YouTube/LinkedIn. Never post a horizontal video on TikTok.
- Missing context. If a clip references something from earlier in the video, the clip won't make sense standalone. Only clip segments that work without context.

#### Escalation triggers
- Source video has copyrighted music in the background. Flag before posting clips.
- Source video shows faces that may not have release consent. Flag.
- Clip contains claims that need fact-checking or disclaimers. Flag.
- Video quality is too low for clipping (blurry, bad audio). Flag.

---

### SOP 26: Thumbnail creation

**Frequency:** As-needed
**Time:** 15-20 minutes per thumbnail
**Skill level:** Basic
**Tools:** Canva (free tier), Google Drive (assets), Google Sheets (thumbnail tracker)

#### Steps

1. Check the thumbnail request queue. Each request specifies: video title/topic, target platform, desired emotion/vibe, face photo (if using).
2. Open Canva. Select the YouTube thumbnail template (1280 x 720 px). Even for non-YouTube thumbnails, this size works for most platforms.
3. Choose a background:
   - Option A: Solid bold color from brand palette (works for text-heavy thumbnails)
   - Option B: Relevant photo/screenshot from the video (works for face thumbnails)
   - Option C: Gradient or pattern (works for series/branded thumbnails)
4. Add the main text (3-5 words max):
   - Font: Bold, sans-serif (Impact, Bebas Neue, or Montserrat Bold)
   - Size: Large enough to read on a phone in a feed (minimum 72pt equivalent)
   - Color: High contrast against background (white on dark, dark on light, or yellow/red on any)
   - Position: Left side or center (right side often gets cut off by video duration overlay)
5. If using a face photo:
   - Place on right 40% of the image
   - Use an expressive face (surprise, excitement, concern - NOT neutral)
   - Apply a subtle border or shadow to separate from background
6. Add visual elements to increase CTR:
   - Arrows or circles pointing to key elements
   - Emoji relevant to the topic (use sparingly, 1-2 max)
   - Number if the content is a list ("7 ways..." = put "7" large)
   - Contrast border (2-3px bright outline around the entire thumbnail)
7. Create 3 variants with different:
   - Text phrasings (same topic, different words)
   - Color schemes
   - Face expressions (if applicable)
8. Export as PNG (highest quality).
9. Name: `[DATE]_thumb_[TOPIC]_v[1/2/3].png`
10. Upload to Drive: `/Content/Assets/Thumbnails/`
11. Update thumbnail tracker: Request ID, Video Title, Variants Created, File Links, Status (READY/SELECTED/POSTED).

#### Quality checklist
- [ ] Dimensions 1280 x 720 px
- [ ] Text readable at small size (screenshot, shrink to 200px wide, can you still read it?)
- [ ] High contrast between text and background
- [ ] 3 variants created
- [ ] No more than 5 words of text
- [ ] Face is expressive (if using)
- [ ] Files properly named and uploaded

#### Common mistakes
- Too much text. Thumbnails are TINY in feeds. 3-5 words maximum. If it looks like a billboard, it has too much text.
- Low contrast. Yellow text on a white background is invisible. Always check contrast.
- Boring/neutral expressions. Thumbnails with expressive faces get 30%+ higher CTR. Never use neutral, posed photos.
- Cluttered composition. One focal point. One message. White space is your friend.
- Forgetting mobile view. 70%+ of views come from mobile. Design for the smallest screen.

#### Escalation triggers
- No brand guidelines available for the account. Flag for creative direction.
- Request requires custom illustration or advanced photo editing. Flag for designer.
- Thumbnail needs to match a specific video that hasn't been filmed yet. Flag for timing.

---

## VA management quick reference

### Onboarding checklist (for each new VA)
1. Share relevant SOPs (only the ones they'll use, not all 26)
2. Grant access to required tools (Google Sheets, Canva, Buffer, etc.)
3. Add to communication channel (Slack or Telegram)
4. Do a test task with feedback before going live
5. Set daily/weekly check-in schedule

### Performance tracking
- Weekly review: Did they complete all assigned tasks? Quality score 1-5.
- Monthly review: Are they improving? Should they get more responsibility?
- Bonus triggers: Exceeding quality standards, finding alpha, zero escalation issues for 30 days.

### Communication protocol
- VA sends end-of-day summary every working day
- VA flags escalations immediately (do not wait for summary)
- Weekly 15-minute video call for alignment
- All work logged in Google Sheets (not just "I did it")

### Cost model (OnlineJobs.ph)
| VA Role | Hours/Week | Rate | Monthly Cost |
|---------|------------|------|-------------|
| Content VA | 20 | $5/hr | $400 |
| Lead Gen VA | 15 | $5/hr | $300 |
| Research VA | 10 | $6/hr | $240 |
| Admin VA | 10 | $4/hr | $160 |
| Full-time VA (all tasks) | 40 | $5/hr | $800 |

**Start with 1 part-time VA ($300-400/mo). Scale to 2-3 VAs when revenue exceeds $3K/mo.**

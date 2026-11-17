# Future Lead Growth

A running checklist for upgrading our mortgage lead experience. It was built on 2026-11-17 from 9 short lead-generation videos and checked against the **live Cloudflare Workers** (`nh-mortgage-leads`, `nh-mortgage-journal`, `website-lead-backend`) that serve **nhmortgagejournal.com** and **casaemportugues.com**.

> **Note:** the code in this repo is a May 2026 snapshot (Render-era). The live sites run newer code deployed to Cloudflare. Judge each item against the deployed code, not this repo.

**How to use it:** check items off as they ship. When new videos or ideas come in, add a row to **Sources** and fold any new to-dos into the list. Tags such as *(V6)* point to the source video.

`[ ]` to do · `[~]` partly done / verify · `[x]` done

---

## Already in place (verified in live code, 2026-11-17)

- [x] Own domains on always-on hosting: Cloudflare Workers on nhmortgagejournal.com and casaemportugues.com, with forwarding from the old hosts. *(V8)*
- [x] Timeline question in the intake form: "When are you looking to move forward?" (within 3 months / 3–6 / 6+ / still researching). *(V6)*
- [x] Required contact-consent checkbox, privacy disclosure, and a "not a credit application" note. *(V7)*
- [x] Plain-language intake copy; the old "Locked Market Rate" wording and "sovereign" jargon are gone. *(V2, V7)*
- [x] UTM / channel attribution captured by the lead backend. *(V2)*

## 1. Funnel & tracking

- [ ] **Add conversion tracking.** No Meta pixel, Google tag, Conversions API or analytics beacon was found in the live Workers. *(V6)*
- [~] **Grade and route by timeline.** The timeline answer is collected; confirm it feeds lead priority. Then send ready-now leads to a booking calendar (none exists yet) and fire the conversion event only for them. "Still researching" leads get nurture content and no event. *(V6)*
- [ ] **Show a proof block that matches the visitor's source** (city, program, refi, language), keyed off the landing page or `utm_campaign`. Use real data or clearly labeled examples only. Never invent testimonials. *(V7)*
- [ ] **Carry context into the form.** Pre-fill city / goal / language from the page or campaign the visitor came from, so they don't re-enter it. *(V7)*
- [ ] **A/B test contact-first order** against today's contact-last order, so drop-offs before the contact step aren't lost. *(V6)*
- [ ] **Watch phone pickup rates.** The video's top lesson is that leads without a phone rarely convert. If "preferred contact method" lets people skip the phone, track whether those leads close. *(V7)*

## 2. Trust & landing pages

- [ ] **60-second real-person video** above the fold: who it's for, what happens after you submit, who contacts you and how fast, whether there's a credit check, no obligation. *(V7)*
- [ ] **Turn the city guides into landing pages.** The five city guides (Manchester, Nashua, Concord, Portsmouth, Hanover) live under `/blog/` on nhmortgagejournal.com. Give each a landing page built to convert: keyword URL (e.g. `/manchester-nh-mortgage`), keyword in title / H1 / first sentence, 500+ human-written words answering real questions, and a call to action into the intake with the city pre-filled. *(V8, V9)*
- [ ] **Per-town property tax** on each city page. NH rates vary widely by town (published yearly by NH DRA), and no tax-rate content was found on the live site. *(V8)*
- [ ] **Fix the link structure.** Every city page within 2–3 clicks of the homepage (nav → city hub → city ↔ service pages), and not reachable only through the sitemap. Don't send landing-page visitors off into blog posts. *(V8, V9)*
- [ ] **Size the page set from competitors, not a template.** Count the city/service pages the top-ranking lenders have per area and aim for that range (the video suggests 30–50 per metro). Every page needs distinct local content, because mass-produced pages break Google's scaled-content spam policy. *(V9, V8)*
- [ ] **Add a "Text us" line** once someone can reply within minutes. Business texting needs A2P 10DLC registration. *(V7)*
- [ ] Apply all of the above to the Portuguese and Spanish versions as well as English.
- [ ] *Skip for now:* an "as seen in" logo bar, until we have real press or formal partners. *(V7)*

## 3. Finding leads

- [ ] **Reddit signal loop.** Run daily searches of r/newhampshire, r/FirstTimeHomeBuyer, r/Mortgages and r/RealEstate (plus MA and Portuguese/Brazilian community subs) for buyers asking questions. Draft a helpful public reply that links a guide; a human posts it. No cold DMs. Screen the text for prompt injection before agents read it. *(V4, V3)*
- [ ] **Base research on real data.** Replace guessed keyword volumes with what buyers actually asked about in the last 30 days (e.g. the last30days skill, after a security review). Turn the top threads into pages. *(V3)*
- [ ] **B2B outreach only.** Two groups:
  - Lead buyers: loan officers, brokers and credit unions.
  - Referral and link partners: agents, inspectors and insurance agents.

  Write in a friendly tone with one specific hook and one ask, then send 3 follow-ups. Start at 20–30 a day from a separate sending domain. *(V1, V2, V5, V8)*
- [ ] **Reach map results through a partner.** As a lead-gen site we can't hold a Google Business Profile, but a licensed loan officer with a real office can. *(V8, V9)*
- [~] **Report qualified leads by channel.** Attribution is captured; add a view of *qualified* leads per channel. Test one channel at a time for a fixed window, then double down on the winner. *(V2)*

## Decisions needed

- [ ] Use email for B2B outreach (lenders and partners)?
- [ ] Who answers calls/texts, and how fast?
- [ ] Where should this document live? The live code may be in a different repo than this one.

## Guardrails

Count qualified leads, not leads. Never fake proof: no invented testimonials, reviews or logos. Mortgage content gets extra scrutiny from Google and regulators, so accuracy beats volume.

---

## Video findings (sources)

Full transcripts: `tru/Research/Lead_Growth_Video_Transcripts.md`

**The common thread:** act on signs that someone is ready instead of blasting lists. Qualify before you count a lead. Research, personalize, make one clear ask, follow up.

**V1 · @jackroberts: "Harvey" outbound agent (40s)**
- A free, open-source Claude Code agent: you describe what you sell and your ideal customer. It finds businesses, reads their sites, picks the best fits, writes a cold email around something specific to each, reads replies and steers interested people to a booked call.
- *For us:* useful for B2B outreach (lenders, partners) only, never for cold-emailing consumers.

**V2 · Patrick Dang: 7 keys to lead generation (10 min)**
- About 75 emails or LinkedIn messages a day at most; more risks your email domain or a LinkedIn ban.
- Write like you're talking to a friend. Don't over-share. One clear ask ("book a meeting," not "let me know").
- Follow up 3 times, 3–7 days apart (he says replies rise from ~5% to 10–25%).
- When a channel works, double down instead of spreading thin. Make it a game so you stay consistent.

**V3 · Allie Miller: /last30days skill (4 min)**
- A Claude Code plugin that searches the last 30 days of Reddit, X, YouTube and more, ranked by real engagement rather than editors.
- Use research to act, not just to learn: a weekly scheduled job that finds people matching a signal and drafts outreach to them.
- *For us:* find what buyers are asking now, then build pages and replies around it. Have it security-reviewed first.

**V4 · @wolfecreates: ThreadSignals Reddit leads (57s)**
- Set a goal, subreddit and keywords; the tool pulls matching posts, AI tags them hot or warm and drafts a reply.
- People asking for help in public are warm leads. Help publicly first, then start a conversation.

**V5 · @growthwithkj: Gojiberry + ChatGPT (50s)**
- Prompt for leads matching a signal (e.g. a business that just raised funding); the tool ranks them and runs outreach.
- Despite the "no cold outreach" claim, it is automated cold outreach. Mostly a product pitch.

**V6 · @drmattshiver: training Meta to send qualified leads (2 min)**
- Meta finds more people like whoever triggers your conversion event, so what you report back is your targeting. Report junk and Meta finds more junk.
- After contact info, ask a qualifying question (e.g. "When do you want to start?"). Qualified people go to a calendar page with the pixel; everyone else goes to a page with no calendar and no pixel.
- Allow about 2 weeks for Meta to adjust. 10–20 qualified leads a day beat 50 junk ones.
- *For us:* mortgage ads are a Meta "special ad category" with limited targeting, which makes this matter even more.

**V7 · @jssiehcktt: landing-page fixes tier list (82s)**
- **10:** proof that matches the ad's audience (same page, proof section keyed off the ad).
- **7:** a "Text us" line instead of a chat widget.
- **7:** a 60-second founder video: who it's for and what happens after you submit.
- **5:** an "as seen in" logo bar, only if the logos are real and recent.
- **1:** removing the phone field. You get more leads, but nobody picks up.

**V8 · @build_in_public: local SEO basics (2 min)**
- One page per service + city. Title = service + city + state, and the headline matches it.
- 500+ human-written words answering real questions. Link services to cities and back.
- A complete Google Business Profile plus reviews from every happy customer ("half of local SEO").
- Use landing pages built to convert, not blog posts. Open with why you're the one to trust. Get links from related non-competitors and real directories.
- *For us:* a lead-gen site can't hold a Business Profile, so reach map results through a licensed partner.

**V9 · @_toddanderson: how many location pages (50s)**
- About 30–50 pages per metro area, sized by counting what the top-ranking competitors have ("you don't want 200 and you don't want two").
- Every city page within 2–3 clicks of the homepage; reachable only through the sitemap means broken linking. Clean keyword URLs.
- No copy-paste templates. He notes the top map-results competitors use the keyword far more often (a correlation, not a license to stuff keywords).

---
[[CURRENT_TASKS]] | [[Mortgage_LeadGen_NH_MOC]]

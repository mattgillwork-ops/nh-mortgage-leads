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

## Sources

| # | Creator | Topic | Takeaway for us |
|---|---|---|---|
| V1 | @jackroberts | "Harvey" open-source outbound agent | AI handles research + personalized outreach; use it for B2B only |
| V2 | Patrick Dang | 7 keys to lead generation | ~75/day cap, friendly tone, one ask, follow up 3×, double down |
| V3 | Allie Miller | /last30days research skill | Research ranked by real engagement → action |
| V4 | @wolfecreates | ThreadSignals Reddit leads | People asking for help in public are warm leads |
| V5 | @growthwithkj | Gojiberry + ChatGPT | Signal-triggered outreach (mostly a product pitch) |
| V6 | @drmattshiver | Training Meta to send qualified leads | What you report back to Meta is your targeting; qualify first |
| V7 | @jssiehcktt | Landing-page fixes tier list | Proof matching the visitor (10), text-us (7), founder video (7), keep phone field |
| V8 | @build_in_public | Local SEO basics | Page per service/city, 500+ human words, internal links, landing pages over blog posts |
| V9 | @_toddanderson | How many location pages | 30–50 per metro sized by competitors; every page 2–3 clicks from home |

Full transcripts: `tru/Research/Lead_Growth_Video_Transcripts.md`

---
[[CURRENT_TASKS]] | [[Mortgage_LeadGen_NH_MOC]]

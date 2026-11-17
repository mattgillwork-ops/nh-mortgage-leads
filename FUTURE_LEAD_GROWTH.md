# Future Lead Growth

A running checklist for upgrading the NH mortgage lead experience. It was built on 2026-11-17 from 9 short lead-generation videos and an audit of our three sites (`mortgage-app`, `nh-mortgage-blog`, `nh-financial-review`).

**How to use it:** check items off as they ship. When new videos or ideas come in, add a row to **Sources** and fold any new to-dos into the list. Tags such as *(V6)* point to the source video.

`[ ]` to do · `[~]` in progress · `[x]` done

---

## 0. Foundation (first)

- [ ] **Own domain + always-on hosting.** All three sites are free Render instances on `onrender.com` (`render.yaml`). They sleep after ~15 min idle and can take up to a minute to wake. That hurts Google crawling, paid clicks and first impressions, and any links we earn point at an address we don't own. *(V8)*
- [ ] **Decide whether to fold the blog into the main site** so content and landing pages share one domain and can link to each other. *(V8, V9)*
- [ ] **Add conversion tracking.** No site has a Meta pixel, Google tag or Conversions API today. *(V6)*

## 1. Funnel (`mortgage-app`)

- [ ] **Ask "when?"** Add a timeline step (0–3 mo / 3–6 / 6–12 / just researching) to `src/components/LeadFunnel.tsx`, and use it in `scoreLead()` in `src/app/api/submit_lead/route.ts`. Today grading uses credit + LTV only. *(V6)*
- [ ] **Route by grade.** A/B leads go to a real booking calendar, which fires the conversion event. C leads go to the report + nurture content, with no event, so ad platforms only learn from qualified leads. *(V6)*
- [ ] **Carry context into the funnel.** City pages, guides and blog links should pass `city` / `goal`. Pre-fill and skip steps from them. Also read the blog calculator's `price`, `down` and `rate`, which the funnel ignores today. *(V7, V8)*
- [ ] **Show a proof block that matches the visitor's source** (city, program, refi), keyed off the link or `utm_campaign`. Use real data or clearly labeled examples only. Never invent testimonials. *(V7)*
- [ ] **Keep the phone field required, and add consent language** next to it before any automated calls or texts (TCPA). *(V7)*
- [ ] **Replace the "Locked Market Rate" label** with "today's average rate". The rate is a static number from `rates.json`, and nothing is locked. *(compliance)*
- [ ] **A/B test asking for contact info first** against today's contact-last order, so drop-offs before step 6 aren't lost. *(V6)*

## 2. Trust & landing pages

- [ ] **60-second real-person video in the hero:** who it's for, what happens after you submit, who contacts you and how fast, whether there's a credit check, no obligation. It replaces the anonymous "SA / Sovereign Mortgage Architect" block. *(V7)*
- [ ] **Plain-language copy.** Drop internal jargon ("sovereign", "intelligence dispatch") and write like you're talking to a friend. *(V2, V7)*
- [ ] **Make the city pages real landing pages.** Today there are 3 cities with ~44 words each, reachable only through the sitemap. Target: 500+ human-written words answering real questions, with the keyword in the title, URL, H1 and first sentence, and a call to action into the funnel with the city pre-filled. Merge in the blog's Manchester, Nashua, Concord, Portsmouth and Hanover guides and redirect them. *(V8, V9)*
- [ ] **Use per-town property tax** from NH DRA instead of the flat 1.8% in `src/utils/mortgage_utils.ts`. That makes each city page different and the payment estimates more accurate. *(V8)*
- [ ] **Fix the link structure.** Every city page within 2–3 clicks of the homepage (nav → city hub → city ↔ service pages). Clean keyword URLs. Don't send landing-page visitors off into blog posts. *(V8, V9)*
- [ ] **Size the page set from competitors, not a template.** Count the city/service pages the top-ranking NH lenders have per area and aim for that range (the video suggests 30–50 per metro). Every page needs distinct local content, because mass-produced pages break Google's scaled-content spam policy. *(V9, V8)*
- [ ] **Add a "Text us" line** once someone can reply within minutes. Business texting needs A2P 10DLC registration. *(V7)*
- [ ] *Skip for now:* an "as seen in" logo bar, until we have real press or formal partners. *(V7)*

## 3. Finding leads

- [ ] **Reddit signal loop.** Run daily RSS searches of r/newhampshire, r/FirstTimeHomeBuyer, r/Mortgages and r/RealEstate for NH terms. Rowan triages, Nova drafts a helpful public reply that links a guide, and a human posts it. No cold DMs. Pass the text through `security_gate.py` before agents read it. *(V4, V3)*
- [ ] **Base research on real data.** Replace the guessed keyword volumes in `research_drive.py` with what NH buyers actually asked about in the last 30 days (e.g. the last30days skill, after Atlas vets it). Turn the top threads into pages. *(V3)*
- [ ] **B2B outreach only.** Two groups:
  - Lead buyers: NH loan officers, brokers and credit unions.
  - Referral and link partners: agents, inspectors and insurance agents.

  Write in a friendly tone with one specific hook and one ask, then send 3 follow-ups. Start at 20–30 a day from a separate sending domain. *(V1, V2, V5, V8)*
- [ ] **Reach map results through a partner.** As a lead-gen site we can't hold a Google Business Profile, but a licensed NH loan officer with a real office can. *(V8, V9)*
- [ ] **Per-channel reporting.** Add qualified leads by UTM source to `scripts/monitor_leads.py`. Test one channel at a time for a fixed window, then double down on the winner. *(V2)*

## Decisions needed

- [ ] Pay for a domain + always-on hosting?
- [ ] Merge the blog into the main site?
- [ ] Reopen email (currently "out of scope" in `GEMINI.md`) for B2B outreach only?
- [ ] Who answers calls/texts, and how fast? (Today's funnel promises a call within 24 hours.)

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

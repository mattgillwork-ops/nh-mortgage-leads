# Future Lead Growth

Our recommendation sheet for growing and upgrading the lead experience. It was built on 2026-11-17 from 9 short lead-generation videos (summarized at the bottom) and checked against the **live Cloudflare build**.

`[ ]` to do · `[~]` partly done / verify · `[x]` done

---

## Our business

- **Model:** we source leads and make a **warm connection** to a partner mortgage company or real estate company, and the partner closes. Our product is a qualified, ready lead, introduced quickly, in the lead's language.
- **Live build:** Cloudflare Workers serving **nhmortgagejournal.com** (English) and **casaemportugues.com** (Portuguese), plus a Spanish version. A shared intake form feeds a lead backend that handles attribution and lead history.
- **Market 1 (priority): Portuguese-speaking Brazilian communities in Massachusetts and nearby.** Middlesex County, MA had the largest Brazilian population of any US county in the 2020 Census.
- **Market 2: English speakers in southern New Hampshire and Massachusetts.**

**Target cities for Market 1.** Estimates are from Census-based sources and should be verified with ACS tables before anything is published.

| Tier | City | Why |
|---|---|---|
| 1 | **Everett, MA** | Largest Brazilian count in MA (~5,100, ~10% of residents) |
| 1 | **Milford, MA** | Densest community (~4,700, ~15.5% of residents) |
| 1 | **Marlborough, MA** | ~4,500, ~11% of residents |
| 1 | **Framingham, MA** | Historic hub of the community; long the largest |
| 2 | Worcester, Somerville, Malden, Lowell | Large communities, smaller share of the population |
| Nearby | **Nashua, NH** | Where most of NH's Brazilian community lives; overlaps with Market 2 |
| Nearby | Danbury, CT | Well-documented Brazilian hub, if CT is in scope |

Sources: [Neilsberg ACS ranking](https://www.neilsberg.com/insights/lists/brazilian-population-in-massachusetts-by-city) · [BPDA](https://www.bostonplans.org/getattachment/ec7b992e-a2e7-485a-b02a-04436b496d6e) · [Census 2020](https://census.gov/library/stories/2023/10/2020-census-dhc-a-some-other-race-population.html) · [GBH](https://www.wgbh.org/news/local/2024-10-24/new-report-says-brazilians-the-biggest-immigrant-group-in-mass-shouldnt-be-forgotten) · [WBJ](https://wbjournal.com/article/brazilian-americans-have-transformed-metrowest-communities-like-framingham-and-marlborough) · [NHPR](https://www.nhpr.org/nh-news/2022-06-17/nh-brazilian-immigrant-healthcare-training-doctors-providers-mental-health) · [Boston Fed](https://www.bostonfed.org/-/media/Documents/cb/PDF/2006_winter_mapping.pdf)

---

## Already in place (verified in live code)

- [x] Own domains on always-on Cloudflare hosting, with forwarding from the old hosts.
- [x] Timeline question: "When are you looking to move forward?" (within 3 months / 3–6 / 6+ / still researching).
- [x] Language choice (English / Portuguese / Spanish) and preferred contact method.
- [x] Required consent checkbox, privacy disclosure, "not a credit application" note, and a spam trap.
- [x] UTM / channel attribution in the lead backend.
- [x] MassHousing content on the journal.

---

## The short list (in priority order)

1. [ ] **Make consent and privacy cover the handoff.** Today the text only authorizes "NH Mortgage Journal's team" to contact the lead, and the privacy note doesn't mention sharing. Since a partner lender or agent makes the follow-up call, say so plainly in every language. At the same time, check that how partners pay us (per lead, per introduction or per closing) fits RESPA Section 8 and MA/NH licensing rules. *Ask a lawyer; this protects the whole business.*
2. [ ] **Make the warm handoff the product.**
   - Contact each new lead within minutes, in their language, and confirm timeline, goal and city.
   - Then introduce them for real to a partner who speaks their language, by three-way call or an introduction text.
   - Track every lead from introduction to partner contact to close, using partner feedback.
   - Leads that came in without a phone number need watching; the videos say they rarely convert. *(V6, V7, V2)*
3. [ ] **Build a bench of Portuguese-speaking partners** (loan officers and agents) in the Tier 1 cities, using V1/V2-style outreach (one specific hook, one ask, 3 follow-ups). Partners also supply what a lead-gen site can't have: Google Business Profile map listings, reviews, and real client stories for proof. *(V1, V2, V8)*
4. [ ] **Portuguese city landing pages for the Tier 1 and 2 cities**, on casaemportugues.com. None exist today.
   - Answer what Brazilian buyers actually ask: buying with an ITIN, loans for the self-employed, building US credit, MassHousing and down-payment help, closing costs.
   - Describe only products our partners actually offer.
   - Use the keyword in the URL, title and headline, and link every city page within 2–3 clicks of the homepage.
   - Size the page set from what competitors have; Portuguese-language competition is likely thin. *(V8, V9)*
5. [ ] **Keep the Portuguese experience Portuguese-branded.** The shared form's header and consent name "NH Mortgage Journal"; for an MA Brazilian visitor, use Casa em Português throughout.
6. [ ] **Offer WhatsApp as the "text us" channel for Portuguese speakers,** answered within minutes. It's the channel the community already uses, and V7 rates "text us" over a chat widget. *(V7)*
7. [ ] **Meet the community where it already gathers:** local Brazilian Facebook groups, Instagram, WhatsApp communities and Portuguese-language media. Help publicly and link a guide; no spam or cold DMs. Use real-signal research (V3) to find what people are asking this month. Reddit is mainly for the English market. *(V3, V4)*
8. [ ] **Add conversion tracking that reports only qualified leads.** There's none today. Fire the event only for ready-now leads (timeline under 3 months, real contact info). Meta mortgage ads have limited targeting, so the Portuguese ad creative plus a clean conversion signal do the targeting. Also A/B test asking for contact info first. *(V6)*
9. [ ] **Real proof plus a 60-second real-person video in Portuguese** covering who we are, who will call and how fast, that we connect you with a Portuguese-speaking partner, and that this is not a credit application. Match the proof to the source city or program. Never invent testimonials. *(V7)*
10. [ ] **English market (southern NH + MA).**
    - Turn the 5 city guides under `/blog/` (Manchester, Nashua, Concord, Portsmouth, Hanover) into landing pages built to convert.
    - Add southern NH and MA cities sized by competitors.
    - Add per-town property tax.
    - Run a Reddit help loop for English-speaking buyers. *(V4, V8, V9)*
11. [~] **Report qualified leads and partner closes by channel, language and city.** Attribution is captured; add the qualified and closed view. Test one channel at a time, then double down on the winner. *(V2)*

## Decisions needed

- [ ] How partners pay us (per lead / per introduction / per closing). Decide after the RESPA and licensing check in item 1.
- [ ] Who makes the first call or WhatsApp message, in which languages, and how fast.
- [ ] Are Connecticut (Danbury) and Florida in scope? The live form already lists Florida as a property state.
- [ ] Use email for B2B partner outreach?

## Guardrails

Count qualified leads and partner closes, not form fills. Never fake proof: no invented testimonials, reviews or logos (skip any "as seen in" bar until there's real press). Only describe loan products partners actually offer. Mortgage content gets extra scrutiny from Google and regulators, so accuracy beats volume.

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

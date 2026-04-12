# 02b — Sample Ad Copy Bank
## LLM Search Ad Copy Evaluator

*LLM Eval Toolkit · Supporting doc for PRD*
*Author: Saurabh Das | Last updated: April 2026*

---

## What The Experience Feels Like

A first-time user lands on the app and sees three ways to evaluate — side-by-side sample comparison, manual input, or bulk upload. They don't need to have an ad ready.

In the sample flow, they pick a product, pick a keyword, and two ad copy variants auto-load — one in each panel. They hit Compare. Within seconds they see both ads scored across five dimensions with a winner declared and a plain-English reason for every score. The weight profile applied shifts automatically based on what the keyword implies — a purchase-intent keyword scores CTA Strength harder; a consideration keyword weights Differentiation higher.

For the user who has their own copy: they paste it into the manual flow and get the same structured output in under 10 seconds. For teams evaluating a batch of LLM variants: they upload a .txt file with up to 10 ads and get a comparison table — all scored on the same rubric, same keyword, same weight profile.

The tool doesn't tell you how to write the ad. It tells you which one wins, why, and what to fix — before you spend a rupee finding out the hard way.

---

## Sample Bank Structure

Used exclusively in **Flow 1 — Side-by-Side Sample Comparison.**

Each Product + Keyword combination has 3 ad copy variants:
- **Variant A** — Strong overall. Expected verdict: ✅ READY TO SERVE
- **Variant B** — Mixed quality. Expected verdict: ⚠️ NEEDS REVISION
- **Variant C** — Weak overall. Expected verdict: ❌ REJECT

Variant B is intentionally the most interesting — it is not obviously bad. It requires the rubric to catch what gut feel would miss. This is what makes the SBS comparison compelling.

**Character limits enforced:**
- Headline ≤ 30 characters
- Description ≤ 90 characters

---

## Nike Running Shoes

**Product Description:**
> Nike Running Shoes — engineered for performance. Available in React foam and Air Zoom cushioning variants for training, racing, and everyday running. Free delivery on orders over ₹3,000. 30-day returns.

---

### Keyword 1: "buy nike running shoes online"
*Inferred intent: **Purchase** — user has decided to buy, choosing where*
*Weight profile: CTA Strength ↑, Intent Alignment ↑*

**Variant A — READY TO SERVE**
```
Headline:    Nike Running Shoes – Shop Now         [29 chars]
Description: Free delivery over ₹3,000. React foam cushioning
             for speed. New arrivals in stock. Order today.   [83 chars]
```
*Why it works: Matches purchase intent precisely. Delivery benefit leads. CTA is direct and funnel-appropriate. No wasted characters.*

**Variant B — NEEDS REVISION**
```
Headline:    Nike Shoes – Great for Running        [30 chars]
Description: Nike offers a wide range of running shoes with
             comfort and style for all types of runners.      [89 chars]
```
*Primary failure: "Great for Running" is generic — any competitor can say this. Description covers the category, not the product. CTA entirely absent. Gut feel says "fine." Rubric catches the differentiation gap.*

**Variant C — REJECT**
```
Headline:    Explore Nike Footwear Online          [28 chars]
Description: Nike has been making shoes for years. Learn about
             our products and find out more online.           [87 chars]
```
*Primary failure: "Explore" and "Learn more" are awareness-stage signals on a purchase-intent query. Zero urgency, zero differentiation. Completely misreads where this searcher is.*

---

### Keyword 2: "best running shoes for marathon training"
*Inferred intent: **Consideration** — researching and comparing options*
*Weight profile: Differentiation ↑, Relevance ↑*

**Variant A — READY TO SERVE**
```
Headline:    Marathon-Ready Nike – Compare         [29 chars]
Description: React vs Air Zoom: Nike's top marathon trainers
             compared. Find your match before race day.       [86 chars]
```
*Why it works: Speaks to the comparison mindset directly. Names two specific models. "Find your match" CTA is exactly right for consideration stage.*

**Variant B — NEEDS REVISION**
```
Headline:    Nike Marathon Shoes – Buy Now         [29 chars]
Description: Top-rated Nike running shoes for marathon
             training. Advanced cushioning for long runs.     [85 chars]
```
*Primary failure: "Buy Now" CTA on a consideration query. User is still researching — this feels premature. Description is accurate but the intent mismatch on CTA is what the rubric catches.*

**Variant C — REJECT**
```
Headline:    Nike Running Shoes Available          [28 chars]
Description: Shop Nike running shoes online. We have many
             options for runners. Visit our website today.    [89 chars]
```
*Primary failure: "Available" is the weakest possible headline word. "Many options" and "Visit our website" are pure filler. No specific benefit, no reason to click this over the next result.*

---

## Trello

**Product Description:**
> Trello is a visual project management tool that uses boards, lists, and cards to help teams organise work. Available on Free, Standard, and Premium plans. 2M+ teams worldwide. 100+ integrations including Slack, Google Drive, and Jira.

---

### Keyword 3: "project management tool for teams"
*Inferred intent: **Consideration** — evaluating options, not ready to buy*
*Weight profile: Differentiation ↑, Relevance ↑*

**Variant A — READY TO SERVE**
```
Headline:    Trello for Teams – See How            [26 chars]
Description: Visual boards, shared timelines, 100+ integrations.
             See why 2M+ teams choose Trello. Free to start.  [88 chars]
```
*Why it works: Social proof (2M+ teams) addresses comparison anxiety. "Free to start" removes commitment friction. "See How" CTA matches consideration stage precisely.*

**Variant B — NEEDS REVISION**
```
Headline:    Trello – Manage Team Projects         [29 chars]
Description: Trello helps teams manage projects using boards,
             lists, and cards to organise work better.        [89 chars]
```
*Primary failure: Describes what Trello is, not why it wins. No differentiator versus Asana or Monday.com. No CTA. Gut feel says "clear and accurate." Rubric catches zero differentiation.*

**Variant C — REJECT**
```
Headline:    Project Management Software           [27 chars]
Description: Looking for a way to manage projects? Trello is
             a tool that can help your team.                  [79 chars]
```
*Primary failure: Headline doesn't mention Trello — could be any product. The description restates the question the user already answered by searching. Zero differentiation, zero CTA.*

---

### Keyword 4: "buy trello premium plan"
*Inferred intent: **Purchase** — user has chosen Trello, deciding on plan*
*Weight profile: CTA Strength ↑, Intent Alignment ↑*

**Variant A — READY TO SERVE**
```
Headline:    Trello Premium – Start Today          [28 chars]
Description: Unlimited boards, priority support, advanced
             checklists. ₹840/user/month. Upgrade now.        [83 chars]
```
*Why it works: Three concrete benefits. Pricing removes uncertainty for a purchase-intent query. "Upgrade now" CTA is direct and appropriate.*

**Variant B — NEEDS REVISION**
```
Headline:    Upgrade to Trello Premium             [25 chars]
Description: Trello Premium unlocks more features and better
             tools for your team's project management.        [88 chars]
```
*Primary failure: "More features" and "better tools" are placeholders, not benefits. No price, no specifics, no reason to upgrade today. A purchase-intent user deserves concrete information.*

**Variant C — REJECT**
```
Headline:    What Is Trello Premium?               [23 chars]
Description: Trello Premium is our paid plan offering
             additional features for teams wanting more.      [83 chars]
```
*Primary failure: A question headline on a purchase query. This user already knows what Trello Premium is. Completely misreads intent. Worst possible CTA for this moment.*

---

## MakeMyTrip

**Product Description:**
> MakeMyTrip is India's leading travel booking platform for flights, hotels, and holiday packages. Lowest fare guarantee, instant booking confirmation, and 24/7 customer support. 500+ routes across India. Price calendar and fare alert features available.

---

### Keyword 5: "cheap flights to Goa this weekend"
*Inferred intent: **Purchase/Urgent** — time-sensitive, price-sensitive, ready to book*
*Weight profile: CTA Strength ↑, Intent Alignment ↑*

**Variant A — READY TO SERVE**
```
Headline:    Goa Flights ₹1,899 – Book Now        [30 chars]
Description: Last-minute seats filling fast. Lowest fare
             guarantee + instant confirmation. Book now.      [86 chars]
```
*Why it works: Price in headline answers the first question immediately. Urgency ("filling fast") is justified. "Instant confirmation" addresses weekend timing anxiety. Nothing wasted.*

**Variant B — NEEDS REVISION**
```
Headline:    Fly to Goa This Weekend               [23 chars]
Description: Find great deals on weekend flights to Goa on
             MakeMyTrip. Compare options and book easily.     [89 chars]
```
*Primary failure: No price despite a price-sensitive query. "Compare options" is consideration language on a high-urgency purchase query — this user isn't comparing, they're booking.*

**Variant C — REJECT**
```
Headline:    MakeMyTrip Flight Booking             [25 chars]
Description: MakeMyTrip offers flight booking services across
             India. Explore our options and learn more.       [90 chars]
```
*Primary failure: Brand awareness copy served to someone who needs a flight this weekend. No price, no urgency, no Goa mention. "Learn more" CTA completely ignores the searcher's time pressure.*

---

### Keyword 6: "compare flight prices india"
*Inferred intent: **Consideration** — researching options, not ready to book*
*Weight profile: Differentiation ↑, Relevance ↑*

**Variant A — READY TO SERVE**
```
Headline:    Compare India Flights – Free          [28 chars]
Description: Price calendar, fare alerts, 500+ routes.
             Compare and lock the best fare on MakeMyTrip.    [87 chars]
```
*Why it works: "Free" removes friction for a comparison task. Price calendar and fare alerts are specific features a comparison searcher actually wants. "Compare" CTA is soft and appropriate.*

**Variant B — NEEDS REVISION**
```
Headline:    Best Flight Prices – Book Now         [29 chars]
Description: MakeMyTrip shows lowest flight prices across all
             major airlines in India. Book today.             [84 chars]
```
*Primary failure: "Book Now" CTA on a comparison query. User is still deciding. Description is accurate and useful — it's purely the intent mismatch on CTA that the rubric catches.*

**Variant C — REJECT**
```
Headline:    Flights Available on MMT              [24 chars]
Description: Compare flight prices on MakeMyTrip. We have
             many airlines and routes to choose from.         [84 chars]
```
*Primary failure: "Flights Available" — of course they are. "Many airlines and routes" is filler. No differentiator, no reason to choose MakeMyTrip over Ixigo or Cleartrip.*

---

## Adding More Samples

This bank is designed to grow. Each new entry follows this format:

```
### Keyword N: "[search keyword]"
*Inferred intent: **[Purchase / Consideration / Awareness]** — [one-line searcher mindset]*
*Weight profile: [which dimensions are weighted up]*

**Variant A — READY TO SERVE**
Headline:    [copy]    [X chars]
Description: [copy]    [X chars]
Why it works: [one-line explanation referencing a rubric dimension]

**Variant B — NEEDS REVISION**
Headline:    [copy]    [X chars]
Description: [copy]    [X chars]
Primary failure: [name the specific rubric dimension that catches this]

**Variant C — REJECT**
Headline:    [copy]    [X chars]
Description: [copy]    [X chars]
Primary failure: [name the specific rubric dimension that catches this]
```

**Rules for new samples:**
- Headline ≤ 30 characters (spaces included)
- Description ≤ 90 characters
- Each combination must have exactly one A, one B, one C
- Variant B must not be obviously bad — it must require the rubric to catch it
- Primary failure must name a rubric dimension, not just say "bad copy"
- Inferred intent must match the keyword signals in the PRD weight table

---

*Referenced by: [02a_prd.md](./02a_prd.md) · [03_ux_flow_wireframe.md](./03_ux_flow_wireframe.md)*

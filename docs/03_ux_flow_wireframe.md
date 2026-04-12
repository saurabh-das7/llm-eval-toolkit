# 03 — UX Flow & Wireframe
## LLM Search Ad Copy Evaluator

*LLM Eval Toolkit · Stage 3 of 8*
*Author: Saurabh Das | Last updated: April 2026*

---

## Overview

The evaluator is a single-page Streamlit application with three tabs — **Compare**, **Evaluate**, and **Batch**. Every flow is designed to be zero-friction: a first-time user can experience the full output of any tab without typing a single character.

The interface is deliberately minimal. There are no dashboards, no navigation menus, no account screens. The entire product is one page, three tabs, and a verdict.

---

## Interface Structure

```
┌─────────────────────────────────────────────────────┐
│  Search Ad Copy Evaluator                           │
│  Evaluate LLM-generated search ads before you       │
│  spend a rupee finding out the hard way             │
├──────────────┬──────────────┬───────────────────────┤
│   Compare    │   Evaluate   │   Batch               │
├──────────────┴──────────────┴───────────────────────┤
│                                                     │
│  [ Tab content renders here ]                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

Active tab is visually highlighted with a dark background fill and bottom border. Inactive tabs are muted. Tab labels are short action verbs — Compare, Evaluate, Batch — with the full flow description rendered as a heading inside each tab.

---

## Tab 1 — Compare (Side-by-Side Comparison)

**Heading inside tab:** "Side-by-side comparison"
**Subheading:** "Compare two ad copies for the same product and keyword. Use samples or enter your own."

### Input source toggle

A toggle at the top of the tab controls whether the user uses pre-built samples or enters their own product and keyword.

```
Input source:  [ Use samples ]  [ Enter manually ]
```

**Use samples (default):**
- Product dropdown: Nike Running Shoes / Trello / MakeMyTrip
- Keyword dropdown: filtered dynamically to the selected product
- Inferred intent label displayed alongside (e.g. "Purchase intent detected")

**Enter manually:**
- Product dropdown and keyword dropdown are replaced with free text inputs
- Product description: textarea (1–5 sentences)
- Target search keyword: text input
- Both panel toggles hide — both panels automatically switch to manual entry mode
- Switching back to "Use samples" resets both panels to sample mode

### Panel layout

Two panels sit side by side — Panel A on the left, Panel B on the right. Each panel is independent.

```
┌──────────────────────┐  ┌──────────────────────┐
│ Panel A              │  │ Panel B              │
│ [Use sample][Manual] │  │ [Use sample][Manual] │
│                      │  │                      │
│ [Variant dropdown]   │  │ [Variant dropdown]   │
│  or                  │  │  or                  │
│ [Headline input]     │  │ [Headline input]     │
│ [Description input]  │  │ [Description input]  │
│                      │  │                      │
│ ┌──────────────────┐ │  │ ┌──────────────────┐ │
│ │ Sponsored        │ │  │ │ Sponsored        │ │
│ │ site.com         │ │  │ │ site.com         │ │
│ │ Headline text    │ │  │ │ Headline text    │ │
│ │ Description...   │ │  │ │ Description...   │ │
│ └──────────────────┘ │  │ └──────────────────┘ │
└──────────────────────┘  └──────────────────────┘
```

**Panel toggle (when source is "Use samples"):**
Each panel has its own "Use sample / Enter manually" toggle. This allows mixing — e.g. a known-good sample in Panel A benchmarked against the user's own copy in Panel B.

**Ad preview card:**
Always visible in each panel. Updates live as the user selects a variant or types into manual fields. Shows the ad exactly as it would appear on a search results page:
- "Sponsored" label
- Display URL
- Headline (in blue, search result style)
- Description

**When source is "Enter manually":**
Panel toggles are hidden. Both panels show headline and description inputs with live character counters (≤30 chars headline, ≤90 chars description). Ad preview updates on every keystroke.

### Output (after clicking Compare)

Intent badge displayed above results:
```
[ Purchase intent · CTA Strength + Intent Alignment weighted higher ]
```

Two scorecards side by side, one per panel:

```
┌─────────────────────────────┐  ┌─────────────────────────────┐
│ Panel A          ✅ Ready   │  │ Panel B        ⚠️ Revision  │
│                             │  │                             │
│ Relevance      ████░  4/5  │  │ Relevance      ████░  4/5  │
│ Intent align   █████  5/5  │  │ Intent align   ██░░░  2/5  │
│ Differentiation████░  4/5  │  │ Differentiation██░░░  2/5  │
│ CTA strength   █████  5/5  │  │ CTA strength   █░░░░  1/5  │
│ Char efficiency████░  4/5  │  │ Char efficiency███░░  3/5  │
│                             │  │                             │
│ Overall score        4.4   │  │ Overall score        2.6   │
└─────────────────────────────┘  └─────────────────────────────┘

Panel A wins — stronger CTA and intent alignment. Panel B fails on
differentiation: no specific reason to click over a competitor.
```

Each dimension score includes a one-line reasoning note below the bar.

---

## Tab 2 — Evaluate (Single Ad Evaluation)

**Heading inside tab:** "Single ad evaluation"
**Subheading:** "Paste your own copy or load a sample. Get a dimensional scorecard in seconds."

### Zero-friction entry point

```
[ Load random sample ]   or fill in your own below
```

Clicking "Load random sample" randomly selects one of the 18 sample ad copies (across all three products) and pre-fills all four fields instantly. The inferred intent label and ad preview appear immediately. User can modify any field before hitting Evaluate.

### Input fields

```
Product description
[ Textarea — 1–5 sentences about the product ]

Target search keyword          Inferred intent
[ Text input ]                 Purchase intent detected

Ad headline                    Ad description
[ Text input — 0/30 ]         [ Text input — 0/90 ]
```

Live character counters on headline and description. Counter turns red when the limit is reached.

### Ad preview

Appears as soon as either the headline or description field has content. Updates live on every keystroke.

```
┌──────────────────────────────────────────┐
│ Sponsored                                │
│ yoursite.com                             │
│ Headline text goes here                  │
│ Description text appears here as typed   │
└──────────────────────────────────────────┘
```

### Output (after clicking Evaluate)

Intent badge, then a single scorecard with all five dimensions, overall score, and verdict. Each dimension includes a one-line reasoning note.

A plain-English evaluator note below the scorecard names the single most important issue (or confirms strength if the ad scores well).

---

## Tab 3 — Batch (Batch Evaluation)

**Heading inside tab:** "Batch evaluation"
**Subheading:** "Evaluate up to 10 ad copy variants for the same product and keyword in one go."

### Zero-friction entry point

```
Load sample scenario: [ — choose a scenario — ▾ ]
  · Nike · buy nike running shoes online (3 variants)
  · Trello · project management tool for teams (3 variants)
  · MakeMyTrip · cheap flights to Goa this weekend (3 variants)
```

Selecting a scenario pre-fills the product description, keyword, and all ad copy rows in one action. User can then modify rows or add more before evaluating.

### Input fields

Product description and keyword at the top (same as Evaluate tab). Below that, a dynamic form with one row per ad copy:

```
1  [ Headline input — 0/30 ]  [ Description input — 0/90 ]
2  [ Headline input — 0/30 ]  [ Description input — 0/90 ]  ×
3  [ Headline input — 0/30 ]  [ Description input — 0/90 ]  ×

[ + Add another ad ]   3 of 10
```

Row 1 cannot be removed (minimum one ad required). Additional rows have a remove button. "+ Add another ad" is disabled once 10 rows are present.

### Secondary upload option

Below the form rows, a clearly separated secondary option:

```
──── or upload a file ────

Upload a .txt file — one ad per line:  Headline | Description
[ Choose file ]   Download sample .txt
```

The sample .txt download gives users a pre-formatted file they can open, edit, and re-upload.

### Output (after clicking Evaluate all)

Intent badge shown once for the batch. Results rendered as a table:

```
#  Headline                       Rel  Intent  Diff  CTA  Char  Score  Verdict
1  Nike Running Shoes – Shop Now   4     5      4     5    4     4.4    ✅ Ready
2  Nike Shoes – Great for Running  4     2      2     1    3     2.3    ⚠️ Revise
3  Explore Nike Footwear Online    3     1      1     1    3     1.7    ❌ Reject
──────────────────────────────────────────────────────────────────────────────
   Summary                                               2.8    Ad 1 best · Intent alignment top failure
```

Summary row at the bottom highlights the best-performing ad and the most common failure dimension across the batch.

---

## Design Principles Applied

**Zero friction by default.** Every tab has a one-click path to a populated, evaluable state. No user should have to type anything to experience the full output.

**Ad preview everywhere.** The sponsored ad card appears in all three tabs. Seeing the copy rendered as it would look on a search results page makes the evaluation feel real rather than abstract.

**Linked dropdowns.** In the Compare tab, changing the product automatically filters the keyword options, which automatically updates the variant options and ad previews. No stale state.

**Consistent empty manual fields.** Manual entry fields are always empty when first shown — across all three tabs. There is no pre-filling in manual mode. This is a deliberate consistency decision: the "load sample" and "load scenario" buttons serve the pre-fill need explicitly.

**One decision drives Compare source.** The top-level "Use samples / Enter manually" toggle in the Compare tab is a single decision that cascades to both panels. When entering manually, both panels switch together and the panel-level toggles are hidden, reducing decision points.

**Verdicts are unambiguous.** Every flow ends in one of four states: ✅ Ready to serve, ⚠️ Needs revision, ❌ Reject, or 🟡 Not evaluable. No hedging, no interpretation required.

---

## Open UX Questions

| Question | Resolution needed by |
|----------|---------------------|
| Should overall score be shown numerically or as a visual bar only? | Build stage |
| Should the weight profile breakdown be shown as percentages or a named label (e.g. "Purchase mode")? | Build stage |
| Should the batch results table be downloadable as CSV in v1? | Tech planning |
| Should Compare tab remember the last selected product/keyword within a session? | Build stage |

---

*Previous: [02a — PRD](./02a_prd.md)*
*Supporting: [02b — Sample Ad Copy Bank](./02b_sample_ad_copy_bank.md)*
*Next: [04 — Tech Stack Decisions](./04_tech_stack_decisions.md)*

# 08 — Launch & Retrospective
## LLM Search Ad Copy Evaluator

*LLM Eval Toolkit · Stage 8 of 8*
*Author: Saurabh Das | Last updated: April 2026*

---

## How to Use This Document

This document has two parts written at different times:

**Part A — Launch Checklist** is written now, before the build begins. Every item must be verified as true before the public URL is shared with anyone. It is the quality gate between "built" and "launched."

**Part B — Retrospective** is written after the app has been live for at least one week. It captures what worked, what didn't, and what the next bets are. It should be written honestly — not as a highlight reel.

---

## Part A — Launch Checklist

### A1 — Functional Verification

All three tabs must work end-to-end on the live Streamlit Community Cloud URL, not just locally.

**Compare tab — sample mode:**
- [ ] Product dropdown loads with three options (Nike / Trello / MakeMyTrip)
- [ ] Selecting a product filters the keyword dropdown correctly
- [ ] Selecting a keyword updates variant dropdowns and ad preview cards
- [ ] Panel A and Panel B dropdowns are independent
- [ ] Panel-level "Use sample / Enter manually" toggle works on both panels
- [ ] Ad preview updates live on variant selection
- [ ] Clicking Compare returns two scorecards with all five dimensions scored
- [ ] Head-to-head winner summary appears below scorecards
- [ ] Results are hidden when inputs change after evaluation

**Compare tab — manual mode:**
- [ ] "Enter manually" source toggle switches product/keyword to text inputs
- [ ] Both panel toggles hide in manual source mode
- [ ] Both panels switch to headline/description inputs
- [ ] Ad preview updates live as user types
- [ ] Clicking Compare returns two scorecards for manually entered copy

**Evaluate tab:**
- [ ] "Load random sample" button pre-fills all four fields
- [ ] Inferred intent label appears alongside keyword field
- [ ] Ad preview appears as soon as headline or description has content
- [ ] Character counters update on every keystroke
- [ ] Character counter turns red at limit
- [ ] Clicking Evaluate returns a full scorecard with verdict and evaluator note
- [ ] Loading indicator shown during API call

**Batch tab:**
- [ ] "Load sample scenario" dropdown pre-fills product, keyword, and all rows
- [ ] Dynamic form rows add up to 10, remove correctly
- [ ] Row 1 cannot be removed
- [ ] .txt upload section is visible with format instructions
- [ ] Sample .txt download link works
- [ ] Clicking Evaluate All returns a results table
- [ ] Summary row appears at bottom of table

---

### A2 — Sample Bank Validation

All 18 sample ad copies must return their expected verdict. This is the ground truth test for evaluation quality.

**Nike — "buy nike running shoes online" (Purchase intent):**
- [ ] Variant A returns ✅ READY TO SERVE
- [ ] Variant B returns ⚠️ NEEDS REVISION
- [ ] Variant C returns ❌ REJECT

**Nike — "best running shoes for marathon training" (Consideration intent):**
- [ ] Variant A returns ✅ READY TO SERVE
- [ ] Variant B returns ⚠️ NEEDS REVISION
- [ ] Variant C returns ❌ REJECT

**Trello — "project management tool for teams" (Consideration intent):**
- [ ] Variant A returns ✅ READY TO SERVE
- [ ] Variant B returns ⚠️ NEEDS REVISION
- [ ] Variant C returns ❌ REJECT

**Trello — "buy trello premium plan" (Purchase intent):**
- [ ] Variant A returns ✅ READY TO SERVE
- [ ] Variant B returns ⚠️ NEEDS REVISION
- [ ] Variant C returns ❌ REJECT

**MakeMyTrip — "cheap flights to Goa this weekend" (Purchase/Urgent intent):**
- [ ] Variant A returns ✅ READY TO SERVE
- [ ] Variant B returns ⚠️ NEEDS REVISION
- [ ] Variant C returns ❌ REJECT

**MakeMyTrip — "compare flight prices india" (Consideration intent):**
- [ ] Variant A returns ✅ READY TO SERVE
- [ ] Variant B returns ⚠️ NEEDS REVISION
- [ ] Variant C returns ❌ REJECT

**Pass rate required:** 18/18. Any failure requires prompt revision before launch.

---

### A3 — Consistency Validation

The same ad copy must produce the same verdict across multiple runs. Test three samples — one per product — three times each.

| Sample | Run 1 | Run 2 | Run 3 | Consistent? |
|--------|-------|-------|-------|-------------|
| Nike Variant B (NEEDS REVISION) | | | | |
| Trello Variant A (READY TO SERVE) | | | | |
| MakeMyTrip Variant C (REJECT) | | | | |

**Pass requirement:** Same verdict on all three runs for all three samples. Score variance per dimension ≤1 point across runs.

---

### A4 — Edge Case Validation

| Edge case | Expected behaviour | Verified |
|-----------|-------------------|---------|
| Empty product description | 🟡 NOT EVALUABLE with explanation | [ ] |
| Headline over 30 characters | Hard fail on Character Efficiency | [ ] |
| Description over 90 characters | Hard fail on Character Efficiency | [ ] |
| Keyword too vague (one word: "shoes") | Warn: defaulting to Consideration weights | [ ] |
| Placeholder text in headline ("Insert USP here") | 🟡 NOT EVALUABLE | [ ] |
| Same variant selected in both Compare panels | Prevented or warned | [ ] |
| Batch .txt file with >10 lines | First 10 processed, user warned | [ ] |

---

### A5 — Security and Configuration

- [ ] GitHub repo contains no API keys (search for "AIza" string before launch)
- [ ] `.env` file is in `.gitignore` and not committed
- [ ] `.streamlit/secrets.toml` is in `.gitignore` and not committed
- [ ] Gemini API key is set correctly in Streamlit Community Cloud secrets manager
- [ ] App loads correctly from a private browser window (no cached state)

---

### A6 — Documentation and Repo

- [ ] All 8 docs in `docs/` folder are committed and render correctly on GitHub
- [ ] `docs/images/` folder contains all 8 wireframe screenshots
- [ ] `README.md` updated with live demo URL
- [ ] `requirements.txt` is complete and matches what the app actually uses
- [ ] `07_build_log.md` updated with M6 entry including live URL
- [ ] Build timeline table in `07_build_log.md` shows all milestones as complete

---

### A7 — Final Smoke Test

Run this exact sequence on the live URL before sharing with anyone:

1. Open the app URL in a private browser window
2. On the Compare tab: select MakeMyTrip → "cheap flights to Goa this weekend" → Variant A vs Variant C → click Compare
3. Verify two scorecards appear with correct verdicts (Ready vs Reject) and a winner summary
4. Switch to Evaluate tab → click "Load random sample" → click Evaluate
5. Verify a full scorecard appears with a non-trivial verdict
6. Switch to Batch tab → select "MakeMyTrip · cheap flights to Goa" scenario → click Evaluate All
7. Verify a results table appears with three rows and a summary row

**All seven steps must pass before the URL is shared.**

---

## Part B — Retrospective

*To be completed after the app has been live for at least one week.*

---

### B1 — What Worked Well

*[Write after launch — what went as planned or better than expected? Which design decisions turned out to be correct? What would you repeat on the next project?]*

---

### B2 — What Was Harder Than Expected

*[Write after launch — what took longer than the roadmap estimated? Where did the plan diverge from reality? What assumptions turned out to be wrong?]*

---

### B3 — What Would Be Done Differently

*[Write after launch — if you were starting this project again with everything you now know, what would you change? Be specific — not "I'd plan better" but "I would have built the evaluation engine before designing the UX, because the API response structure changed the output design.]*

---

### B4 — Evaluation Quality Assessment

*[Write after launch — run the sample bank validation again after one week of live usage. Has the model's verdict consistency held? Are there any patterns in unexpected verdicts? What would you change in the rubric or prompt?]*

| Sample | Expected verdict | Actual verdict (1 week post-launch) | Match? |
|--------|-----------------|-------------------------------------|--------|
| Nike Variant A | READY TO SERVE | | |
| Nike Variant B | NEEDS REVISION | | |
| Nike Variant C | REJECT | | |
| Trello Variant A | READY TO SERVE | | |
| Trello Variant B | NEEDS REVISION | | |
| Trello Variant C | REJECT | | |
| MakeMyTrip Variant A | READY TO SERVE | | |
| MakeMyTrip Variant B | NEEDS REVISION | | |
| MakeMyTrip Variant C | REJECT | | |

---

### B5 — Next Bets (Post-MVP Backlog, Prioritised)

*[Write after launch — from the post-MVP backlog in the roadmap, which two or three items would you build next based on what you observed during and after the build? Prioritise based on what you learned, not what was on the original list.]*

| Priority | Feature | Why this, why now |
|----------|---------|------------------|
| 1 | | |
| 2 | | |
| 3 | | |

---

### B6 — What This Project Taught Me

*[Write after launch — one paragraph. Not a summary of what was built, but what you understand now that you didn't when you started. About AI product development, about evaluation frameworks, about solo builds, about your own working style.]*

---

*Previous: [07 — Build Log](./07_build_log.md)*
*This is the final document in the LLM Eval Toolkit series.*

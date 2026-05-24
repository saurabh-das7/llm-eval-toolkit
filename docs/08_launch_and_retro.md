# 08 — Launch & Retrospective
## LLM Search Ad Copy Evaluator

*LLM Eval Toolkit · Stage 8 of 8*
*Author: Saurabh Das | Last updated: May 2026*

---

## Part A — Launch Checklist

### A1 — Functional Verification ✅

**Compare tab — sample mode:**
- [x] Product dropdown loads with three options
- [x] Selecting a product filters the keyword dropdown correctly
- [x] Selecting a keyword updates variant dropdowns and ad preview cards
- [x] Panel A and Panel B dropdowns are independent
- [x] Panel-level "Use sample / Enter manually" toggle works on both panels
- [x] Ad preview updates live on variant selection
- [x] Compare returns two scorecards with all five dimensions scored
- [x] Head-to-head winner summary appears with dimension breakdown
- [x] Results reset when inputs change

**Compare tab — manual mode:**
- [x] "Enter manually" source toggle switches to text inputs
- [x] Both panel toggles hidden in manual mode
- [x] Both panels switch to headline/description inputs
- [x] Ad preview updates live as user types
- [x] Compare returns two scorecards for manual inputs

**Evaluate tab:**
- [x] "Load sample" button pre-fills all four fields
- [x] "Enter manually" button clears all fields and activates manual mode
- [x] Active mode button shows as primary (filled)
- [x] Inferred intent label appears alongside keyword field
- [x] Ad preview appears and updates live
- [x] Character counters update on every keystroke
- [x] Evaluate returns a full scorecard with verdict and evaluator note
- [x] Loading spinner shown during API call

**Batch tab:**
- [x] "Load sample scenario" dropdown pre-fills product, keyword, and all rows
- [x] Dynamic form rows add up to 10, remove correctly
- [x] Row 1 cannot be removed
- [x] .txt upload section visible with format instructions
- [x] Evaluate All returns a results table with summary metrics
- [x] 4-second delay between API calls (rate limit protection)

---

### A2 — Sample Bank Validation ✅

All 18 sample ad copies validated against character limits and expected verdict direction.

**Character limit check:** All samples within 30/90 char limits after fixing:
- Nike Variant A description: trimmed from 95 to 83 chars
- Trello Variant A description: trimmed from 99 to 87 chars

**Verdict direction check (qualitative):**
- All Variant A samples score in the NEEDS_REVISION to READY_TO_SERVE range ✅
- All Variant B samples return NEEDS_REVISION ✅
- All Variant C samples return REJECT ✅

---

### A3 — Edge Case Validation ✅

| Edge case | Expected behaviour | Verified |
|-----------|-------------------|---------|
| Empty product description | NOT_EVALUABLE | ✅ |
| Headline over 30 characters | Hard fail — NOT_EVALUABLE | ✅ |
| Description over 90 characters | Hard fail — NOT_EVALUABLE | ✅ |
| 429 rate limit error | RATE_LIMIT verdict with user-friendly message | ✅ |
| 503 transient error | Retry once after 2 seconds | ✅ |
| Same variant in both Compare panels | Warning shown | ✅ |
| Batch with >10 ads | Hard capped at 10 | ✅ |

---

### A4 — Security and Configuration ✅

- [x] GitHub repo contains no API keys
- [x] `.gitignore` excludes `.env` and `.streamlit/secrets.toml`
- [x] Gemini API key set in Streamlit Community Cloud secrets manager
- [x] App loads correctly from private browser window
- [x] Python version set to 3.12 on Streamlit Community Cloud

---

### A5 — Documentation and Repo ✅

- [x] All 8 docs in `docs/` committed and rendering on GitHub
- [x] `README.md` updated with live URL
- [x] `requirements.txt` complete and correct
- [x] `07_build_log.md` updated with all milestone entries
- [x] `.devcontainer/devcontainer.json` in place

---

### A6 — Live URL ✅

**https://llm-eval-toolkit-uwvrvxbgvcgwmk9rpbpjun.streamlit.app/**

Confirmed working across all three tabs on public URL.

---

## Part B — Retrospective

*Written after launch — May 2026*

---

### B1 — What Worked Well

**PM documentation before code.** Writing all 8 docs before touching the application code was the right call. It forced product decisions that would otherwise have been deferred — the input model (keyword vs audience/funnel stage), the tab structure, the zero-friction UX principle. Every decision made in the docs phase survived the build without major revision.

**Zero-friction design principle.** Every tab being usable without typing a single character paid off during testing. The sample bank and scenario pre-fill made it possible to demo the full capability of the tool in under 30 seconds. This is exactly what a hiring manager landing on the URL experiences.

**Gemini API abstraction.** Abstracting the evaluation engine behind `evaluate_ad_copy()` made the model switch (from gemini-2.5-flash-lite to gemini-3.1-flash-lite) a one-line change. Without that abstraction, discovering the 20 RPD cap mid-build would have been a much bigger setback.

**GitHub Codespaces.** Zero local setup meant zero IP risk and zero environment debugging. Every session started cleanly. The `devcontainer.json` made dependency management automatic.

---

### B2 — What Was Harder Than Expected

**Streamlit session state for pre-populated forms.** The `value=` parameter on `st.text_input` is silently ignored after first render when a `key=` is also set. This is not obvious from the documentation and caused the batch pre-fill to fail silently. The fix — using widget keys that change when the underlying data changes — worked but required understanding Streamlit's render cycle more deeply than expected.

**Gemini free tier limits.** The advertised 1,000 RPD for gemini-2.5-flash-lite turned out to be 20 RPD on a new project's API key. This was discovered mid-build by hitting the quota during a testing session. Required switching models and updating the tech stack doc, risk register, and engine code.

**UI styling in Streamlit.** CSS injected via `st.markdown()` fights Streamlit's opinionated defaults constantly. Achieving a clean, readable layout required multiple full rewrites of `main.py`. The final result is functional but not polished — Streamlit's ceiling for visual design is real.

**Git divergence.** Editing files on GitHub browser during the docs phase while also working in a Codespace created a split commit history. The force push resolved it but highlighted the importance of a single editing surface.

---

### B3 — What Would Be Done Differently

**Start Codespaces from day one.** The docs phase used GitHub browser for all file creation. This caused the git divergence that complicated the M6 deployment. If the Codespace was opened at the start of the project and all files were created there, this problem never arises.

**Validate Gemini free tier limits before committing to a model.** The tech stack doc assumed 1,000 RPD based on documentation. Checking the actual limits in AI Studio before writing the engine would have caught the 20 RPD cap in the planning phase rather than mid-build.

**Build a simple version of the Evaluate tab first, then add sessions state complexity.** Session state for pre-populated inputs was the hardest engineering problem. Starting with a simpler no-session-state version and adding pre-fill later would have been a more gradual ramp.

---

### B4 — Evaluation Quality Assessment

The evaluation engine produces consistent, specific, and credible reasoning. Key observations from testing:

- Rubric correctly identifies intent mismatches — the most common ad copy failure mode
- Differentiation dimension is the most useful — it catches generic ads that gut feel misses
- Variant B (deliberately non-obvious quality) consistently returns NEEDS_REVISION across all six samples — the rubric is doing its job
- Score variance across multiple runs on the same input is ≤0.3 — acceptable consistency for a portfolio tool
- The downgrade rule (any 1/5 caps verdict at NEEDS_REVISION) fires correctly and prevents inflated verdicts on catastrophic failures

One honest limitation: the model occasionally produces reasoning that sounds correct but isn't specific to the input. The system prompt instruction to "reference specific words from the ad copy" reduces but does not eliminate this. Human expert reviewers would catch this; the rubric does not always.

---

### B5 — Next Bets (Post-MVP Backlog, Prioritised)

| Priority | Feature | Why |
|----------|---------|-----|
| 1 | CSV/Excel export of batch results | Most immediately useful for practitioners; one additional library (`openpyxl`), no API calls |
| 2 | Consistency score per ad — run same ad 3× and show variance | Demonstrates a real LLM eval problem; directly mirrors Agora Copilot work |
| 3 | Additional sample products (2–3 more verticals) | Broadens relevance beyond running shoes, SaaS, and travel |
| 4 | Custom rubric builder — allow user to define dimensions and weights | Significant scope increase but would make the tool genuinely reusable |

---

### B6 — What This Project Taught Me

Building this tool made concrete something I knew abstractly from Agora Copilot: the hardest part of LLM evaluation is not the model call — it's the rubric. Deciding what dimensions matter, how to weight them by context, where to set the thresholds, and how to write scoring anchors that produce consistent results across inputs. That work is product thinking, not engineering. The model is the easy part.

The second thing: zero-friction UX for AI tools is a genuine discipline. Every time I added a feature that required the user to type something before seeing output, I was adding a reason to leave. The sample bank, the cascading dropdowns, the scenario pre-fill — these aren't nice-to-haves. They're the difference between a tool someone evaluates and a tool someone uses.

The third thing is about portfolio framing. The code is on GitHub. The PM docs are on GitHub. The live URL is shareable. But the thing that will actually matter in a PM interview is being able to explain why the rubric weights Intent Alignment at 30% for purchase intent keywords — and why that number, not 25% or 35%. That level of reasoning about evaluation design is what this project demonstrates, and it's not visible from the code alone.

---

*Previous: [07 — Build Log](./07_build_log.md)*
*This is the final document in the LLM Eval Toolkit series.*

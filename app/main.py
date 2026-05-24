import random
import time
import streamlit as st
from engine import evaluate_ad_copy, infer_intent
from samples import ALL_SAMPLES, SAMPLES

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Search Ad Copy Evaluator",
    page_icon="🎯",
    layout="wide",
)

# ── Global CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
.section {
    background:#fafafa; border-left:3px solid #d0d0d0;
    border-radius:0 6px 6px 0; padding:14px 18px; margin-bottom:14px;
}
.section-results {
    background:#f8fffe; border-left:3px solid #b7dfca;
    border-radius:0 6px 6px 0; padding:14px 18px; margin-bottom:14px;
}
.section-summary {
    background:#fff8f0; border-left:3px solid #f0c080;
    border-radius:0 6px 6px 0; padding:14px 18px; margin-bottom:14px;
}
.section-label {
    font-size:11px; color:#888; font-weight:600;
    text-transform:uppercase; letter-spacing:.6px; margin-bottom:8px;
}
.score-green { background:#e6f4ea; color:#1e7e34; font-weight:600;
               padding:2px 8px; border-radius:6px; font-size:13px; }
.score-amber { background:#fff8e1; color:#b45309; font-weight:600;
               padding:2px 8px; border-radius:6px; font-size:13px; }
.score-red   { background:#fdecea; color:#c0392b; font-weight:600;
               padding:2px 8px; border-radius:6px; font-size:13px; }
.dim-row { padding:8px 0; border-bottom:1px solid #eeeeee; }
.dim-row:last-child { border-bottom:none; }
.dim-label { font-size:13px; color:#333; font-weight:500; }
.dim-reasoning { font-size:12px; color:#666; margin-top:3px; }
.intent-pill {
    display:inline-block; background:#e8f0fe; color:#1a73e8;
    padding:3px 10px; border-radius:12px; font-size:12px; margin-bottom:8px;
}
.winner-card {
    background:#f0faf4; border-left:3px solid #52b788;
    border-radius:0 6px 6px 0; padding:12px 16px; margin-top:8px;
}
.ad-preview-box {
    background:#ffffff; border:1px solid #e0e0e0; border-radius:8px;
    padding:12px 16px; margin-top:8px; margin-bottom:4px;
}
.header-meta {
    font-size:13px; color:#666; margin-top:4px; margin-bottom:20px;
    border-bottom:1px solid #f0f0f0; padding-bottom:14px;
}
.header-meta a { color:#1a73e8; text-decoration:none; margin-right:16px; }
.header-meta a:hover { text-decoration:underline; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("## Search Ad Copy Evaluator")
st.markdown(
    "Evaluate LLM-generated search ads against a structured, "
    "intent-aware rubric — before you spend a rupee finding out the hard way."
)
st.markdown("""
<div class="header-meta">
    Built by <strong>Saurabh Das</strong> &mdash; demonstrating LLM evaluation
    frameworks, rubric design, and AI product thinking in practice.
    &nbsp;&nbsp;
    <a href="https://linkedin.com/in/saurabhdas7" target="_blank">LinkedIn</a>
    <a href="https://github.com/saurabh-das7" target="_blank">GitHub</a>
    <a href="https://github.com/saurabh-das7/llm-eval-toolkit" target="_blank">
    Project repo</a>
</div>
""", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────
tab_compare, tab_evaluate, tab_batch = st.tabs(["Compare", "Evaluate", "Batch"])

# ── Shared helpers ─────────────────────────────────────────────────────────
VERDICT_MAP = {
    "READY_TO_SERVE": ("✅ READY TO SERVE", "success"),
    "NEEDS_REVISION":  ("⚠️ NEEDS REVISION",  "warning"),
    "REJECT":          ("❌ REJECT",           "error"),
    "NOT_EVALUABLE":   ("🟡 NOT EVALUABLE",   "warning"),
    "RATE_LIMIT":      ("🚫 RATE LIMIT REACHED", "error"),
}
DIM_LABELS = {
    "relevance":            "Relevance",
    "intent_alignment":     "Intent Alignment",
    "differentiation":      "Differentiation",
    "cta_strength":         "CTA Strength",
    "character_efficiency": "Character Efficiency",
}

def score_badge(score):
    if score >= 4:
        return f"<span class='score-green'>{score}/5</span>"
    elif score == 3:
        return f"<span class='score-amber'>{score}/5</span>"
    else:
        return f"<span class='score-red'>{score}/5</span>"

def overall_badge(score):
    if score >= 4:
        return f"<span class='score-green'>{score}/5</span>"
    elif score >= 2.5:
        return f"<span class='score-amber'>{score}/5</span>"
    else:
        return f"<span class='score-red'>{score}/5</span>"

def ad_preview_html(headline, description, url="yoursite.com"):
    return f"""<div class="ad-preview-box">
        <span style='font-size:11px;border:1px solid #888;border-radius:3px;
                     padding:1px 5px;color:#666;'>Sponsored</span><br>
        <span style='font-size:12px;color:#555;'>{url}</span><br>
        <span style='font-size:17px;color:#1a0dab;font-weight:400;
                     line-height:1.4;'>{headline}</span><br>
        <span style='font-size:13px;color:#444;'>{description}</span>
    </div>"""

def render_verdict(verdict):
    label, vtype = VERDICT_MAP.get(verdict, (verdict, "info"))
    if vtype == "success":   st.success(f"**{label}**")
    elif vtype == "error":   st.error(f"**{label}**")
    else:                    st.warning(f"**{label}**")

def render_scorecard(result, panel_label=None):
    """Two-section layout: dimensions → summary."""
    if panel_label:
        st.markdown(f"**{panel_label}**")

    verdict = result.get("verdict", "NOT_EVALUABLE")
    dims    = result.get("dimensions", {})
    overall = result.get("overall_score")
    note    = result.get("evaluator_note", "")
    intent  = result.get("intent")

    # Section 1 — Dimension scores
    if dims:
        st.markdown("<div class='section-results'>", unsafe_allow_html=True)
        st.markdown("<p class='section-label'>Dimension scores</p>",
                    unsafe_allow_html=True)
        for dim_key, dim_label in DIM_LABELS.items():
            dim = dims.get(dim_key)
            if dim:
                badge = score_badge(dim["score"])
                st.markdown(
                    f"<div class='dim-row'>"
                    f"<span class='dim-label'>{dim_label}</span>"
                    f"&nbsp;&nbsp;{badge}<br>"
                    f"<span class='dim-reasoning'>{dim['reasoning']}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)

    # Section 2 — Summary
    st.markdown("<div class='section-summary'>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Evaluation summary</p>",
                unsafe_allow_html=True)

    if intent:
        st.markdown(
            f"<span class='intent-pill'>🔍 {intent} intent</span>",
            unsafe_allow_html=True,
        )

    render_verdict(verdict)

    if overall is not None:
        st.markdown(
            f"<p style='font-size:15px;font-weight:600;margin:6px 0;'>"
            f"Overall score: {overall_badge(overall)}</p>",
            unsafe_allow_html=True,
        )

    if note:
        if verdict == "RATE_LIMIT":
            st.error(f"🚫 {note}")
        else:
            st.markdown(
                f"<p style='font-size:13px;color:#555;font-style:italic;"
                f"margin-top:6px;'>💡 {note}</p>",
                unsafe_allow_html=True,
            )

    if result.get("char_warnings"):
        for w in result["char_warnings"]:
            st.warning(f"⚠️ {w}")

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# TAB 1 — COMPARE
# ══════════════════════════════════════════════════════════════════════════
with tab_compare:
    st.subheader("Side-by-side comparison")
    st.write("Compare two ad copies for the same product and keyword. "
             "Use samples or enter your own.")

    source_mode = st.radio(
        "Input source", ["Use samples", "Enter manually"],
        horizontal=True, key="cmp_source",
    )

    if source_mode == "Use samples":
        col_prod, col_kw, col_intent = st.columns([2, 3, 1])
        with col_prod:
            product_choice = st.selectbox(
                "Product", list(SAMPLES.keys()), key="cmp_product")
        with col_kw:
            keyword_choice = st.selectbox(
                "Keyword", list(SAMPLES[product_choice].keys()),
                key="cmp_keyword")
        with col_intent:
            kw_data = SAMPLES[product_choice][keyword_choice]
            st.markdown("**Intent**")
            st.markdown(f"`{kw_data['intent']}`")

        variant_labels = [v["label"] for v in kw_data["variants"]]
        product_desc   = kw_data["product_desc"]
        url            = kw_data["url"]

        col_pa, col_pb = st.columns(2)

        with col_pa:
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("**Panel A**")
            pa_mode = st.radio(
                "", ["Use sample", "Enter manually"],
                horizontal=True, key="pa_mode",
                label_visibility="collapsed")
            if pa_mode == "Use sample":
                pa_label = st.selectbox("", variant_labels, index=0,
                    key="pa_variant", label_visibility="collapsed")
                pa_v = next(v for v in kw_data["variants"]
                            if v["label"] == pa_label)
                pa_hl, pa_desc = pa_v["headline"], pa_v["description"]
            else:
                pa_hl = st.text_input("Headline", placeholder="Max 30 chars",
                    max_chars=30, key="pa_hl_manual")
                st.markdown(
                    f"<p style='font-size:11px;color:gray'>{len(pa_hl)}/30</p>",
                    unsafe_allow_html=True)
                pa_desc = st.text_input("Description",
                    placeholder="Max 90 chars",
                    max_chars=90, key="pa_desc_manual")
                st.markdown(
                    f"<p style='font-size:11px;color:gray'>{len(pa_desc)}/90</p>",
                    unsafe_allow_html=True)
            if pa_hl or pa_desc:
                st.markdown(ad_preview_html(pa_hl, pa_desc, url),
                            unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_pb:
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("**Panel B**")
            pb_mode = st.radio(
                "", ["Use sample", "Enter manually"],
                horizontal=True, key="pb_mode",
                label_visibility="collapsed")
            if pb_mode == "Use sample":
                pb_label = st.selectbox("", variant_labels, index=1,
                    key="pb_variant", label_visibility="collapsed")
                pb_v = next(v for v in kw_data["variants"]
                            if v["label"] == pb_label)
                pb_hl, pb_desc = pb_v["headline"], pb_v["description"]
            else:
                pb_hl = st.text_input("Headline", placeholder="Max 30 chars",
                    max_chars=30, key="pb_hl_manual")
                st.markdown(
                    f"<p style='font-size:11px;color:gray'>{len(pb_hl)}/30</p>",
                    unsafe_allow_html=True)
                pb_desc = st.text_input("Description",
                    placeholder="Max 90 chars",
                    max_chars=90, key="pb_desc_manual")
                st.markdown(
                    f"<p style='font-size:11px;color:gray'>{len(pb_desc)}/90</p>",
                    unsafe_allow_html=True)
            if pb_hl or pb_desc:
                st.markdown(ad_preview_html(pb_hl, pb_desc, url),
                            unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        col_mprod, col_mkw = st.columns(2)
        with col_mprod:
            product_desc = st.text_area(
                "Product description",
                placeholder="Describe your product in 1–5 sentences.",
                height=100, key="cmp_prod_manual")
        with col_mkw:
            keyword_choice = st.text_input(
                "Target search keyword",
                placeholder="e.g. buy nike running shoes online",
                key="cmp_kw_manual")
            if keyword_choice:
                st.markdown(
                    f"`{infer_intent(keyword_choice)} intent detected`")

        url = "yoursite.com"
        st.markdown("---")
        col_pa, col_pb = st.columns(2)

        with col_pa:
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("**Panel A**")
            pa_hl = st.text_input("Headline A",
                placeholder="Max 30 chars", max_chars=30, key="pa_hl_m")
            st.markdown(
                f"<p style='font-size:11px;color:gray'>{len(pa_hl)}/30</p>",
                unsafe_allow_html=True)
            pa_desc = st.text_input("Description A",
                placeholder="Max 90 chars", max_chars=90, key="pa_desc_m")
            st.markdown(
                f"<p style='font-size:11px;color:gray'>{len(pa_desc)}/90</p>",
                unsafe_allow_html=True)
            if pa_hl or pa_desc:
                st.markdown(ad_preview_html(pa_hl, pa_desc),
                            unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_pb:
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("**Panel B**")
            pb_hl = st.text_input("Headline B",
                placeholder="Max 30 chars", max_chars=30, key="pb_hl_m")
            st.markdown(
                f"<p style='font-size:11px;color:gray'>{len(pb_hl)}/30</p>",
                unsafe_allow_html=True)
            pb_desc = st.text_input("Description B",
                placeholder="Max 90 chars", max_chars=90, key="pb_desc_m")
            st.markdown(
                f"<p style='font-size:11px;color:gray'>{len(pb_desc)}/90</p>",
                unsafe_allow_html=True)
            if pb_hl or pb_desc:
                st.markdown(ad_preview_html(pb_hl, pb_desc),
                            unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        product_desc = st.session_state.get("cmp_prod_manual", "")

    st.markdown("")
    if st.button("Compare", type="primary", key="cmp_submit"):
        prod = product_desc
        kw   = keyword_choice
        if not pa_hl or not pb_hl:
            st.warning("Both panels need a headline before comparing.")
        elif pa_hl == pb_hl and pa_desc == pb_desc:
            st.warning("Panels are identical — select different variants.")
        else:
            with st.spinner("Evaluating both ads..."):
                result_a = evaluate_ad_copy(prod, kw, pa_hl, pa_desc)
                result_b = evaluate_ad_copy(prod, kw, pb_hl, pb_desc)
            st.session_state["cmp_result_a"] = result_a
            st.session_state["cmp_result_b"] = result_b

    result_a = st.session_state.get("cmp_result_a")
    result_b = st.session_state.get("cmp_result_b")

    if result_a and result_b:
        st.divider()
        col_ra, col_rb = st.columns(2)
        with col_ra:
            render_scorecard(result_a, "Panel A")
        with col_rb:
            render_scorecard(result_b, "Panel B")

        # Head-to-head summary
        st.divider()
        score_a = result_a.get("overall_score") or 0
        score_b = result_b.get("overall_score") or 0
        a_wins, b_wins = [], []
        if result_a.get("dimensions") and result_b.get("dimensions"):
            for dim, label in DIM_LABELS.items():
                sa = result_a["dimensions"].get(dim, {}).get("score", 0)
                sb = result_b["dimensions"].get(dim, {}).get("score", 0)
                if sa > sb: a_wins.append(label)
                elif sb > sa: b_wins.append(label)

        if score_a > score_b:
            winner      = "Panel A"
            winner_score = score_a
            loser_score  = score_b
            winner_note  = result_a.get("evaluator_note", "")
        elif score_b > score_a:
            winner      = "Panel B"
            winner_score = score_b
            loser_score  = score_a
            winner_note  = result_b.get("evaluator_note", "")
        else:
            winner      = "Tie"
            winner_note = "Both ads score equally overall."

        st.markdown("<div class='winner-card'>", unsafe_allow_html=True)
        st.markdown("<p class='section-label'>Head-to-head summary</p>",
                    unsafe_allow_html=True)
        if winner == "Tie":
            st.markdown(f"🤝 **Tie** — {winner_note}")
        else:
            loser = "Panel B" if winner == "Panel A" else "Panel A"
            st.markdown(
                f"🏆 **Overall winner: {winner}** "
                f"({winner_score}/5 vs {loser_score}/5)"
            )
            if a_wins:
                st.markdown(
                    f"<p style='font-size:13px;margin:4px 0;'>"
                    f"Panel A stronger on: {', '.join(a_wins)}</p>",
                    unsafe_allow_html=True)
            if b_wins:
                st.markdown(
                    f"<p style='font-size:13px;margin:4px 0;'>"
                    f"Panel B stronger on: {', '.join(b_wins)}</p>",
                    unsafe_allow_html=True)
            st.markdown(
                f"<p style='font-size:13px;font-style:italic;color:#555;"
                f"margin-top:6px;'>💡 {winner_note}</p>",
                unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# TAB 2 — EVALUATE
# ══════════════════════════════════════════════════════════════════════════
with tab_evaluate:
    st.subheader("Single ad evaluation")
    st.write("Load a sample or enter your own copy. "
             "Get a dimensional scorecard in seconds.")

    # Mode buttons
    if "ev_mode" not in st.session_state:
        st.session_state["ev_mode"] = "sample"

    col_b1, col_b2, _ = st.columns([1.2, 1.4, 4])
    with col_b1:
        load_type = "primary" if st.session_state["ev_mode"] == "sample" \
                    else "secondary"
        if st.button("🎲 Load sample", key="load_sample", type=load_type):
            sample = random.choice(ALL_SAMPLES)
            st.session_state.update({
                "ev_product":     sample["product_desc"],
                "ev_keyword":     sample["keyword"],
                "ev_headline":    sample["headline"],
                "ev_description": sample["description"],
                "ev_result":      None,
                "ev_mode":        "sample",
            })
            st.rerun()
    with col_b2:
        man_type = "primary" if st.session_state["ev_mode"] == "manual" \
                   else "secondary"
        if st.button("✏️ Enter manually", key="manual_mode", type=man_type):
            st.session_state.update({
                "ev_product":     "",
                "ev_keyword":     "",
                "ev_headline":    "",
                "ev_description": "",
                "ev_result":      None,
                "ev_mode":        "manual",
            })
            st.rerun()

    st.markdown("")

    # Inputs
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    product = st.text_area(
        "Product description",
        value=st.session_state.get("ev_product", ""),
        placeholder="Describe your product in 1–5 sentences.",
        height=90, key="ev_product",
    )
    col_kw, col_intent = st.columns([2, 1])
    with col_kw:
        keyword = st.text_input(
            "Target search keyword",
            value=st.session_state.get("ev_keyword", ""),
            placeholder="e.g. buy nike running shoes online",
            key="ev_keyword",
        )
    with col_intent:
        if keyword:
            st.markdown("**Inferred intent**")
            st.markdown(f"`{infer_intent(keyword)}`")

    col_hl, col_desc = st.columns(2)
    with col_hl:
        headline = st.text_input(
            "Ad headline",
            value=st.session_state.get("ev_headline", ""),
            placeholder="Max 30 characters",
            max_chars=30, key="ev_headline",
        )
        hl_len = len(headline)
        st.markdown(
            f"<p style='font-size:11px;"
            f"color:{'red' if hl_len > 30 else 'gray'}'>"
            f"{hl_len}/30</p>",
            unsafe_allow_html=True)
    with col_desc:
        description = st.text_input(
            "Ad description",
            value=st.session_state.get("ev_description", ""),
            placeholder="Max 90 characters",
            max_chars=90, key="ev_description",
        )
        desc_len = len(description)
        st.markdown(
            f"<p style='font-size:11px;"
            f"color:{'red' if desc_len > 90 else 'gray'}'>"
            f"{desc_len}/90</p>",
            unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Ad preview
    if headline or description:
        st.markdown(ad_preview_html(headline, description),
                    unsafe_allow_html=True)
        st.markdown("")

    # Evaluate button
    if st.button("Evaluate", type="primary", key="ev_submit"):
        if not product or not keyword or not headline or not description:
            st.warning("Please fill in all four fields before evaluating.")
        else:
            with st.spinner("Evaluating..."):
                result = evaluate_ad_copy(
                    product, keyword, headline, description)
            st.session_state["ev_result"] = result

    # Results
    result = st.session_state.get("ev_result")
    if result:
        st.divider()
        render_scorecard(result)


# ══════════════════════════════════════════════════════════════════════════
# TAB 3 — BATCH
# ══════════════════════════════════════════════════════════════════════════
with tab_batch:
    st.subheader("Batch evaluation")
    st.write("Evaluate up to 10 ad copy variants for the same product "
             "and keyword in one go.")

    # Init session state
    defaults = {
        "batch_rows":          [{"headline":"","description":""},
                                 {"headline":"","description":""}],
        "batch_last_scenario": None,
        "batch_result":        None,
        "batch_product":       "",
        "batch_keyword":       "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Scenario dropdown
    scenario_options = {"— fill in manually below —": None}
    for product, keywords in SAMPLES.items():
        for keyword in keywords:
            scenario_options[f"{product} · {keyword}"] = (product, keyword)

    scenario_choice = st.selectbox(
        "Load sample scenario",
        list(scenario_options.keys()),
        key="batch_scenario",
    )

    if scenario_choice != "— fill in manually below —":
        if st.session_state["batch_last_scenario"] != scenario_choice:
            pname, kname = scenario_options[scenario_choice]
            kd = SAMPLES[pname][kname]
            st.session_state.update({
                "batch_product":       kd["product_desc"],
                "batch_keyword":       kname,
                "batch_rows":          [
                    {"headline": v["headline"],
                     "description": v["description"]}
                    for v in kd["variants"]
                ],
                "batch_last_scenario": scenario_choice,
                "batch_result":        None,
            })
    else:
        if st.session_state["batch_last_scenario"] is not None:
            st.session_state.update({
                "batch_product":       "",
                "batch_keyword":       "",
                "batch_last_scenario": None,
            })

    # Product + keyword inputs
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    col_bprod, col_bkw = st.columns([3, 2])
    with col_bprod:
        st.text_area(
            "Product description",
            placeholder="Describe your product in 1–5 sentences.",
            height=80, key="batch_product")
    with col_bkw:
        st.text_input(
            "Target search keyword",
            placeholder="e.g. buy nike running shoes online",
            key="batch_keyword")
        if st.session_state["batch_keyword"]:
            st.markdown(
                f"`{infer_intent(st.session_state['batch_keyword'])} "
                f"intent detected`")
    st.markdown("</div>", unsafe_allow_html=True)

    # Ad copy rows
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("**Ad copies**")
    rows = st.session_state["batch_rows"]
    for i, row in enumerate(rows):
        c_num, c_hl, c_desc, c_del = st.columns([0.3, 2, 3, 0.3])
        with c_num:
            st.markdown(
                f"<p style='text-align:center;color:gray;"
                f"margin-top:32px;font-size:13px'>{i+1}</p>",
                unsafe_allow_html=True)
        with c_hl:
            new_hl = st.text_input(
                f"HL{i}", value=row["headline"],
                placeholder="Headline (max 30)",
                max_chars=30,
                key=f"batch_hl_{i}_{row['headline'][:5]}",
                label_visibility="collapsed")
            st.markdown(
                f"<p style='font-size:11px;color:gray;"
                f"margin:-8px 0 4px 0'>{len(new_hl)}/30</p>",
                unsafe_allow_html=True)
            st.session_state["batch_rows"][i]["headline"] = new_hl
        with c_desc:
            new_desc = st.text_input(
                f"DC{i}", value=row["description"],
                placeholder="Description (max 90)",
                max_chars=90,
                key=f"batch_desc_{i}_{row['description'][:5]}",
                label_visibility="collapsed")
            st.markdown(
                f"<p style='font-size:11px;color:gray;"
                f"margin:-8px 0 4px 0'>{len(new_desc)}/90</p>",
                unsafe_allow_html=True)
            st.session_state["batch_rows"][i]["description"] = new_desc
        with c_del:
            if i > 0:
                if st.button("×", key=f"del_{i}"):
                    st.session_state["batch_rows"].pop(i)
                    st.session_state["batch_result"] = None
                    st.rerun()

    col_add, col_count = st.columns([2, 4])
    with col_add:
        if len(rows) < 10:
            if st.button("+ Add another ad", key="add_row"):
                st.session_state["batch_rows"].append(
                    {"headline": "", "description": ""})
                st.rerun()
    with col_count:
        st.markdown(
            f"<p style='color:gray;font-size:13px;margin-top:8px'>"
            f"{len(rows)} of 10 max</p>",
            unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # txt upload
    with st.expander(
            "Or upload a .txt file  (Headline | Description, one per line)"):
        uploaded_file = st.file_uploader(
            "", type=["txt"], key="batch_upload",
            label_visibility="collapsed")
        st.caption(
            "Format: `Headline | Description` — one ad per line, max 10.")
        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
            lines = [l.strip() for l in content.splitlines()
                     if l.strip()][:10]
            parsed, errors = [], []
            for j, line in enumerate(lines):
                if "|" not in line:
                    errors.append(f"Line {j+1}: missing | separator")
                    continue
                parts = line.split("|", 1)
                parsed.append({
                    "headline":    parts[0].strip(),
                    "description": parts[1].strip(),
                })
            for e in errors:
                st.warning(e)
            if parsed and st.button("Load from file", key="load_file"):
                st.session_state["batch_rows"]   = parsed
                st.session_state["batch_result"] = None
                st.rerun()

    # Evaluate all
    st.markdown("")
    if st.button("Evaluate all", type="primary", key="batch_submit"):
        bp = st.session_state["batch_product"]
        bk = st.session_state["batch_keyword"]
        if not bp or not bk:
            st.warning("Please enter a product description and keyword.")
        else:
            valid_rows = [
                r for r in st.session_state["batch_rows"]
                if r["headline"] and r["description"]
            ][:10]
            if not valid_rows:
                st.warning("Please add at least one ad copy row.")
            else:
                results  = []
                progress = st.progress(0)
                status   = st.empty()
                for idx, row in enumerate(valid_rows):
                    status.text(
                        f"Evaluating ad {idx+1} of {len(valid_rows)}...")
                    res = evaluate_ad_copy(
                        bp, bk, row["headline"], row["description"])
                    results.append({"row": row, "result": res})
                    progress.progress((idx+1) / len(valid_rows))
                    if idx < len(valid_rows) - 1:
                        time.sleep(4)
                status.empty()
                progress.empty()
                st.session_state["batch_result"] = results

    # Results
    batch_results = st.session_state.get("batch_result")
    if batch_results:
        st.divider()
        VERDICT_ICONS = {
            "READY_TO_SERVE": "✅", "NEEDS_REVISION": "⚠️",
            "REJECT": "❌", "NOT_EVALUABLE": "🟡", "RATE_LIMIT": "🚫",
        }
        table_rows, scores_list = [], []
        for idx, item in enumerate(batch_results):
            row     = item["row"]
            res     = item["result"]
            dims    = res.get("dimensions", {})
            score   = res.get("overall_score")
            verdict = res.get("verdict", "NOT_EVALUABLE")
            table_rows.append({
                "#":        idx + 1,
                "Headline": row["headline"],
                "Rel":    dims.get("relevance", {}).get("score", "-"),
                "Intent": dims.get("intent_alignment", {}).get("score", "-"),
                "Diff":   dims.get("differentiation", {}).get("score", "-"),
                "CTA":    dims.get("cta_strength", {}).get("score", "-"),
                "Char":   dims.get("character_efficiency", {}).get("score", "-"),
                "Score":  score if score is not None else "-",
                "Verdict": (f"{VERDICT_ICONS.get(verdict,'')} "
                            f"{verdict.replace('_',' ')}"),
            })
            if score is not None:
                scores_list.append((score, idx))

        import pandas as pd
        st.dataframe(pd.DataFrame(table_rows),
                     use_container_width=True, hide_index=True)

        if scores_list:
            best_score, best_idx   = max(scores_list, key=lambda x: x[0])
            worst_score, worst_idx = min(scores_list, key=lambda x: x[0])
            avg = round(
                sum(s for s, _ in scores_list) / len(scores_list), 1)

            dim_totals = {d: 0 for d in DIM_LABELS}
            for item in batch_results:
                dims = item["result"].get("dimensions", {})
                for d in DIM_LABELS:
                    dim_totals[d] += dims.get(d, {}).get("score", 5)
            weakest  = min(dim_totals, key=dim_totals.get)
            strongest = max(dim_totals, key=dim_totals.get)

            bk = st.session_state["batch_keyword"]
            if bk:
                st.markdown(
                    f"<span class='intent-pill'>"
                    f"🔍 {infer_intent(bk)} intent · weights applied"
                    f"</span>",
                    unsafe_allow_html=True)
                st.markdown("")

            st.markdown(
                "<div class='section-summary'>", unsafe_allow_html=True)
            st.markdown(
                "<p class='section-label'>Batch summary</p>",
                unsafe_allow_html=True)

            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric("Average score", f"{avg} / 5")
            with col_s2:
                st.metric("Best ad",
                          f"Ad {best_idx+1}  ({best_score}/5)")
            with col_s3:
                st.metric("Weakest ad",
                          f"Ad {worst_idx+1}  ({worst_score}/5)")

            st.markdown(
                f"<p style='font-size:13px;margin-top:8px;'>"
                f"⚠️ <strong>Top failure dimension:</strong> "
                f"{DIM_LABELS[weakest]} &nbsp;|&nbsp; "
                f"✅ <strong>Strongest dimension:</strong> "
                f"{DIM_LABELS[strongest]}</p>",
                unsafe_allow_html=True)

            best_note = batch_results[best_idx]["result"].get(
                "evaluator_note", "")
            if best_note:
                st.markdown(
                    f"<p style='font-size:13px;font-style:italic;"
                    f"color:#555;margin-top:4px;'>"
                    f"💡 Best ad insight: {best_note}</p>",
                    unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
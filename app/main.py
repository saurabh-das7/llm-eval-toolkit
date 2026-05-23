import random
import streamlit as st
from engine import evaluate_ad_copy
from samples import ALL_SAMPLES

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Search Ad Copy Evaluator",
    page_icon="🎯",
    layout="wide",
)

# ── Header ─────────────────────────────────────────────────────────────────
st.title("Search Ad Copy Evaluator")
st.caption(
    "Evaluate LLM-generated search ads before you spend a rupee "
    "finding out the hard way"
)

# ── Tabs ───────────────────────────────────────────────────────────────────
tab_evaluate, tab_compare, tab_batch = st.tabs(
    ["Evaluate", "Compare", "Batch"]
)

# ══════════════════════════════════════════════════════════════════════════
# TAB 1 — EVALUATE
# ══════════════════════════════════════════════════════════════════════════
with tab_evaluate:
    st.subheader("Single ad evaluation")
    st.write(
        "Paste your own copy or load a sample. "
        "Get a dimensional scorecard in seconds."
    )

    # ── Load random sample ─────────────────────────────────────────────
    if st.button("🎲 Load random sample", key="load_sample"):
        sample = random.choice(ALL_SAMPLES)
        st.session_state["ev_product"] = sample["product_desc"]
        st.session_state["ev_keyword"] = sample["keyword"]
        st.session_state["ev_headline"] = sample["headline"]
        st.session_state["ev_description"] = sample["description"]
        st.session_state["ev_result"] = None

    # ── Inputs ─────────────────────────────────────────────────────────
    product = st.text_area(
        "Product description",
        value=st.session_state.get("ev_product", ""),
        placeholder="Describe your product in 1–5 sentences. Include key features, pricing, and what makes it different.",
        height=100,
        key="ev_product",
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
            from engine import infer_intent
            intent_label = infer_intent(keyword)
            st.markdown(f"**Inferred intent**")
            st.markdown(f"`{intent_label}`")

    col_hl, col_desc = st.columns(2)
    with col_hl:
        headline = st.text_input(
            "Ad headline",
            value=st.session_state.get("ev_headline", ""),
            placeholder="Max 30 characters",
            max_chars=30,
            key="ev_headline",
        )
        hl_len = len(headline)
        hl_color = "red" if hl_len > 30 else "gray"
        st.markdown(
            f"<p style='color:{hl_color}; font-size:12px'>{hl_len} / 30</p>",
            unsafe_allow_html=True,
        )

    with col_desc:
        description = st.text_input(
            "Ad description",
            value=st.session_state.get("ev_description", ""),
            placeholder="Max 90 characters",
            max_chars=90,
            key="ev_description",
        )
        desc_len = len(description)
        desc_color = "red" if desc_len > 90 else "gray"
        st.markdown(
            f"<p style='color:{desc_color}; font-size:12px'>{desc_len} / 90</p>",
            unsafe_allow_html=True,
        )

    # ── Live ad preview ────────────────────────────────────────────────
    if headline or description:
        st.markdown("**Ad preview**")
        st.markdown(
            f"""
            <div style='border:1px solid #ddd; border-radius:8px;
                        padding:12px 16px; max-width:600px;
                        background:#fff; color:#000;'>
                <span style='font-size:11px; border:1px solid #888;
                             border-radius:3px; padding:1px 5px;
                             color:#555;'>Sponsored</span><br>
                <span style='font-size:12px; color:#555;'>yoursite.com</span><br>
                <span style='font-size:18px; color:#1a0dab;
                             font-weight:400;'>{headline}</span><br>
                <span style='font-size:13px; color:#444;'>{description}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("")

    # ── Evaluate button ────────────────────────────────────────────────
    if st.button("Evaluate", type="primary", key="ev_submit"):
        if not product or not keyword or not headline or not description:
            st.warning("Please fill in all four fields before evaluating.")
        else:
            with st.spinner("Evaluating..."):
                result = evaluate_ad_copy(product, keyword, headline, description)
            st.session_state["ev_result"] = result

    # ── Scorecard output ───────────────────────────────────────────────
    result = st.session_state.get("ev_result")
    if result:
        st.divider()

        # Intent badge
        if result.get("intent"):
            st.markdown(
                f"<span style='background:#e8f0fe; color:#1a73e8; "
                f"padding:4px 10px; border-radius:12px; font-size:13px;'>"
                f"🔍 {result['intent']} intent detected</span>",
                unsafe_allow_html=True,
            )
            st.markdown("")

        # Verdict
        verdict = result["verdict"]
        verdict_map = {
            "READY_TO_SERVE":  ("✅ READY TO SERVE",  "success"),
            "NEEDS_REVISION":  ("⚠️ NEEDS REVISION",  "warning"),
            "REJECT":          ("❌ REJECT",           "error"),
            "NOT_EVALUABLE":   ("🟡 NOT EVALUABLE",   "warning"),
        }
        verdict_label, verdict_type = verdict_map.get(
            verdict, (verdict, "info")
        )

        if verdict_type == "success":
            st.success(f"**{verdict_label}**")
        elif verdict_type == "error":
            st.error(f"**{verdict_label}**")
        else:
            st.warning(f"**{verdict_label}**")

        # Dimension scores
        if result.get("dimensions"):
            st.markdown("**Scorecard**")
            dim_labels = {
                "relevance": "Relevance",
                "intent_alignment": "Intent Alignment",
                "differentiation": "Differentiation",
                "cta_strength": "CTA Strength",
                "character_efficiency": "Character Efficiency",
            }
            for dim_key, dim_label in dim_labels.items():
                dim = result["dimensions"].get(dim_key)
                if dim:
                    score = dim["score"]
                    reasoning = dim["reasoning"]
                    col_name, col_bar, col_score = st.columns([2, 4, 1])
                    with col_name:
                        st.markdown(
                            f"<p style='font-size:13px; margin:4px 0;'>"
                            f"{dim_label}</p>",
                            unsafe_allow_html=True,
                        )
                    with col_bar:
                        st.progress(score / 5)
                    with col_score:
                        st.markdown(
                            f"<p style='font-size:13px; font-weight:600; "
                            f"margin:4px 0;'>{score}/5</p>",
                            unsafe_allow_html=True,
                        )
                    st.markdown(
                        f"<p style='font-size:12px; color:#666; "
                        f"margin:-8px 0 8px 0;'>{reasoning}</p>",
                        unsafe_allow_html=True,
                    )

        # Overall score
        if result.get("overall_score") is not None:
            st.markdown(
                f"**Overall score: {result['overall_score']} / 5**"
            )

        # Evaluator note
        if result.get("evaluator_note"):
            st.info(f"💡 {result['evaluator_note']}")

        # Char warnings
        if result.get("char_warnings"):
            for w in result["char_warnings"]:
                st.warning(f"⚠️ {w}")

# ══════════════════════════════════════════════════════════════════════════
# TAB 2 — COMPARE
# ══════════════════════════════════════════════════════════════════════════
with tab_compare:
    st.subheader("Side-by-side comparison")
    st.write(
        "Compare two ad copies for the same product and keyword. "
        "Use samples or enter your own."
    )

    # ── Source toggle ──────────────────────────────────────────────────
    source_mode = st.radio(
        "Input source",
        ["Use samples", "Enter manually"],
        horizontal=True,
        key="cmp_source",
    )

    from samples import SAMPLES

    if source_mode == "Use samples":
        # ── Linked dropdowns ───────────────────────────────────────────
        col_prod, col_kw, col_intent = st.columns([2, 3, 1])
        with col_prod:
            product_choice = st.selectbox(
                "Product",
                list(SAMPLES.keys()),
                key="cmp_product",
            )
        with col_kw:
            keyword_choice = st.selectbox(
                "Keyword",
                list(SAMPLES[product_choice].keys()),
                key="cmp_keyword",
            )
        with col_intent:
            kw_data = SAMPLES[product_choice][keyword_choice]
            st.markdown("**Inferred intent**")
            st.markdown(f"`{kw_data['intent']}`")

        variant_labels = [v["label"] for v in kw_data["variants"]]
        product_desc = kw_data["product_desc"]
        url = kw_data["url"]

        col_pa, col_pb = st.columns(2)

        # Panel A
        with col_pa:
            st.markdown("**Panel A**")
            pa_mode = st.radio(
                "Panel A source",
                ["Use sample", "Enter manually"],
                horizontal=True,
                key="pa_mode",
                label_visibility="collapsed",
            )
            if pa_mode == "Use sample":
                pa_variant_label = st.selectbox(
                    "Ad copy — Panel A",
                    variant_labels,
                    index=0,
                    key="pa_variant",
                )
                pa_variant = next(
                    v for v in kw_data["variants"]
                    if v["label"] == pa_variant_label
                )
                pa_hl = pa_variant["headline"]
                pa_desc = pa_variant["description"]
            else:
                pa_hl = st.text_input(
                    "Headline A", placeholder="Max 30 chars",
                    max_chars=30, key="pa_hl_manual"
                )
                st.markdown(
                    f"<p style='font-size:12px;color:gray'>"
                    f"{len(pa_hl)}/30</p>",
                    unsafe_allow_html=True,
                )
                pa_desc = st.text_input(
                    "Description A", placeholder="Max 90 chars",
                    max_chars=90, key="pa_desc_manual"
                )
                st.markdown(
                    f"<p style='font-size:12px;color:gray'>"
                    f"{len(pa_desc)}/90</p>",
                    unsafe_allow_html=True,
                )

            # Panel A preview
            if pa_hl or pa_desc:
                st.markdown(
                    f"""<div style='border:1px solid #ddd;border-radius:8px;
                        padding:10px 14px;background:#fff;color:#000;
                        margin-top:8px;'>
                        <span style='font-size:11px;border:1px solid #888;
                        border-radius:3px;padding:1px 5px;color:#555;'>
                        Sponsored</span><br>
                        <span style='font-size:12px;color:#555;'>{url}</span><br>
                        <span style='font-size:16px;color:#1a0dab;
                        font-weight:400;'>{pa_hl}</span><br>
                        <span style='font-size:13px;color:#444;'>
                        {pa_desc}</span></div>""",
                    unsafe_allow_html=True,
                )

        # Panel B
        with col_pb:
            st.markdown("**Panel B**")
            pb_mode = st.radio(
                "Panel B source",
                ["Use sample", "Enter manually"],
                horizontal=True,
                key="pb_mode",
                label_visibility="collapsed",
            )
            if pb_mode == "Use sample":
                pb_variant_label = st.selectbox(
                    "Ad copy — Panel B",
                    variant_labels,
                    index=1,
                    key="pb_variant",
                )
                pb_variant = next(
                    v for v in kw_data["variants"]
                    if v["label"] == pb_variant_label
                )
                pb_hl = pb_variant["headline"]
                pb_desc = pb_variant["description"]
            else:
                pb_hl = st.text_input(
                    "Headline B", placeholder="Max 30 chars",
                    max_chars=30, key="pb_hl_manual"
                )
                st.markdown(
                    f"<p style='font-size:12px;color:gray'>"
                    f"{len(pb_hl)}/30</p>",
                    unsafe_allow_html=True,
                )
                pb_desc = st.text_input(
                    "Description B", placeholder="Max 90 chars",
                    max_chars=90, key="pb_desc_manual"
                )
                st.markdown(
                    f"<p style='font-size:12px;color:gray'>"
                    f"{len(pb_desc)}/90</p>",
                    unsafe_allow_html=True,
                )

            # Panel B preview
            if pb_hl or pb_desc:
                st.markdown(
                    f"""<div style='border:1px solid #ddd;border-radius:8px;
                        padding:10px 14px;background:#fff;color:#000;
                        margin-top:8px;'>
                        <span style='font-size:11px;border:1px solid #888;
                        border-radius:3px;padding:1px 5px;color:#555;'>
                        Sponsored</span><br>
                        <span style='font-size:12px;color:#555;'>{url}</span><br>
                        <span style='font-size:16px;color:#1a0dab;
                        font-weight:400;'>{pb_hl}</span><br>
                        <span style='font-size:13px;color:#444;'>
                        {pb_desc}</span></div>""",
                    unsafe_allow_html=True,
                )

    else:
        # ── Manual source mode ─────────────────────────────────────────
        col_mprod, col_mkw = st.columns(2)
        with col_mprod:
            product_desc = st.text_area(
                "Product description",
                placeholder="Describe your product in 1–5 sentences.",
                height=100,
                key="cmp_prod_manual",
            )
        with col_mkw:
            keyword_choice = st.text_input(
                "Target search keyword",
                placeholder="e.g. buy nike running shoes online",
                key="cmp_kw_manual",
            )
            if keyword_choice:
                intent_label = infer_intent(keyword_choice)
                st.markdown(f"`{intent_label} intent detected`")

        url = "yoursite.com"
        st.markdown("---")

        col_pa, col_pb = st.columns(2)
        with col_pa:
            st.markdown("**Panel A**")
            pa_hl = st.text_input(
                "Headline A", placeholder="Max 30 chars",
                max_chars=30, key="pa_hl_m"
            )
            st.markdown(
                f"<p style='font-size:12px;color:gray'>"
                f"{len(pa_hl)}/30</p>",
                unsafe_allow_html=True,
            )
            pa_desc = st.text_input(
                "Description A", placeholder="Max 90 chars",
                max_chars=90, key="pa_desc_m"
            )
            st.markdown(
                f"<p style='font-size:12px;color:gray'>"
                f"{len(pa_desc)}/90</p>",
                unsafe_allow_html=True,
            )
            if pa_hl or pa_desc:
                st.markdown(
                    f"""<div style='border:1px solid #ddd;border-radius:8px;
                        padding:10px 14px;background:#fff;color:#000;
                        margin-top:8px;'>
                        <span style='font-size:11px;border:1px solid #888;
                        border-radius:3px;padding:1px 5px;color:#555;'>
                        Sponsored</span><br>
                        <span style='font-size:12px;color:#555;'>{url}</span><br>
                        <span style='font-size:16px;color:#1a0dab;
                        font-weight:400;'>{pa_hl}</span><br>
                        <span style='font-size:13px;color:#444;'>
                        {pa_desc}</span></div>""",
                    unsafe_allow_html=True,
                )

        with col_pb:
            st.markdown("**Panel B**")
            pb_hl = st.text_input(
                "Headline B", placeholder="Max 30 chars",
                max_chars=30, key="pb_hl_m"
            )
            st.markdown(
                f"<p style='font-size:12px;color:gray'>"
                f"{len(pb_hl)}/30</p>",
                unsafe_allow_html=True,
            )
            pb_desc = st.text_input(
                "Description B", placeholder="Max 90 chars",
                max_chars=90, key="pb_desc_m"
            )
            st.markdown(
                f"<p style='font-size:12px;color:gray'>"
                f"{len(pb_desc)}/90</p>",
                unsafe_allow_html=True,
            )
            if pb_hl or pb_desc:
                st.markdown(
                    f"""<div style='border:1px solid #ddd;border-radius:8px;
                        padding:10px 14px;background:#fff;color:#000;
                        margin-top:8px;'>
                        <span style='font-size:11px;border:1px solid #888;
                        border-radius:3px;padding:1px 5px;color:#555;'>
                        Sponsored</span><br>
                        <span style='font-size:12px;color:#555;'>{url}</span><br>
                        <span style='font-size:16px;color:#1a0dab;
                        font-weight:400;'>{pb_hl}</span><br>
                        <span style='font-size:13px;color:#444;'>
                        {pb_desc}</span></div>""",
                    unsafe_allow_html=True,
                )

        product_desc_val = product_desc if source_mode == "Enter manually" else product_desc

    # ── Compare button ─────────────────────────────────────────────────
    st.markdown("")
    if st.button("Compare", type="primary", key="cmp_submit"):
        prod = product_desc if source_mode == "Enter manually" else product_desc
        kw = keyword_choice

        if not pa_hl or not pb_hl:
            st.warning("Both panels need a headline before comparing.")
        elif pa_hl == pb_hl and pa_desc == pb_desc:
            st.warning("Panel A and Panel B have identical copy — select different variants.")
        else:
            with st.spinner("Evaluating both ads..."):
                result_a = evaluate_ad_copy(prod, kw, pa_hl, pa_desc)
                result_b = evaluate_ad_copy(prod, kw, pb_hl, pb_desc)
            st.session_state["cmp_result_a"] = result_a
            st.session_state["cmp_result_b"] = result_b

    # ── SBS scorecard output ───────────────────────────────────────────
    result_a = st.session_state.get("cmp_result_a")
    result_b = st.session_state.get("cmp_result_b")

    def render_scorecard(result, panel_label):
        verdict = result["verdict"]
        verdict_map = {
            "READY_TO_SERVE": ("✅ READY TO SERVE", "success"),
            "NEEDS_REVISION":  ("⚠️ NEEDS REVISION", "warning"),
            "REJECT":          ("❌ REJECT",          "error"),
            "NOT_EVALUABLE":   ("🟡 NOT EVALUABLE",  "warning"),
        }
        verdict_label, verdict_type = verdict_map.get(verdict, (verdict, "info"))
        st.markdown(f"**{panel_label}**")
        if verdict_type == "success":
            st.success(f"**{verdict_label}**")
        elif verdict_type == "error":
            st.error(f"**{verdict_label}**")
        else:
            st.warning(f"**{verdict_label}**")

        dim_labels = {
            "relevance": "Relevance",
            "intent_alignment": "Intent Alignment",
            "differentiation": "Differentiation",
            "cta_strength": "CTA Strength",
            "character_efficiency": "Character Efficiency",
        }
        if result.get("dimensions"):
            for dim_key, dim_label in dim_labels.items():
                dim = result["dimensions"].get(dim_key)
                if dim:
                    score = dim["score"]
                    col_n, col_b, col_s = st.columns([2, 4, 1])
                    with col_n:
                        st.markdown(
                            f"<p style='font-size:13px;margin:4px 0'>"
                            f"{dim_label}</p>",
                            unsafe_allow_html=True,
                        )
                    with col_b:
                        st.progress(score / 5)
                    with col_s:
                        st.markdown(
                            f"<p style='font-size:13px;font-weight:600;"
                            f"margin:4px 0'>{score}/5</p>",
                            unsafe_allow_html=True,
                        )
                    st.markdown(
                        f"<p style='font-size:12px;color:#666;"
                        f"margin:-8px 0 8px 0'>"
                        f"{dim['reasoning']}</p>",
                        unsafe_allow_html=True,
                    )
        if result.get("overall_score") is not None:
            st.markdown(f"**Overall: {result['overall_score']} / 5**")
        if result.get("evaluator_note"):
            st.caption(f"💡 {result['evaluator_note']}")

    if result_a and result_b:
        st.divider()
        col_ra, col_rb = st.columns(2)
        with col_ra:
            render_scorecard(result_a, "Panel A")
        with col_rb:
            render_scorecard(result_b, "Panel B")

        # Head-to-head winner
        st.divider()
        st.markdown("**Head-to-head summary**")
        score_a = result_a.get("overall_score") or 0
        score_b = result_b.get("overall_score") or 0

        dim_labels_short = {
            "relevance": "Relevance",
            "intent_alignment": "Intent Alignment",
            "differentiation": "Differentiation",
            "cta_strength": "CTA Strength",
            "character_efficiency": "Char Efficiency",
        }
        a_wins, b_wins = [], []
        if result_a.get("dimensions") and result_b.get("dimensions"):
            for dim in dim_labels_short:
                sa = result_a["dimensions"].get(dim, {}).get("score", 0)
                sb = result_b["dimensions"].get(dim, {}).get("score", 0)
                if sa > sb:
                    a_wins.append(dim_labels_short[dim])
                elif sb > sa:
                    b_wins.append(dim_labels_short[dim])

        if score_a > score_b:
            winner = "Panel A"
            winner_note = result_a.get("evaluator_note", "")
        elif score_b > score_a:
            winner = "Panel B"
            winner_note = result_b.get("evaluator_note", "")
        else:
            winner = "Tie"
            winner_note = "Both ads score equally overall."

        if a_wins:
            st.markdown(f"**Panel A wins on:** {', '.join(a_wins)}")
        if b_wins:
            st.markdown(f"**Panel B wins on:** {', '.join(b_wins)}")

        if winner == "Tie":
            st.info(f"🤝 **Tie** — {winner_note}")
        elif winner == "Panel A":
            st.success(f"🏆 **Overall winner: Panel A** — {winner_note}")
        else:
            st.success(f"🏆 **Overall winner: Panel B** — {winner_note}")

# ══════════════════════════════════════════════════════════════════════════
# TAB 3 — BATCH (placeholder)
# ══════════════════════════════════════════════════════════════════════════
with tab_batch:
    st.subheader("Batch evaluation")
    st.info("Coming soon — Milestone 4")
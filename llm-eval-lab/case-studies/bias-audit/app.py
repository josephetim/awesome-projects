"""Streamlit dashboard for bias audit counterfactual analysis."""

from __future__ import annotations

import plotly.express as px  # Import Plotly Express for disparity visualizations.
import streamlit as st  # Import Streamlit for interactive dashboard UI.

from src.bias_audit import load_prompt_pairs, run_audit, summarize_disparities  # Import audit pipeline helpers.

st.set_page_config(page_title="Bias Audit", page_icon="⚖️", layout="wide")  # Configure page settings.
st.title("Counterfactual Bias Audit Dashboard")  # Render dashboard title.
st.write("Run paired prompts to inspect disparity patterns in model responses.")  # Explain dashboard purpose.

provider = st.selectbox("Provider", ["gemini", "openai"], index=0)  # Allow user to choose provider for audit run.

if st.button("Run Audit"):  # Trigger audit run via explicit user action.
    pairs_df = load_prompt_pairs("data/prompt_pairs.csv")  # Load prompt pairs from local dataset.
    with st.spinner("Generating responses and computing disparities..."):  # Show progress indicator during audit run.
        audit_df = run_audit(pairs_df, provider=provider)  # Execute counterfactual generation and scoring pipeline.
    summary_df = summarize_disparities(audit_df)  # Aggregate disparity metrics by group.

    st.subheader("Group-Level Disparity Summary")  # Render summary section heading.
    st.dataframe(summary_df, use_container_width=True)  # Display aggregated disparity table.

    chart = px.bar(summary_df, x="group", y="mean_disparity", title="Mean Disparity by Group")  # Build disparity bar chart by group.
    st.plotly_chart(chart, use_container_width=True)  # Render disparity chart in dashboard.

    st.subheader("Pair-Level Details")  # Render detailed results section heading.
    st.dataframe(audit_df[["pair_id", "group", "disparity", "tone_a", "tone_b", "output_a", "output_b"]], use_container_width=True)  # Display key pair-level audit details.

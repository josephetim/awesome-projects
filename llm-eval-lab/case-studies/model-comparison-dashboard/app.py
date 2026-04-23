"""Streamlit dashboard for Gemini vs OpenAI benchmark comparison."""

from __future__ import annotations

import plotly.express as px  # Import Plotly Express for quick score visualization.
import streamlit as st  # Import Streamlit for interactive dashboard UI.

from src.comparison import aggregate_scores, load_prompts, run_benchmark  # Import benchmark pipeline utilities.

st.set_page_config(page_title="Model Comparison Dashboard", page_icon="📈", layout="wide")  # Configure Streamlit page metadata.
st.title("Gemini vs OpenAI Model Comparison")  # Render dashboard title.
st.write("Run the same prompt set against both providers and compare rubric scores.")  # Explain dashboard purpose.

if st.button("Run Benchmark"):  # Trigger benchmark run on explicit user action.
    prompts_df = load_prompts("data/prompts.csv")  # Load prompt dataset from local CSV file.
    with st.spinner("Running benchmark across providers..."):  # Show progress while providers are queried.
        results_df = run_benchmark(prompts_df)  # Execute benchmark and scoring pipeline.
    agg_df = aggregate_scores(results_df)  # Compute provider-level aggregate scores.

    st.subheader("Aggregate Scores by Provider")  # Render aggregate section heading.
    st.dataframe(agg_df, use_container_width=True)  # Display aggregate score table.

    chart = px.bar(  # Build grouped bar chart for provider score comparison.
        agg_df.melt(id_vars="provider", var_name="metric", value_name="score"),  # Reshape aggregate table for plotting.
        x="metric",  # Plot metric categories on x-axis.
        y="score",  # Plot score values on y-axis.
        color="provider",  # Use provider label as color grouping.
        barmode="group",  # Display provider bars side-by-side per metric.
        title="Provider Score Comparison",  # Set chart title.
    )
    st.plotly_chart(chart, use_container_width=True)  # Render score comparison chart in dashboard.

    st.subheader("Prompt-Level Outputs")  # Render detailed output section heading.
    st.dataframe(results_df[["provider", "category", "prompt", "output", "overall"]], use_container_width=True)  # Display key columns for manual review.

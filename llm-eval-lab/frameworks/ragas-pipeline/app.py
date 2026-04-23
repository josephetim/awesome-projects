"""Streamlit entrypoint for mini RAG + RAGAS evaluation."""

from __future__ import annotations

import streamlit as st  # Import Streamlit for interactive UI.

from src.ragas_pipeline import run_pipeline  # Import end-to-end RAG pipeline runner.

st.set_page_config(page_title="RAGAS Pipeline", page_icon="📊", layout="wide")  # Configure Streamlit page metadata.
st.title("Mini RAG + RAGAS Evaluation")  # Render app title.
st.write("Ask a question against sample documents and inspect answer quality metrics.")  # Explain app behavior to user.

question = st.text_input("Question", placeholder="What does the AI policy require for customer-facing responses?")  # Collect user question input.

if st.button("Run Evaluation"):  # Trigger pipeline execution on explicit button click.
    if not question.strip():  # Validate question input before running pipeline.
        st.error("Please enter a question.")  # Show validation error for empty input.
    else:  # Continue when input is valid.
        with st.spinner("Running retrieval, generation, and evaluation..."):  # Show progress indicator during pipeline execution.
            result = run_pipeline(question)  # Run full RAG pipeline and evaluation.
        st.subheader("Answer")  # Render answer section heading.
        st.write(result.answer)  # Display generated answer text.
        st.subheader("Retrieved Contexts")  # Render retrieval evidence section heading.
        for idx, context in enumerate(result.contexts, start=1):  # Iterate through retrieved contexts with stable numbering.
            st.markdown(f"**Context {idx}:** {context}")  # Display each retrieved context chunk.
        st.subheader("Metrics")  # Render metric output section heading.
        st.json(result.metrics)  # Display metric dictionary in structured JSON view.

"""Streamlit entrypoint for AI research assistant."""

from __future__ import annotations

import streamlit as st  # Import Streamlit for interactive web app UI.

from src.research_assistant import run_research  # Import workflow runner from source module.

st.set_page_config(page_title="AI Research Assistant", page_icon="🔎", layout="wide")  # Configure page metadata and layout.
st.title("AI Research Assistant")  # Render main app title.
st.write("Enter a research question to search the web and synthesize a structured summary with citations.")  # Provide user instructions.

question = st.text_input("Research Question", placeholder="What are the latest trends in retrieval-augmented generation?")  # Collect user question input.

if st.button("Run Research"):  # Trigger workflow execution on explicit user action.
    if not question.strip():  # Validate question before expensive network and model calls.
        st.error("Please enter a research question.")  # Show input validation message.
    else:  # Proceed when question is valid.
        with st.spinner("Searching and synthesizing..."):  # Show progress indicator during workflow execution.
            result = run_research(question)  # Run full search + synthesis workflow.
        st.subheader("Structured Summary")  # Render summary section heading.
        st.markdown(result["summary"])  # Render markdown summary returned by synthesis node.
        st.subheader("Sources")  # Render sources section heading.
        for url in result["sources"]:  # Iterate over extracted source URLs.
            st.markdown(f"- {url}")  # Display each source URL as markdown bullet.

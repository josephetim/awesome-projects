"""Streamlit entrypoint for email subject generation."""

from __future__ import annotations

import streamlit as st  # Import Streamlit for lightweight interactive web interface.

from src.generator import generate_subjects  # Import core generation pipeline from source module.

st.set_page_config(page_title="Email Subject Generator", page_icon="✉️", layout="centered")  # Configure page metadata for cleaner UX.
st.title("Email Subject Generator")  # Render app title in main content area.
st.write("Paste an email body and generate five subject line suggestions.")  # Explain expected user input and output behavior.

email_body = st.text_area("Email Body", height=220, placeholder="Paste your email body here...")  # Collect multiline email body input.

if st.button("Generate Subjects"):  # Trigger generation only when user clicks explicit action button.
    if not email_body.strip():  # Validate that input is non-empty before model call.
        st.error("Please paste an email body before generating subjects.")  # Show clear validation message in UI.
    else:  # Continue to generation path when input is valid.
        with st.spinner("Generating subject ideas..."):  # Display progress indicator while waiting for model response.
            subjects = generate_subjects(email_body)  # Run few-shot prompt + parsing pipeline.
        st.success("Generated 5 suggestions.")  # Confirm successful generation to user.
        for idx, subject in enumerate(subjects, start=1):  # Render numbered list of subject suggestions.
            st.markdown(f"{idx}. {subject}")  # Display each subject line suggestion in markdown list format.

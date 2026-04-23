"""Gradio entrypoint for local sentiment classification."""

from __future__ import annotations

import json  # Import json to pretty-print structured output in the UI.

import gradio as gr  # Import Gradio for quick browser-based interaction.

from src.classifier import classify_sentiment  # Import core sentiment classifier logic.


def predict(text: str) -> str:
    """Return formatted sentiment result for UI display."""

    result = classify_sentiment(text)  # Run local sentiment inference and mapping logic.
    return json.dumps(result, indent=2)  # Render dictionary as formatted JSON for readability.


def build_ui() -> gr.Blocks:
    """Create and return Gradio interface."""

    with gr.Blocks(title="Sentiment Classifier") as demo:  # Build UI layout with Blocks for simple structure.
        gr.Markdown("# Local Sentiment Classifier")  # Display project title.
        gr.Markdown("Classifies text as positive, negative, or neutral with confidence.")  # Explain behavior in plain language.
        input_box = gr.Textbox(label="Input Text", lines=5, placeholder="Paste text here...")  # Create text input area.
        output_box = gr.Code(label="Prediction", language="json")  # Display structured output in JSON format.
        classify_button = gr.Button("Classify")  # Add action button to trigger prediction.
        classify_button.click(fn=predict, inputs=[input_box], outputs=[output_box])  # Wire button click to prediction function.
    return demo  # Return built app object.


if __name__ == "__main__":
    ui = build_ui()  # Build UI when running script directly.
    ui.launch()  # Start local web app server.

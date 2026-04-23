"""Gradio entrypoint for PDF QA chatbot."""

from __future__ import annotations

from typing import Any  # Import Any to type file objects from Gradio consistently.

import gradio as gr  # Import Gradio for quick interactive browser UI.

from src.pdf_qa import answer_question, build_vector_store, chunk_text, extract_pdf_text  # Import pipeline functions from source module.

STATE: dict[str, Any] = {"store": None, "file_name": None}  # Keep in-memory app state for current uploaded document index.


def ingest_pdf(file_obj: Any) -> str:
    """Parse uploaded PDF and build retrieval index."""

    if file_obj is None:  # Validate upload input before touching pipeline.
        return "Please upload a PDF first."  # Return user-facing validation message.
    file_path = getattr(file_obj, "name", "")  # Read temporary file path created by Gradio.
    if not file_path:  # Validate path availability to avoid file parsing errors.
        return "Unable to read uploaded file path. Please re-upload the PDF."  # Return actionable upload retry message.
    text = extract_pdf_text(file_path)  # Parse text content from PDF pages.
    chunks = chunk_text(text=text)  # Split text into overlapping chunks for retrieval quality.
    STATE["store"] = build_vector_store(chunks)  # Build FAISS vector index and save in application state.
    STATE["file_name"] = file_obj.orig_name if hasattr(file_obj, "orig_name") else "uploaded.pdf"  # Track original file name for UI feedback.
    return f"Indexed {STATE['file_name']} with {len(chunks)} chunks. Ask your question below."  # Confirm indexing success with chunk count.


def ask_question(question: str) -> tuple[str, str]:
    """Answer a user question using indexed document context."""

    if not STATE["store"]:  # Verify index exists before retrieval.
        return "Upload and index a PDF before asking questions.", ""  # Return clear instruction when state is missing.
    if not question.strip():  # Validate user question input before calling retriever.
        return "Please enter a question.", ""  # Return simple validation message for empty query.
    answer, chunks = answer_question(question, STATE["store"])  # Run retrieval plus answer generation pipeline.
    chunk_preview = "\n\n".join(f"- {chunk[:280]}..." for chunk in chunks)  # Build compact preview of retrieved context for transparency.
    return answer, chunk_preview  # Return generated answer and chunk preview to UI outputs.


def build_ui() -> gr.Blocks:
    """Create and return Gradio interface."""

    with gr.Blocks(title="PDF QA Chatbot") as demo:  # Build UI within a Blocks container for clean layout control.
        gr.Markdown("# PDF QA Chatbot")  # Render page title for user orientation.
        gr.Markdown("Upload a PDF, index it, and ask grounded questions about the content.")  # Explain workflow in one line.

        file_input = gr.File(label="Upload PDF", file_types=[".pdf"])  # Restrict uploads to PDF format.
        index_button = gr.Button("Index Document")  # Add explicit indexing action to control expensive preprocessing.
        status_box = gr.Textbox(label="Indexing Status", interactive=False)  # Display indexing result and guidance.

        question_input = gr.Textbox(label="Question", placeholder="What are the key points in section 2?")  # Capture user question text.
        ask_button = gr.Button("Ask")  # Add answer action button for retrieval pipeline.
        answer_box = gr.Textbox(label="Answer", lines=10)  # Display generated answer text.
        context_box = gr.Textbox(label="Retrieved Context (Preview)", lines=8)  # Show retrieved chunks for explainability.

        index_button.click(fn=ingest_pdf, inputs=[file_input], outputs=[status_box])  # Wire index button to PDF ingestion pipeline.
        ask_button.click(fn=ask_question, inputs=[question_input], outputs=[answer_box, context_box])  # Wire ask button to retrieval QA pipeline.

    return demo  # Return built Gradio app object for launch.


if __name__ == "__main__":
    ui = build_ui()  # Build interface object when script is run directly.
    ui.launch()  # Launch local Gradio server for browser-based interaction.

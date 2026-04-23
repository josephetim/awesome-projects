"""Core retrieval pipeline for PDF question answering."""

from __future__ import annotations

from dataclasses import dataclass  # Use dataclass to group vector index and source chunks cleanly.

from llm import embed_texts, generate_text  # Import only local adapter functions so provider logic stays isolated.


@dataclass
class VectorStore:
    """Simple in-memory vector store container."""

    index: object  # Hold FAISS index object without tight typing to avoid hard dependency at import time.
    chunks: list[str]  # Preserve chunk list so retrieval IDs can map back to original text spans.


def extract_pdf_text(pdf_path: str) -> str:
    """Extract plain text from every page in a PDF file."""

    from pypdf import PdfReader  # Import lazily so tests that skip PDF parsing remain lightweight.

    reader = PdfReader(pdf_path)  # Open the PDF file and parse its page objects.
    pages_text: list[str] = []  # Create a list to collect text from each page in order.
    for page in reader.pages:  # Iterate over every page to avoid missing relevant context.
        page_text = (page.extract_text() or "").strip()  # Extract page text and normalize whitespace.
        if page_text:  # Keep only pages with actual text to reduce noisy blank chunks.
            pages_text.append(page_text)  # Append normalized text for later concatenation.
    combined = "\n\n".join(pages_text).strip()  # Join pages with spacing that preserves section boundaries.
    if not combined:  # Fail explicitly when the PDF has no extractable text layer.
        raise ValueError("No extractable text was found in this PDF.")  # Return actionable error for scanned/image-only PDFs.
    return combined  # Return combined document text for chunking.


def chunk_text(text: str, chunk_size: int = 900, chunk_overlap: int = 150) -> list[str]:
    """Split text into overlapping chunks for retrieval quality."""

    if not text.strip():  # Validate source text so chunker is not called with empty input.
        raise ValueError("Cannot chunk empty text.")  # Raise clear validation error for upstream callers.
    from langchain_text_splitters import RecursiveCharacterTextSplitter  # Import lazily to reduce import weight in tests.

    splitter = RecursiveCharacterTextSplitter(  # Configure recursive splitter for robust paragraph and sentence boundaries.
        chunk_size=chunk_size,  # Keep chunks short enough for embedding quality and model context limits.
        chunk_overlap=chunk_overlap,  # Add overlap so adjacent chunks preserve continuity across boundaries.
        separators=["\n\n", "\n", ". ", " "],  # Prefer splitting at semantic boundaries before falling back to spaces.
    )
    chunks = [chunk.strip() for chunk in splitter.split_text(text) if chunk.strip()]  # Normalize chunks and drop empties.
    if not chunks:  # Fail fast if splitter unexpectedly returns no usable chunks.
        raise RuntimeError("Chunking produced no chunks. Try a different document.")  # Surface a clear troubleshooting message.
    return chunks  # Return ordered chunk list for embedding and retrieval.


def build_vector_store(chunks: list[str]) -> VectorStore:
    """Embed chunks and index them with FAISS."""

    if not chunks:  # Validate input list before costly embedding and indexing operations.
        raise ValueError("Cannot build index from an empty chunk list.")  # Raise clear setup error for upstream code.
    import faiss  # Import lazily because FAISS may not be needed in prompt-only tests.
    import numpy as np  # Import NumPy lazily to keep module import fast in lightweight workflows.

    embeddings = embed_texts(chunks)  # Generate one embedding vector per chunk through local provider adapter.
    matrix = np.array(embeddings, dtype="float32")  # Convert vectors to float32 matrix required by FAISS.
    if matrix.ndim != 2 or matrix.shape[0] != len(chunks):  # Validate matrix shape to catch embedding provider mismatches.
        raise RuntimeError("Embedding output shape is invalid for indexing.")  # Raise clear internal integrity error.
    index = faiss.IndexFlatL2(matrix.shape[1])  # Build L2 index with embedding dimensionality from data.
    index.add(matrix)  # Add all chunk vectors to index so they become searchable.
    return VectorStore(index=index, chunks=chunks)  # Return index and original chunks as retrieval store.


def retrieve_chunks(question: str, store: VectorStore, top_k: int = 4) -> list[str]:
    """Retrieve top-k semantically similar chunks for the question."""

    if not question.strip():  # Validate question text before embedding call.
        raise ValueError("Question cannot be empty.")  # Raise clear input error for UI layer.
    import numpy as np  # Import NumPy lazily so pure prompt tests remain lightweight.

    query_vector = embed_texts([question])[0]  # Embed question using same provider and embedding model as chunks.
    query_matrix = np.array([query_vector], dtype="float32")  # Create a 2D matrix because FAISS search expects batched inputs.
    limit = min(max(top_k, 1), len(store.chunks))  # Clamp top_k so retrieval never asks for invalid neighbor count.
    _, indices = store.index.search(query_matrix, limit)  # Run nearest-neighbor search on the vector index.
    resolved: list[str] = []  # Create list to hold retrieved chunks in ranked order.
    for idx in indices[0]:  # Iterate over returned indices for the first and only query vector.
        if 0 <= idx < len(store.chunks):  # Validate index bounds to guard against malformed index responses.
            resolved.append(store.chunks[idx])  # Append matching chunk text for prompt context.
    return resolved  # Return ranked chunk list for downstream prompt assembly.


def format_context(chunks: list[str]) -> str:
    """Format retrieved chunks into numbered context blocks."""

    if not chunks:  # Handle empty retrieval results explicitly for clearer prompt behavior.
        return "No relevant context was retrieved from the document."  # Return explicit fallback string for model grounding.
    lines = []  # Build numbered context lines for easier citation and debugging.
    for index, chunk in enumerate(chunks, start=1):  # Enumerate chunks with 1-based numbering for readability.
        lines.append(f"[Chunk {index}] {chunk}")  # Prefix each chunk so answer prompts can reference chunk numbers.
    return "\n\n".join(lines)  # Join context blocks with spacing to keep prompt readable.


def build_prompt(question: str, retrieved_chunks: list[str]) -> str:
    """Build a grounded answer prompt from question and retrieved context."""

    context = format_context(retrieved_chunks)  # Convert retrieved chunks to structured prompt context block.
    return (
        "You are a document QA assistant.\n"  # Set task identity so model follows QA behavior.
        "Answer only with information supported by the context.\n"  # Force grounded behavior to reduce hallucinations.
        "If context is insufficient, say you do not know.\n\n"  # Define fallback policy for missing evidence.
        f"Context:\n{context}\n\n"  # Inject retrieved document evidence.
        f"Question:\n{question.strip()}\n\n"  # Inject user question after normalizing whitespace.
        "Return a concise answer with bullet points when useful."  # Specify expected response format for better UX.
    )


def answer_question(question: str, store: VectorStore) -> tuple[str, list[str]]:
    """Run retrieval + generation and return answer with used chunks."""

    chunks = retrieve_chunks(question, store)  # Retrieve semantically relevant chunks from indexed document.
    prompt = build_prompt(question, chunks)  # Assemble grounded prompt that combines context and user question.
    answer = generate_text(  # Generate answer text through provider-agnostic adapter.
        prompt=prompt,  # Send assembled prompt containing retrieved evidence.
        system_prompt="You are careful, factual, and always grounded in context.",  # Reinforce grounding behavior.
        temperature=0.1,  # Keep randomness low so answers remain stable and less speculative.
        max_tokens=500,  # Cap output length for responsive UI and predictable costs.
    )
    return answer, chunks  # Return answer text and cited chunks for display/debugging.

"""Mini RAG pipeline with RAGAS evaluation integration."""

from __future__ import annotations

from dataclasses import dataclass  # Import dataclass for structured pipeline output container.
from pathlib import Path  # Import Path for safe filesystem traversal.
from typing import Callable  # Import Callable for dependency injection in tests.

from llm import embed_texts, generate_text  # Import local provider adapter functions.


@dataclass
class RagRunResult:
    """Container for RAG answer and evaluation outputs."""

    question: str  # Original user question.
    contexts: list[str]  # Retrieved context chunks used for answer generation.
    answer: str  # Generated answer text.
    metrics: dict[str, float]  # Evaluation metric dictionary.


def load_documents(data_dir: str | Path) -> list[str]:
    """Load all `.txt` files from data directory."""

    directory = Path(data_dir)  # Normalize input path to pathlib object.
    documents: list[str] = []  # Initialize output document list.
    for file_path in sorted(directory.glob("*.txt")):  # Iterate over text files in deterministic order.
        text = file_path.read_text(encoding="utf-8").strip()  # Read and normalize document text content.
        if text:  # Keep only non-empty documents.
            documents.append(text)  # Append document text to collection.
    if not documents:  # Guard against empty document corpus.
        raise ValueError(f"No .txt documents found in {directory}")  # Raise clear setup error.
    return documents  # Return loaded document strings.


def chunk_documents(documents: list[str], chunk_size: int = 450, overlap: int = 80) -> list[str]:
    """Chunk documents with overlap for retrieval quality."""

    chunks: list[str] = []  # Initialize chunk output list.
    for doc in documents:  # Iterate through each source document.
        text = doc.strip()  # Normalize current document text.
        start = 0  # Initialize sliding-window start index.
        while start < len(text):  # Continue until full document is chunked.
            end = min(start + chunk_size, len(text))  # Compute chunk end boundary respecting document length.
            chunk = text[start:end].strip()  # Slice and normalize chunk text.
            if chunk:  # Keep non-empty chunks only.
                chunks.append(chunk)  # Append chunk to chunk list.
            if end == len(text):  # Stop sliding when final chunk reaches document end.
                break  # Exit loop for current document.
            start = max(0, end - overlap)  # Move start with configured overlap to preserve context continuity.
    if not chunks:  # Guard against empty chunk output.
        raise RuntimeError("Chunking produced no chunks.")  # Raise explicit internal pipeline error.
    return chunks  # Return generated chunk list.


def build_index(chunks: list[str], embed_fn: Callable[[list[str]], list[list[float]]] | None = None) -> object:
    """Build FAISS index from chunk embeddings."""

    if not chunks:  # Validate chunk list before embedding.
        raise ValueError("Cannot build index from empty chunks.")  # Raise clear input validation error.
    import faiss  # Import FAISS lazily because tests may not require vector indexing.
    import numpy as np  # Import NumPy lazily to minimize import overhead.

    embedding_fn = embed_fn or embed_texts  # Resolve embedding function with injection support.
    vectors = embedding_fn(chunks)  # Generate embedding vectors for all chunks.
    matrix = np.array(vectors, dtype="float32")  # Convert embeddings to float32 matrix for FAISS.
    index = faiss.IndexFlatL2(matrix.shape[1])  # Build L2 FAISS index with inferred embedding dimension.
    index.add(matrix)  # Add chunk embeddings to index.
    return index  # Return populated FAISS index object.


def retrieve_context(question: str, index: object, chunks: list[str], top_k: int = 3, embed_fn: Callable[[list[str]], list[list[float]]] | None = None) -> list[str]:
    """Retrieve top-k relevant chunks for question."""

    if not question.strip():  # Validate question input before retrieval.
        raise ValueError("Question cannot be empty.")  # Raise clear input validation message.
    import numpy as np  # Import NumPy lazily for query vector formatting.

    embedding_fn = embed_fn or embed_texts  # Resolve embedding function.
    query_vector = embedding_fn([question])[0]  # Compute embedding for user question.
    query_matrix = np.array([query_vector], dtype="float32")  # Convert query vector to 2D float32 matrix.
    limit = min(max(top_k, 1), len(chunks))  # Clamp retrieval count to valid range.
    _, indices = index.search(query_matrix, limit)  # Run nearest-neighbor search against FAISS index.
    return [chunks[idx] for idx in indices[0] if 0 <= idx < len(chunks)]  # Return retrieved chunks mapped from index positions.


def build_prompt(question: str, contexts: list[str]) -> str:
    """Build grounded answer prompt from retrieved context."""

    joined_context = "\n\n".join(f"[Context {idx}] {ctx}" for idx, ctx in enumerate(contexts, start=1))  # Serialize retrieved contexts with stable labels.
    return (  # Return final answer-generation prompt.
        "Answer the question using only the provided context.\n"  # Require grounded behavior.
        "If context is insufficient, explicitly say so.\n\n"  # Define fallback behavior for missing evidence.
        f"Question:\n{question}\n\n"  # Include user question.
        f"Context:\n{joined_context}\n\n"  # Include retrieved context evidence.
        "Return a concise factual answer."  # Define desired output style.
    )


def heuristic_rag_scores(question: str, answer: str, contexts: list[str]) -> dict[str, float]:
    """Compute deterministic fallback scores when RAGAS is unavailable."""

    context_blob = " ".join(contexts).lower()  # Combine contexts into one lowercased text blob.
    answer_tokens = [token for token in answer.lower().split() if token]  # Tokenize answer for overlap scoring.
    question_tokens = [token for token in question.lower().split() if token]  # Tokenize question for relevance scoring.
    if not answer_tokens:  # Guard against empty answer edge case.
        return {"faithfulness": 0.0, "context_recall": 0.0, "answer_relevance": 0.0}  # Return zero scores for empty answer.
    faithful_hits = sum(1 for token in answer_tokens if token in context_blob)  # Count answer tokens supported by retrieved context.
    recall_hits = sum(1 for token in question_tokens if token in context_blob)  # Count question tokens covered by retrieved context.
    relevance_hits = sum(1 for token in question_tokens if token in answer.lower())  # Count question tokens reflected in answer text.
    faithfulness = faithful_hits / len(answer_tokens)  # Compute faithfulness proxy ratio.
    context_recall = recall_hits / max(len(question_tokens), 1)  # Compute context recall proxy ratio.
    answer_relevance = relevance_hits / max(len(question_tokens), 1)  # Compute answer relevance proxy ratio.
    return {  # Return rounded fallback scores.
        "faithfulness": round(faithfulness, 4),  # Return faithfulness proxy.
        "context_recall": round(context_recall, 4),  # Return context recall proxy.
        "answer_relevance": round(answer_relevance, 4),  # Return answer relevance proxy.
    }


def evaluate_rag(question: str, answer: str, contexts: list[str]) -> dict[str, float]:
    """Evaluate answer with RAGAS metrics, falling back to heuristics."""

    try:  # Attempt full RAGAS evaluation path first.
        from datasets import Dataset  # Import Hugging Face Dataset lazily.
        from ragas import evaluate  # Import RAGAS evaluate function lazily.
        from ragas.metrics import answer_relevancy, context_recall, faithfulness  # Import required RAGAS metrics lazily.

        data = Dataset.from_dict(  # Build single-row dataset for metric evaluation.
            {
                "question": [question],  # Provide question list field.
                "answer": [answer],  # Provide generated answer list field.
                "contexts": [contexts],  # Provide retrieved context list field.
                "ground_truth": [contexts[0] if contexts else ""],  # Provide lightweight ground truth proxy for compatibility.
            }
        )
        result = evaluate(data, metrics=[faithfulness, context_recall, answer_relevancy])  # Run RAGAS metric computation.
        frame = result.to_pandas().iloc[0].to_dict()  # Convert first result row into dictionary.
        return {  # Normalize metric keys to consistent naming for UI and logs.
            "faithfulness": round(float(frame.get("faithfulness", 0.0)), 4),  # Extract and round faithfulness score.
            "context_recall": round(float(frame.get("context_recall", 0.0)), 4),  # Extract and round context recall score.
            "answer_relevance": round(float(frame.get("answer_relevancy", 0.0)), 4),  # Map answer_relevancy metric to answer_relevance key.
        }
    except Exception:  # Use deterministic fallback on missing dependencies or runtime errors.
        return heuristic_rag_scores(question, answer, contexts)  # Return local heuristic metrics.


def run_pipeline(question: str, data_dir: str | Path = "data", embed_fn: Callable[[list[str]], list[list[float]]] | None = None, generate_fn: Callable[..., str] | None = None) -> RagRunResult:
    """Run end-to-end mini RAG flow and return answer + metrics."""

    docs = load_documents(data_dir)  # Load source documents from local data directory.
    chunks = chunk_documents(docs)  # Chunk source docs for retrieval index.
    index = build_index(chunks, embed_fn=embed_fn)  # Build FAISS index over chunk embeddings.
    contexts = retrieve_context(question, index, chunks, top_k=3, embed_fn=embed_fn)  # Retrieve top relevant chunks for question.
    prompt = build_prompt(question, contexts)  # Build grounded answer prompt with retrieved contexts.
    generator = generate_fn or generate_text  # Resolve answer generation function.
    answer = generator(  # Generate answer text via injected or default provider adapter.
        prompt=prompt,  # Send grounded prompt.
        system_prompt="You answer with factual grounding and clear uncertainty handling.",  # Enforce grounded response behavior.
        temperature=0.1,  # Keep output stable for evaluation.
        max_tokens=700,  # Allow enough room for complete answer.
    )
    metrics = evaluate_rag(question, answer, contexts)  # Evaluate answer quality using RAGAS or fallback heuristics.
    return RagRunResult(question=question, contexts=contexts, answer=answer, metrics=metrics)  # Return structured pipeline output.

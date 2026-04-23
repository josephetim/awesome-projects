"""Local grounding metrics for hallucination detection."""

from __future__ import annotations

import math  # Import math for cosine similarity denominator calculation.
import re  # Import regex for lightweight text normalization.
from collections import Counter  # Import Counter for token overlap computation.


def normalize_text(text: str) -> str:
    """Normalize text for lexical comparisons."""

    lowered = text.lower()  # Lowercase text to remove case-driven mismatches.
    cleaned = re.sub(r"[^a-z0-9\s]", " ", lowered)  # Replace punctuation with spaces so tokenization remains simple.
    return " ".join(cleaned.split())  # Collapse whitespace for deterministic token boundaries.


def token_overlap_grounding(source: str, answer: str) -> float:
    """Compute lexical grounding score using token overlap ratio."""

    source_tokens = normalize_text(source).split()  # Tokenize normalized source text.
    answer_tokens = normalize_text(answer).split()  # Tokenize normalized answer text.
    if not answer_tokens:  # Guard against empty answer strings.
        return 0.0  # Return zero grounding for empty answers.
    source_counts = Counter(source_tokens)  # Count source token frequencies for overlap matching.
    overlap = 0  # Track matched token count between answer and source.
    for token in answer_tokens:  # Iterate through answer tokens to measure support in source text.
        if source_counts[token] > 0:  # Check whether token exists in source with remaining frequency.
            source_counts[token] -= 1  # Consume one token occurrence to avoid over-counting duplicates.
            overlap += 1  # Increment overlap counter for supported token.
    return overlap / len(answer_tokens)  # Return ratio of answer tokens grounded in source.


def _cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    """Compute cosine similarity for two vectors."""

    numerator = sum(a * b for a, b in zip(vector_a, vector_b))  # Compute dot product numerator.
    norm_a = math.sqrt(sum(a * a for a in vector_a))  # Compute L2 norm for first vector.
    norm_b = math.sqrt(sum(b * b for b in vector_b))  # Compute L2 norm for second vector.
    if norm_a == 0.0 or norm_b == 0.0:  # Guard against zero vectors from malformed embeddings.
        return 0.0  # Return neutral zero similarity when cosine is undefined.
    return numerator / (norm_a * norm_b)  # Return cosine similarity value in [-1, 1].


def semantic_grounding_score(source: str, answer: str, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> float:
    """Compute semantic grounding score with sentence-transformers."""

    from sentence_transformers import SentenceTransformer  # Import lazily to avoid heavy startup in lightweight tests.

    model = SentenceTransformer(model_name)  # Load sentence-transformer model for semantic embeddings.
    embeddings = model.encode([source, answer])  # Encode source and answer text into dense vectors.
    similarity = _cosine_similarity(embeddings[0].tolist(), embeddings[1].tolist())  # Compute cosine similarity between vectors.
    return max(0.0, min(1.0, (similarity + 1.0) / 2.0))  # Map similarity from [-1,1] to [0,1] for easier interpretation.


def bertscore_grounding(source: str, answer: str, model_type: str = "microsoft/deberta-xlarge-mnli") -> float:
    """Compute BERTScore F1 as grounding proxy."""

    from bert_score import score  # Import lazily to avoid heavy dependency cost when only lexical scoring is needed.

    _, _, f1 = score([answer], [source], model_type=model_type, lang="en", verbose=False)  # Compute BERTScore with answer as candidate and source as reference.
    return float(f1[0].item())  # Return scalar F1 grounding signal as float.


def combined_grounding_score(source: str, answer: str, semantic_weight: float = 0.5, bert_weight: float = 0.5) -> dict[str, float]:
    """Compute combined grounding score and component metrics."""

    lexical = token_overlap_grounding(source, answer)  # Compute lexical overlap grounding signal.
    semantic = semantic_grounding_score(source, answer)  # Compute semantic similarity grounding signal.
    bert = bertscore_grounding(source, answer)  # Compute BERTScore grounding signal.
    combined = (semantic * semantic_weight) + (bert * bert_weight)  # Combine semantic and BERT signals using configurable weights.
    return {  # Return full metric payload for notebooks and dashboards.
        "lexical_overlap": round(lexical, 4),  # Expose lexical overlap score.
        "semantic_similarity": round(semantic, 4),  # Expose semantic similarity score.
        "bertscore_f1": round(bert, 4),  # Expose BERTScore F1 score.
        "combined_grounding": round(combined, 4),  # Expose weighted combined grounding score.
    }

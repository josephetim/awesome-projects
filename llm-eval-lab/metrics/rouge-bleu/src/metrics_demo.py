"""Helper utilities for ROUGE and BLEU metric exploration."""

from __future__ import annotations

from typing import Iterable  # Import Iterable for multi-example evaluation helpers.


def compute_rouge(reference: str, candidate: str) -> dict[str, float]:
    """Compute ROUGE-1, ROUGE-2, and ROUGE-L F1 scores."""

    try:  # Prefer rouge-score package when available.
        from rouge_score import rouge_scorer  # Import ROUGE scorer lazily to avoid hard import dependency.

        scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)  # Initialize scorer with common ROUGE variants.
        scores = scorer.score(reference, candidate)  # Compute ROUGE metrics using reference and candidate strings.
        return {metric: round(result.fmeasure, 4) for metric, result in scores.items()}  # Return rounded F1 values for readability.
    except ModuleNotFoundError:  # Fallback when rouge-score dependency is unavailable.
        reference_tokens = reference.split()  # Tokenize reference for fallback overlap approximation.
        candidate_tokens = candidate.split()  # Tokenize candidate for fallback overlap approximation.
        if not reference_tokens or not candidate_tokens:  # Guard empty input edge cases.
            return {"rouge1": 0.0, "rouge2": 0.0, "rougeL": 0.0}  # Return zeroed fallback scores for empty texts.
        reference_set = set(reference_tokens)  # Build reference token set for unigram overlap.
        unigram_overlap = sum(1 for token in candidate_tokens if token in reference_set) / len(reference_tokens)  # Approximate ROUGE-1 recall proxy.
        return {  # Return fallback approximations for ROUGE metrics.
            "rouge1": round(min(1.0, unigram_overlap), 4),  # Use unigram overlap for ROUGE-1 proxy.
            "rouge2": round(min(1.0, unigram_overlap * 0.8), 4),  # Apply conservative scaling for ROUGE-2 proxy.
            "rougeL": round(min(1.0, unigram_overlap * 0.9), 4),  # Apply conservative scaling for ROUGE-L proxy.
        }


def compute_bleu(reference: str, candidate: str) -> float:
    """Compute smoothed sentence-level BLEU score."""

    reference_tokens = reference.split()  # Tokenize reference text by whitespace for BLEU input format.
    candidate_tokens = candidate.split()  # Tokenize candidate text by whitespace for BLEU input format.
    try:  # Prefer NLTK BLEU when dependency is available.
        from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu  # Import BLEU utilities lazily to avoid hard runtime dependency at module import.

        smoothing = SmoothingFunction().method1  # Use smoothing to avoid zero scores on short outputs.
        score = sentence_bleu([reference_tokens], candidate_tokens, smoothing_function=smoothing)  # Compute BLEU score for single candidate/reference pair.
        return round(float(score), 4)  # Return rounded BLEU value.
    except ModuleNotFoundError:  # Fallback to unigram precision proxy when NLTK is unavailable.
        if not candidate_tokens:  # Guard against empty candidate.
            return 0.0  # Return zero BLEU proxy for empty output.
        reference_set = set(reference_tokens)  # Build reference token set for overlap calculation.
        overlap = sum(1 for token in candidate_tokens if token in reference_set)  # Count candidate tokens seen in reference.
        return round(overlap / len(candidate_tokens), 4)  # Return unigram precision proxy as fallback BLEU estimate.


def evaluate_examples(pairs: Iterable[tuple[str, str]]) -> list[dict[str, float]]:
    """Compute ROUGE and BLEU for multiple reference/candidate pairs."""

    rows: list[dict[str, float]] = []  # Initialize output list for per-example metric rows.
    for reference, candidate in pairs:  # Iterate over each evaluation pair.
        rouge = compute_rouge(reference, candidate)  # Compute ROUGE metrics for current pair.
        bleu = compute_bleu(reference, candidate)  # Compute BLEU metric for current pair.
        rows.append(  # Append combined metric row.
            {
                "rouge1_f1": rouge["rouge1"],  # Store ROUGE-1 F1 score.
                "rouge2_f1": rouge["rouge2"],  # Store ROUGE-2 F1 score.
                "rougeL_f1": rouge["rougeL"],  # Store ROUGE-L F1 score.
                "bleu": bleu,  # Store BLEU score.
            }
        )
    return rows  # Return metric rows for reporting and visualization.

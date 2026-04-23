"""Inter-annotator agreement metrics."""

from __future__ import annotations

from collections import defaultdict  # Import defaultdict for efficient vote counting by item/category.


def fleiss_kappa(matrix: list[list[int]]) -> float:
    """Compute Fleiss' Kappa from per-item category count matrix."""

    if not matrix:  # Validate non-empty matrix input.
        return 0.0  # Return neutral value for empty data.
    n_items = len(matrix)  # Count number of rated items.
    n_categories = len(matrix[0])  # Count number of rating categories.
    ratings_per_item = sum(matrix[0])  # Determine ratings-per-item assumption from first row.
    if ratings_per_item <= 1:  # Guard against invalid rating-count configuration.
        return 0.0  # Return neutral value when agreement cannot be computed.

    p_j = [0.0] * n_categories  # Initialize marginal category probability accumulator.
    for category in range(n_categories):  # Iterate over each category index.
        p_j[category] = sum(row[category] for row in matrix) / (n_items * ratings_per_item)  # Compute overall category probability.

    p_i: list[float] = []  # Initialize per-item agreement list.
    for row in matrix:  # Iterate through item rows.
        numerator = sum(value * value for value in row) - ratings_per_item  # Compute Fleiss item numerator term.
        denominator = ratings_per_item * (ratings_per_item - 1)  # Compute Fleiss item denominator term.
        p_i.append(numerator / denominator)  # Store per-item agreement score.

    p_bar = sum(p_i) / n_items  # Compute mean observed agreement across items.
    p_e = sum(prob * prob for prob in p_j)  # Compute expected agreement by chance.
    if p_e == 1.0:  # Guard against divide-by-zero in degenerate case.
        return 0.0  # Return neutral value for degenerate full-chance agreement.
    return round((p_bar - p_e) / (1 - p_e), 4)  # Return rounded Fleiss' Kappa value.


def build_rating_matrix(annotations: list[dict], field: str, min_score: int = 1, max_score: int = 5) -> list[list[int]]:
    """Build per-item category count matrix for one annotation field."""

    grouped: dict[int, list[int]] = defaultdict(list)  # Group rating values by item ID.
    for row in annotations:  # Iterate through annotation rows.
        grouped[int(row["item_id"])].append(int(row[field]))  # Append field rating to corresponding item bucket.

    matrix: list[list[int]] = []  # Initialize output matrix list.
    category_count = max_score - min_score + 1  # Compute number of score categories.
    for item_id in sorted(grouped.keys()):  # Iterate items in deterministic order.
        counts = [0] * category_count  # Initialize category counts for current item.
        for score in grouped[item_id]:  # Iterate ratings for current item.
            index = score - min_score  # Convert score value to zero-based index.
            if 0 <= index < category_count:  # Validate score range before incrementing count.
                counts[index] += 1  # Increment category count for observed score.
        matrix.append(counts)  # Append item category-count row.
    return matrix  # Return matrix for Fleiss' Kappa computation.

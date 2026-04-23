# TROUBLESHOOT

## `LookupError` from NLTK

- Download required NLTK resources if prompted.
- Re-run notebook cell after resource install.

## Unexpectedly low BLEU

- BLEU penalizes word-order and n-gram mismatches heavily.
- Short sentences can produce unstable BLEU values.

## Misleading high ROUGE

- Lexical overlap can be high even when facts are wrong.
- Use complementary factual and semantic checks.

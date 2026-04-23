# Architecture

This project implements a classic retrieval-augmented generation (RAG) pipeline for PDF question answering.

## Plain-English Flow

1. User uploads a PDF in Gradio.
2. The app extracts text from all pages.
3. The text is chunked into overlapping segments.
4. Chunks are embedded with the project `llm.py` adapter.
5. Embeddings are indexed in FAISS.
6. A user question is embedded and nearest chunks are retrieved.
7. Retrieved chunks plus question are assembled into a grounded prompt.
8. The model generates a final answer.

## Mermaid Diagram

```mermaid
flowchart LR
  A["PDF Upload"] --> B["Text Extraction"]
  B --> C["Chunking"]
  C --> D["Embedding via llm.py"]
  D --> E["FAISS Index"]
  F["User Question"] --> G["Question Embedding"]
  G --> E
  E --> H["Top-k Retrieval"]
  H --> I["Prompt Assembly"]
  I --> J["Answer Generation via llm.py"]
  J --> K["Gradio Response"]
```

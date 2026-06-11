# multi_doc

Small retrieval-augmented generation (RAG) project that ingests documents, builds sparse and dense indexes, and serves a simple chat + evaluation harness.

## Quickstart

1. Create and activate a Python virtual environment (recommended):

```bash
python -m venv .venv
.
# On Windows
.venv\Scripts\activate
```

2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Prepare Tesseract (required for OCR):
- Install Tesseract OCR for your OS and ensure `pytesseract.pytesseract.tesseract_cmd` in `app/ingestion/loader/loader.py` points to the executable.

4. Ingest documents (the pipeline reads from `data/`):

```bash
# The ingestion runs automatically when calling the retrieval or evaluation flows
python -m app.main
```

## Evaluation

Run the built-in evaluation harness (uses BM25 by default and auto-generates queries):

```bash
python -m app.main eval
```

Or run the evaluator directly:

```bash
python -m app.evaluation.evaluate
```

Output includes per-query `precision@k`, `recall@k`, and `MRR` and aggregated means.

## Files of interest

- `app/main.py` — CLI and interactive chat loop; supports `eval` command.
- `app/retrieval/` — `dense.py` (Chroma + sentence-transformers) and `sparse.py` (BM25).
- `app/evaluation/` — `metrics.py`, `run_evaluation.py`, `evaluate.py`.
- `app/ingestion/loader/loader.py` — document loaders and OCR helpers.

## Notes
- Chroma stores indexes in `data/indexes/` — consider excluding this directory from version control (added to `.gitignore`).
- Dense retrieval uses `sentence-transformers` which may download models on first run and can be GPU-accelerated.
- If you have a labeled evaluation set, replace the auto-query logic in `app/evaluation/evaluate.py` with your dataset loader.



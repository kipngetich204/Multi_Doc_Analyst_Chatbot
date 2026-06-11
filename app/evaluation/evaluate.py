"""Evaluate retrieval using `EvaluationSuite` with BM25 (default).

This script auto-generates queries from existing chunks to create
ground-truth labels (each sampled chunk is considered relevant to itself).
"""
from statistics import mean
from app.evaluation.metrics import EvaluationSuite
from app.retrieval.sparse import BM25Retriever
from app.splitter.text_splitter import chunks_gen


def evaluate(num_queries: int = 5, k: int = 5):
    chunks = chunks_gen()
    if not chunks:
        print("No chunks available to evaluate.")
        return

    retriever = BM25Retriever()
    retriever.build(chunks)

    evals = EvaluationSuite()

    p_list = []
    r_list = []
    mrr_list = []

    num_queries = min(num_queries, len(chunks))

    for i in range(num_queries):
        # Use a snippet from the chunk as the query to ensure relevance
        query = " ".join(chunks[i]["text"].split()[:10])
        relevant = [i]

        results = retriever.search(query, k)

        # Map retrieved docs to their original indices by matching text
        retrieved_ids = []
        for doc in results:
            try:
                idx = next(idx for idx, c in enumerate(chunks) if c["text"] == doc["page_content"])
            except StopIteration:
                idx = None
            if idx is not None:
                retrieved_ids.append(idx)

        p = evals.precision_at_k(retrieved_ids, relevant, k)
        r = evals.recall_at_k(retrieved_ids, relevant, k)
        m = evals.mrr(retrieved_ids, relevant)

        p_list.append(p)
        r_list.append(r)
        mrr_list.append(m)

        print(f"Query {i+1}: p@{k}={p:.3f}, r@{k}={r:.3f}, mrr={m:.3f}")

    print("\nAggregated:")
    print(f"Mean precision@{k}: {mean(p_list):.3f}")
    print(f"Mean recall@{k}: {mean(r_list):.3f}")
    print(f"Mean MRR: {mean(mrr_list):.3f}")


if __name__ == "__main__":
    evaluate(num_queries=5, k=5)

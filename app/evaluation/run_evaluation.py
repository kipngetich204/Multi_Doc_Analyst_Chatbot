"""Simple runner demonstrating EvaluationSuite usage."""
from app.evaluation.metrics import EvaluationSuite


def demo():
    # Example corpus retrieval IDs (ordered by relevance from a retriever)
    # For a query 'windy London' the retriever returned doc ids in this order
    retrieved = [1, 2, 0]

    # Ground-truth relevant document ids for the query
    relevant = [1]

    evals = EvaluationSuite()

    k = 1
    p_at_k = evals.precision_at_k(retrieved, relevant, k)
    r_at_k = evals.recall_at_k(retrieved, relevant, k)
    mrr = evals.mrr(retrieved, relevant)

    print(f"precision@{k}: {p_at_k:.3f}")
    print(f"recall@{k}: {r_at_k:.3f}")
    print(f"mrr: {mrr:.3f}")


if __name__ == "__main__":
    demo()

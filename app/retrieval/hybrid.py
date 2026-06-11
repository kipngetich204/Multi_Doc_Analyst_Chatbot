from collections import defaultdict

from app.retrieval.dense import DenseRetriever
from app.retrieval.sparse import BM25Retriever


class HybridRetriever:
    def __init__(self):
        self.dense = DenseRetriever()
        self.sparse = BM25Retriever()

    def build(self, chunks):
        self.dense.build(chunks)
        self.sparse.build(chunks)

    def reciprocal_rank_fusion(self, dense_results, sparse_results, k=60):
        scores = defaultdict(float)
        documents = {} 

        for rank, doc in enumerate(dense_results):  
            key = doc["page_content"]
            scores[key] += 1 / (rank + k)
            documents[key] = doc

        for rank, doc in enumerate(sparse_results):
            key = doc["page_content"]
            scores[key] += 1 / (rank + k)
            documents[key] = doc

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return [documents[text] for text, _ in ranked]

    def retrieve(self, query: str, k: int = 5):
        dense_results = self.dense.search(query, k)
        sparse_results = self.sparse.search(query, k)

        return self.reciprocal_rank_fusion(
            dense_results,
            sparse_results
        )[:k]
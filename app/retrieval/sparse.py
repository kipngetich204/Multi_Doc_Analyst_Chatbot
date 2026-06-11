import pickle
from rank_bm25 import BM25Okapi


class BM25Retriever:
    def __init__(self):
        self.index = None
        self.chunks = []

    def build(self, chunks):
        self.chunks = chunks

        tokenized = [c["text"].split() for c in chunks]
        self.index = BM25Okapi(tokenized)

        with open("data/indexes/bm25_index.pkl", "wb") as f:
            pickle.dump((self.index, self.chunks), f)

    def load(self):
        with open("data/indexes/bm25_index.pkl", "rb") as f:
            self.index, self.chunks = pickle.load(f)
    def search(self, query: str, k: int = 5):
        scores = self.index.get_scores(query.split())

        ranked = sorted(
            zip(self.chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )[:k]

        return [
            {
                "page_content": item[0]["text"],
                "metadata": item[0]["metadata"],
                "score": item[1]
            }
            for item in ranked
        ]

import chromadb
from sentence_transformers import SentenceTransformer


class DenseRetriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="data/indexes/chroma")
        self.collection = self.client.get_or_create_collection("documents")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def build(self, chunks):
        for idx, chunk in enumerate(chunks):
            embedding = self.model.encode(chunk["text"]).tolist()

            self.collection.add(
                ids=[str(idx)],
                documents=[chunk["text"]],
                embeddings=[embedding],
                metadatas=[chunk["metadata"]]
            )
    def search(self, query: str, k: int = 5):
        embedding = self.model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=k
        )

        docs = []
        for i in range(len(results["documents"][0])):
            docs.append({
                "page_content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "score": results["distances"][0][i]
            })

        return docs
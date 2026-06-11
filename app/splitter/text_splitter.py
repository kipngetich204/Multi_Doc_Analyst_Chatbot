from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.ingestion.pipeline import Pipeline


class RecursiveTextSplitter:

    def __init__(self, chunk_size=512, overlap=64):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap
        )

    def split(self, docs):
        return self.splitter.split_documents(docs)
    

docs= Pipeline.build_pipeline()


recursiveSplitter= RecursiveTextSplitter()


def chunks_gen():
    split_docs = recursiveSplitter.split(docs)

    chunks = []

    for chunk in split_docs:
        chunks.append({
            "text": chunk.page_content,
            "metadata": chunk.metadata
        })

    return chunks
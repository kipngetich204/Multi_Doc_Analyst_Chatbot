from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
# --- Independent Helper Functions ---

def load_webpage(url: str) -> list[Document]:
    """Loads a single web page into a list of Documents."""
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        if docs:
            print(f"Webpage Metadata: {docs[0].metadata}")
        return docs
    except Exception as e:
        print(f"Error loading webpage {url}: {e}")
        return []


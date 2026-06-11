from app.retrieval.hybrid import HybridRetriever
from sentence_transformers import SentenceTransformer
from app.splitter.text_splitter import chunks_gen
from app.generation.chain import generate_answer
from app.history.memory import ConversationMemory
from app.generation.citation import extract_citations
from app.evaluation.evaluate import evaluate as run_evaluate
import sys


_memory = ConversationMemory()


def search(query: str):
    hybrid_retriever = HybridRetriever()

    # vector = embedding_model.embed_documents([chunk.page_content for chunk in chunks])
    text = chunks_gen()
    hybrid_retriever.build(text)

    docs = hybrid_retriever.retrieve(query)
    citations = extract_citations(docs)

    tokens = []

    for token in generate_answer(query, docs, _memory):
        tokens.append(token)
        print(token, end="", flush=True)

    if citations:
        for cite in citations:
            print(f"📌 Source: {cite.get('source')}")

            pages = [p for p in cite.get('pages', []) if p is not None]

            if pages:
                page_str = ", ".join(str(p) for p in pages)
                print(f"   └── Pages: {page_str}")
            else:
                print(f"   └── Pages: N/A")
            print()

    _memory.add("User", query)
    _memory.add("Assistant", "".join(tokens))


if __name__ == "__main__":
    # Support `eval` command to run the evaluation harness
    if len(sys.argv) > 1 and sys.argv[1] == "eval":
        run_evaluate(num_queries=5, k=5)
        sys.exit(0)

    while True:
        question = str(input("Ask Questions relating to the document: "))
        if question.lower() == "exit":
            break
        if not question:
            continue

        print("ChatBot: ", end="")
        search(question)
        print()





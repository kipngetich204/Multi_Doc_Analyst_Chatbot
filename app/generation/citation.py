from collections import defaultdict


def extract_citations(retrieved_docs):
    grouped = defaultdict(list)

    for doc in retrieved_docs:
        source = doc["metadata"]["source"]
        grouped[source].append(doc["metadata"].get("page"))

    citations = []

    for source, pages in grouped.items():
        citations.append({
            "source": source,
            "pages": list(set(pages))
        })

    return citations
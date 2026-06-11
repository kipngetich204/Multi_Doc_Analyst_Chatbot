import json
import requests
from app.generation.prompts import SYSTEM_PROMPT
from app.history.memory import ConversationMemory

OLLAMA_URL = "http://127.0.0.1:11434"
MODEL = "qwen2.5:3b"


def _ollama_stream(prompt: str):
    """Low-level helper: POST a prompt to Ollama and yield response tokens."""
    response = requests.post(
        f"{OLLAMA_URL.rstrip('/')}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "max_tokens": 1024,
            "temperature": 0.0,
            "top_p": 0.95,
            "stream": True,
        },
        timeout=500,
    )
    response.raise_for_status()

    for line in response.iter_lines():
        if not line:
            continue
        payload = json.loads(line.decode("utf-8"))
        token = payload.get("response", "")
        if token:
            yield token


def _ollama_complete(prompt: str) -> str:
    """Blocking (non-streaming) call — collects all tokens and returns full text."""
    return "".join(_ollama_stream(prompt))


def _rewrite_query(query: str, memory_context: str) -> str:
    """
    Use the LLM to rewrite a follow-up question into a standalone question,
    given the conversation history.  Calls Ollama directly — NO recursion.
    """
    prompt = (
        f"Conversation History:\n{memory_context}\n\n"
        f"Current Question:\n{query}\n\n"
        "Rewrite the current question into a clear standalone question "
        "that makes sense without the conversation history.\n"
        "Return ONLY the rewritten question, nothing else."
    )
    return _ollama_complete(prompt).strip()


def _build_prompt(query: str, docs: list, memory_context: str) -> str:
    """Build the final RAG prompt from retrieved docs and conversation history."""
    context = "\n\n".join(
        f"Source: {d['metadata'].get('source', 'unknown')} "
        f"| Page: {d['metadata'].get('page', 1)}\n{d['page_content']}"
        for d in docs
    )

    history_section = (
        f"Conversation History:\n{memory_context}\n\n" if memory_context.strip() else ""
    )

    return (
        f"{SYSTEM_PROMPT.strip()}\n\n"
        f"{history_section}"
        f"Use the context below to answer the question with source citations.\n\n"
        f"{context}\n\n"
        f"Question: {query}\n\nAnswer:"
    )


def generate_answer(query: str, docs: list, memory: ConversationMemory):
    """
    Main entry point.  Accepts a query, retrieved docs, and the shared memory
    object.  Yields response tokens as they arrive from Ollama.

    Steps:
      1. If there is conversation history, rewrite the query into a standalone
         question so retrieval context stays coherent.
      2. Build the RAG prompt.
      3. Stream tokens from Ollama.
    """
    memory_context = memory.get_context()

    # Step 1: query rewriting (only when there is prior context)
    if memory_context.strip():
        standalone_query = _rewrite_query(query, memory_context)
    else:
        standalone_query = query

    # Step 2: build prompt
    prompt = _build_prompt(standalone_query, docs, memory_context)

    # Step 3: stream answer
    yield from _ollama_stream(prompt)
"""
Multi-Document Analyst & RAGBot — Streamlit UI
All backend functions are placeholders (marked with # TODO).
"""

import time
import streamlit as st
from pathlib import Path


# ─── Page config (must be first Streamlit call) ────────────────────────────
st.set_page_config(
    page_title="DocMind · RAGBot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─── Global CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Root palette ── */
:root {
    --bg:        #0d0f12;
    --surface:   #13161b;
    --surface2:  #1a1e26;
    --border:    #242830;
    --accent:    #4fffb0;
    --accent2:   #00b8ff;
    --danger:    #ff5757;
    --warn:      #ffb347;
    --text:      #e8eaf0;
    --muted:     #6b7280;
    --radius:    10px;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem; max-width: 100% !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container { padding: 1.2rem 1rem; }

/* ── Sidebar wordmark ── */
.wordmark {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.35rem;
    letter-spacing: -0.02em;
    color: var(--accent);
    margin-bottom: 0.15rem;
}
.wordmark span { color: var(--accent2); }
.tagline {
    font-size: 0.68rem;
    color: var(--muted);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* ── Section headers ── */
.sidebar-section {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.4rem 0 0.5rem;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid var(--border);
}

/* ── Status pill ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.68rem;
    font-family: 'DM Mono', monospace;
    padding: 2px 8px;
    border-radius: 99px;
    margin-bottom: 0.6rem;
}
.status-pill.ok   { background: #0d2e1e; color: var(--accent); border: 1px solid #1a4d32; }
.status-pill.busy { background: #1e2a10; color: #a8e060; border: 1px solid #2e4418; }
.status-pill.idle { background: #1e1e26; color: var(--muted); border: 1px solid var(--border); }
.dot { width: 6px; height: 6px; border-radius: 50%; display: inline-block; }
.dot.green  { background: var(--accent); box-shadow: 0 0 5px var(--accent); }
.dot.yellow { background: var(--warn); box-shadow: 0 0 5px var(--warn); }
.dot.gray   { background: var(--muted); }

/* ── Imported files list ── */
.file-scroll-container {
    max-height: 220px;
    overflow-y: auto;
    padding-right: 4px;
    margin-bottom: 0.5rem;
}
.file-scroll-container::-webkit-scrollbar { width: 3px; }
.file-scroll-container::-webkit-scrollbar-track { background: transparent; }
.file-scroll-container::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

.file-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 8px;
    border-radius: var(--radius);
    margin-bottom: 4px;
    font-size: 0.75rem;
    font-family: 'DM Mono', monospace;
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
    transition: border-color 0.2s;
}
.file-item:hover { border-color: #3a3f50; }
.file-item .fname { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.file-item .ftype {
    font-size: 0.6rem;
    padding: 1px 5px;
    border-radius: 4px;
    background: #0d1520;
    color: var(--accent2);
    border: 1px solid #1a2a3a;
    flex-shrink: 0;
}
.file-item .ftype.pdf  { color: #ff8c69; border-color: #3a1a10; background: #1e0e08; }
.file-item .ftype.csv  { color: #a8e060; border-color: #1e3010; background: #0e1808; }
.file-item .ftype.txt  { color: var(--muted); border-color: var(--border); background: var(--surface); }
.file-item .ftype.mp4  { color: #c49fff; border-color: #2a1a40; background: #160e24; }
.file-item .ftype.img  { color: #ffd479; border-color: #3a2a08; background: #1e1608; }

/* ── Pipeline progress bar ── */
.pipeline-stage {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 8px;
    border-radius: var(--radius);
    margin-bottom: 4px;
    background: var(--surface2);
    border: 1px solid var(--border);
    font-size: 0.73rem;
    font-family: 'DM Mono', monospace;
    color: var(--muted);
}
.pipeline-stage.active { border-color: var(--accent); color: var(--accent); background: #0d2218; }
.pipeline-stage.done   { border-color: #1a3a28; color: #5adf90; background: #0a1e14; }
.pipeline-stage.error  { border-color: #3a1010; color: var(--danger); background: #1e0808; }
.stage-icon { font-size: 0.85rem; flex-shrink: 0; }
.stage-label { flex: 1; }
.stage-count { font-size: 0.62rem; color: var(--muted); }

.mini-progress-bar {
    height: 2px;
    background: var(--border);
    border-radius: 2px;
    margin: 2px 0 6px;
    overflow: hidden;
}
.mini-progress-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.4s ease;
}
.mini-progress-fill.green { background: var(--accent); }
.mini-progress-fill.blue  { background: var(--accent2); }
.mini-progress-fill.warn  { background: var(--warn); }

/* ── Main area header ── */
.main-header {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.6rem;
    color: var(--text);
    letter-spacing: -0.03em;
    margin-bottom: 0.1rem;
}
.main-header span { color: var(--accent); }

/* ── Tab strip ── */
[data-testid="stTabs"] [role="tablist"] {
    gap: 4px;
    border-bottom: 1px solid var(--border) !important;
}
[data-testid="stTabs"] button {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.04em !important;
    color: var(--muted) !important;
    border-radius: var(--radius) var(--radius) 0 0 !important;
    padding: 6px 14px !important;
    border: 1px solid transparent !important;
    border-bottom: none !important;
    background: transparent !important;
    transition: all 0.15s !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--accent) !important;
    background: var(--surface2) !important;
    border-color: var(--border) !important;
}

/* ── Chat bubbles ── */
.chat-wrap { display: flex; flex-direction: column; gap: 12px; margin-top: 1rem; }
.bubble {
    max-width: 76%;
    padding: 12px 16px;
    border-radius: 12px;
    font-size: 0.875rem;
    line-height: 1.6;
    white-space: pre-wrap;
}
.bubble.user {
    align-self: flex-end;
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
    border-bottom-right-radius: 3px;
}
.bubble.bot {
    align-self: flex-start;
    background: #0d2218;
    border: 1px solid #1a4030;
    color: #d4f5e5;
    border-bottom-left-radius: 3px;
    font-family: 'DM Sans', sans-serif;
}
.bubble.bot .src-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    color: var(--accent);
    margin-top: 8px;
    padding-top: 6px;
    border-top: 1px solid #1a4030;
}

/* ── Metric cards ── */
.metric-row { display: flex; gap: 12px; margin: 0.8rem 0; flex-wrap: wrap; }
.metric-card {
    flex: 1;
    min-width: 120px;
    padding: 14px 16px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
}
.metric-card .mc-label { font-size: 0.62rem; font-family: 'DM Mono', monospace; color: var(--muted); letter-spacing: 0.08em; text-transform: uppercase; }
.metric-card .mc-val   { font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 700; color: var(--text); margin-top: 3px; }
.metric-card .mc-sub   { font-size: 0.68rem; color: var(--muted); margin-top: 2px; }

/* ── Chunk preview card ── */
.chunk-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 12px 14px;
    margin-bottom: 8px;
    font-size: 0.78rem;
    line-height: 1.6;
    color: var(--text);
    font-family: 'DM Mono', monospace;
    position: relative;
}
.chunk-card .chunk-meta {
    font-size: 0.62rem;
    color: var(--muted);
    margin-bottom: 6px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}
.chunk-card .chunk-score {
    position: absolute;
    top: 10px;
    right: 12px;
    font-size: 0.65rem;
    color: var(--accent);
    font-family: 'DM Mono', monospace;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(79,255,176,0.1) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #0d2e1e !important;
    color: var(--accent) !important;
    border: 1px solid #1a4d32 !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.04em !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: #123d25 !important;
    border-color: var(--accent) !important;
}

/* ── Select / slider ── */
.stSelectbox [data-baseweb="select"] > div,
.stSlider [data-testid="stThumbValue"] {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    color: var(--text) !important;
}

/* ── Scrollable result panel ── */
.result-scroll {
    max-height: 420px;
    overflow-y: auto;
    padding-right: 6px;
}
.result-scroll::-webkit-scrollbar { width: 3px; }
.result-scroll::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 0.8rem 0 !important; }
</style>
""", unsafe_allow_html=True)


# ─── Session state defaults ─────────────────────────────────────────────────
def _init_state():
    defaults = {
        "uploaded_files": [],          # list of {"name", "type", "size", "status"}
        "pipeline_stages": {
            "load":     {"label": "Document loading",  "icon": "📂", "status": "idle",   "progress": 0, "count": ""},
            "chunk":    {"label": "Chunking",          "icon": "✂️", "status": "idle",   "progress": 0, "count": ""},
            "embed":    {"label": "Embedding",         "icon": "🧬", "status": "idle",   "progress": 0, "count": ""},
            "index":    {"label": "Vector indexing",   "icon": "🗂️", "status": "idle",   "progress": 0, "count": ""},
        },
        "chat_history": [],            # list of {"role": "user"|"bot", "text", "sources"}
        "query_results": [],           # list of retrieved chunks
        "documents": [],               # loaded LangChain docs
        "chunks": [],                  # chunked docs
        "vectorstore": None,
        "analysis_results": {},
        "selected_model_llm": "gpt-4o",
        "selected_model_embed": "text-embedding-3-small",
        "chunk_size": 500,
        "chunk_overlap": 50,
        "top_k": 5,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


# ═══════════════════════════════════════════════════════════════════════════
# PLACEHOLDER BACKEND FUNCTIONS
# Replace each body with your real implementation.
# ═══════════════════════════════════════════════════════════════════════════

def load_documents(file_objects: list) -> list:
    """TODO: Use DocumentLoader.load_directory() or per-file loaders.
    Returns list[Document]."""
    time.sleep(0.5)
    return [{"page_content": f"Content of {f['name']}", "metadata": {"source": f["name"]}} for f in file_objects]


def chunk_documents(docs: list, chunk_size: int, overlap: int) -> list:
    """TODO: Apply RecursiveCharacterTextSplitter or similar.
    Returns list[Document] (chunks)."""
    time.sleep(0.3)
    return docs * 3  # placeholder: pretend each doc → 3 chunks


def embed_and_index(chunks: list, embed_model: str) -> object:
    """TODO: Run embedding model and build FAISS / Chroma / Pinecone index.
    Returns vectorstore object."""
    time.sleep(0.5)
    return {"type": "faiss", "size": len(chunks)}


def query_vectorstore(vectorstore, query: str, top_k: int) -> list:
    """TODO: vectorstore.similarity_search(query, k=top_k).
    Returns list of {page_content, metadata, score}."""
    time.sleep(0.2)
    return [
        {"page_content": f"[Placeholder chunk {i+1}] Retrieved for: '{query}'",
         "metadata": {"source": "sample.pdf", "page": i+1},
         "score": round(0.97 - i * 0.08, 2)}
        for i in range(top_k)
    ]


def generate_answer(query: str, context_chunks: list, llm_model: str) -> str:
    """TODO: Build prompt, call LLM (OpenAI / Anthropic / Ollama), return answer."""
    time.sleep(0.4)
    return f"[Placeholder answer for '{query}' using {llm_model}]\n\nBased on {len(context_chunks)} retrieved chunks, the answer would appear here."


def run_document_analysis(docs: list, analysis_type: str) -> dict:
    """TODO: Run summary / comparison / entity extraction / topic modelling.
    Returns dict with structured results."""
    time.sleep(0.6)
    return {
        "summary": f"[Placeholder {analysis_type} analysis across {len(docs)} documents]",
        "entities": ["Entity A", "Entity B", "Entity C"],
        "topics": ["Topic 1", "Topic 2"],
        "doc_comparison": {d["metadata"]["source"]: "Similar to others" for d in docs},
    }


def get_index_stats(vectorstore) -> dict:
    """TODO: Return vector count, dimension, index type from your store."""
    if not vectorstore:
        return {}
    return {"vectors": vectorstore.get("size", 0) * 10, "dim": 1536, "type": vectorstore.get("type", "N/A")}


# ═══════════════════════════════════════════════════════════════════════════
# PIPELINE RUNNER
# ═══════════════════════════════════════════════════════════════════════════

def run_pipeline(files):
    stages = st.session_state.pipeline_stages

    def set_stage(name, status, progress=0, count=""):
        stages[name]["status"]   = status
        stages[name]["progress"] = progress
        stages[name]["count"]    = count

    # ── Load
    set_stage("load", "active", 10)
    docs = load_documents(files)
    st.session_state.documents = docs
    set_stage("load", "done", 100, f"{len(docs)} docs")

    # ── Chunk
    set_stage("chunk", "active", 10)
    chunks = chunk_documents(docs, st.session_state.chunk_size, st.session_state.chunk_overlap)
    st.session_state.chunks = chunks
    set_stage("chunk", "done", 100, f"{len(chunks)} chunks")

    # ── Embed + index
    set_stage("embed", "active", 10)
    for i in range(1, 4):
        set_stage("embed", "active", int(i / 3 * 90))
        time.sleep(0.15)
    vs = embed_and_index(chunks, st.session_state.selected_model_embed)
    st.session_state.vectorstore = vs
    set_stage("embed", "done", 100, f"{len(chunks)} embedded")
    set_stage("index", "done", 100, f"{get_index_stats(vs).get('vectors', '?')} vectors")

    for f in st.session_state.uploaded_files:
        f["status"] = "indexed"

    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown('<div class="wordmark">Doc<span>Mind</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Multi-doc analyst · RAGBot</div>', unsafe_allow_html=True)

    # ── Model selection ───────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section">LLM Model</div>', unsafe_allow_html=True)
    llm_options = {
        "gpt-4o":            "OpenAI — GPT-4o",
        "gpt-4o-mini":       "OpenAI — GPT-4o mini",
        "claude-sonnet-4-6": "Anthropic — Claude Sonnet 4.6",
        "claude-haiku-4-5":  "Anthropic — Claude Haiku 4.5",
        "llama3:70b":        "Ollama — Llama 3 70B",
        "llama3:8b":         "Ollama — Llama 3 8B",
        "mistral":           "Ollama — Mistral 7B",
        "gemma2":            "Ollama — Gemma 2 9B",
    }
    st.session_state.selected_model_llm = st.selectbox(
        "LLM", list(llm_options.keys()),
        format_func=lambda k: llm_options[k], label_visibility="collapsed"
    )

    st.markdown('<div class="sidebar-section">Embedding Model</div>', unsafe_allow_html=True)
    embed_options = {
        "text-embedding-3-small": "OpenAI · 3-small",
        "text-embedding-3-large": "OpenAI · 3-large",
        "nomic-embed-text":       "Ollama · nomic-embed",
        "mxbai-embed-large":      "Ollama · mxbai-large",
    }
    st.session_state.selected_model_embed = st.selectbox(
        "Embed", list(embed_options.keys()),
        format_func=lambda k: embed_options[k], label_visibility="collapsed"
    )

    # ── Chunking params ───────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section">Chunking</div>', unsafe_allow_html=True)
    st.session_state.chunk_size    = st.slider("Chunk size",    100, 2000, st.session_state.chunk_size,    step=50)
    st.session_state.chunk_overlap = st.slider("Chunk overlap",  0,  400,  st.session_state.chunk_overlap, step=10)
    st.session_state.top_k         = st.slider("Top-K retrieval", 1, 20,   st.session_state.top_k)

    # ── File uploader ─────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section">Import documents</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Drop files", accept_multiple_files=True,
        type=["pdf", "txt", "csv", "mp4", "avi", "mov", "png", "jpg", "jpeg", "tiff"],
        label_visibility="collapsed"
    )
    if uploaded:
        existing_names = {f["name"] for f in st.session_state.uploaded_files}
        for uf in uploaded:
            if uf.name not in existing_names:
                ext = Path(uf.name).suffix.lstrip(".").lower()
                st.session_state.uploaded_files.append({
                    "name": uf.name, "type": ext,
                    "size": f"{uf.size / 1024:.1f} KB", "status": "pending"
                })

    # ── Scrollable file list ──────────────────────────────────────────────
    if st.session_state.uploaded_files:
        type_icons = {"pdf": "📄", "txt": "📝", "csv": "📊", "mp4": "🎬",
                      "avi": "🎬", "mov": "🎬", "png": "🖼", "jpg": "🖼",
                      "jpeg": "🖼", "tiff": "🖼"}
        items_html = ""
        for f in st.session_state.uploaded_files:
            icon = type_icons.get(f["type"], "📎")
            css_type = f["type"] if f["type"] in ["pdf", "csv", "txt"] else (
                "mp4" if f["type"] in ["mp4", "avi", "mov"] else "img"
            )
            badge = "✓ " if f["status"] == "indexed" else ""
            items_html += f"""
            <div class="file-item">
                <span>{icon}</span>
                <span class="fname">{badge}{f['name']}</span>
                <span class="ftype {css_type}">{f['type'].upper()}</span>
            </div>"""
        st.markdown(f'<div class="file-scroll-container">{items_html}</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⚡ Run pipeline", use_container_width=True):
                with st.spinner("Running..."):
                    run_pipeline(st.session_state.uploaded_files)
        with col2:
            if st.button("🗑 Clear all", use_container_width=True):
                for k in ["uploaded_files", "documents", "chunks", "vectorstore", "query_results", "chat_history", "analysis_results"]:
                    st.session_state[k] = [] if k != "vectorstore" else None
                    if k == "analysis_results": st.session_state[k] = {}
                for s in st.session_state.pipeline_stages.values():
                    s.update({"status": "idle", "progress": 0, "count": ""})
                st.rerun()

    # ── Pipeline progress ─────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section">Pipeline status</div>', unsafe_allow_html=True)
    color_map = {"done": "green", "active": "blue", "error": "warn", "idle": "gray"}
    for key, stage in st.session_state.pipeline_stages.items():
        status  = stage["status"]
        css_cls = "active" if status == "active" else ("done" if status == "done" else ("error" if status == "error" else ""))
        bar_color = color_map.get(status, "gray")
        count_html = f'<span class="stage-count">{stage["count"]}</span>' if stage["count"] else ""
        spinner = " ⟳" if status == "active" else ""
        st.markdown(f"""
        <div class="pipeline-stage {css_cls}">
            <span class="stage-icon">{stage['icon']}</span>
            <span class="stage-label">{stage['label']}{spinner}</span>
            {count_html}
        </div>
        <div class="mini-progress-bar">
            <div class="mini-progress-fill {bar_color}" style="width:{stage['progress']}%"></div>
        </div>""", unsafe_allow_html=True)

    # ── Status indicator ──────────────────────────────────────────────────
    vs = st.session_state.vectorstore
    all_done = all(s["status"] == "done" for s in st.session_state.pipeline_stages.values())
    if all_done and vs:
        st.markdown('<div class="status-pill ok"><span class="dot green"></span>Index ready</div>', unsafe_allow_html=True)
    elif any(s["status"] == "active" for s in st.session_state.pipeline_stages.values()):
        st.markdown('<div class="status-pill busy"><span class="dot yellow"></span>Processing…</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-pill idle"><span class="dot gray"></span>Awaiting files</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# MAIN AREA
# ═══════════════════════════════════════════════════════════════════════════

st.markdown('<div class="main-header">Doc<span>Mind</span> Workspace</div>', unsafe_allow_html=True)
st.markdown("---")

tab_chat, tab_analysis, tab_explorer, tab_settings = st.tabs(
    ["💬  RAGBot", "🔍  Analysis", "🗂  Doc Explorer", "⚙  Settings"]
)


# ─── TAB 1 · RAGBot ────────────────────────────────────────────────────────
with tab_chat:
    # Metric row
    vs = st.session_state.vectorstore
    stats = get_index_stats(vs) if vs else {}
    n_docs   = len(st.session_state.documents)
    n_chunks = len(st.session_state.chunks)
    n_vecs   = stats.get("vectors", 0)
    n_turns  = len(st.session_state.chat_history)

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="mc-label">Documents</div>
            <div class="mc-val">{n_docs}</div>
            <div class="mc-sub">loaded</div>
        </div>
        <div class="metric-card">
            <div class="mc-label">Chunks</div>
            <div class="mc-val">{n_chunks}</div>
            <div class="mc-sub">size {st.session_state.chunk_size}</div>
        </div>
        <div class="metric-card">
            <div class="mc-label">Vectors</div>
            <div class="mc-val">{n_vecs}</div>
            <div class="mc-sub">{stats.get('type','—')} · dim {stats.get('dim','—')}</div>
        </div>
        <div class="metric-card">
            <div class="mc-label">Turns</div>
            <div class="mc-val">{n_turns}</div>
            <div class="mc-sub">in session</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Chat history
    if st.session_state.chat_history:
        bubbles_html = '<div class="chat-wrap">'
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                bubbles_html += f'<div class="bubble user">{msg["text"]}</div>'
            else:
                sources_html = ""
                if msg.get("sources"):
                    srcs = " · ".join(set(s["metadata"].get("source", "?") for s in msg["sources"]))
                    sources_html = f'<div class="src-tag">📎 Sources: {srcs}</div>'
                bubbles_html += f'<div class="bubble bot">{msg["text"]}{sources_html}</div>'
        bubbles_html += "</div>"
        st.markdown(bubbles_html, unsafe_allow_html=True)
        st.markdown("---")

    # Query input
    col_q, col_btn = st.columns([5, 1])
    with col_q:
        query = st.text_input("Ask anything about your documents…",
                              placeholder="e.g. What are the key findings across all reports?",
                              label_visibility="collapsed", key="query_input")
    with col_btn:
        send = st.button("Ask →", use_container_width=True)

    if send and query.strip():
        if not st.session_state.vectorstore:
            st.warning("⚠ Run the pipeline first to build the index.")
        else:
            with st.spinner("Retrieving…"):
                chunks = query_vectorstore(st.session_state.vectorstore, query, st.session_state.top_k)
                st.session_state.query_results = chunks
            with st.spinner("Generating answer…"):
                answer = generate_answer(query, chunks, st.session_state.selected_model_llm)
            st.session_state.chat_history.append({"role": "user",  "text": query})
            st.session_state.chat_history.append({"role": "bot",   "text": answer, "sources": chunks})
            st.rerun()

    # Retrieved chunks expander
    if st.session_state.query_results:
        with st.expander(f"Retrieved chunks ({len(st.session_state.query_results)})"):
            st.markdown('<div class="result-scroll">', unsafe_allow_html=True)
            for i, c in enumerate(st.session_state.query_results):
                st.markdown(f"""
                <div class="chunk-card">
                    <div class="chunk-meta">
                        <span>#{i+1}</span>
                        <span>📎 {c['metadata'].get('source','?')}</span>
                        <span>p.{c['metadata'].get('page','?')}</span>
                    </div>
                    <span class="chunk-score">score {c.get('score','?')}</span>
                    {c['page_content']}
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


# ─── TAB 2 · Analysis ──────────────────────────────────────────────────────
with tab_analysis:
    if not st.session_state.documents:
        st.info("📂 Load and process documents first.")
    else:
        c1, c2 = st.columns([3, 1])
        with c1:
            analysis_type = st.selectbox("Analysis type", [
                "Summary", "Cross-document comparison",
                "Entity extraction", "Topic modelling", "Timeline extraction",
            ])
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            run_btn = st.button("Run analysis →", use_container_width=True)

        if run_btn:
            with st.spinner("Analysing…"):
                result = run_document_analysis(st.session_state.documents, analysis_type)
                st.session_state.analysis_results = result

        if st.session_state.analysis_results:
            r = st.session_state.analysis_results
            st.markdown("**Summary**")
            st.markdown(f'<div class="chunk-card">{r.get("summary","")}</div>', unsafe_allow_html=True)

            if r.get("entities"):
                st.markdown("**Entities**")
                st.markdown(" ".join(
                    f'<span style="background:#0d2218;border:1px solid #1a4030;color:#4fffb0;'
                    f'padding:2px 8px;border-radius:99px;font-size:0.75rem;font-family:DM Mono,monospace">{e}</span>'
                    for e in r["entities"]
                ), unsafe_allow_html=True)

            if r.get("topics"):
                st.markdown("**Topics**")
                cols = st.columns(len(r["topics"]))
                for i, t in enumerate(r["topics"]):
                    with cols[i]:
                        st.markdown(f'<div class="metric-card"><div class="mc-label">Topic {i+1}</div>'
                                    f'<div class="mc-val" style="font-size:1rem">{t}</div></div>',
                                    unsafe_allow_html=True)

            if r.get("doc_comparison"):
                st.markdown("**Per-document notes**")
                for src, note in r["doc_comparison"].items():
                    st.markdown(f'<div class="chunk-card"><div class="chunk-meta"><span>📎 {src}</span></div>{note}</div>',
                                unsafe_allow_html=True)


# ─── TAB 3 · Doc Explorer ──────────────────────────────────────────────────
with tab_explorer:
    if not st.session_state.documents:
        st.info("📂 Load and process documents to explore them here.")
    else:
        st.markdown(f"**{len(st.session_state.documents)} documents · {len(st.session_state.chunks)} chunks**")
        search_term = st.text_input("Search within chunks…", placeholder="keyword or phrase",
                                    label_visibility="collapsed")

        chunks_to_show = [
            c for c in st.session_state.chunks
            if not search_term or search_term.lower() in c["page_content"].lower()
        ]
        st.caption(f"{len(chunks_to_show)} chunk(s) shown")

        st.markdown('<div class="result-scroll">', unsafe_allow_html=True)
        for i, c in enumerate(chunks_to_show[:50]):   # cap for perf
            src = c["metadata"].get("source", "?")
            st.markdown(f"""
            <div class="chunk-card">
                <div class="chunk-meta"><span>#{i+1}</span><span>📎 {src}</span></div>
                {c['page_content'][:300]}{'…' if len(c['page_content']) > 300 else ''}
            </div>""", unsafe_allow_html=True)
        if len(chunks_to_show) > 50:
            st.caption(f"Showing first 50 of {len(chunks_to_show)}")
        st.markdown('</div>', unsafe_allow_html=True)


# ─── TAB 4 · Settings ──────────────────────────────────────────────────────
with tab_settings:
    st.markdown("#### Vector store")
    vs_type = st.selectbox("Backend", ["FAISS (local)", "Chroma (local)", "Pinecone (cloud)", "Weaviate (cloud)"])
    persist_path = st.text_input("Persist path", value="./vectorstore")

    st.markdown("#### Retrieval")
    retrieval_mode = st.selectbox("Mode", ["Similarity search", "MMR (diverse)", "Hybrid BM25 + dense"])
    score_threshold = st.slider("Score threshold", 0.0, 1.0, 0.5, step=0.05)

    st.markdown("#### LLM generation")
    temperature  = st.slider("Temperature",  0.0, 2.0, 0.3, step=0.05)
    max_tokens   = st.slider("Max tokens",   128, 4096, 1024, step=64)
    system_prompt = st.text_area("System prompt",
        value="You are an expert document analyst. Answer only from the provided context. "
              "Cite your sources by document name and page number.",
        height=100)

    st.markdown("#### API keys")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("OpenAI API key",    type="password", placeholder="sk-…")
        st.text_input("Pinecone API key",  type="password", placeholder="")
    with c2:
        st.text_input("Anthropic API key", type="password", placeholder="sk-ant-…")
        st.text_input("Weaviate API key",  type="password", placeholder="")

    if st.button("💾 Save settings"):
        st.success("Settings saved (placeholder — wire to your config store).")
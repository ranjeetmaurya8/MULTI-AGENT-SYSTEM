import time

import streamlit as st

from agents import build_search_reader_agent, build_search_agent, critic_chain, writer_chain

APP_NAME = "DeepLens AI"
APP_TAGLINE = "AI Research Intelligence"

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{APP_NAME} · {APP_TAGLINE}",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Styles ───────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #0b0f19;
    --surface: rgba(255,255,255,0.03);
    --border: rgba(255,255,255,0.08);
    --text: #e6e9f0;
    --muted: #a3abbd;
    --accent: #5b8cff;
    --accent-2: #7c5cff;
    --ok: #34d399;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--text); }

.stApp {
    background: var(--bg);
    background-image:
        radial-gradient(ellipse 70% 45% at 15% -10%, rgba(91,140,255,0.14) 0%, transparent 60%),
        radial-gradient(ellipse 55% 40% at 85% 110%, rgba(124,92,255,0.10) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 3rem 3rem; max-width: 1200px; }

/* Hero */
.hero { text-align: center; padding: 2.8rem 0 2rem; }
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem; letter-spacing: 0.25em; text-transform: uppercase;
    color: var(--accent); margin-bottom: 1rem;
}
.hero h1 {
    font-size: clamp(2.6rem, 6vw, 4.6rem); font-weight: 800;
    line-height: 1.05; letter-spacing: -0.035em; margin: 0 0 1rem; color: #fff;
}
.hero h1 span {
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
    -webkit-background-clip: text; background-clip: text; color: transparent;
}
.hero-sub { font-size: 1.02rem; font-weight: 300; color: var(--muted);
    max-width: 560px; margin: 0 auto; line-height: 1.7; }

.divider { height: 1px; margin: 1.5rem 0;
    background: linear-gradient(90deg, transparent, rgba(91,140,255,0.35), transparent); }

/* Inputs */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important; color: #fff !important;
    padding: 0.75rem 1rem !important; font-size: 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(91,140,255,0.18) !important;
}
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.72rem !important;
    letter-spacing: 0.15em !important; text-transform: uppercase !important;
    color: var(--accent) !important;
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
    border-radius: 10px !important; font-weight: 600 !important;
    transition: transform .15s, box-shadow .15s !important;
}
.stButton > button[kind="primary"], button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
    color: #fff !important; border: none !important;
    padding: 0.7rem 2rem !important;
    box-shadow: 0 4px 18px rgba(91,140,255,0.3) !important;
}
.stButton > button[kind="primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover {
    transform: translateY(-2px); box-shadow: 0 8px 26px rgba(91,140,255,0.42) !important;
}
.stButton > button[kind="secondary"], button[data-testid="stBaseButton-secondary"] {
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    color: var(--muted) !important; font-weight: 400 !important; font-size: 0.78rem !important;
}
.stButton > button[kind="secondary"]:hover,
button[data-testid="stBaseButton-secondary"]:hover {
    border-color: var(--accent) !important; color: #fff !important;
}

/* Pipeline cards */
.section-heading { font-size: 1.15rem; font-weight: 700; margin: 0 0 1rem; color: #fff; }
.step-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 1.1rem 1.4rem; margin-bottom: 0.9rem;
    position: relative; overflow: hidden; transition: all .3s;
}
.step-card::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0;
    width: 3px; background: rgba(255,255,255,0.06); }
.step-card.active { border-color: rgba(91,140,255,0.45); background: rgba(91,140,255,0.05); }
.step-card.active::before { background: var(--accent); }
.step-card.done { border-color: rgba(52,211,153,0.3); background: rgba(52,211,153,0.03); }
.step-card.done::before { background: var(--ok); }
.step-header { display: flex; align-items: center; gap: 0.8rem; }
.step-num { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
    color: var(--accent); opacity: 0.8; }
.step-title { font-size: 0.95rem; font-weight: 600; color: #fff; }
.step-status { margin-left: auto; font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem; letter-spacing: 0.1em; }
.status-waiting { color: #4b5367; }
.status-running { color: var(--accent); }
.status-done { color: var(--ok); }
.step-desc { font-size: 0.8rem; color: var(--muted); margin-top: 0.3rem; }

/* Result containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface); border-color: var(--border) !important; border-radius: 14px;
}
.panel-label { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
    letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 0.6rem; }
.panel-label.blue { color: var(--accent); }
.panel-label.green { color: var(--ok); }

/* Readable markdown content: colors only, formatting untouched */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] td,
[data-testid="stMarkdownContainer"] th,
[data-testid="stMarkdownContainer"] blockquote { color: #f1f4fa !important; }
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] strong { color: #ffffff !important; }
[data-testid="stMarkdownContainer"] a { color: #8fb3ff !important; }
[data-testid="stCaptionContainer"] p { color: #aab2c5 !important; }
[data-testid="stExpander"] summary p { color: #dfe4f0 !important; }
.step-desc { color: #a3abbd !important; }

details summary { font-size: 0.85rem !important; color: #dfe4f0 !important; }

.notice { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #4b5367;
    text-align: center; margin-top: 3rem; letter-spacing: 0.08em; }

@media (max-width: 768px) { .block-container { padding: 1rem 1rem 2rem; } }
</style>
""",
    unsafe_allow_html=True,
)

# ── Constants & helpers ──────────────────────────────────────────────────────
STEPS = [
    ("search", "01", "Search Agent", "Gathers recent web information"),
    ("reader", "02", "Reader Agent", "Scrapes & extracts deep content"),
    ("writer", "03", "Writer Chain", "Drafts the full research report"),
    ("critic", "04", "Critic Chain", "Reviews & scores the report"),
]
EXAMPLES = ["LLM agents 2026", "CRISPR gene editing", "Fusion energy progress"]
STATUS = {
    "waiting": ("WAITING", "status-waiting", ""),
    "running": ("● RUNNING", "status-running", "active"),
    "done": ("✓ DONE", "status-done", "done"),
}


def step_card(num: str, title: str, state: str, desc: str) -> str:
    label, status_cls, card_cls = STATUS[state]
    return (
        f'<div class="step-card {card_cls}"><div class="step-header">'
        f'<span class="step-num">{num}</span><span class="step-title">{title}</span>'
        f'<span class="step-status {status_cls}">{label}</span></div>'
        f'<div class="step-desc">{desc}</div></div>'
    )


def render_pipeline(slot, results: dict, active: str | None = None) -> None:
    html = "".join(
        step_card(
            num,
            title,
            "done" if key in results else "running" if key == active else "waiting",
            desc,
        )
        for key, num, title, desc in STEPS
    )
    slot.markdown(html, unsafe_allow_html=True)


def set_example(text: str) -> None:
    st.session_state.topic_input = text


# ── Session state ────────────────────────────────────────────────────────────
defaults = {"results": {}, "running": False, "error": None, "active_topic": ""}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent Research Intelligence</div>
    <h1>{APP_NAME}<span> Research</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, reading, writing
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""",
    unsafe_allow_html=True,
)

# ── Layout ───────────────────────────────────────────────────────────────────
col_input, _, col_pipeline = st.columns([5, 0.4, 4])

with col_input:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2026",
        key="topic_input",
        disabled=st.session_state.running,
    )
    run_btn = st.button(
        "Run Research Pipeline",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.running,
    )
    st.caption("Try an example:")
    chip_cols = st.columns(len(EXAMPLES))
    for col, ex in zip(chip_cols, EXAMPLES):
        col.button(
            ex,
            key=f"ex_{ex}",
            on_click=set_example,
            args=(ex,),
            use_container_width=True,
            disabled=st.session_state.running,
        )

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)
    pipeline_slot = st.empty()

render_pipeline(pipeline_slot, st.session_state.results)

# ── Start run ────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.error = None
        st.session_state.active_topic = topic.strip()
        st.session_state.running = True
        st.rerun()

# ── Execute pipeline ─────────────────────────────────────────────────────────
if st.session_state.running:
    topic_val = st.session_state.active_topic
    results: dict = {}

    def advance(key: str, label: str, fn):
        render_pipeline(pipeline_slot, results, active=key)
        with st.spinner(label):
            results[key] = fn()
        st.session_state.results = dict(results)

    try:
        def run_search():
            agent = build_search_agent()
            out = agent.invoke({"messages": [(
                "user", f"Find recent, reliable and detailed information about: {topic_val}"
            )]})
            return out["messages"][-1].content

        def run_reader():
            agent = build_search_reader_agent()
            out = agent.invoke({"messages": [(
                "user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}",
            )]})
            return out["messages"][-1].content

        def run_writer():
            combined = (
                f"SEARCH RESULTS:\n{results['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
            )
            return writer_chain.invoke({"topic": topic_val, "research": combined})

        def run_critic():
            return critic_chain.invoke({"report": results["writer"]})

        advance("search", "🔍  Search Agent is working…", run_search)
        advance("reader", "📄  Reader Agent is scraping top resources…", run_reader)
        advance("writer", "✍️  Writer is drafting the report…", run_writer)
        advance("critic", "🧐  Critic is reviewing the report…", run_critic)
    except Exception as exc:  # surface errors instead of a blank crash
        st.session_state.error = f"{type(exc).__name__}: {exc}"

    st.session_state.running = False
    st.rerun()

# ── Results ──────────────────────────────────────────────────────────────────
if st.session_state.error:
    st.error(f"Pipeline failed — {st.session_state.error}")

r = st.session_state.results
if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("🔍 Search results (raw)"):
            st.markdown(r["search"])
    if "reader" in r:
        with st.expander("📄 Scraped content (raw)"):
            st.markdown(r["reader"])

    if "writer" in r:
        with st.container(border=True):
            st.markdown('<div class="panel-label blue">📝 Final Research Report</div>',
                        unsafe_allow_html=True)
            st.markdown(r["writer"])
        st.download_button(
            "⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"{APP_NAME.lower()}_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        with st.container(border=True):
            st.markdown('<div class="panel-label green">🧐 Critic Feedback</div>',
                        unsafe_allow_html=True)
            st.markdown(r["critic"])

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    f'<div class="notice">{APP_NAME} · Powered by a LangChain multi-agent pipeline · Built with Streamlit</div>',
    unsafe_allow_html=True,
)
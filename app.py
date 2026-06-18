import streamlit as st
from pipeline import run_research_pipeline
from datetime import datetime

st.set_page_config(
    page_title="Research Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Sora:wght@300;400;600;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #1A1612 !important;
    color: #E8E0D5 !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] { display: none; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stHeader"] { background: transparent !important; }
footer { display: none !important; }

/* ── Main wrapper ── */
.block-container {
    max-width: 900px !important;
    padding: 0 2rem !important;
    margin: 0 auto !important;
}

/* ── Header ── */
.rs-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2.5rem 0 3rem 0;
    border-bottom: 1px solid #2D2720;
    margin-bottom: 3.5rem;
}
.rs-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.rs-logo-mark {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #CC785C 0%, #E8956D 100%);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    font-weight: 700;
    color: #1A1612;
    letter-spacing: -0.5px;
    font-family: 'Sora', sans-serif;
}
.rs-logo-text {
    font-family: 'Sora', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #E8E0D5;
    letter-spacing: -0.01em;
}
.rs-logo-sub {
    font-size: 0.7rem;
    color: #7A6E65;
    font-weight: 400;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 1px;
}

/* ── Hero Section ── */
.rs-hero {
    margin-bottom: 3rem;
}
.rs-hero-eyebrow {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #CC785C;
    margin-bottom: 1rem;
}
.rs-hero-title {
    font-family: 'Sora', sans-serif;
    font-size: 2.8rem;
    font-weight: 300;
    line-height: 1.15;
    color: #E8E0D5;
    letter-spacing: -0.03em;
    margin-bottom: 1rem;
}
.rs-hero-title strong {
    font-weight: 700;
    color: #F5EDE4;
}
.rs-hero-desc {
    font-size: 0.95rem;
    color: #7A6E65;
    line-height: 1.7;
    max-width: 520px;
}

/* ── Input Area ── */
.rs-input-wrap {
    background: #221E1A;
    border: 1px solid #2D2720;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.rs-input-wrap:hover { border-color: #3D342C; }
.rs-input-label {
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #7A6E65;
    margin-bottom: 0.75rem;
}

.stTextInput > div > div > input {
    background: #2A2420 !important;
    border: 1px solid #3D342C !important;
    border-radius: 8px !important;
    color: #E8E0D5 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    caret-color: #CC785C !important;
}
.stTextInput > div > div > input:focus {
    border-color: #CC785C !important;
    box-shadow: 0 0 0 3px rgba(204, 120, 92, 0.12) !important;
}
.stTextInput > div > div > input::placeholder { color: #4D4540 !important; }
.stTextInput label { display: none !important; }

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #CC785C 0%, #B5633F 100%) !important;
    color: #FFF8F5 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    padding: 0.75rem 1.5rem !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #D98A6E 0%, #CC785C 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(204, 120, 92, 0.3) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Pipeline Steps ── */
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: #2D2720;
    border-radius: 12px;
    overflow: hidden;
    margin: 2rem 0;
}
.pipeline-step {
    background: #1E1A16;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}
.pipeline-step-number {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    color: #4D4540;
    text-transform: uppercase;
}
.pipeline-step-name {
    font-size: 0.8rem;
    font-weight: 500;
    color: #A09080;
}
.pipeline-step.active .pipeline-step-number { color: #CC785C; }
.pipeline-step.active .pipeline-step-name { color: #E8E0D5; }
.pipeline-step.done .pipeline-step-number { color: #6B9B5E; }
.pipeline-step.done .pipeline-step-name { color: #9DC48F; }
.step-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #2D2720;
    margin-top: 0.25rem;
}
.pipeline-step.active .step-dot { background: #CC785C; }
.pipeline-step.done .step-dot { background: #6B9B5E; }

/* ── Results ── */
.rs-result-section {
    margin-bottom: 1.5rem;
}
.rs-section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    background: #221E1A;
    border: 1px solid #2D2720;
    border-radius: 10px 10px 0 0;
    cursor: pointer;
}
.rs-section-icon {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
}
.icon-orange { background: rgba(204,120,92,0.15); }
.icon-blue { background: rgba(92,140,204,0.15); }
.icon-green { background: rgba(107,155,94,0.15); }
.icon-purple { background: rgba(160,92,204,0.15); }

.rs-section-title {
    font-size: 0.82rem;
    font-weight: 600;
    color: #C4B8AE;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    flex: 1;
}
.rs-section-body {
    background: #1E1A16;
    border: 1px solid #2D2720;
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 1.5rem;
    font-size: 0.9rem;
    line-height: 1.75;
    color: #C4B8AE;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #2D2720 !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #7A6E65 !important;
    border: none !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.75rem 1.25rem !important;
    letter-spacing: 0.04em !important;
    border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
    color: #E8E0D5 !important;
    border-bottom: 2px solid #CC785C !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 2rem 0 0 0 !important;
}

/* ── Download Button ── */
.stDownloadButton > button {
    background: transparent !important;
    color: #CC785C !important;
    border: 1px solid #3D342C !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    border-color: #CC785C !important;
    background: rgba(204,120,92,0.08) !important;
}

/* ── Alert / Success ── */
.stAlert {
    background: rgba(107,155,94,0.1) !important;
    border: 1px solid rgba(107,155,94,0.3) !important;
    border-radius: 8px !important;
    color: #9DC48F !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #CC785C !important; }

/* ── Divider ── */
hr { border-color: #2D2720 !important; }

/* ── Checkbox ── */
.stCheckbox label span { color: #7A6E65 !important; font-size: 0.85rem !important; }

/* ── Footer ── */
.rs-footer {
    margin-top: 5rem;
    padding: 2rem 0;
    border-top: 1px solid #2D2720;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.rs-footer-left { font-size: 0.75rem; color: #4D4540; }
.rs-footer-right {
    font-size: 0.7rem;
    color: #3D342C;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── Status badge inline ── */
.badge-running {
    display: inline-block;
    background: rgba(204,120,92,0.15);
    color: #CC785C;
    border: 1px solid rgba(204,120,92,0.3);
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.badge-done {
    display: inline-block;
    background: rgba(107,155,94,0.15);
    color: #9DC48F;
    border: 1px solid rgba(107,155,94,0.3);
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── Error ── */
.stException, [data-testid="stException"] {
    background: rgba(180,60,60,0.1) !important;
    border: 1px solid rgba(180,60,60,0.3) !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="rs-header">
    <div class="rs-logo">
        <div class="rs-logo-mark">R</div>
        <div>
            <div class="rs-logo-text">Research Intelligence</div>
            <div class="rs-logo-sub">Multi-Agent System</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="rs-hero">
    <div class="rs-hero-eyebrow">◆ Four agents. One report.</div>
    <h1 class="rs-hero-title">Research anything.<br><strong>Deeply.</strong></h1>
    <p class="rs-hero-desc">
        Enter a topic and four specialized agents get to work — searching the web,
        reading source material, drafting a report, and reviewing it for accuracy.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────
if "research_state" not in st.session_state:
    st.session_state.research_state = None
if "topic" not in st.session_state:
    st.session_state.topic = ""

# ── Input ─────────────────────────────────────────────────────────────────
st.markdown('<div class="rs-input-label">Research Topic</div>', unsafe_allow_html=True)

col_input, col_btn = st.columns([4, 1])
with col_input:
    research_topic = st.text_input(
        "topic",
        placeholder="e.g.  Quantum computing breakthroughs in 2025",
        label_visibility="collapsed"
    )
with col_btn:
    run_button = st.button("Run Research ◆", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Pipeline ──────────────────────────────────────────────────────────────
STEPS = [
    ("01", "Search Agent",  "Finds recent, reliable sources"),
    ("02", "Reader Agent",  "Scrapes & extracts page content"),
    ("03", "Writer Agent",  "Drafts the research report"),
    ("04", "Critic Agent",  "Reviews for gaps & accuracy"),
]

def render_pipeline(active_idx=None, done_set=None):
    done_set = done_set or set()
    cols = st.columns(4)
    for i, (num, name, desc) in enumerate(STEPS):
        state_cls = "done" if i in done_set else ("active" if i == active_idx else "")
        indicator = "✓" if i in done_set else ("●" if i == active_idx else "○")
        with cols[i]:
            st.markdown(f"""
            <div style="padding:1.2rem 1rem; background:#1E1A16;
                        border:1px solid {'#6B9B5E' if i in done_set else ('#CC785C' if i==active_idx else '#2D2720')};
                        border-radius:10px; transition:all 0.3s;">
                <div style="font-size:0.62rem;font-weight:600;letter-spacing:0.12em;
                            color:{'#6B9B5E' if i in done_set else ('#CC785C' if i==active_idx else '#4D4540')};
                            text-transform:uppercase;margin-bottom:0.4rem;">
                    {num} &nbsp; {indicator}
                </div>
                <div style="font-size:0.82rem;font-weight:600;
                            color:{'#9DC48F' if i in done_set else ('#E8E0D5' if i==active_idx else '#7A6E65')};
                            margin-bottom:0.25rem;">{name}</div>
                <div style="font-size:0.72rem;color:#4D4540;line-height:1.4;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Run ───────────────────────────────────────────────────────────────────
if run_button and research_topic:
    st.session_state.research_state = None

    st.markdown("<br>", unsafe_allow_html=True)
    pipeline_placeholder = st.empty()
    status_placeholder = st.empty()
    result_placeholder = st.empty()

    try:
        for step_idx in range(4):
            with pipeline_placeholder.container():
                render_pipeline(active_idx=step_idx, done_set=set(range(step_idx)))
            with status_placeholder.container():
                st.markdown(
                    f'<div style="margin-top:1rem;font-size:0.8rem;color:#7A6E65;">'
                    f'Running <span class="badge-running">{STEPS[step_idx][1]}</span> &nbsp;—&nbsp; {STEPS[step_idx][2]}</div>',
                    unsafe_allow_html=True
                )

        with st.spinner(""):
            research_state = run_research_pipeline(research_topic)

        # All done
        with pipeline_placeholder.container():
            render_pipeline(done_set={0, 1, 2, 3})
        with status_placeholder.container():
            st.markdown(
                '<div style="margin-top:1rem;font-size:0.8rem;color:#9DC48F;">'
                '✓ &nbsp;<span class="badge-done">Complete</span>&nbsp; All agents finished successfully.</div>',
                unsafe_allow_html=True
            )

        st.session_state.research_state = research_state
        st.session_state.topic = research_topic

    except Exception as e:
        pipeline_placeholder.empty()
        status_placeholder.empty()
        st.error(f"Pipeline error: {str(e)}")

elif not run_button:
    # Show idle pipeline
    render_pipeline()

# ── Results ───────────────────────────────────────────────────────────────
if st.session_state.research_state:
    state = st.session_state.research_state
    topic = st.session_state.topic

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
        <div style="font-size:0.7rem;color:#CC785C;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.4rem;">Research Output</div>
        <div style="font-family:'Sora',sans-serif;font-size:1.5rem;font-weight:600;color:#E8E0D5;letter-spacing:-0.02em;">{topic}</div>
        <div style="font-size:0.75rem;color:#4D4540;margin-top:0.3rem;">{datetime.now().strftime('%B %d, %Y · %H:%M')}</div>
    </div>
    """, unsafe_allow_html=True)

    def to_str(val):
        """Safely convert any pipeline value (str, list, object) to a plain string."""
        if val is None:
            return ""
        if isinstance(val, list):
            return "\n\n".join(
                item.content if hasattr(item, "content") else str(item)
                for item in val
            )
        if hasattr(val, "content"):
            return val.content
        return str(val)

    def clean_report(text):
        """Remove boilerplate metadata lines the writer agent adds."""
        import re
        # Remove lines like: Prepared by: ..., Date: ..., Institution/Organization: ...
        text = re.sub(r'(?im)^\s*\*{0,2}(prepared\s+by|date|institution[\s/]*organization)\*{0,2}\s*:.*$', '', text)
        # Collapse 3+ consecutive blank lines down to 2
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def render_report(content):
        text = clean_report(to_str(content))
        if not text:
            st.markdown('<div style="color:#4D4540;font-size:0.85rem;font-style:italic;">No report generated.</div>', unsafe_allow_html=True)
            return
        st.markdown(f"""
        <div style="background:#1E1A16;border:1px solid #2D2720;border-radius:10px;
                    padding:1.75rem;font-size:0.9rem;line-height:1.8;color:#C4B8AE;
                    white-space:pre-wrap;word-break:break-word;max-height:620px;overflow-y:auto;">
{text}
        </div>
        """, unsafe_allow_html=True)

    render_report(state.get("report", ""))

    # Export row
    st.markdown("<br>", unsafe_allow_html=True)
    col_dl, col_new, col_blank = st.columns([1.5, 1.5, 4])

    full_export = (
        "RESEARCH INTELLIGENCE — EXPORT\n"
        "================================\n"
        f"Topic    : {topic}\n"
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        "FINAL REPORT\n"
        "------------\n"
        + to_str(state.get('report', ''))
    )
    with col_dl:
        st.download_button(
            label="↓  Download report",
            data=full_export,
            file_name=f"research_{topic.replace(' ', '_')[:40]}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col_new:
        if st.button("↺  New research", use_container_width=True):
            st.session_state.research_state = None
            st.session_state.topic = ""
            st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div class="rs-footer">
    <div class="rs-footer-left">Research Intelligence · Multi-Agent System · LangChain + Streamlit</div>
    <div class="rs-footer-right">◆ Powered by Mistral AI</div>
</div>
""", unsafe_allow_html=True)

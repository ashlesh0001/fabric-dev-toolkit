import json
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from services.ai import call_ai

load_dotenv()

# ── Helpers ───────────────────────────────────────────────────────────────────
def load_prompt(name: str) -> dict:
    path = Path(__file__).parent / "prompts" / f"{name}.json"
    with open(path) as f:
        return json.load(f)

def strip_fences(text: str) -> str:
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fabric Dev Toolkit · FABCON 2026",
    page_icon="🔧",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f1117; }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1a1d27;
        padding: 8px 12px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #252836;
        border-radius: 8px;
        color: #a0aec0;
        padding: 8px 20px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0066ff !important;
        color: white !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0066ff, #0044bb);
        border: none;
        border-radius: 8px;
        padding: 10px 28px;
        font-weight: 600;
        letter-spacing: 0.3px;
        transition: opacity 0.2s;
    }
    .stButton > button[kind="primary"]:hover { opacity: 0.85; }

    .stTextArea textarea {
        background-color: #1a1d27;
        border: 1px solid #2d3148;
        border-radius: 8px;
        color: #e2e8f0;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 13px;
    }

    h1, h2, h3 { color: #e2e8f0 !important; }

    [data-testid="stSidebar"] {
        background-color: #13151f;
        border-right: 1px solid #1e2130;
    }

    .profile-card {
        background: linear-gradient(135deg, #1a1d27, #252836);
        border: 1px solid #2d3148;
        border-radius: 12px;
        padding: 16px;
        margin-top: 12px;
        text-align: center;
    }
    .profile-name { font-size: 15px; font-weight: 700; color: #e2e8f0; margin-bottom: 2px; }
    .profile-title { font-size: 12px; color: #718096; margin-bottom: 10px; }
    .linkedin-btn {
        display: inline-block;
        background: #0077b5;
        color: white !important;
        text-decoration: none !important;
        padding: 6px 16px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
    }
    .linkedin-btn:hover { background: #005f8e; }

    .hero {
        background: linear-gradient(135deg, #0d1b4b 0%, #0f1117 60%);
        border: 1px solid #1e3a8a;
        border-radius: 14px;
        padding: 28px 32px;
        margin-bottom: 24px;
    }
    .hero h1 { font-size: 26px; font-weight: 800; color: #e2e8f0 !important; margin: 0 0 6px 0; }
    .hero p { color: #718096; margin: 0; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔧 Fabric Dev Toolkit")
    st.markdown(
        "<span style='color:#718096;font-size:13px'>"
        "A free AI-powered toolkit for **MS Fabric** and **MS SQL** developers. "
        "Built for the FABCON 2026 community.</span>",
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown(
        """
        **Tools included:**
        - 🔍 Pipeline Failure Analyzer
        - 🩺 SQL Query Health Checker
        - ⚡ T-SQL → Spark Translator
        - 🏗 Architecture Advisor
        - 🗂 Lakehouse Explorer
        """,
    )
    st.divider()
    st.markdown(
        """
        <div class="profile-card">
            <div class="profile-name">Ashlesh Patel</div>
            <div class="profile-title">AI Enabler</div>
            <a href="https://www.linkedin.com/in/ashleshpatel/" target="_blank" class="linkedin-btn">
                🔗 Connect on LinkedIn
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.caption("Powered by Google Gemini · FABCON 2026")

# ── Hero banner ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🔧 Fabric Dev Toolkit</h1>
    <p>AI-powered tools for MS Fabric & MS SQL developers · Diagnose pipeline failures · Optimize queries · Translate T-SQL to Spark · Design Fabric architectures · Explore Lakehouse metadata</p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Pipeline Analyzer",
    "🩺 SQL Health Checker",
    "⚡ T-SQL → Spark",
    "🏗 Architecture Advisor",
    "🗂 Lakehouse Explorer",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — Pipeline Failure Analyzer
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    p = load_prompt("pipeline_analyzer")
    st.markdown("#### Paste an MS Fabric Data Factory or Spark pipeline error log and get an instant AI diagnosis.")

    with st.expander("📋 Load example log"):
        for ex in p["examples"]:
            if st.button(ex["label"], key=f"pipe_ex_{ex['label']}"):
                st.session_state["pipeline_text"] = ex["content"]

    log_input = st.text_area(
        "Error log / pipeline failure message",
        height=220,
        placeholder="Paste your pipeline error log here…",
        key="pipeline_text",
    )

    if st.button("🔍 Analyze Failure", type="primary", key="pipeline_analyze"):
        if not log_input.strip():
            st.warning("Please paste an error log before analyzing.")
        else:
            with st.spinner("Analyzing your pipeline failure…"):
                try:
                    result = call_ai(p["system_prompt"], log_input.strip())
                    sections = {"Root Cause": "", "Plain English Explanation": "", "Step-by-Step Fix": ""}
                    current = None
                    for line in result.splitlines():
                        s = line.strip()
                        if s.startswith("## Root Cause"):
                            current = "Root Cause"
                        elif s.startswith("## Plain English Explanation"):
                            current = "Plain English Explanation"
                        elif s.startswith("## Step-by-Step Fix"):
                            current = "Step-by-Step Fix"
                        elif current:
                            sections[current] += line + "\n"

                    st.divider()
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.error("**🔴 Root Cause**\n\n" + sections["Root Cause"].strip())
                    with col2:
                        st.info("**💡 Plain English Explanation**\n\n" + sections["Plain English Explanation"].strip())
                    st.markdown("### 🛠 Step-by-Step Fix")
                    st.markdown(sections["Step-by-Step Fix"].strip())
                except Exception as e:
                    st.error(f"Error: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — SQL Query Health Checker
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    p = load_prompt("sql_health_checker")
    st.markdown("#### Paste a MS SQL or Fabric SQL query to detect anti-patterns, performance issues, and get an optimised rewrite.")

    with st.expander("📋 Load example query"):
        for ex in p["examples"]:
            if st.button(ex["label"], key=f"sql_ex_{ex['label']}"):
                st.session_state["sql_text"] = ex["content"]

    sql_input = st.text_area(
        "SQL query",
        height=220,
        placeholder="Paste your SQL query here…",
        key="sql_text",
    )

    if st.button("🩺 Check Query Health", type="primary", key="sql_analyze"):
        if not sql_input.strip():
            st.warning("Please paste a SQL query before analyzing.")
        else:
            with st.spinner("Analyzing your query…"):
                try:
                    result = call_ai(p["system_prompt"], sql_input.strip())
                    sections = {"Issues Found": "", "Optimised Query": "", "Changes Explained": ""}
                    current = None
                    for line in result.splitlines():
                        s = line.strip()
                        if s.startswith("## Issues Found"):
                            current = "Issues Found"
                        elif s.startswith("## Optimised Query"):
                            current = "Optimised Query"
                        elif s.startswith("## Changes Explained"):
                            current = "Changes Explained"
                        elif current:
                            sections[current] += line + "\n"

                    st.divider()
                    st.markdown("### 🚨 Issues Found")
                    for line in sections["Issues Found"].strip().splitlines():
                        line = line.strip()
                        if not line:
                            continue
                        if "[HIGH]" in line:
                            st.error(line.replace("**[HIGH]**", "🔴 HIGH"))
                        elif "[MEDIUM]" in line:
                            st.warning(line.replace("**[MEDIUM]**", "🟡 MEDIUM"))
                        elif "[LOW]" in line:
                            st.info(line.replace("**[LOW]**", "🔵 LOW"))
                        else:
                            st.markdown(line)

                    st.markdown("### ✅ Optimised Query")
                    st.code(strip_fences(sections["Optimised Query"]), language="sql")
                    st.markdown("### 📝 Changes Explained")
                    st.markdown(sections["Changes Explained"].strip())
                except Exception as e:
                    st.error(f"Error: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — T-SQL to Fabric Spark Translator
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    p = load_prompt("tsql_spark")
    st.markdown("#### Paste a T-SQL query or stored procedure and get a production-ready PySpark + Spark SQL translation for MS Fabric Notebooks.")

    with st.expander("📋 Load example T-SQL"):
        for ex in p["examples"]:
            if st.button(ex["label"], key=f"tsql_ex_{ex['label']}"):
                st.session_state["tsql_text"] = ex["content"]

    tsql_input = st.text_area(
        "T-SQL query or stored procedure",
        height=220,
        placeholder="Paste your T-SQL here…",
        key="tsql_text",
    )

    if st.button("⚡ Translate to Spark", type="primary", key="tsql_analyze"):
        if not tsql_input.strip():
            st.warning("Please paste a T-SQL query before translating.")
        else:
            with st.spinner("Translating your T-SQL to Spark…"):
                try:
                    result = call_ai(p["system_prompt"], tsql_input.strip())
                    sections = {"PySpark Version": "", "Spark SQL Version": "", "Migration Notes": ""}
                    current = None
                    for line in result.splitlines():
                        s = line.strip()
                        if s.startswith("## PySpark Version"):
                            current = "PySpark Version"
                        elif s.startswith("## Spark SQL Version"):
                            current = "Spark SQL Version"
                        elif s.startswith("## Migration Notes"):
                            current = "Migration Notes"
                        elif current:
                            sections[current] += line + "\n"

                    st.divider()
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### 🐍 PySpark Version")
                        st.code(strip_fences(sections["PySpark Version"]), language="python")
                    with col2:
                        st.markdown("### 🗄 Spark SQL Version")
                        st.code(strip_fences(sections["Spark SQL Version"]), language="sql")
                    st.markdown("### 📋 Migration Notes")
                    st.markdown(sections["Migration Notes"].strip())
                except Exception as e:
                    st.error(f"Error: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — MS Fabric Architecture Advisor
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    p = load_prompt("architecture_advisor")
    st.markdown("#### Describe your data scenario in plain English and get a tailored MS Fabric architecture recommendation.")

    with st.expander("📋 Load example scenario"):
        for ex in p["examples"]:
            if st.button(ex["label"], key=f"arch_ex_{ex['label']}"):
                st.session_state["arch_text"] = ex["content"]

    arch_input = st.text_area(
        "Describe your data scenario",
        height=180,
        placeholder="e.g. I have 10TB of IoT sensor data coming in real-time and need Power BI dashboards refreshed every 5 minutes…",
        key="arch_text",
    )

    if st.button("🏗 Get Architecture Recommendation", type="primary", key="arch_analyze"):
        if not arch_input.strip():
            st.warning("Please describe your scenario before getting a recommendation.")
        else:
            with st.spinner("Designing your Fabric architecture…"):
                try:
                    result = call_ai(p["system_prompt"], arch_input.strip())
                    sections = {
                        "Recommended Components": "",
                        "Architecture Flow": "",
                        "Key Decisions & Trade-offs": "",
                        "Getting Started Checklist": "",
                    }
                    current = None
                    for line in result.splitlines():
                        s = line.strip()
                        if s.startswith("## Recommended Components"):
                            current = "Recommended Components"
                        elif s.startswith("## Architecture Flow"):
                            current = "Architecture Flow"
                        elif s.startswith("## Key Decisions"):
                            current = "Key Decisions & Trade-offs"
                        elif s.startswith("## Getting Started"):
                            current = "Getting Started Checklist"
                        elif current:
                            sections[current] += line + "\n"

                    st.divider()
                    st.markdown("### 🧩 Recommended Components")
                    st.markdown(sections["Recommended Components"].strip())
                    st.markdown("### 🔀 Architecture Flow")
                    st.code(sections["Architecture Flow"].strip(), language=None)
                    st.markdown("### ⚖️ Key Decisions & Trade-offs")
                    st.markdown(sections["Key Decisions & Trade-offs"].strip())
                    st.markdown("### ✅ Getting Started Checklist")
                    st.markdown(sections["Getting Started Checklist"].strip())
                except Exception as e:
                    st.error(f"Error: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — Fabric Lakehouse Explorer (RAG)
# ─────────────────────────────────────────────────────────────────────────────
with tab5:
    # Lazy import — RAG dependencies are heavy; only load when this tab is used
    try:
        from services.rag import index_documents, retrieve_context, build_rag_prompt
        rag_available = True
    except ImportError as e:
        rag_available = False
        st.error(f"RAG dependencies not installed: {e}")

    p = load_prompt("lakehouse_explorer")

    if not rag_available:
        st.stop()

    # ── Init session state ────────────────────────────────────────────────────
    if "vectorstore" not in st.session_state:
        st.session_state["vectorstore"] = None
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "indexed" not in st.session_state:
        st.session_state["indexed"] = False

    st.markdown("#### Upload your Lakehouse metadata and chat with it using natural language.")
    st.info(
        "💡 On first use, the embedding model (~90 MB) downloads automatically. "
        "This takes ~30 seconds on Streamlit Cloud — subsequent loads are instant."
    )

    # ── Section 1: Upload & Index ─────────────────────────────────────────────
    st.markdown("### 📤 Upload & Index Metadata")

    with st.expander("📄 Expected file format (click to see example)"):
        st.code(p["sample_metadata"], language="csv")

    uploaded_file = st.file_uploader(
        "Upload your Lakehouse metadata (.txt or .csv)",
        type=["txt", "csv"],
        key="metadata_file",
    )

    col_index, col_sample, col_clear = st.columns([2, 2, 1])
    with col_index:
        index_btn = st.button("📥 Index my Lakehouse metadata", type="primary", key="index_btn")
    with col_sample:
        sample_btn = st.button("🧪 Load sample data", key="sample_btn")
    with col_clear:
        if st.button("🗑 Clear", key="clear_index"):
            st.session_state["vectorstore"] = None
            st.session_state["chat_history"] = []
            st.session_state["indexed"] = False
            st.rerun()

    if sample_btn:
        sample_path = Path(__file__).parent / "demo_data" / "lakehouse_metadata.csv"
        content = sample_path.read_text(encoding="utf-8")
        with st.spinner("Indexing sample Lakehouse metadata…"):
            try:
                vectorstore, chunk_count = index_documents(content)
                st.session_state["vectorstore"] = vectorstore
                st.session_state["indexed"] = True
                st.session_state["chat_history"] = []
                st.success(f"✅ Sample data indexed — {chunk_count} chunks stored. Start asking questions!")
            except Exception as e:
                st.error(f"Indexing error: {e}")

    if index_btn:
        if uploaded_file is None:
            st.warning("Please upload a metadata file first.")
        else:
            content = uploaded_file.read().decode("utf-8")
            with st.spinner("Indexing your metadata…"):
                try:
                    vectorstore, chunk_count = index_documents(content)
                    st.session_state["vectorstore"] = vectorstore
                    st.session_state["indexed"] = True
                    st.session_state["chat_history"] = []
                    st.success(f"✅ Indexed successfully — {chunk_count} chunks stored.")
                except Exception as e:
                    st.error(f"Indexing error: {e}")

    # ── Section 2: Chat ───────────────────────────────────────────────────────
    st.divider()
    st.markdown("### 💬 Ask Questions")

    if not st.session_state["indexed"]:
        st.markdown(
            "<div style='background:#1a1d27;border:1px solid #2d3148;border-radius:10px;"
            "padding:24px;text-align:center;color:#718096'>"
            "📂 Upload and index your Lakehouse metadata above to start chatting."
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        # Sample question buttons
        st.markdown("**Try an example question:**")
        q_cols = st.columns(2)
        for i, question in enumerate(p["example_questions"]):
            if q_cols[i % 2].button(question, key=f"sample_q_{i}"):
                st.session_state["lake_question"] = question

        question_input = st.text_input(
            "Your question",
            value=st.session_state.get("lake_question", ""),
            placeholder="e.g. Which tables contain customer data?",
            key="lake_question",
        )

        if st.button("🔎 Ask", type="primary", key="lake_ask"):
            if not question_input.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Searching metadata and generating answer…"):
                    try:
                        context_chunks = retrieve_context(
                            question_input.strip(),
                            st.session_state["vectorstore"],
                        )
                        rag_user_prompt = build_rag_prompt(question_input.strip(), context_chunks)
                        answer = call_ai(p["system_prompt"], rag_user_prompt)

                        st.session_state["chat_history"].append({
                            "question": question_input.strip(),
                            "answer": answer,
                            "context": context_chunks,
                        })
                        # Keep last 5 Q&As
                        st.session_state["chat_history"] = st.session_state["chat_history"][-5:]
                        # Clear input
                        st.session_state["lake_question"] = ""
                    except Exception as e:
                        st.error(f"Error: {e}")

        # ── Chat history ──────────────────────────────────────────────────────
        if st.session_state["chat_history"]:
            st.divider()
            st.markdown("### 🗨 Chat History")
            for entry in reversed(st.session_state["chat_history"]):
                st.markdown(f"**Q: {entry['question']}**")
                st.markdown(entry["answer"])
                with st.expander("🔍 View source context retrieved"):
                    for i, chunk in enumerate(entry["context"], 1):
                        st.markdown(f"**Chunk {i}:**")
                        st.code(chunk, language=None)
                st.divider()

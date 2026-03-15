import os
from google import genai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fabric Dev Toolkit · FABCON 2026",
    page_icon="🔧",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }

    /* Tab styling */
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

    /* Buttons */
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

    /* Text areas */
    .stTextArea textarea {
        background-color: #1a1d27;
        border: 1px solid #2d3148;
        border-radius: 8px;
        color: #e2e8f0;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 13px;
    }

    /* Headers */
    h1, h2, h3 { color: #e2e8f0 !important; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #13151f;
        border-right: 1px solid #1e2130;
    }

    /* Profile card */
    .profile-card {
        background: linear-gradient(135deg, #1a1d27, #252836);
        border: 1px solid #2d3148;
        border-radius: 12px;
        padding: 16px;
        margin-top: 12px;
        text-align: center;
    }
    .profile-name {
        font-size: 15px;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 2px;
    }
    .profile-title {
        font-size: 12px;
        color: #718096;
        margin-bottom: 10px;
    }
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

    /* Hero banner */
    .hero {
        background: linear-gradient(135deg, #0d1b4b 0%, #0f1117 60%);
        border: 1px solid #1e3a8a;
        border-radius: 14px;
        padding: 28px 32px;
        margin-bottom: 24px;
    }
    .hero h1 {
        font-size: 26px;
        font-weight: 800;
        color: #e2e8f0 !important;
        margin: 0 0 6px 0;
    }
    .hero p {
        color: #718096;
        margin: 0;
        font-size: 14px;
    }

    /* Result cards */
    .result-box {
        background-color: #1a1d27;
        border: 1px solid #2d3148;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
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


# ── AI call ───────────────────────────────────────────────────────────────────
def call_ai(system: str, user: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set. Add it to your .env file or Streamlit secrets.")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=user,
        config={"system_instruction": system},
    )
    return response.text


# ── Hero banner ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🔧 Fabric Dev Toolkit</h1>
    <p>AI-powered tools for MS Fabric & MS SQL developers · Diagnose pipeline failures · Optimize queries · Translate T-SQL to Spark · Design Fabric architectures</p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Pipeline Analyzer", "🩺 SQL Health Checker", "⚡ T-SQL → Spark", "🏗 Architecture Advisor"])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — Pipeline Failure Analyzer
# ─────────────────────────────────────────────────────────────────────────────
PIPELINE_SYSTEM = """You are a senior Microsoft Fabric and Azure Data Factory engineer
with deep expertise in Spark, Delta Lake, and distributed data pipelines.

When given an error log or pipeline failure message, respond EXACTLY in this format
(use these exact headers):

## Root Cause
<one-sentence root cause>

## Plain English Explanation
<2-4 sentences explaining what went wrong in non-technical language>

## Step-by-Step Fix
<numbered list of concrete remediation steps, including any code snippets where helpful>

Be specific, actionable, and concise. If the log is incomplete, state what additional
information would be needed."""

PIPELINE_EXAMPLE = """\
[2025-03-14 10:23:41] ERROR SparkContext: Error initializing SparkContext
org.apache.spark.SparkException: Job aborted due to stage failure:
Task 3 in stage 2.0 failed 4 times, most recent failure:
Lost task 3.3 in stage 2.0 (TID 47, 10.0.0.5, executor 2):
java.lang.OutOfMemoryError: GC overhead limit exceeded
    at org.apache.spark.sql.execution.UnsafeExternalRowSorter.insertRow(UnsafeExternalRowSorter.java:135)
    at org.apache.spark.sql.execution.SortExec$$anonfun$1.apply(SortExec.scala:108)
Driver stacktrace:
    at org.apache.spark.scheduler.DAGScheduler.failJobAndIndependentStages(DAGScheduler.scala:2059)
[2025-03-14 10:23:41] INFO Pipeline 'daily_sales_transform' — Activity 'Sort_By_Customer' FAILED
"""

with tab1:
    st.markdown("#### Paste an MS Fabric Data Factory or Spark pipeline error log and get an instant AI diagnosis.")

    with st.expander("📋 Load example log"):
        if st.button("Use example error log", key="pipeline_example"):
            st.session_state["pipeline_text"] = PIPELINE_EXAMPLE

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
                    result = call_ai(PIPELINE_SYSTEM, log_input.strip())
                    sections = {"Root Cause": "", "Plain English Explanation": "", "Step-by-Step Fix": ""}
                    current = None
                    for line in result.splitlines():
                        stripped = line.strip()
                        if stripped.startswith("## Root Cause"):
                            current = "Root Cause"
                        elif stripped.startswith("## Plain English Explanation"):
                            current = "Plain English Explanation"
                        elif stripped.startswith("## Step-by-Step Fix"):
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
SQL_HEALTH_SYSTEM = """You are a senior MS SQL Server and Microsoft Fabric SQL analytics engineer
specialising in query optimisation and performance tuning.

When given a SQL query, respond EXACTLY in this format (use these exact headers):

## Issues Found
For each issue, use this sub-format:
**[HIGH|MEDIUM|LOW]** — <issue name>: <one-sentence description>

If no issues are found, write: No significant issues found.

## Optimised Query
```sql
<the rewritten, optimised query>
```

## Changes Explained
<numbered list explaining each change made and why it improves performance>

Focus on: SELECT *, missing indexes, implicit type conversions, N+1 patterns,
non-sargable predicates, missing WHERE clauses on large tables, unnecessary
subqueries, and best-practice naming. Be specific and actionable."""

SQL_EXAMPLE = """\
SELECT *
FROM dbo.Orders o, dbo.Customers c, dbo.OrderItems oi
WHERE o.CustomerID = c.CustomerID
AND oi.OrderID = o.OrderID
AND YEAR(o.OrderDate) = 2024
AND UPPER(c.Email) = 'JOHN@EXAMPLE.COM'
AND o.Status != 'Cancelled'
ORDER BY o.OrderDate DESC
"""

with tab2:
    st.markdown("#### Paste a MS SQL or Fabric SQL query to detect anti-patterns, performance issues, and get an optimised rewrite.")

    with st.expander("📋 Load example query"):
        if st.button("Use example query", key="sql_example"):
            st.session_state["sql_text"] = SQL_EXAMPLE

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
                    result = call_ai(SQL_HEALTH_SYSTEM, sql_input.strip())

                    sections = {"Issues Found": "", "Optimised Query": "", "Changes Explained": ""}
                    current = None
                    for line in result.splitlines():
                        stripped = line.strip()
                        if stripped.startswith("## Issues Found"):
                            current = "Issues Found"
                        elif stripped.startswith("## Optimised Query"):
                            current = "Optimised Query"
                        elif stripped.startswith("## Changes Explained"):
                            current = "Changes Explained"
                        elif current:
                            sections[current] += line + "\n"

                    st.divider()

                    st.markdown("### 🚨 Issues Found")
                    issues_text = sections["Issues Found"].strip()
                    if issues_text:
                        for line in issues_text.splitlines():
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
                    optimised = sections["Optimised Query"].strip()
                    lines = optimised.splitlines()
                    if lines and lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].strip() == "```":
                        lines = lines[:-1]
                    st.code("\n".join(lines), language="sql")

                    st.markdown("### 📝 Changes Explained")
                    st.markdown(sections["Changes Explained"].strip())

                except Exception as e:
                    st.error(f"Error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — T-SQL to Fabric Spark Translator
# ─────────────────────────────────────────────────────────────────────────────
TSQL_SYSTEM = """You are an expert in both T-SQL/SQL Server and Apache Spark (PySpark + Spark SQL)
running on Microsoft Fabric.

When given a T-SQL query or stored procedure, respond EXACTLY in this format
(use these exact headers):

## PySpark Version
```python
<equivalent PySpark DataFrame API code, fully runnable in a Fabric Notebook>
```

## Spark SQL Version
```sql
<equivalent Spark SQL, runnable via spark.sql() in a Fabric Notebook>
```

## Migration Notes
<bullet list of important differences, gotchas, function mappings, and things to watch out for
when moving from T-SQL to Spark — e.g. NULL handling, TOP vs LIMIT, GETDATE() vs current_timestamp(),
identity columns, temp tables, CTEs, transaction semantics, etc.>

Be thorough and production-ready. Include comments in the code where helpful."""

TSQL_EXAMPLE = """\
WITH RecentOrders AS (
    SELECT
        c.CustomerID,
        c.FirstName + ' ' + c.LastName AS FullName,
        COUNT(o.OrderID) AS TotalOrders,
        SUM(oi.Quantity * oi.UnitPrice) AS TotalSpend,
        MAX(o.OrderDate) AS LastOrderDate
    FROM dbo.Customers c
    INNER JOIN dbo.Orders o ON c.CustomerID = o.CustomerID
    INNER JOIN dbo.OrderItems oi ON o.OrderID = oi.OrderID
    WHERE o.OrderDate >= DATEADD(MONTH, -6, GETDATE())
    GROUP BY c.CustomerID, c.FirstName, c.LastName
)
SELECT TOP 10
    FullName,
    TotalOrders,
    TotalSpend,
    LastOrderDate
FROM RecentOrders
WHERE TotalSpend > 1000
ORDER BY TotalSpend DESC;
"""

with tab3:
    st.markdown("#### Paste a T-SQL query or stored procedure and get a production-ready PySpark + Spark SQL translation for MS Fabric Notebooks.")

    with st.expander("📋 Load example T-SQL"):
        if st.button("Use example T-SQL", key="tsql_example"):
            st.session_state["tsql_text"] = TSQL_EXAMPLE

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
                    result = call_ai(TSQL_SYSTEM, tsql_input.strip())

                    sections = {"PySpark Version": "", "Spark SQL Version": "", "Migration Notes": ""}
                    current = None
                    for line in result.splitlines():
                        stripped = line.strip()
                        if stripped.startswith("## PySpark Version"):
                            current = "PySpark Version"
                        elif stripped.startswith("## Spark SQL Version"):
                            current = "Spark SQL Version"
                        elif stripped.startswith("## Migration Notes"):
                            current = "Migration Notes"
                        elif current:
                            sections[current] += line + "\n"

                    def strip_fences(text: str) -> str:
                        lines = text.strip().splitlines()
                        if lines and lines[0].startswith("```"):
                            lines = lines[1:]
                        if lines and lines[-1].strip() == "```":
                            lines = lines[:-1]
                        return "\n".join(lines)

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
ARCH_SYSTEM = """You are a Microsoft Fabric solution architect with deep expertise
in all Fabric workloads including Data Engineering, Data Warehouse, Real-Time Analytics,
Data Science, and Power BI. You help data teams choose the right Fabric components
for their use case. Always be specific, practical, and opinionated — don't just list
options, recommend the best one for the scenario described.

Respond EXACTLY in this format (use these exact headers):

## Recommended Components
List each recommended Fabric component with a one-sentence justification.
Cover: Lakehouse vs Warehouse vs Eventhouse, ingestion method, compute layer,
reporting layer, and any ML/DS workloads if relevant.

## Architecture Flow
A simple text-based diagram showing how data flows through the components.
Use arrows (→) to show the flow. Example format:
Source → Ingestion Layer → Storage Layer → Compute Layer → Reporting Layer

## Key Decisions & Trade-offs
Bullet list of WHY each major component was chosen over alternatives, and
what trade-offs the team should be aware of.

## Getting Started Checklist
A numbered list of the first 5–7 concrete steps to implement this architecture
in MS Fabric, ordered by priority."""

ARCH_EXAMPLES = {
    "Real-time IoT → Power BI (sub-5min refresh)": (
        "I have 10TB of IoT sensor data coming in real-time from 50,000 devices. "
        "I need Power BI dashboards refreshed every 5 minutes for operations teams. "
        "Data must be retained for 2 years for compliance."
    ),
    "Migrate SQL Server DW to Fabric": (
        "We have a legacy SQL Server data warehouse with 200 stored procedures, "
        "500GB of data, and 30 Power BI reports. We want to migrate everything to "
        "Microsoft Fabric with minimal disruption to business users."
    ),
    "Daily ML training on large dataset": (
        "I need to process 5TB of daily clickstream data from our website, "
        "run feature engineering pipelines, train churn prediction ML models daily, "
        "and expose predictions to our CRM via API."
    ),
}

with tab4:
    st.markdown("#### Describe your data scenario in plain English and get a tailored MS Fabric architecture recommendation.")

    with st.expander("📋 Load example scenario"):
        for label, scenario in ARCH_EXAMPLES.items():
            if st.button(label, key=f"arch_ex_{label[:20]}"):
                st.session_state["arch_text"] = scenario

    arch_input = st.text_area(
        "Describe your data scenario",
        height=180,
        placeholder=(
            "e.g. I have 10TB of IoT sensor data coming in real-time and need "
            "Power BI dashboards refreshed every 5 minutes…"
        ),
        key="arch_text",
    )

    if st.button("🏗 Get Architecture Recommendation", type="primary", key="arch_analyze"):
        if not arch_input.strip():
            st.warning("Please describe your scenario before getting a recommendation.")
        else:
            with st.spinner("Designing your Fabric architecture…"):
                try:
                    result = call_ai(ARCH_SYSTEM, arch_input.strip())

                    sections = {
                        "Recommended Components": "",
                        "Architecture Flow": "",
                        "Key Decisions & Trade-offs": "",
                        "Getting Started Checklist": "",
                    }
                    current = None
                    for line in result.splitlines():
                        stripped = line.strip()
                        if stripped.startswith("## Recommended Components"):
                            current = "Recommended Components"
                        elif stripped.startswith("## Architecture Flow"):
                            current = "Architecture Flow"
                        elif stripped.startswith("## Key Decisions"):
                            current = "Key Decisions & Trade-offs"
                        elif stripped.startswith("## Getting Started"):
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

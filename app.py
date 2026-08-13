from __future__ import annotations

import time
from datetime import datetime

import pandas as pd
import streamlit as st
import altair as alt

from redaction_engine import redact_docx_bytes


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PII Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# MODERN DARK-LIGHT HYBRID THEME
# ============================================================

st.markdown(
    """
    <style>
    /* ==========================================================
       GLOBAL RESET & BASE
       ========================================================== */
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    .stApp {
        background: linear-gradient(165deg, #f0f4f9 0%, #e8edf5 100%);
        color: #1a2332;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .block-container {
        max-width: 1360px;
        padding: 2rem 2rem 3rem 2rem;
        margin: 0 auto;
    }

    /* Hide Streamlit default header */
    [data-testid="stHeader"] {
        background: transparent;
        border: none;
        backdrop-filter: blur(0px);
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* ==========================================================
       SIDEBAR - Premium Glass Design
       ========================================================== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1a2e 0%, #162033 50%, #1a2a40 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
        box-shadow: 4px 0 30px rgba(0,0,0,0.25);
        backdrop-filter: blur(10px);
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.8rem 1.2rem 2rem 1.2rem;
    }

    /* Sidebar Brand */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0.8rem 0.4rem 0.2rem 0.4rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1.8rem;
        padding-bottom: 1.2rem;
    }

    .sidebar-brand-icon {
        font-size: 32px;
        background: linear-gradient(135deg, #4a9eff, #6c5ce7);
        padding: 8px 12px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(74, 158, 255, 0.3);
    }

    .sidebar-brand-text h1 {
        color: #ffffff !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        margin: 0 !important;
        letter-spacing: -0.3px;
        background: linear-gradient(135deg, #ffffff 60%, #8ab4f8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .sidebar-brand-text p {
        color: rgba(255,255,255,0.5) !important;
        font-size: 10px !important;
        font-weight: 500 !important;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin: 0 !important;
        -webkit-text-fill-color: rgba(255,255,255,0.5);
    }

    /* ==========================================================
       SIDEBAR NAVIGATION — CLEAN BUTTONS
       Exactly ONE indicator character per item.
       No Streamlit radio controls are used.
       ========================================================== */

    .sidebar-nav-title {
        color: rgba(255,255,255,0.42);
        font-size: 10px;
        font-weight: 750;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin: 0 0 9px 2px;
    }

    section[data-testid="stSidebar"] .stButton {
        margin-bottom: 7px !important;
    }

    /* Inactive navigation item */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        min-height: 45px !important;
        padding: 0 14px !important;
        border-radius: 10px !important;

        background: rgba(255,255,255,0.035) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        color: rgba(255,255,255,0.78) !important;

        box-shadow: none !important;
        transform: none !important;
        transition: all 0.2s ease !important;
        text-align: left !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(74,158,255,0.10) !important;
        border-color: rgba(74,158,255,0.38) !important;
        color: #ffffff !important;
        transform: translateX(2px) !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.12) !important;
    }

    section[data-testid="stSidebar"] .stButton > button p,
    section[data-testid="stSidebar"] .stButton > button span,
    section[data-testid="stSidebar"] .stButton > button div {
        color: inherit !important;
        font-size: 13.5px !important;
        font-weight: 550 !important;
    }

    /* Active navigation item */
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(
            135deg,
            #2563eb 0%,
            #3b82f6 100%
        ) !important;
        border: 1px solid #4a9eff !important;
        color: #ffffff !important;
        box-shadow:
            0 4px 16px rgba(37,99,235,0.24) !important;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background: linear-gradient(
            135deg,
            #1d4ed8 0%,
            #2563eb 100%
        ) !important;
        border-color: #69a9ff !important;
        transform: translateX(2px) !important;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"] p,
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] span,
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] div {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    /* Sidebar Info Cards */
    .sidebar-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 14px 16px;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
    }

    .sidebar-card .card-label {
        color: rgba(255,255,255,0.35) !important;
        font-size: 9px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px !important;
    }

    .sidebar-card .card-item {
        color: rgba(255,255,255,0.65) !important;
        font-size: 12.5px !important;
        padding: 4px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .sidebar-card .card-item::before {
        content: "▸";
        color: #4a9eff;
        font-size: 10px;
        opacity: 0.6;
    }

    .sidebar-footer {
        margin-top: auto;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255,255,255,0.06);
    }

    .sidebar-footer p {
        color: rgba(255,255,255,0.25) !important;
        font-size: 10px !important;
        text-align: center;
        letter-spacing: 0.5px;
        -webkit-text-fill-color: rgba(255,255,255,0.25);
    }

    /* ==========================================================
       MAIN CONTENT AREA
       ========================================================== */

    /* Main Headers */
    .main-title {
        background: linear-gradient(135deg, #1a2332 0%, #2a3a55 100%);
        padding: 1.8rem 2.2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        position: relative;
        overflow: hidden;
    }

    .main-title::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(74,158,255,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }

    .main-title h1 {
        color: #ffffff !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
        margin: 0 !important;
    }

    .main-title .subtitle {
        color: rgba(255,255,255,0.6) !important;
        font-size: 13px !important;
        margin-top: 4px !important;
        letter-spacing: 0.3px;
    }

    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 1.8rem 0 1rem 0;
    }

    .section-header h2, .section-header h3 {
        color: #1a2332 !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }

    .section-header .badge {
        background: linear-gradient(135deg, #4a9eff, #6c5ce7);
        color: white;
        font-size: 10px;
        font-weight: 700;
        padding: 2px 12px;
        border-radius: 20px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    /* ==========================================================
       METRIC CARDS
       ========================================================== */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid rgba(26,35,50,0.06);
        border-radius: 14px;
        padding: 20px 22px;
        min-height: 100px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    [data-testid="stMetric"]::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4a9eff, #6c5ce7);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.08);
        border-color: rgba(74,158,255,0.2);
    }

    [data-testid="stMetric"]:hover::before {
        opacity: 1;
    }

    [data-testid="stMetricLabel"] {
        color: #6b7a93 !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    [data-testid="stMetricValue"] {
        color: #1a2332 !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #1a2332, #2a3a55);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ==========================================================
       BUTTONS - Premium
       ========================================================== */
    .stButton > button,
    .stDownloadButton > button {
        min-height: 48px;
        padding: 0 28px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        background: linear-gradient(135deg, #4a9eff 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 16px rgba(74, 158, 255, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.3px;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::after,
    .stDownloadButton > button::after {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
        transition: left 0.6s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 30px rgba(74, 158, 255, 0.4) !important;
    }

    .stButton > button:hover::after,
    .stDownloadButton > button:hover::after {
        left: 100%;
    }

    .stButton > button:active,
    .stDownloadButton > button:active {
        transform: scale(0.97);
    }

    /* ==========================================================
       FILE UPLOADER
       ========================================================== */

    [data-testid="stFileUploader"] {
        background: #ffffff;
        border: 2px dashed rgba(26,35,50,0.12);
        border-radius: 14px;
        padding: 20px;
        transition: all 0.3s ease;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #4a9eff;
        background: rgba(74,158,255,0.02);
    }

    [data-testid="stFileUploaderDropzone"] {
        background: transparent !important;
        border: none !important;
        border-radius: 8px;
    }

    [data-testid="stFileUploaderDropzone"] button {
        background: linear-gradient(135deg, #4a9eff, #3b82f6) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 8px 20px !important;
        box-shadow: 0 2px 12px rgba(74,158,255,0.25) !important;
    }

    [data-testid="stFileUploaderDropzone"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(74,158,255,0.35) !important;
    }

    /* ==========================================================
       TABLES - Modern Glass Design
       ========================================================== */
    .pii-table-wrap {
        background: #ffffff;
        border: 1px solid rgba(26,35,50,0.06);
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        margin-top: 12px;
        transition: all 0.3s ease;
    }

    .pii-table-wrap:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.06);
        border-color: rgba(74,158,255,0.15);
    }

    table.pii-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 13.5px;
        color: #1a2332;
        background: #ffffff;
    }

    table.pii-table th {
        background: linear-gradient(180deg, #f8faff 0%, #f0f4f9 100%);
        color: #1a2332;
        text-align: left;
        font-weight: 700;
        padding: 14px 16px;
        border-bottom: 2px solid rgba(26,35,50,0.06);
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #4a6a8a;
    }

    table.pii-table td {
        padding: 12px 16px;
        border-bottom: 1px solid rgba(26,35,50,0.04);
        vertical-align: middle;
        background: #ffffff;
        color: #1a2332;
        font-weight: 450;
    }

    table.pii-table tr:hover td {
        background: #f8fbff;
    }

    table.pii-table tr:last-child td {
        border-bottom: none;
    }

    /* Type badges in tables */
    .type-badge {
        display: inline-block;
        padding: 3px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }

    .type-badge-email { background: #dbeafe; color: #1a56db; }
    .type-badge-phone { background: #d1fae5; color: #065f46; }
    .type-badge-name { background: #fef3c7; color: #92400e; }
    .type-badge-address { background: #ede9fe; color: #5b21b6; }
    .type-badge-ssn { background: #fce4ec; color: #b71c1c; }
    .type-badge-credit { background: #fce4ec; color: #b71c1c; }
    .type-badge-date { background: #e0f2fe; color: #0369a1; }
    .type-badge-default { background: #f1f5f9; color: #475569; }

    /* ==========================================================
       ALERTS & NOTIFICATIONS
       ========================================================== */
    div[data-testid="stAlert"] {
        border-radius: 12px;
        border: none !important;
        padding: 16px 20px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        backdrop-filter: blur(10px);
    }

    div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
        color: #1a2332 !important;
    }

    .stAlert > div {
        background: transparent !important;
    }

    /* ==========================================================
       EXPANDER
       ========================================================== */
    [data-testid="stExpander"] {
        background: #ffffff;
        border: 1px solid rgba(26,35,50,0.06);
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    [data-testid="stExpander"] details {
        padding: 4px 0;
    }

    [data-testid="stExpander"] summary {
        font-weight: 600;
        color: #1a2332;
        padding: 8px 4px;
    }

    /* ==========================================================
       SELECT BOX & INPUTS
       ========================================================== */
    [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid rgba(26,35,50,0.1) !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }

    [data-baseweb="select"] > div:hover {
        border-color: #4a9eff !important;
        box-shadow: 0 0 0 3px rgba(74,158,255,0.1);
    }

    /* ==========================================================
       DIVIDERS
       ========================================================== */
    hr {
        border: none;
        border-top: 1px solid rgba(26,35,50,0.06);
        margin: 2rem 0;
    }

    /* ==========================================================
       PROGRESS BAR
       ========================================================== */
    [data-testid="stProgressBar"] {
        height: 6px !important;
        border-radius: 10px !important;
        background: rgba(26,35,50,0.06) !important;
        overflow: hidden;
        margin: 12px 0;
    }

    [data-testid="stProgressBar"] > div {
        background: linear-gradient(90deg, #4a9eff, #6c5ce7) !important;
        border-radius: 10px !important;
        height: 100% !important;
    }

    /* ==========================================================
       CHART CONTAINER
       ========================================================== */
    .chart-container {
        background: #ffffff;
        border: 1px solid rgba(26,35,50,0.06);
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }

    .chart-container:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.06);
        border-color: rgba(74,158,255,0.15);
    }

    /* ==========================================================
       RESPONSIVE ADJUSTMENTS
       ========================================================== */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 1rem 2rem 1rem;
        }
        .main-title {
            padding: 1.2rem 1.5rem;
        }
        .main-title h1 {
            font-size: 24px !important;
        }
        [data-testid="stMetric"] {
            padding: 14px 16px;
            min-height: 80px;
        }
        [data-testid="stMetricValue"] {
            font-size: 22px !important;
        }
        section[data-testid="stSidebar"] > div {
            padding: 1rem 0.8rem 1.5rem 0.8rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "audit" not in st.session_state:
    st.session_state.audit = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    # Brand
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">🛡️</div>
            <div class="sidebar-brand-text">
                <h1>PII Shield</h1>
                <p>Privacy Platform</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Navigation
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Overview"

    st.markdown(
        '<div class="sidebar-nav-title">Workspace</div>',
        unsafe_allow_html=True,
    )

    navigation_items = [
        ("Overview", "nav_overview"),
        ("Detection Explorer", "nav_detection"),
        ("Before / After", "nav_before"),
        ("Validation", "nav_validation"),
        ("Audit Log", "nav_audit"),
    ]

    for nav_name, nav_key in navigation_items:
        is_active = st.session_state.current_page == nav_name

        # The bullet is intentionally part of the label so there is
        # exactly ONE visible indicator and no hidden radio indicator.
        nav_label = (
            f"●  {nav_name}"
            if is_active
            else f"○  {nav_name}"
        )

        if st.button(
            nav_label,
            key=nav_key,
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            st.session_state.current_page = nav_name
            st.rerun()

    page_clean = st.session_state.current_page

    # Engine Info
    st.markdown(
        """
        <div class="sidebar-card">
            <div class="card-label">⚡ Detection Engine</div>
            <div class="card-item">Regex pattern matching</div>
            <div class="card-item">Contextual heuristics</div>
            <div class="card-item">Synthetic replacement</div>
            <div class="card-item">Post-redaction validation</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # System Info
    st.markdown(
        """
        <div class="sidebar-card" style="margin-top: 0.8rem;">
            <div class="card-label">💻 System</div>
            <div class="card-item">PII Shield v1.0</div>
            <div class="card-item">Document Privacy Platform</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-footer">
            <p>© 2026 PII Shield · Enterprise Edition</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_type_badge(pii_type):
    """Return HTML badge for PII type."""
    type_map = {
        'EMAIL': 'email',
        'PHONE': 'phone',
        'NAME': 'name',
        'ADDRESS': 'address',
        'SSN': 'ssn',
        'CREDIT': 'credit',
        'DATE': 'date',
    }
    badge_class = type_map.get(pii_type.upper(), 'default')
    return f'<span class="type-badge type-badge-{badge_class}">{pii_type}</span>'


def create_table_html(df, columns=None, max_rows=None):
    """Create styled HTML table from dataframe."""
    if columns:
        df = df[columns]
    
    if max_rows and len(df) > max_rows:
        df = df.head(max_rows)
    
    html = '<div class="pii-table-wrap"><table class="pii-table"><thead><tr>'
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'
    
    for _, row in df.iterrows():
        html += '<tr>'
        for col in df.columns:
            value = row[col]
            if col == 'Type' and isinstance(value, str):
                value = get_type_badge(value)
            elif isinstance(value, float):
                value = f'{value:.2f}'
            html += f'<td>{value}</td>'
        html += '</tr>'
    
    html += '</tbody></table></div>'
    return html


# ============================================================
# PAGE: OVERVIEW
# ============================================================

if page_clean == "Overview":

    # Header
    st.markdown(
        """
        <div class="main-title">
            <h1>🛡️ PII Shield</h1>
            <div class="subtitle">Document Privacy &amp; Redaction Platform — Detect, classify, replace, and validate sensitive information</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-header">
            <h2>📄 Document Analysis</h2>
            <span class="badge">Upload &amp; Process</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload DOCX document for PII analysis",
        type=["docx"],
        help="Select a Microsoft Word document to begin the privacy analysis.",
        label_visibility="collapsed",
    )

    if uploaded_file is None:
        st.info(
            "📤 Upload a DOCX document above to begin the analysis.",
            icon="ℹ️",
        )

        st.markdown(
            """
            <div class="section-header" style="margin-top: 2.5rem;">
                <h3>🔄 Redaction Workflow</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("01", "Detect")
            st.caption("Identify sensitive information within the document.")

        with col2:
            st.metric("02", "Classify")
            st.caption("Assign each detected value to a PII category.")

        with col3:
            st.metric("03", "Replace")
            st.caption("Generate consistent synthetic replacement values.")

        with col4:
            st.metric("04", "Validate")
            st.caption("Re-scan the sanitized document for remaining PII.")

    else:
        st.success(f"✅ Document ready: **{uploaded_file.name}**")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "📦 File Size",
                f"{uploaded_file.size / 1024:.1f} KB",
            )

        with col2:
            st.metric("📄 Format", "DOCX")

        with col3:
            st.metric("⚡ Status", "READY")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "🚀 Analyze & Redact Document",
            type="primary",
            use_container_width=False,
        ):

            file_bytes = uploaded_file.getvalue()

            progress = st.progress(
                0,
                text="⏳ Initializing document analyzer...",
            )

            status = st.empty()

            start_time = time.time()

            def update_progress(value):
                percentage = int(value * 100)
                progress.progress(
                    percentage,
                    text=f"⏳ Processing document... {percentage}%",
                )

            status.info("📖 Reading document structure...")

            try:

                result = redact_docx_bytes(
                    file_bytes,
                    progress_callback=update_progress,
                )

                elapsed = time.time() - start_time

                result["processing_time"] = elapsed
                result["filename"] = uploaded_file.name
                result["timestamp"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                st.session_state.result = result

                current_time = datetime.now().strftime(
                    "%H:%M:%S"
                )

                st.session_state.audit = [
                    {
                        "Time": current_time,
                        "Event": "Document uploaded",
                    },
                    {
                        "Time": current_time,
                        "Event": "Document structure analyzed",
                    },
                    {
                        "Time": current_time,
                        "Event": "PII detection completed",
                    },
                    {
                        "Time": current_time,
                        "Event": (
                            f"{result['total_replacements']} "
                            "entities processed"
                        ),
                    },
                    {
                        "Time": current_time,
                        "Event": (
                            "Synthetic replacements generated"
                        ),
                    },
                    {
                        "Time": current_time,
                        "Event": (
                            "Post-redaction validation completed"
                        ),
                    },
                ]

                progress.progress(
                    100,
                    text="✅ Processing complete",
                )

                status.success(
                    "🎉 Document successfully processed."
                )

            except Exception as error:

                progress.empty()
                status.empty()

                st.error(
                    f"❌ Processing failed: {error}"
                )

                st.exception(error)
                st.stop()

        # Results
        result = st.session_state.result

        if result:

            st.divider()

            st.markdown(
                """
                <div class="section-header">
                    <h2>📊 Analysis Summary</h2>
                    <span class="badge">Results</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            stats = result["stats"]

            total = sum(stats.values())

            active_types = sum(
                1
                for value in stats.values()
                if value > 0
            )

            paragraphs = result["document_info"]["paragraphs"]
            tables = result["document_info"]["tables"]
            processing_time = result["processing_time"]

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric("🔍 PII Detected", total)

            with col2:
                st.metric("📋 PII Types", active_types)

            with col3:
                st.metric("📝 Paragraphs", paragraphs)

            with col4:
                st.metric("📊 Tables", tables)

            with col5:
                st.metric(
                    "⏱️ Processing",
                    f"{processing_time:.1f}s",
                )

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                """
                <div class="section-header">
                    <h3>📈 Detection Breakdown</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )

            chart_data = pd.DataFrame(
                {
                    "PII Type": list(stats.keys()),
                    "Count": list(stats.values()),
                }
            )

            chart_data = chart_data[
                chart_data["Count"] > 0
            ]

            if not chart_data.empty:
                chart = (
                    alt.Chart(chart_data)
                    .mark_bar(
                        color="#4a9eff",
                        cornerRadiusTopLeft=8,
                        cornerRadiusTopRight=8,
                        opacity=0.85,
                    )
                    .encode(
                        x=alt.X(
                            "PII Type:N",
                            sort="-y",
                            axis=alt.Axis(
                                title=None,
                                labelAngle=0,
                                labelColor="#475569",
                                labelFontWeight=500,
                            ),
                        ),
                        y=alt.Y(
                            "Count:Q",
                            axis=alt.Axis(
                                title="Detected Entities",
                                titleColor="#6b7a93",
                                labelColor="#6b7a93",
                                gridColor="#e8edf5",
                                titleFontWeight=600,
                            ),
                        ),
                        tooltip=[
                            alt.Tooltip(
                                "PII Type:N",
                                title="PII Type",
                            ),
                            alt.Tooltip(
                                "Count:Q",
                                title="Count",
                            ),
                        ],
                    )
                    .properties(
                        height=380,
                        background="transparent",
                    )
                    .configure_view(
                        stroke="transparent",
                    )
                )

                st.markdown(
                    '<div class="chart-container">',
                    unsafe_allow_html=True,
                )
                st.altair_chart(
                    chart,
                    use_container_width=True,
                )
                st.markdown(
                    '</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.info("✅ No PII was detected in the document.")

            st.markdown(
                """
                <div class="section-header" style="margin-top: 2rem;">
                    <h3>✅ Validation Summary</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )

            validation = result["validation"]

            validation_col1, validation_col2, validation_col3 = (
                st.columns(3)
            )

            with validation_col1:
                st.metric(
                    "🔍 Detected Entities",
                    result["total_replacements"],
                )

            with validation_col2:
                st.metric(
                    "⚠️ Remaining Entities",
                    validation["remaining_count"],
                )

            with validation_col3:
                st.metric(
                    "📋 Validation Status",
                    (
                        "✅ PASSED"
                        if validation["passed"]
                        else "⚠️ REVIEW"
                    ),
                )

            if validation["passed"]:
                st.success(
                    "✅ Validation passed. No remaining detectable "
                    "PII was identified."
                )
            else:
                st.warning(
                    "⚠️ The validation scan identified potential "
                    "remaining entities. Manual review is recommended."
                )

            st.markdown(
                """
                <div class="section-header" style="margin-top: 2rem;">
                    <h3>📥 Export</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.download_button(
                label="📥 Download Redacted DOCX",
                data=result["document"],
                file_name=(
                    "PII_Shield_Redacted_"
                    + uploaded_file.name
                ),
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                type="primary",
            )


# ============================================================
# PAGE: DETECTION EXPLORER
# ============================================================

elif page_clean == "Detection Explorer":

    st.markdown(
        """
        <div class="main-title">
            <h1>🔍 Detection Explorer</h1>
            <div class="subtitle">Review detected entities, their category, and synthetic replacement values</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    result = st.session_state.result

    if not result:

        st.info(
            "📤 Please analyze a document from the **Overview** page first.",
            icon="ℹ️",
        )

    else:

        records = result.get("records", [])

        if not records:

            st.success("✅ No PII was detected in the document.")

        else:

            df = pd.DataFrame(records)

            df_display = df[
                [
                    "label",
                    "original",
                    "replacement",
                    "start",
                    "end",
                ]
            ].copy()

            df_display.columns = [
                "Type",
                "Original",
                "Replacement",
                "Start",
                "End",
            ]

            available_types = sorted(
                df_display["Type"].unique()
            )

            filter_col, count_col = st.columns(
                [3, 1]
            )

            with filter_col:

                selected_type = st.selectbox(
                    "🔍 Filter by PII Category",
                    ["ALL"] + available_types,
                    label_visibility="collapsed",
                )

            if selected_type == "ALL":
                filtered = df_display
            else:
                filtered = df_display[
                    df_display["Type"] == selected_type
                ]

            with count_col:

                st.metric(
                    "📊 Records",
                    len(filtered),
                )

            st.markdown("<br>", unsafe_allow_html=True)

            if not filtered.empty:
                html_table = create_table_html(
                    filtered,
                    columns=["Type", "Original", "Replacement", "Start", "End"],
                    max_rows=100,
                )
                st.markdown(html_table, unsafe_allow_html=True)

                if len(filtered) > 100:
                    st.caption(
                        "📌 Showing the first 100 records. "
                        f"Total: {len(filtered)} records."
                    )
            else:
                st.info("No records match the selected filter.")

            st.markdown("<br>", unsafe_allow_html=True)

            st.download_button(
                "📥 Download Detection CSV",
                data=filtered.to_csv(
                    index=False
                ).encode("utf-8"),
                file_name="detection_results.csv",
                mime="text/csv",
            )


# ============================================================
# PAGE: BEFORE / AFTER
# ============================================================

elif page_clean == "Before / After":

    st.markdown(
        """
        <div class="main-title">
            <h1>📝 Replacement Review</h1>
            <div class="subtitle">Compare detected source values with their generated synthetic replacements</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    result = st.session_state.result

    if not result:

        st.info(
            "📤 Please analyze a document from the **Overview** page first.",
            icon="ℹ️",
        )

    else:

        records = result.get("records", [])

        if not records:

            st.success("✅ No PII was detected in the document.")

        else:

            df = pd.DataFrame(records)

            review_df = df[
                [
                    "label",
                    "original",
                    "replacement",
                ]
            ].copy()

            review_df.columns = [
                "Type",
                "Original Value",
                "Synthetic Replacement",
            ]

            st.info(
                f"📊 Showing {len(review_df)} detected entities.",
                icon="ℹ️",
            )

            st.markdown("<br>", unsafe_allow_html=True)

            html_table = create_table_html(
                review_df,
                columns=["Type", "Original Value", "Synthetic Replacement"],
                max_rows=100,
            )
            st.markdown(html_table, unsafe_allow_html=True)

            if len(review_df) > 100:
                st.caption(
                    "📌 Showing the first 100 records. "
                    f"Total: {len(review_df)} records."
                )


# ============================================================
# PAGE: VALIDATION
# ============================================================

elif page_clean == "Validation":

    st.markdown(
        """
        <div class="main-title">
            <h1>✅ Validation Report</h1>
            <div class="subtitle">Post-redaction verification of the sanitized document</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    result = st.session_state.result

    if not result:

        st.info(
            "📤 Please analyze a document from the **Overview** page first.",
            icon="ℹ️",
        )

    else:

        # Read the validation payload safely. This keeps the Validation
        # page connected to the result generated by redaction_engine
        # while preventing a broken page when an older result is missing
        # one optional validation field.
        validation = result.get("validation") or {}

        remaining = validation.get(
            "remaining_entities",
            [],
        )

        remaining_count = validation.get(
            "remaining_count",
            len(remaining),
        )

        passed = validation.get(
            "passed",
            remaining_count == 0,
        )

        total_replacements = result.get(
            "total_replacements",
            len(result.get("records", [])),
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🔍 Detected Entities",
                total_replacements,
            )

        with col2:
            st.metric(
                "⚠️ Remaining Entities",
                remaining_count,
            )

        with col3:
            st.metric(
                "📋 Validation Status",
                "✅ PASSED" if passed else "⚠️ REVIEW",
            )

        st.divider()

        if passed:

            st.success(
                "✅ Validation passed. No remaining detectable "
                "PII was identified."
            )

        else:

            st.warning(
                "⚠️ The validation scan identified potential "
                "remaining entities. Manual review is recommended."
            )

            if remaining:

                remaining_df = pd.DataFrame(remaining)

                st.markdown(
                    """
                    <div class="section-header" style="margin-top: 1.5rem;">
                        <h3>⚠️ Remaining Entities</h3>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                html_table = create_table_html(
                    remaining_df,
                    columns=list(remaining_df.columns),
                )
                st.markdown(
                    html_table,
                    unsafe_allow_html=True,
                )
            else:
                st.info(
                    "The validation result is marked for review, "
                    "but no remaining entity records were returned."
                )


# ============================================================
# PAGE: AUDIT LOG
# ============================================================

elif page_clean == "Audit Log":

    st.markdown(
        """
        <div class="main-title">
            <h1>📋 Activity Log</h1>
            <div class="subtitle">Processing events recorded during the current session</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    audit = st.session_state.audit

    if not audit:

        st.info(
            "📭 No processing activity recorded yet.",
            icon="ℹ️",
        )

    else:

        audit_df = pd.DataFrame(audit)

        st.info(
            f"📊 Showing {len(audit_df)} audit events.",
            icon="ℹ️",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        html_table = create_table_html(
            audit_df,
            columns=["Time", "Event"],
        )
        st.markdown(html_table, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🛡️ PII Shield  |  Document Privacy & Redaction Platform  |  v1.0  |  Enterprise Edition"
)
"""
theme.py

Global Streamlit UI styling.
"""


import streamlit as st


def apply_theme():
    """
    Apply global UI styling.
    """

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL
        ===================================================== */

        .stApp {
            background-color: #f8fafc;
        }

        .main {
            padding-top: 1rem;
        }

        /* =====================================================
           HEADER
        ===================================================== */

        .app-header {
            padding: 1.5rem 0 1rem 0;
        }

        .app-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #111827;
            margin-bottom: 0.2rem;
        }

        .app-subtitle {
            font-size: 1rem;
            color: #6b7280;
        }

        /* =====================================================
           SECTION HEADERS
        ===================================================== */

        .section-title {
            font-size: 1.25rem;
            font-weight: 650;
            color: #111827;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
        }

        /* =====================================================
           METRIC CARDS
        ===================================================== */

        .metric-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.2rem;
            min-height: 110px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        }

        .metric-icon {
            font-size: 1.3rem;
        }

        .metric-label {
            color: #6b7280;
            font-size: 0.85rem;
            margin-top: 0.3rem;
        }

        .metric-value {
            color: #111827;
            font-size: 1.7rem;
            font-weight: 700;
        }

        /* =====================================================
           DOCUMENT CARD
        ===================================================== */

        .document-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 0.7rem;
        }

        .document-name {
            font-weight: 600;
            color: #111827;
            font-size: 1rem;
        }

        .document-meta {
            color: #6b7280;
            font-size: 0.8rem;
        }

        /* =====================================================
           STATUS
        ===================================================== */

        .status-ready {
            display: inline-block;
            background: #dcfce7;
            color: #166534;
            padding: 0.3rem 0.7rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .status-empty {
            display: inline-block;
            background: #fef3c7;
            color: #92400e;
            padding: 0.3rem 0.7rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        /* =====================================================
           CHAT
        ===================================================== */

        [data-testid="stChatMessage"] {
            border-radius: 12px;
        }

        /* =====================================================
           SOURCE CARD
        ===================================================== */

        .source-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 0.8rem;
        }

        .source-title {
            font-weight: 650;
            color: #111827;
        }

        .source-meta {
            color: #6b7280;
            font-size: 0.8rem;
        }

        /* =====================================================
           SIDEBAR
        ===================================================== */

        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e5e7eb;
        }

        /* =====================================================
           BUTTONS
        ===================================================== */

        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
        }

        /* =====================================================
           FILE UPLOADER
        ===================================================== */

        [data-testid="stFileUploader"] {
            border-radius: 12px;
        }

        /* =====================================================
           EXPANDERS
        ===================================================== */

        .streamlit-expanderHeader {
            font-weight: 600;
        }

        /* =====================================================
           FOOTER
        ===================================================== */

        .app-footer {
            text-align: center;
            color: #9ca3af;
            font-size: 0.8rem;
            padding: 2rem 0 1rem 0;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
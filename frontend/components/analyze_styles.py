import streamlit as st


def inject_analyze_styles():
    """Premium styling for the Analyze Resume page."""

    st.markdown(
        """
        <style>

        /* ---------- Labels ---------- */
        [data-testid="stWidgetLabel"] p {
            color: #CBD5E1 !important;
            font-size: 14px !important;
            font-weight: 600 !important;
        }

        /* ---------- File uploader ---------- */
        [data-testid="stFileUploader"] {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }

        [data-testid="stFileUploaderDropzone"] {
            background: linear-gradient(
                145deg,
                rgba(17,24,39,0.98),
                rgba(15,23,42,0.98)
            ) !important;
            border: 1.5px dashed rgba(139,92,246,0.45) !important;
            border-radius: 16px !important;
            padding: 28px 20px !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stFileUploaderDropzone"]:hover {
            border-color: rgba(167,139,250,0.85) !important;
            background: rgba(139,92,246,0.06) !important;
        }

        [data-testid="stFileUploaderDropzone"] span,
        [data-testid="stFileUploaderDropzone"] small,
        [data-testid="stFileUploaderDropzone"] div {
            color: #94A3B8 !important;
        }

        [data-testid="stFileUploaderDropzone"] svg {
            color: #A78BFA !important;
            fill: #A78BFA !important;
        }

        [data-testid="stFileUploaderDropzone"] button {
            background: linear-gradient(135deg, #8B5CF6, #6366F1) !important;
            border: none !important;
            border-radius: 10px !important;
            box-shadow: 0 6px 18px rgba(99,102,241,0.30) !important;
        }

        [data-testid="stFileUploaderDropzone"] button,
        [data-testid="stFileUploaderDropzone"] button * {
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }

        /* Uploaded file row */
        [data-testid="stFileUploaderFile"] {
            background: rgba(139,92,246,0.08) !important;
            border: 1px solid rgba(139,92,246,0.25) !important;
            border-radius: 12px !important;
            padding: 8px 12px !important;
            margin-top: 10px !important;
        }

        [data-testid="stFileUploaderFile"] * {
            color: #E2E8F0 !important;
        }

        /* ---------- Textarea ---------- */
        div[data-baseweb="textarea"],
        div[data-baseweb="base-input"] {
            background: #111827 !important;
            border: 1px solid rgba(255,255,255,0.10) !important;
            border-radius: 14px !important;
            transition: all 0.2s ease !important;
        }

        div[data-baseweb="textarea"]:focus-within {
            border-color: rgba(139,92,246,0.70) !important;
            box-shadow: 0 0 0 3px rgba(139,92,246,0.18) !important;
        }

        div[data-baseweb="textarea"] textarea {
            background: transparent !important;
            color: #F8FAFC !important;
            -webkit-text-fill-color: #F8FAFC !important;
            font-size: 14.5px !important;
            line-height: 1.6 !important;
            border: none !important;
        }

        div[data-baseweb="textarea"] textarea::placeholder {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            opacity: 1 !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
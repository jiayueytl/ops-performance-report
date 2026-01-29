import streamlit as st
import pandas as pd
import io
import os
import zipfile
from jinja2 import Template

# Import modular components
from pdf_utils import generate_pdf_bytes
from logic_helpers import (
    process_data, 
    get_performance_context, 
    get_invoice_context
)
from templates.S1_PERFORMANCE_REPORT import S1_PERFORMANCE_REPORT
from templates.S2_PERFORMANCE_REPORT import S2_PERFORMANCE_REPORT
from templates.INVOICE_TEMPLATE import INVOICE_TEMPLATE
from templates.INVOICE_TEMPLATE_TASKREVIEW import INVOICE_TEMPLATE_TASKREVIEW

st.set_page_config(layout="wide", page_title="DataAnno Ops Reporting")

# --- 1. CONFIGURATION & REGISTRY ---
# This dictionary maps a "Report Type" to its Template and Logic Script
REPORT_CONFIG = {
    "Performance Report(S1)": {
        "template": S1_PERFORMANCE_REPORT,
        "logic_func": get_performance_context,
        "prefix": "Perf"
    },
    "Performance Report(S2)": {
        "template": S2_PERFORMANCE_REPORT,
        "logic_func": get_performance_context,
        "prefix": "Perf"
    },
    "Invoice-ImageCollection": {
        "template": INVOICE_TEMPLATE,
        "logic_func": get_invoice_context,
        "prefix": "Inv"
    },
    "Invoice-Standard Task Review": {
        "template": INVOICE_TEMPLATE_TASKREVIEW,
        "logic_func": get_invoice_context,
        "prefix": "Inv"
    }
}

st.sidebar.title("🛠️ Pipeline Config")
task_period = st.sidebar.text_input("Task Period", "23 Dec 2025 - 05 Jan 2026")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# 2. Source Selection Logic
df = None
if uploaded_file:
    df = pd.read_csv(uploaded_file)
elif os.path.exists("s1_performance_summary.csv"):
    df = pd.read_csv("s1_performance_summary.csv")

# 3. Main Pipeline
if df is not None:
    df, annotators = process_data(df)
    
    # NEW: Global Selector for Template/Script
    st.sidebar.subheader("📄 Template Selection")
    report_mode = st.sidebar.selectbox("Choose Report Type", list(REPORT_CONFIG.keys()))
    
    # Extract current config
    current_cfg = REPORT_CONFIG[report_mode]
    active_template = current_cfg["template"]
    active_logic = current_cfg["logic_func"]

    tab1, tab2 = st.tabs(["🔍 Preview & Edit", "🚀 Bulk Export"])

    # --- TAB 1: PREVIEW & LIVE EDIT ---
    with tab1:
        col_ed, col_pre = st.columns([1, 1])
        
        with col_ed:
            st.subheader("Edit Template")
            # Allows you to tweak the HTML/CSS on the fly
            editable_template = st.text_area("Live CSS/HTML Editor", value=active_template, height=600)
        
        with col_pre:
            st.subheader(f"Preview: {report_mode}")
            sel_name = st.selectbox("Select Annotator", annotators)
            
            # RUN THE SELECTED SCRIPT
            data = active_logic(df, sel_name, task_period)
            
            # RENDER THE SELECTED TEMPLATE
            rendered = Template(editable_template).render(data["ctx"])
            st.components.v1.html(rendered, height=600, scrolling=True)
            
            if st.button(f"Generate Single {report_mode}"):
                pdf_bytes = generate_pdf_bytes(rendered)
                st.download_button("Download PDF", pdf_bytes, file_name=data["filename"])

    # --- TAB 2: BULK EXPORT ---
    with tab2:
        st.subheader(f"Bulk Export: {report_mode}")
        st.info(f"Ready to process {len(annotators)} items using the **{report_mode}** logic.")
        
        if st.button(f"🚀 Run Bulk {report_mode} Generation"):
            zip_buf = io.BytesIO()
            pb = st.progress(0)
            
            with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for i, name in enumerate(annotators):
                    # Execute logic script
                    d = active_logic(df, name, task_period)
                    # Render current template
                    h = Template(active_template).render(d["ctx"])
                    
                    try:
                        zf.writestr(d["filename"], generate_pdf_bytes(h))
                    except Exception as e:
                        st.error(f"Error for {name}: {e}")
                    pb.progress((i + 1) / len(annotators))
            
            st.success("Batch Complete!")
            st.download_button(
                f"📥 Download All {report_mode}s", 
                zip_buf.getvalue(), 
                f"{current_cfg['prefix']}_Bulk.zip"
            )
else:
    st.warning("Please upload a CSV file to begin.")
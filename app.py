import streamlit as st
import pandas as pd
import io
import os
import zipfile
from jinja2 import Template
from datetime import datetime

# Import modular components
from pdf_utils import generate_pdf_bytes
from logic_helpers import process_data, get_performance_context, get_invoice_context
from templates.S1_PERFORMANCE_REPORT import S1_PERFORMANCE_REPORT
from templates.INVOICE_TEMPLATE import INVOICE_TEMPLATE

st.set_page_config(layout="wide", page_title="DataAnno Ops Reporting")

st.sidebar.title("🛠️ Pipeline Config")

# 1. Configuration
DEFAULT_CSV_PATH = "s1_performance_summary.csv"
task_period = st.sidebar.text_input("Task Period", "23 Dec 2025 - 05 Jan 2026")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# 2. Source Selection Logic
df = None
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Using uploaded file.")
elif os.path.exists(DEFAULT_CSV_PATH):
    df = pd.read_csv(DEFAULT_CSV_PATH)
    st.sidebar.info(f"Auto-loaded: {os.path.basename(DEFAULT_CSV_PATH)}")
else:
    st.sidebar.warning("Please upload a CSV file to begin.")

# 3. Main Application Pipeline
if df is not None:
    # Clean data and get annotator list
    df, annotators = process_data(df) 
    
    tab1, tab2, tab3 = st.tabs(["🔍 Report Preview", "📦 Bulk Reports", "🧾 Invoices (Bulk & Single)"])

    # --- TAB 1: INDIVIDUAL PERFORMANCE ---
    with tab1:
        col_ed, col_pre = st.columns([1, 1])
        with col_ed:
            html_template = st.text_area("Live CSS Editor", value=S1_PERFORMANCE_REPORT, height=500)
        with col_pre:
            sel_name = st.selectbox("Select Annotator", annotators, key="perf_sel")
            data = get_performance_context(df, sel_name, task_period)
            rendered = Template(html_template).render(data["ctx"])
            st.components.v1.html(rendered, height=600, scrolling=True)
            if st.button("Generate PDF"):
                st.download_button("Download", generate_pdf_bytes(rendered), file_name=data["filename"])

    # --- TAB 2: BULK REPORTS ---
    with tab2:
        st.subheader("Bulk Performance Reports")
        if st.button("🚀 Bulk Generate All Performance Reports"):
            zip_buf = io.BytesIO()
            pb = st.progress(0)
            with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for i, name in enumerate(annotators):
                    data = get_performance_context(df, name, task_period)
                    html = Template(S1_PERFORMANCE_REPORT).render(data["ctx"])
                    zf.writestr(data["filename"], generate_pdf_bytes(html))
                    pb.progress((i + 1) / len(annotators))
            st.success("ZIP Ready!")
            st.download_button("📥 Download Reports ZIP", zip_buf.getvalue(), "Reports_Bulk.zip")

    # --- TAB 3: INVOICES (SINGLE & BULK) ---
    with tab3:
        inv_col1, inv_col2 = st.columns(2)
        with inv_col1:
            st.subheader("Individual Preview")
            inv_sel = st.selectbox("Select for Invoice", annotators, key="inv_sel")
            inv_data = get_invoice_context(df, inv_sel, task_period)
            inv_html = Template(INVOICE_TEMPLATE).render(inv_data["ctx"])
            st.components.v1.html(inv_html, height=600, scrolling=True)
            
            if st.button("Generate Single Invoice"):
                inv_pdf = generate_pdf_bytes(inv_html)
                st.download_button("Download PDF", data=inv_pdf, file_name=inv_data["filename"])

        with inv_col2:
            st.subheader("Bulk Export")
            st.write(f"Generate {len(annotators)} invoice templates.")
            if st.button("🚀 Bulk Generate All Invoices"):
                i_zip_buf = io.BytesIO()
                i_pb = st.progress(0)
                with zipfile.ZipFile(i_zip_buf, "w", zipfile.ZIP_DEFLATED) as i_zf:
                    for i, name in enumerate(annotators):
                        inv_d = get_invoice_context(df, name, task_period)
                        inv_h = Template(INVOICE_TEMPLATE).render(inv_d["ctx"])
                        try:
                            i_zf.writestr(inv_d["filename"], generate_pdf_bytes(inv_h))
                        except Exception as e:
                            st.error(f"Error for {name}: {e}")
                        i_pb.progress((i + 1) / len(annotators))
                st.success("Invoice ZIP Ready!")
                st.download_button("📥 Download Invoices ZIP", i_zip_buf.getvalue(), "Invoices_Bulk.zip")
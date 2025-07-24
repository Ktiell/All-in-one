import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="JobTracker+", layout="centered")

# Simple style
st.markdown("""
<style>
body { background-color: #f5f5dc; }
h1, h2, h3 { color: #4f6f52; font-family: 'Segoe UI', sans-serif; }
.stButton>button, .stDownloadButton>button {
    background-color: #4f6f52;
    color: white;
    border-radius: 8px;
    padding: 0.4rem 1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🧰 JobTracker+")

tab1, tab2, tab3 = st.tabs(["Tools & Materials", "Job Log", "Inventory"])

# -----------------------------
# TOOLS & MATERIAL TRACKER
# -----------------------------
with tab1:
    st.header("Tools & Materials")
    with st.form("tool_form"):
        tool = st.text_input("Tool or Material Name")
        location = st.text_input("Stored In / Location")
        quantity = st.number_input("Quantity", min_value=1, value=1)
        submit_tool = st.form_submit_button("Add Tool")
        if submit_tool and tool:
            new_row = {"Item": tool, "Location": location, "Quantity": quantity}
            st.session_state.setdefault("tools", []).append(new_row)
            st.success(f"Added: {tool}")

    tools_df = pd.DataFrame(st.session_state.get("tools", []))
    if not tools_df.empty:
        st.dataframe(tools_df)
        csv = tools_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Tools CSV", csv, "tools.csv", "text/csv")

# -----------------------------
# JOB LOGGER
# -----------------------------
with tab2:
    st.header("Job Logger")
    with st.form("job_form"):
        job_name = st.text_input("Job Name")
        start_time = st.time_input("Start Time", value=datetime.now().time())
        end_time = st.time_input("End Time", value=datetime.now().time())
        notes = st.text_area("Notes / Changes")
        photo = st.file_uploader("Attach Photo (optional)", type=["jpg", "png"])
        submit_job = st.form_submit_button("Log Job")
        if submit_job and job_name:
            log_row = {
                "Job": job_name,
                "Start": str(start_time),
                "End": str(end_time),
                "Notes": notes,
                "Photo": photo.name if photo else "None"
            }
            st.session_state.setdefault("jobs", []).append(log_row)
            st.success(f"Logged job: {job_name}")

    job_df = pd.DataFrame(st.session_state.get("jobs", []))
    if not job_df.empty:
        st.dataframe(job_df)
        job_csv = job_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Job Log CSV", job_csv, "job_log.csv", "text/csv")

# -----------------------------
# INVENTORY TRACKER
# -----------------------------
with tab3:
    st.header("Product Inventory")
    with st.form("inv_form"):
        item = st.text_input("Item Name")
        price = st.number_input("Price ($)", min_value=0.0)
        status = st.selectbox("Status", ["For Sale", "Sold"])
        inv_photo = st.file_uploader("Photo (optional)", type=["jpg", "png"])
        submit_inv = st.form_submit_button("Add to Inventory")
        if submit_inv and item:
            inv_row = {
                "Item": item,
                "Price": price,
                "Status": status,
                "Photo": inv_photo.name if inv_photo else "None"
            }
            st.session_state.setdefault("inventory", []).append(inv_row)
            st.success(f"Added to inventory: {item}")

    inv_df = pd.DataFrame(st.session_state.get("inventory", []))
    if not inv_df.empty:
        st.dataframe(inv_df)
        inv_csv = inv_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Inventory CSV", inv_csv, "inventory.csv", "text/csv")

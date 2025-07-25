import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(page_title="Board & Soul Estimator", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
    body {
        background-color: #f5f5dc;
    }
    section.main > div {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    h1, h2, h3, h4 {
        color: #4f6f52;
        font-family: 'Segoe UI', sans-serif;
    }
    hr {
        border: none;
        border-top: 1px solid #ccc;
        margin: 1rem 0;
    }
    .stButton>button {
        background-color: #4f6f52;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.image("https://i.imgur.com/fMMms9B.png", width=200)
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>Board & Soul Estimator</h1><hr>", unsafe_allow_html=True)

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["Inventory", "Tools", "Materials", "Job Hours"])

# --- Inventory ---
with tab1:
    st.subheader("Inventory")

    if "inventory" not in st.session_state:
        st.session_state.inventory = []

    with st.expander("➕ Add Inventory Item"):
        item = st.text_input("Item Name", key="inv_name")
        qty = st.number_input("Quantity", min_value=0, key="inv_qty")
        price = st.number_input("Price", min_value=0.0, format="%.2f", key="inv_price")
        if st.button("Add", key="add_inv"):
            st.session_state.inventory.append({"item": item, "qty": qty, "price": price})

    headers = st.columns([2, 1, 1, 2, 1])
    headers[0].markdown("**Item**")
    headers[1].markdown("**Qty**")
    headers[2].markdown("**Price**")
    headers[3].markdown("**Actions**")
    headers[4].markdown("**Delete**")

    for i, inv in enumerate(st.session_state.inventory):
        cols = st.columns([2, 1, 1, 2, 1])
        cols[0].write(inv["item"])
        cols[1].write(str(inv["qty"]))
        cols[2].write(f"${inv['price']:.2f}")

        with cols[3]:
            col_plus, col_minus = st.columns(2)
            if col_plus.button("➕", key=f"inc_inv_{i}"):
                st.session_state.inventory[i]["qty"] += 1
            if col_minus.button("➖", key=f"dec_inv_{i}"):
                st.session_state.inventory[i]["qty"] = max(0, st.session_state.inventory[i]["qty"] - 1)

        if cols[4].button("🗑️", key=f"del_inv_{i}"):
            st.session_state.inventory.pop(i)
            st.experimental_rerun()

# --- Tools ---
with tab2:
    st.subheader("Tools")
    if "tools" not in st.session_state:
        st.session_state.tools = []

    tool = st.text_input("Tool Name", key="tool_input")
    if st.button("Add Tool"):
        st.session_state.tools.append(tool)

    for i, tool in enumerate(st.session_state.tools):
        col1, col2 = st.columns([4, 1])
        col1.write(tool)
        if col2.button("🗑️", key=f"del_tool_{i}"):
            st.session_state.tools.pop(i)
            st.experimental_rerun()

# --- Materials ---
with tab3:
    st.subheader("Materials")
    if "materials" not in st.session_state:
        st.session_state.materials = []

    mat = st.text_input("Material", key="mat_input")
    if st.button("Add Material"):
        st.session_state.materials.append(mat)

    for i, mat in enumerate(st.session_state.materials):
        col1, col2 = st.columns([4, 1])
        col1.write(mat)
        if col2.button("🗑️", key=f"del_mat_{i}"):
            st.session_state.materials.pop(i)
            st.experimental_rerun()

# --- Job Hours ---
with tab4:
    st.subheader("Job Hours")

    if "job_log" not in st.session_state:
        st.session_state.job_log = []

    if "clock_running" not in st.session_state:
        st.session_state.clock_running = False

    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    desc = st.text_input("Job Description", key="job_desc")

    if not st.session_state.clock_running:
        if st.button("Start Clock"):
            st.session_state.start_time = time.time()
            st.session_state.clock_running = True
    else:
        if st.button("End Clock"):
            end_time = time.time()
            elapsed = round((end_time - st.session_state.start_time) / 3600, 2)
            st.session_state.job_log.append({"desc": desc, "hours": elapsed, "ts": datetime.now().strftime("%Y-%m-%d %H:%M")})
            st.session_state.clock_running = False

    st.markdown("### Logged Hours")

    total_week = sum(log["hours"] for log in st.session_state.job_log)
    st.write(f"**Total This Month:** {round(total_week, 2)} hours")

    for i, log in enumerate(st.session_state.job_log):
        col1, col2 = st.columns([5, 1])
        col1.write(f"{log['ts']} - {log['desc']} — {log['hours']} hrs")
        if col2.button("🗑️", key=f"del_log_{i}"):
            st.session_state.job_log.pop(i)
            st.experimental_rerun()

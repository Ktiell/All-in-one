import streamlit as st
import pandas as pd
import time
from datetime import datetime

# ---- Page Config ----
st.set_page_config(page_title="All in One", layout="centered")

# ---- Session State ----
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'tools' not in st.session_state:
    st.session_state.tools = []
if 'materials' not in st.session_state:
    st.session_state.materials = []
if 'job_logs' not in st.session_state:
    st.session_state.job_logs = []
if 'active_job' not in st.session_state:
    st.session_state.active_job = None

# ---- Tabs ----
tab1, tab2, tab3, tab4 = st.tabs(["Inventory", "Tools", "Materials", "Job Hours"])

# ---- INVENTORY TAB ----
with tab1:
    st.subheader("Add Inventory Item")
    item = st.text_input("Item Name", key="inv_name")
    qty = st.number_input("Quantity", min_value=0, step=1, key="inv_qty")
    price = st.number_input("Price", min_value=0.0, format="%.2f", step=0.5, key="inv_price")
    if st.button("Add", key="inv_add"):
        st.session_state.inventory.append({"item": item, "qty": qty, "price": price})

    st.markdown("## Current Inventory")
    if st.session_state.inventory:
        headers = st.columns([2, 1, 1, 2])
        headers[0].write("**Item**")
        headers[1].write("**Qty**")
        headers[2].write("**Price**")
        headers[3].write("**Actions**")

        for i, entry in enumerate(st.session_state.inventory):
            cols = st.columns([2, 1, 1, 2])
            cols[0].write(entry["item"])
            cols[1].write(entry["qty"])
            cols[2].write(f"${entry['price']:.2f}")
            with cols[3]:
                colA, colB, colC = st.columns(3)
                if colA.button("➕", key=f"add_{i}"):
                    st.session_state.inventory[i]["qty"] += 1
                if colB.button("➖", key=f"sub_{i}") and st.session_state.inventory[i]["qty"] > 0:
                    st.session_state.inventory[i]["qty"] -= 1
                if colC.button("🗑️", key=f"del_{i}"):
                    st.session_state.inventory.pop(i)
                    st.experimental_rerun()
    else:
        st.write("No items in inventory.")

# ---- TOOLS TAB ----
with tab2:
    st.subheader("Add Tool")
    tool = st.text_input("Tool Name", key="tool_input")
    if st.button("Add Tool"):
        if tool:
            st.session_state.tools.append(tool)

    st.markdown("## Tool List")
    for i, t in enumerate(st.session_state.tools):
        cols = st.columns([5, 1])
        cols[0].write(t)
        if cols[1].button("🗑️", key=f"del_tool_{i}"):
            st.session_state.tools.pop(i)
            st.experimental_rerun()

# ---- MATERIALS TAB ----
with tab3:
    st.subheader("Add Material")
    material = st.text_input("Material Name", key="mat_input")
    if st.button("Add Material"):
        if material:
            st.session_state.materials.append(material)

    st.markdown("## Material List")
    for i, m in enumerate(st.session_state.materials):
        cols = st.columns([5, 1])
        cols[0].write(m)
        if cols[1].button("🗑️", key=f"del_mat_{i}"):
            st.session_state.materials.pop(i)
            st.experimental_rerun()

# ---- JOB HOURS TAB ----
with tab4:
    st.subheader("Log Work Hours")

    desc = st.text_input("Job Description", key="job_desc")
    if st.session_state.active_job is None:
        if st.button("Start Clock"):
            st.session_state.active_job = {
                "desc": desc,
                "start": time.time()
            }
    else:
        if st.button("End Clock"):
            end_time = time.time()
            duration = round((end_time - st.session_state.active_job["start"]) / 3600, 2)
            st.session_state.job_logs.append({
                "desc": st.session_state.active_job["desc"],
                "start": datetime.fromtimestamp(st.session_state.active_job["start"]).strftime("%Y-%m-%d %H:%M"),
                "duration": duration
            })
            st.session_state.active_job = None

    st.markdown("## Logged Hours")
    total_week = 0
    total_month = 0
    now = datetime.now()

    for i, log in enumerate(st.session_state.job_logs):
        st.write(f"- **{log['desc']}** | {log['start']} | ⏱️ {log['duration']} hrs")
        log_time = datetime.strptime(log["start"], "%Y-%m-%d %H:%M")
        if log_time.isocalendar()[1] == now.isocalendar()[1]:
            total_week += log["duration"]
        if log_time.month == now.month:
            total_month += log["duration"]
        if st.button("❌ Delete", key=f"del_log_{i}"):
            st.session_state.job_logs.pop(i)
            st.experimental_rerun()

    st.markdown(f"**Total This Week:** {total_week:.2f} hrs")
    st.markdown(f"**Total This Month:** {total_month:.2f} hrs")

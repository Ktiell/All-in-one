import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="All in One", layout="centered")

# Custom CSS
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
.stButton>button {
    background-color: #4f6f52;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1 style='text-align: center;'>All in One</h1><hr>", unsafe_allow_html=True)

# Session state
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "tools" not in st.session_state:
    st.session_state.tools = []
if "materials" not in st.session_state:
    st.session_state.materials = []
if "job_logs" not in st.session_state:
    st.session_state.job_logs = []
if "clock" not in st.session_state:
    st.session_state.clock = {"active": False, "start": None}

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Inventory", "Tools", "Materials", "Job Hours"])

# ---------------- INVENTORY TAB ----------------
with tab1:
    st.subheader("Inventory")
    with st.expander("➕ Add Inventory Item"):
        item = st.text_input("Item Name", key="inv_name")
        qty = st.number_input("Quantity", min_value=0, step=1, key="inv_qty")
        price = st.number_input("Price", min_value=0.0, step=0.01, key="inv_price")
        if st.button("Add", key="inv_add_btn"):
            st.session_state.inventory.append({"name": item, "qty": qty, "price": price})

    # Headers
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 2, 1])
    col1.markdown("**Item**")
    col2.markdown("**Qty**")
    col3.markdown("**Price**")
    col4.markdown("**Actions**")
    col5.markdown("**Delete**")

    for i, item in enumerate(st.session_state.inventory):
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 2, 1])
        col1.markdown(item["name"])
        col2.markdown(str(item["qty"]))
        col3.markdown(f"${item['price']:.2f}")
        with col4:
            plus, minus = st.columns(2)
            if plus.button("➕", key=f"inv_add_{i}"):
                st.session_state.inventory[i]["qty"] += 1
            if minus.button("➖", key=f"inv_sub_{i}"):
                if st.session_state.inventory[i]["qty"] > 0:
                    st.session_state.inventory[i]["qty"] -= 1
        with col5:
            if st.button("🗑️", key=f"inv_del_{i}"):
                st.session_state.inventory.pop(i)
                st.experimental_rerun()

# ---------------- TOOLS TAB ----------------
with tab2:
    st.subheader("Tools")
    with st.expander("➕ Add Tool"):
        tool = st.text_input("Tool Name", key="tool_name")
        qty = st.number_input("Quantity", min_value=0, step=1, key="tool_qty")
        if st.button("Add", key="tool_add_btn"):
            st.session_state.tools.append({"name": tool, "qty": qty})

    col1, col2, col3, col4 = st.columns([4, 1, 3, 1])
    col1.markdown("**Item**")
    col2.markdown("**Qty**")
    col3.markdown("**Actions**")
    col4.markdown("**Delete**")

    for i, tool in enumerate(st.session_state.tools):
        col1, col2, col3, col4 = st.columns([4, 1, 3, 1])
        col1.markdown(tool["name"])
        col2.markdown(str(tool["qty"]))
        with col3:
            plus, minus = st.columns(2)
            if plus.button("➕", key=f"tool_add_{i}"):
                st.session_state.tools[i]["qty"] += 1
            if minus.button("➖", key=f"tool_sub_{i}"):
                if st.session_state.tools[i]["qty"] > 0:
                    st.session_state.tools[i]["qty"] -= 1
        with col4:
            if st.button("🗑️", key=f"tool_del_{i}"):
                st.session_state.tools.pop(i)
                st.experimental_rerun()

# ---------------- MATERIALS TAB ----------------
with tab3:
    st.subheader("Materials")
    with st.expander("➕ Add Material"):
        mat = st.text_input("Material Name", key="mat_name")
        qty = st.number_input("Quantity", min_value=0, step=1, key="mat_qty")
        if st.button("Add", key="mat_add_btn"):
            st.session_state.materials.append({"name": mat, "qty": qty})

    col1, col2, col3, col4 = st.columns([4, 1, 3, 1])
    col1.markdown("**Item**")
    col2.markdown("**Qty**")
    col3.markdown("**Actions**")
    col4.markdown("**Delete**")

    for i, mat in enumerate(st.session_state.materials):
        col1, col2, col3, col4 = st.columns([4, 1, 3, 1])
        col1.markdown(mat["name"])
        col2.markdown(str(mat["qty"]))
        with col3:
            plus, minus = st.columns(2)
            if plus.button("➕", key=f"mat_add_{i}"):
                st.session_state.materials[i]["qty"] += 1
            if minus.button("➖", key=f"mat_sub_{i}"):
                if st.session_state.materials[i]["qty"] > 0:
                    st.session_state.materials[i]["qty"] -= 1
        with col4:
            if st.button("🗑️", key=f"mat_del_{i}"):
                st.session_state.materials.pop(i)
                st.experimental_rerun()

# ---------------- JOB HOURS TAB ----------------
with tab4:
    st.subheader("Job Hours")
    desc = st.text_input("Task Description", key="job_desc")
    if not st.session_state.clock["active"]:
        if st.button("Start Clock"):
            st.session_state.clock["active"] = True
            st.session_state.clock["start"] = datetime.now()
            st.experimental_rerun()
    else:
        if st.button("End Clock"):
            end_time = datetime.now()
            start_time = st.session_state.clock["start"]
            duration = (end_time - start_time).total_seconds() / 3600
            st.session_state.job_logs.append({
                "desc": desc,
                "start": start_time,
                "end": end_time,
                "hours": round(duration, 2)
            })
            st.session_state.clock["active"] = False
            st.session_state.clock["start"] = None
            st.experimental_rerun()

    week_hours = sum(log["hours"] for log in st.session_state.job_logs
                     if log["start"].isocalendar()[1] == datetime.now().isocalendar()[1])
    month_hours = sum(log["hours"] for log in st.session_state.job_logs
                      if log["start"].month == datetime.now().month)

    st.markdown(f"**Total This Week:** {week_hours:.2f} hrs")
    st.markdown(f"**Total This Month:** {month_hours:.2f} hrs")

    for i, log in enumerate(st.session_state.job_logs):
        st.write(f"🛠️ **{log['desc']}** — ⏱️ {log['hours']} hrs")
        if st.button("Delete", key=f"log_del_{i}"):
            st.session_state.job_logs.pop(i)
            st.experimental_rerun()

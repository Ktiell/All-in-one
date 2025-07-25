import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(page_title="All in One", layout="centered")

# Custom style
st.markdown("""
<style>
.stButton>button {
    background-color: #4f6f52;
    color: white;
    border-radius: 8px;
    padding: 0.3rem 1rem;
    margin: 0.1rem;
}
.stTextInput>div>input {
    padding: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

# Init session state
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "tools" not in st.session_state:
    st.session_state.tools = []
if "materials" not in st.session_state:
    st.session_state.materials = []
if "job_logs" not in st.session_state:
    st.session_state.job_logs = []
if "clock_running" not in st.session_state:
    st.session_state.clock_running = False
    st.session_state.start_time = None

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Inventory", "Tools", "Materials", "Job Hours"])

# ---------------- INVENTORY ----------------
with tab1:
    st.header("Inventory")
    with st.form("add_inventory"):
        c1, c2, c3 = st.columns([3, 1, 2])
        item = c1.text_input("Item")
        qty = c2.number_input("Qty", min_value=0, step=1)
        price = c3.number_input("Price", min_value=0.0, step=0.5)
        if st.form_submit_button("Add"):
            if item:
                st.session_state.inventory.append({"item": item, "qty": qty, "price": price})

    if st.session_state.inventory:
        st.subheader("Current Inventory")
        header = st.columns([3, 1, 2, 1, 1, 1])
        header[0].write("**Item**")
        header[1].write("**Qty**")
        header[2].write("**Price**")
        header[3].write("**➕**")
        header[4].write("**➖**")
        header[5].write("**🗑️**")

        for i, entry in enumerate(st.session_state.inventory):
            row = st.columns([3, 1, 2, 1, 1, 1])
            row[0].write(entry["item"])
            row[1].write(entry["qty"])
            row[2].write(f"${entry['price']:.2f}")
            if row[3].button("+", key=f"add_{i}"):
                st.session_state.inventory[i]["qty"] += 1
            if row[4].button("-", key=f"sub_{i}"):
                st.session_state.inventory[i]["qty"] = max(0, entry["qty"] - 1)
            if row[5].button("🗑️", key=f"del_{i}"):
                st.session_state.inventory.pop(i)
                st.experimental_rerun()
    else:
        st.info("No inventory yet.")

# ---------------- TOOLS ----------------
with tab2:
    st.header("Tools")
    tool = st.text_input("Add Tool", key="tool_input")
    if st.button("Add Tool"):
        if tool:
            st.session_state.tools.append(tool)
            st.experimental_rerun()
    for i, t in enumerate(st.session_state.tools):
        cols = st.columns([6, 1])
        cols[0].write(t)
        if cols[1].button("🗑️", key=f"tool_del_{i}"):
            st.session_state.tools.pop(i)
            st.experimental_rerun()

# ---------------- MATERIALS ----------------
with tab3:
    st.header("Materials")
    material = st.text_input("Add Material", key="mat_input")
    if st.button("Add Material"):
        if material:
            st.session_state.materials.append(material)
            st.experimental_rerun()
    for i, m in enumerate(st.session_state.materials):
        cols = st.columns([6, 1])
        cols[0].write(m)
        if cols[1].button("🗑️", key=f"mat_del_{i}"):
            st.session_state.materials.pop(i)
            st.experimental_rerun()

# ---------------- JOB HOURS ----------------
with tab4:
    st.header("Job Hours")
    desc = st.text_input("Job Description")
    if not st.session_state.clock_running:
        if st.button("Start Clock"):
            st.session_state.start_time = datetime.now()
            st.session_state.clock_running = True
            st.session_state.current_desc = desc
    else:
        if st.button("End Clock"):
            end_time = datetime.now()
            duration = (end_time - st.session_state.start_time).total_seconds() / 3600
            st.session_state.job_logs.append({
                "desc": st.session_state.current_desc,
                "start": st.session_state.start_time,
                "end": end_time,
                "hours": round(duration, 2)
            })
            st.session_state.clock_running = False
            st.session_state.start_time = None

    st.subheader("Log")
    now = datetime.now()
    week_total = 0
    month_total = 0

    for i, log in enumerate(st.session_state.job_logs):
        if log["start"].isocalendar()[1] == now.isocalendar()[1]:
            week_total += log["hours"]
        if log["start"].month == now.month:
            month_total += log["hours"]
        cols = st.columns([4, 2, 2, 2, 1])
        cols[0].write(log["desc"])
        cols[1].write(log["start"].strftime("%m/%d %H:%M"))
        cols[2].write(log["end"].strftime("%m/%d %H:%M"))
        cols[3].write(f"{log['hours']:.2f} hrs")
        if cols[4].button("🗑️", key=f"log_del_{i}"):
            st.session_state.job_logs.pop(i)
            st.experimental_rerun()

    st.markdown(f"**Total This Week:** {week_total:.2f} hrs")
    st.markdown(f"**Total This Month:** {month_total:.2f} hrs")

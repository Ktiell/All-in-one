import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="All in One", layout="centered")
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

# Session states
if "inventory" not in st.session_state:
    st.session_state.inventory = []

if "tools" not in st.session_state:
    st.session_state.tools = ["Hammer", "Drill", "Saw"]

if "materials" not in st.session_state:
    st.session_state.materials = ["Cedar", "Glue", "Walnut"]

if "job_log" not in st.session_state:
    st.session_state.job_log = []

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Inventory", "Tools", "Materials", "Job Hours"])

# ---------------- INVENTORY ----------------
with tab1:
    st.header("Inventory")
    with st.form("add_item"):
        c1, c2, c3 = st.columns([3, 2, 2])
        item = c1.text_input("Item")
        qty = c2.number_input("Qty", min_value=0, step=1)
        price = c3.number_input("Price", min_value=0.0, step=0.5)
        add = st.form_submit_button("Add")
        if add and item:
            st.session_state.inventory.append({"item": item, "qty": qty, "price": price})

    st.subheader("Current Inventory")
    for idx, row in enumerate(st.session_state.inventory):
        col1, col2, col3, col4, col5 = st.columns([3, 1, 2, 3, 2])
        col1.write(row["item"])
        col2.write(row["qty"])
        col3.write(f"${row['price']:.2f}")
        if col4.button("+", key=f"add_{idx}"):
            st.session_state.inventory[idx]["qty"] += 1
        if col4.button("-", key=f"sub_{idx}") and row["qty"] > 0:
            st.session_state.inventory[idx]["qty"] -= 1
        if col5.button("🗑️", key=f"del_{idx}"):
            st.session_state.inventory.pop(idx)
            st.experimental_rerun()

# ---------------- TOOLS ----------------
with tab2:
    st.header("Tools")
    tool_input = st.text_input("Add Tool", key="tool_input")
    if st.button("Add Tool"):
        if tool_input:
            st.session_state.tools.append(tool_input)
            st.experimental_rerun()
    for i, tool in enumerate(st.session_state.tools):
        cols = st.columns([8, 1])
        cols[0].write(tool)
        if cols[1].button("🗑️", key=f"tool_del_{i}"):
            st.session_state.tools.pop(i)
            st.experimental_rerun()

# ---------------- MATERIALS ----------------
with tab3:
    st.header("Materials")
    mat_input = st.text_input("Add Material", key="mat_input")
    if st.button("Add Material"):
        if mat_input:
            st.session_state.materials.append(mat_input)
            st.experimental_rerun()
    for i, mat in enumerate(st.session_state.materials):
        cols = st.columns([8, 1])
        cols[0].write(mat)
        if cols[1].button("🗑️", key=f"mat_del_{i}"):
            st.session_state.materials.pop(i)
            st.experimental_rerun()

# ---------------- JOB HOURS ----------------
with tab4:
    st.header("Job Hours")
    desc = st.text_input("Job Description")
    if "clock_running" not in st.session_state:
        st.session_state.clock_running = False
        st.session_state.start_time = None

    if not st.session_state.clock_running:
        if st.button("Start Clock"):
            st.session_state.start_time = pd.Timestamp.now()
            st.session_state.clock_running = True
    else:
        if st.button("End Clock"):
            end_time = pd.Timestamp.now()
            duration = (end_time - st.session_state.start_time).total_seconds() / 3600
            st.session_state.job_log.append({
                "desc": desc,
                "start": st.session_state.start_time,
                "end": end_time,
                "hours": round(duration, 2)
            })
            st.session_state.clock_running = False

    st.subheader("Job Log")
    total_week = 0
    total_month = 0
    now = pd.Timestamp.now()
    for i, log in enumerate(st.session_state.job_log):
        log_date = log["start"]
        if log_date.isocalendar().week == now.isocalendar().week:
            total_week += log["hours"]
        if log_date.month == now.month:
            total_month += log["hours"]
        cols = st.columns([4, 2, 2, 2, 1])
        cols[0].write(f"**{log['desc']}**")
        cols[1].write(log["start"].strftime("%m/%d %H:%M"))
        cols[2].write(log["end"].strftime("%m/%d %H:%M"))
        cols[3].write(f"{log['hours']} hrs")
        if cols[4].button("🗑️", key=f"log_del_{i}"):
            st.session_state.job_log.pop(i)
            st.experimental_rerun()

    st.markdown(f"**Total This Week:** {round(total_week, 2)} hrs")
    st.markdown(f"**Total This Month:** {round(total_month, 2)} hrs")

import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- PAGE CONFIG & STYLE ---
st.set_page_config(page_title="All in One", layout="centered")
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
.stButton>button, .stDownloadButton>button {
    background-color: #4f6f52;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    border: none;
}
</style>
""", unsafe_allow_html=True)

st.title("All in One")

# --- SESSION STATE SETUP ---
for key in ['inventory', 'tools', 'materials', 'job_log', 'clock_running', 'start_time']:
    if key not in st.session_state:
        st.session_state[key] = [] if 'log' in key or key in ['inventory', 'tools', 'materials'] else False

# --- INVENTORY TAB ---
def inventory_tab():
    st.header("Inventory")

    col1, col2 = st.columns(2)
    with col1:
        item = st.text_input("Item Name")
        qty = st.number_input("Quantity", min_value=0, step=1)
    with col2:
        price = st.number_input("Price", min_value=0.0, format="%.2f", step=0.5)

    if st.button("Add", type="primary"):
        if item:
            st.session_state.inventory.append({'item': item, 'qty': qty, 'price': price})

    if st.session_state.inventory:
        st.markdown("### Current Inventory")
        for i, row in enumerate(st.session_state.inventory):
            cols = st.columns([2, 1, 1, 1, 1])
            cols[0].write(row['item'])
            cols[1].write(str(row['qty']))
            cols[2].write(f"${row['price']:.2f}")
            if cols[3].button("➕", key=f"plus_{i}"):
                st.session_state.inventory[i]['qty'] += 1
            if cols[3].button("➖", key=f"minus_{i}"):
                st.session_state.inventory[i]['qty'] = max(0, row['qty'] - 1)
            if cols[4].button("🗑️", key=f"delete_{i}"):
                st.session_state.inventory.pop(i)
                st.experimental_rerun()

# --- TOOLS TAB ---
def tools_tab():
    st.header("Tools")
    tool = st.text_input("Tool Name", key="tool_input")
    if st.button("Add Tool"):
        if tool:
            st.session_state.tools.append(tool)
    if st.session_state.tools:
        st.markdown("### Tool List")
        for i, t in enumerate(st.session_state.tools):
            cols = st.columns([5, 1])
            cols[0].write(t)
            if cols[1].button("🗑️", key=f"tool_del_{i}"):
                st.session_state.tools.pop(i)
                st.experimental_rerun()

# --- MATERIALS TAB ---
def materials_tab():
    st.header("Materials")
    material = st.text_input("Material Name", key="material_input")
    if st.button("Add Material"):
        if material:
            st.session_state.materials.append(material)
    if st.session_state.materials:
        st.markdown("### Material List")
        for i, m in enumerate(st.session_state.materials):
            cols = st.columns([5, 1])
            cols[0].write(m)
            if cols[1].button("🗑️", key=f"mat_del_{i}"):
                st.session_state.materials.pop(i)
                st.experimental_rerun()

# --- JOB HOURS TAB ---
def job_hours_tab():
    st.header("Job Hours")
    desc = st.text_input("Task Description")

    if not st.session_state.clock_running:
        if st.button("Start Clock"):
            st.session_state.start_time = time.time()
            st.session_state.job_log.append({"desc": desc, "start": datetime.now(), "end": None})
            st.session_state.clock_running = True
    else:
        if st.button("End Clock"):
            end_time = time.time()
            duration = round((end_time - st.session_state.start_time) / 3600, 2)
            st.session_state.job_log[-1]['end'] = datetime.now()
            st.session_state.job_log[-1]['duration'] = duration
            st.session_state.clock_running = False

    if st.session_state.job_log:
        st.markdown("### Logged Hours")
        total_week = 0
        total_month = 0
        now = datetime.now()
        for i, log in enumerate(st.session_state.job_log):
            start_time = log['start']
            duration = log.get('duration', 0)
            if start_time.isocalendar()[1] == now.isocalendar()[1]:
                total_week += duration
            if start_time.month == now.month:
                total_month += duration

            st.write(f"- {log['desc']} | {duration:.2f} hrs | {start_time.strftime('%m/%d %H:%M')} to {log['end'].strftime('%H:%M') if log['end'] else '...'}")
            if st.button("🗑️", key=f"job_del_{i}"):
                st.session_state.job_log.pop(i)
                st.experimental_rerun()

        st.write(f"**Total this week:** {total_week:.2f} hrs")
        st.write(f"**Total this month:** {total_month:.2f} hrs")

# --- MAIN APP ---
tabs = {
    "Inventory": inventory_tab,
    "Tools": tools_tab,
    "Materials": materials_tab,
    "Job Hours": job_hours_tab
}
selected_tab = st.tabs(list(tabs.keys()))
for i, name in enumerate(tabs):
    with selected_tab[i]:
        tabs[name]()


import streamlit as st
from fractions import Fraction
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="All in One", layout="wide")
st.markdown("## ðŸ“‹ All in One")

# Session state setup
if "inventory" not in st.session_state: st.session_state.inventory = []
if "tools" not in st.session_state: st.session_state.tools = []
if "materials" not in st.session_state: st.session_state.materials = []
if "labor_log" not in st.session_state: st.session_state.labor_log = []
if "clock" not in st.session_state: st.session_state.clock = {"is_running": False, "start": None}

tabs = st.tabs(["Inventory", "Tools", "Materials", "Labor Log"])

# Inventory tab
with tabs[0]:
    st.subheader("Inventory")
    status_filter = st.selectbox("Status", ["For Sale", "Sold"])
    name = st.text_input("Item Name")
    qty = st.number_input("Qty", 1, step=1)
    price = st.number_input("Price", 0.0, step=0.01)
    if st.button("Add Inventory Item"):
        st.session_state.inventory.append({"name": name, "qty": qty, "price": price, "status": status_filter})
    for i, item in enumerate(sorted(st.session_state.inventory, key=lambda x: x["name"])):
        st.text(f"{item['name']} - Qty: {item['qty']} - ${item['price']:.2f} - {item['status']}")
        col1, col2 = st.columns(2)
        with col1:
            item["status"] = st.selectbox(f"Status", ["For Sale", "Sold"], key=f"inv_status_{i}")
        with col2:
            if st.button("ðŸ—‘ï¸", key=f"inv_delete_{i}"):
                st.session_state.inventory.pop(i)
                st.experimental_rerun()

# Tools tab
with tabs[1]:
    st.subheader("Tools")
    tool = st.text_input("Tool Name")
    if st.button("Add Tool"):
        st.session_state.tools.append(tool)
    for i, t in enumerate(sorted(st.session_state.tools)):
        col1, col2 = st.columns([3,1])
        col1.text(t)
        if col2.button("ðŸ—‘ï¸", key=f"tool_delete_{i}"):
            st.session_state.tools.pop(i)
            st.experimental_rerun()

# Materials tab
with tabs[2]:
    st.subheader("Materials")
    material = st.text_input("Material Name")
    if st.button("Add Material"):
        st.session_state.materials.append(material)
    for i, m in enumerate(sorted(st.session_state.materials)):
        col1, col2 = st.columns([3,1])
        col1.text(m)
        if col2.button("ðŸ—‘ï¸", key=f"material_delete_{i}"):
            st.session_state.materials.pop(i)
            st.experimental_rerun()

# Labor Log tab
with tabs[3]:
    st.subheader("Labor Log")
    task = st.text_input("Task Description", key="task_desc")
    if not st.session_state.clock["is_running"]:
        if st.button("Start Clock"):
            st.session_state.clock["is_running"] = True
            st.session_state.clock["start"] = datetime.now()
            st.rerun()
    else:
        if st.button("Stop Clock"):
            end_time = datetime.now()
            duration = (end_time - st.session_state.clock["start"]).total_seconds() / 3600
            st.session_state.labor_log.append({
                "task": st.session_state.task_desc,
                "start": st.session_state.clock["start"],
                "end": end_time,
                "hours": round(duration, 2)
            })
            st.session_state.clock["is_running"] = False
            st.session_state.clock["start"] = None
            st.session_state.task_desc = ""
            st.rerun()
        st.success("Clock running...")

    # Summary
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)

    hours_today = sum(e["hours"] for e in st.session_state.labor_log if e["start"].date() == today)
    hours_week = sum(e["hours"] for e in st.session_state.labor_log if e["start"].date() >= week_start)
    hours_month = sum(e["hours"] for e in st.session_state.labor_log if e["start"].date() >= month_start)
    hours_year = sum(e["hours"] for e in st.session_state.labor_log if e["start"].date() >= year_start)

    st.write(f"**Hours Today:** {hours_today:.2f} hrs")
    st.write(f"**Hours This Week:** {hours_week:.2f} hrs")
    st.write(f"**Hours This Month:** {hours_month:.2f} hrs")
    st.write(f"**Hours This Year:** {hours_year:.2f} hrs")

    # Manual entries
    with st.expander("âž• New Manual Log Entry"):
        manual_task = st.text_input("Task")
        manual_hours = st.number_input("Hours Worked", 0.0, step=0.25)
        if st.button("Add Manual Entry"):
            st.session_state.labor_log.append({
                "task": manual_task,
                "start": datetime.now(),
                "end": datetime.now(),
                "hours": manual_hours
            })
            st.success("Manual entry added.")

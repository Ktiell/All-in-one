import streamlit as st
from fractions import Fraction
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="All in One", layout="wide")
st.markdown("## 📋 All in One")

# Session state
if "inventory" not in st.session_state: st.session_state.inventory = []
if "tools" not in st.session_state: st.session_state.tools = []
if "materials" not in st.session_state: st.session_state.materials = []
if "labor_log" not in st.session_state: st.session_state.labor_log = []
if "clock" not in st.session_state: st.session_state.clock = {"is_running": False, "start": None}
if "task_desc" not in st.session_state: st.session_state.task_desc = ""

tabs = st.tabs(["Inventory", "Tools", "Materials", "Labor Log"])

# --------------------
# Inventory Tab
# --------------------
with tabs[0]:
    st.subheader("Inventory")

    name = st.text_input("Item Name")
    qty = st.number_input("Qty", 1, step=1)
    price = st.number_input("Price", 0.0, step=0.01)

    if st.button("Add Inventory Item"):
        st.session_state.inventory.append({"name": name, "qty": qty, "price": price})
        st.rerun()

    st.markdown("### Current Inventory")

    if not st.session_state.inventory:
        st.info("No inventory items yet.")
    else:
        headers = st.columns([4, 1, 3])
        headers[0].markdown("**Item**")
        headers[1].markdown("**Qty**")
        headers[2].markdown("**Actions**")

        for i, item in enumerate(sorted(st.session_state.inventory, key=lambda x: x["name"])):
            col1, col2, col3 = st.columns([4, 1, 3])
            col1.write(item["name"])
            col2.write(str(item["qty"]))
            with col3:
                plus, minus, delete = st.columns(3)
                if plus.button("+", key=f"plus_{i}"):
                    item["qty"] += 1
                    st.rerun()
                if minus.button("-", key=f"minus_{i}"):
                    if item["qty"] > 0:
                        item["qty"] -= 1
                        st.rerun()
                if delete.button("X", key=f"del_{i}"):
                    st.session_state.inventory.pop(i)
                    st.rerun()

# --------------------
# Tools Tab
# --------------------
with tabs[1]:
    st.subheader("Tools")
    tool = st.text_input("Tool Name")
    if st.button("Add Tool"):
        st.session_state.tools.append(tool)
        st.rerun()
    
    for i, t in enumerate(sorted(st.session_state.tools)):
        col1, col2 = st.columns([3, 1])
        col1.text(t)
        if col2.button("Delete", key=f"tool_delete_{i}"):
            st.session_state.tools.pop(i)
            st.rerun()

# --------------------
# Materials Tab
# --------------------
with tabs[2]:
    st.subheader("Materials")
    material = st.text_input("Material Name")
    if st.button("Add Material"):
        st.session_state.materials.append(material)
        st.rerun()
    
    for m in sorted(st.session_state.materials):
        col1, col2 = st.columns([3, 1])
        col1.text(m)
        if col2.button("Delete", key=f"material_delete_{m}"):
            st.session_state.materials.remove(m)
            st.rerun()

# --------------------
# Labor Log Tab
# --------------------
with tabs[3]:
    st.subheader("Labor Log")

    st.session_state.task_desc = st.text_input("Task Description", value=st.session_state.task_desc)

    if not st.session_state.clock["is_running"]:
        if st.button("Start Clock"):
            st.session_state.clock["is_running"] = True
            st.session_state.clock["start"] = datetime.now()
            st.rerun()
    else:
        st.success("Clock running...")
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

    # Log list with delete buttons
    if st.session_state.labor_log:
        st.write("### Logged Sessions")
        for i, log in enumerate(st.session_state.labor_log):
            st.write(f"{log['task']} | {log['start'].strftime('%Y-%m-%d %H:%M')} – {log['end'].strftime('%H:%M')} | {log['hours']:.2f} hrs")
            if st.button("Delete Log Entry", key=f"del_log_{i}"):
                st.session_state.labor_log.pop(i)
                st.rerun()

    # Manual Entry
    with st.expander("➕ New Manual Log Entry"):
        manual_task = st.text_input("Manual Task")
        manual_hours = st.number_input("Hours Worked", 0.0, step=0.25)
        if st.button("Add Manual Entry"):
            now = datetime.now()
            st.session_state.labor_log.append({
                "task": manual_task,
                "start": now,
                "end": now,
                "hours": manual_hours
            })
            st.success("Manual entry added.")
            st.rerun()

import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="All in One", layout="wide")

# --- Init ---
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "clock_start" not in st.session_state:
    st.session_state.clock_start = None
if "job_logs" not in st.session_state:
    st.session_state.job_logs = []

# --- INVENTORY TAB ---
tab1, tab2 = st.tabs(["Inventory", "Job Hours"])

with tab1:
    st.header("Inventory")

    # Header row
    header = st.columns([3, 1, 2, 1])
    header[0].markdown("**Item**")
    header[1].markdown("**Qty**")
    header[2].markdown("**Actions**")
    header[3].markdown("**Delete**")

    # Inventory rows
    for i, item in enumerate(st.session_state.inventory):
        row = st.columns([3, 1, 2, 1])
        row[0].markdown(item["item"])
        row[1].markdown(str(item["qty"]))

        col_plus, col_minus = row[2].columns(2)
        if col_plus.button("➕", key=f"plus_{i}"):
            item["qty"] += 1
            st.experimental_rerun()
        if col_minus.button("➖", key=f"minus_{i}"):
            if item["qty"] > 0:
                item["qty"] -= 1
                st.experimental_rerun()

        if row[3].button("🗑️", key=f"delete_{i}"):
            st.session_state.inventory.pop(i)
            st.experimental_rerun()

    # Add new item
    with st.expander("➕ Add Inventory Item"):
        with st.form("add_inventory"):
            item = st.text_input("Item Name")
            qty = st.number_input("Quantity", min_value=0, step=1)
            if st.form_submit_button("Add"):
                if item:
                    st.session_state.inventory.append({"item": item, "qty": int(qty)})
                    st.success(f"Added: {item}")
                    st.experimental_rerun()

# --- JOB HOURS TAB ---
with tab2:
    st.header("Job Clock")

    desc = st.text_input("Task Description")

    if st.session_state.clock_start is None:
        if st.button("Start Clock"):
            st.session_state.clock_start = datetime.now()
    else:
        try:
            st.markdown(f"**Started:** {st.session_state.clock_start.strftime('%I:%M:%S %p')}")
        except:
            st.warning("Start time not set.")
        if st.button("End Clock"):
            end_time = datetime.now()
            duration = end_time - st.session_state.clock_start
            minutes = int(duration.total_seconds() / 60)
            st.session_state.job_logs.append({
                "desc": desc or "No description",
                "start": st.session_state.clock_start,
                "end": end_time,
                "minutes": minutes
            })
            st.session_state.clock_start = None
            st.success(f"Logged {minutes} minutes")
            st.experimental_rerun()

    st.subheader("Job Log History")
    week_total = 0
    month_total = 0
    now = datetime.now()

    for i, log in enumerate(st.session_state.job_logs):
        st.markdown(f"- **{log['desc']}** | {log['minutes']} min | {log['start'].strftime('%m/%d %I:%M %p')}")
        if st.button("Delete", key=f"log_delete_{i}"):
            st.session_state.job_logs.pop(i)
            st.experimental_rerun()
        if log["start"].date() >= (now - timedelta(days=7)).date():
            week_total += log["minutes"]
        if log["start"].month == now.month and log["start"].year == now.year:
            month_total += log["minutes"]

    st.markdown(f"**Total This Week:** {round(week_total / 60, 2)} hrs")
    st.markdown(f"**Total This Month:** {round(month_total / 60, 2)} hrs")

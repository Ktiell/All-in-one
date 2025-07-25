import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="All in One", layout="wide")

# --- Initialize State ---
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "clock_start" not in st.session_state:
    st.session_state.clock_start = None
if "job_logs" not in st.session_state:
    st.session_state.job_logs = []

# --- Tabs ---
tab1, tab2 = st.tabs(["Inventory", "Job Hours"])

# === INVENTORY TAB ===
with tab1:
    st.header("Inventory")

    # Header
    cols = st.columns([3, 1, 2, 1])
    cols[0].markdown("**Item**")
    cols[1].markdown("**Qty**")
    cols[2].markdown("**Actions**")
    cols[3].markdown("**Delete**")

    # Inventory Rows
    for i, item in enumerate(st.session_state.inventory):
        row = st.columns([3, 1, 2, 1])
        row[0].markdown(item["item"])
        row[1].markdown(str(item["qty"]))

        btn_plus, btn_minus = row[2].columns(2)
        if btn_plus.button("➕", key=f"plus_{i}"):
            item["qty"] += 1
            st.experimental_rerun()
        if btn_minus.button("➖", key=f"minus_{i}"):
            if item["qty"] > 0:
                item["qty"] -= 1
                st.experimental_rerun()

        if row[3].button("🗑️", key=f"del_{i}"):
            st.session_state.inventory.pop(i)
            st.experimental_rerun()

    # Add Item Form
    with st.expander("➕ Add Inventory Item"):
        with st.form("add_inventory"):
            item = st.text_input("Item Name")
            qty = st.number_input("Quantity", min_value=0, step=1)
            if st.form_submit_button("Add"):
                if item:
                    st.session_state.inventory.append({"item": item, "qty": int(qty)})
                    st.success(f"Added: {item}")
                    st.experimental_rerun()

# === JOB HOURS TAB ===
with tab2:
    st.header("Job Clock")
    desc = st.text_input("Task Description")

    if st.session_state.clock_start is None:
        if st.button("Start Clock"):
            st.session_state.clock_start = datetime.now()
    else:
        start_time = st.session_state.clock_start
        if isinstance(start_time, datetime):
            st.markdown(f"**Started:** {start_time.strftime('%I:%M:%S %p')}")
        else:
            st.warning("⚠️ Invalid start time.")
        if st.button("End Clock"):
            end_time = datetime.now()
            minutes = int((end_time - start_time).total_seconds() / 60)
            st.session_state.job_logs.append({
                "desc": desc or "No description",
                "start": start_time,
                "end": end_time,
                "minutes": minutes
            })
            st.session_state.clock_start = None
            st.success(f"Logged {minutes} minutes")
            st.experimental_rerun()

    # Job Log
    st.subheader("Job Log History")
    total_week = total_month = 0
    now = datetime.now()

    for i, log in enumerate(st.session_state.job_logs):
        try:
            started = log["start"]
            line = f"- **{log['desc']}** | {log['minutes']} min"
            if isinstance(started, datetime):
                line += f" | {started.strftime('%m/%d %I:%M %p')}"
        except:
            line = f"- **{log['desc']}** | {log['minutes']} min"

        st.markdown(line)

        if st.button("Delete", key=f"log_del_{i}"):
            st.session_state.job_logs.pop(i)
            st.experimental_rerun()

        if isinstance(log.get("start"), datetime):
            if log["start"].date() >= (now - timedelta(days=7)).date():
                total_week += log["minutes"]
            if log["start"].month == now.month and log["start"].year == now.year:
                total_month += log["minutes"]

    st.markdown(f"**This Week:** {round(total_week / 60, 2)} hrs")
    st.markdown(f"**This Month:** {round(total_month / 60, 2)} hrs")

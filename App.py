import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="All in One", layout="wide")

# Initialize
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "clock_start" not in st.session_state:
    st.session_state.clock_start = None
if "job_logs" not in st.session_state:
    st.session_state.job_logs = []

# Tabs
tab1, tab2 = st.tabs(["Inventory", "Job Hours"])

# === INVENTORY TAB ===
with tab1:
    st.header("Inventory")

    # Header Row
    col_hdr = st.columns([3, 1, 1, 2, 1])
    col_hdr[0].markdown("**Item**")
    col_hdr[1].markdown("**Qty**")
    col_hdr[2].markdown("**Price**")
    col_hdr[3].markdown("**Actions**")
    col_hdr[4].markdown("**Delete**")

    # Inventory Rows
    for i, item in enumerate(st.session_state.inventory):
        cols = st.columns([3, 1, 1, 2, 1])
        cols[0].markdown(item["item"])
        cols[1].markdown(str(item["qty"]))
        cols[2].markdown(f"${item['price']:.2f}")

        plus, minus = cols[3].columns(2)
        if plus.button("➕", key=f"plus_{i}"):
            st.session_state.inventory[i]["qty"] += 1
            st.rerun()
        if minus.button("➖", key=f"minus_{i}"):
            if st.session_state.inventory[i]["qty"] > 0:
                st.session_state.inventory[i]["qty"] -= 1
                st.rerun()

        if cols[4].button("🗑️", key=f"delete_{i}"):
            st.session_state.inventory.pop(i)
            st.rerun()

    # Add Inventory Item
    with st.expander("➕ Add Inventory Item"):
        with st.form("add_item_form"):
            item = st.text_input("Item Name")
            qty = st.number_input("Quantity", min_value=0, step=1)
            price = st.number_input("Price", min_value=0.0, step=0.01)
            if st.form_submit_button("Add"):
                if item:
                    st.session_state.inventory.append({
                        "item": item,
                        "qty": int(qty),
                        "price": float(price)
                    })
                    st.success(f"Added: {item}")
                    st.rerun()

# === JOB HOURS TAB ===
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
            st.warning("⚠️ Invalid start time.")

        if st.button("End Clock"):
            end = datetime.now()
            minutes = int((end - st.session_state.clock_start).total_seconds() / 60)
            st.session_state.job_logs.append({
                "desc": desc or "No description",
                "start": st.session_state.clock_start,
                "end": end,
                "minutes": minutes
            })
            st.session_state.clock_start = None
            st.success(f"Logged {minutes} minutes")
            st.rerun()

    st.subheader("Job Log History")
    week_total = 0
    month_total = 0
    now = datetime.now()

    for i, log in enumerate(st.session_state.job_logs):
        try:
            time_str = log["start"].strftime('%m/%d %I:%M %p')
        except:
            time_str = "Unknown time"

        st.markdown(f"- **{log['desc']}** | {log['minutes']} min | {time_str}")
        if st.button("Delete", key=f"log_delete_{i}"):
            st.session_state.job_logs.pop(i)
            st.rerun()

        if isinstance(log.get("start"), datetime):
            if log["start"].date() >= (now - timedelta(days=7)).date():
                week_total += log["minutes"]
            if log["start"].month == now.month and log["start"].year == now.year:
                month_total += log["minutes"]

    st.markdown(f"**This Week:** {round(week_total / 60, 2)} hrs")
    st.markdown(f"**This Month:** {round(month_total / 60, 2)} hrs")

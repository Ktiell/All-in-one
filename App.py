import streamlit as st
import datetime

# ---- Setup ----
st.set_page_config(page_title="All in One", layout="centered")
if "inventory" not in st.session_state:
    st.session_state.inventory = []

# ---- Tabs ----
tabs = st.tabs(["Inventory", "Tools", "Materials", "Job Hours"])
tab_inventory, tab_tools, tab_materials, tab_hours = tabs

# ---- Inventory Tab ----
with tab_inventory:
    st.subheader("Inventory")

    with st.expander("➕ Add Inventory Item"):
        item_name = st.text_input("Item Name")
        qty = st.number_input("Quantity", min_value=0, step=1)
        price = st.number_input("Price", min_value=0.0, step=0.01, format="%.2f")
        if st.button("Add", key="add_inv"):
            st.session_state.inventory.append({"name": item_name, "qty": qty, "price": price})

    if st.session_state.inventory:
        st.markdown("### Current Inventory")
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
                c1, c2 = st.columns(2)
                if c1.button("➕", key=f"inc_{i}"):
                    item["qty"] += 1
                if c2.button("➖", key=f"dec_{i}"):
                    item["qty"] = max(0, item["qty"] - 1)
            if col5.button("🗑️", key=f"del_{i}"):
                st.session_state.inventory.pop(i)
                st.experimental_rerun()

# ---- Tools Tab ----
with tab_tools:
    st.subheader("Tools")
    st.write("🛠️ Manage your tools list here (future feature)")

# ---- Materials Tab ----
with tab_materials:
    st.subheader("Materials")
    st.write("🪵 Manage your materials list here (future feature)")

# ---- Job Hours Tab ----
with tab_hours:
    st.subheader("Job Hours")
    if "job_log" not in st.session_state:
        st.session_state.job_log = []
    if "clock_running" not in st.session_state:
        st.session_state.clock_running = False
        st.session_state.start_time = None

    desc = st.text_input("Task Description")
    if not st.session_state.clock_running:
        if st.button("Start Clock"):
            st.session_state.start_time = datetime.datetime.now()
            st.session_state.clock_running = True
            st.session_state.job_desc = desc
    else:
        if st.button("End Clock"):
            end_time = datetime.datetime.now()
            duration = end_time - st.session_state.start_time
            st.session_state.job_log.append({
                "desc": st.session_state.job_desc,
                "start": st.session_state.start_time,
                "end": end_time,
                "duration": duration
            })
            st.session_state.clock_running = False
            st.session_state.start_time = None

    # Show logs
    if st.session_state.job_log:
        st.markdown("### Log")
        for i, log in enumerate(st.session_state.job_log):
            with st.expander(f"{log['desc']} — {log['duration']}"):
                st.write(f"**Start:** {log['start'].strftime('%Y-%m-%d %H:%M:%S')}")
                st.write(f"**End:** {log['end'].strftime('%Y-%m-%d %H:%M:%S')}")
                st.write(f"**Duration:** {str(log['duration'])}")
                if st.button("Delete", key=f"del_log_{i}"):
                    st.session_state.job_log.pop(i)
                    st.experimental_rerun()

        # Show summary
        week_total = sum((log["duration"] for log in st.session_state.job_log if log["start"].isocalendar()[1] == datetime.datetime.now().isocalendar()[1]), datetime.timedelta())
        month_total = sum((log["duration"] for log in st.session_state.job_log if log["start"].month == datetime.datetime.now().month), datetime.timedelta())
        st.info(f"**Total This Week:** {week_total}\n\n**Total This Month:** {month_total}")

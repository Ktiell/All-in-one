import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="All in One", layout="wide")
st.title("📋 All-in-One App")

# Initialize session state
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
    st.header("Add Inventory Item")
    with st.form("add_item_form", clear_on_submit=True):
        name = st.text_input("Item Name")
        qty = st.number_input("Quantity", min_value=0, step=1)
        price = st.number_input("Price", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Add Inventory Item")
        if submitted:
            st.session_state.inventory.append({
                "name": name,
                "qty": qty,
                "price": price
            })

    st.header("Current Inventory")
    if st.session_state.inventory:
        cols = st.columns([3, 2, 2, 1.5, 1.5, 1.5])
        for col, header in zip(cols, ["Item", "Qty", "Price", "Add", "Remove", "Delete"]):
            col.markdown(f"**{header}**")

        for i, item in enumerate(st.session_state.inventory):
            cols = st.columns([3, 2, 2, 1.5, 1.5, 1.5])
            cols[0].write(item["name"])
            cols[1].write(str(item["qty"]))
            cols[2].write(f"${item['price']:.2f}")
            if cols[3].button("➕", key=f"add_{i}"):
                item["qty"] += 1
            if cols[4].button("➖", key=f"remove_{i}"):
                if item["qty"] > 0:
                    item["qty"] -= 1
            if cols[5].button("❌", key=f"delete_{i}"):
                st.session_state.inventory.pop(i)
                st.experimental_rerun()
    else:
        st.info("No inventory items yet.")

# --------------------
# Tools Tab
# --------------------
with tabs[1]:
    st.header("Tools")
    new_tool = st.text_input("Add Tool", key="tool_input")
    if st.button("Add Tool"):
        st.session_state.tools.append(new_tool)
        st.experimental_rerun()

    for i, tool in enumerate(sorted(st.session_state.tools)):
        col1, col2 = st.columns([4, 1])
        col1.write(tool)
        if col2.button("Delete", key=f"del_tool_{i}"):
            st.session_state.tools.pop(i)
            st.experimental_rerun()

# --------------------
# Materials Tab
# --------------------
with tabs[2]:
    st.header("Materials")
    new_mat = st.text_input("Add Material", key="mat_input")
    if st.button("Add Material"):
        st.session_state.materials.append(new_mat)
        st.experimental_rerun()

    for i, mat in enumerate(sorted(st.session_state.materials)):
        col1, col2 = st.columns([4, 1])
        col1.write(mat)
        if col2.button("Delete", key=f"del_mat_{i}"):
            st.session_state.materials.remove(m)
            st.experimental_rerun()

# --------------------
# Labor Log Tab
# --------------------
with tabs[3]:
    st.header("Labor Log")

    st.session_state.task_desc = st.text_input("Task Description", value=st.session_state.task_desc)

    if not st.session_state.clock["is_running"]:
        if st.button("Start Clock"):
            st.session_state.clock["is_running"] = True
            st.session_state.clock["start"] = datetime.now()
            st.experimental_rerun()
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
            st.experimental_rerun()

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

    st.write("### Logged Sessions")
    for i, log in enumerate(st.session_state.labor_log):
        st.write(f"{log['task']} | {log['start'].strftime('%Y-%m-%d %H:%M')} – {log['end'].strftime('%H:%M')} | {log['hours']:.2f} hrs")
        if st.button("Delete Entry", key=f"del_log_{i}"):
            st.session_state.labor_log.pop(i)
            st.experimental_rerun()

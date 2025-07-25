import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page config and custom styling
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
.stButton>button {
    background-color: #4f6f52;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    border: none;
}
.stDownloadButton>button {
    background-color: #4f6f52;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>All in One</h1>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top: 0;'>", unsafe_allow_html=True)

# === Session State Setup ===
for key in ["inventory", "tools", "materials", "job_logs"]:
    if key not in st.session_state:
        st.session_state[key] = []
if "clock_start" not in st.session_state:
    st.session_state.clock_start = None

# === TABS ===
tab1, tab2, tab3, tab4 = st.tabs(["Inventory", "Tools", "Materials", "Job Hours"])

# === INVENTORY TAB ===
with tab1:
    st.subheader("Inventory")
    headers = st.columns([3, 1, 1, 2, 1])
    headers[0].markdown("**Item**")
    headers[1].markdown("**Qty**")
    headers[2].markdown("**Price**")
    headers[3].markdown("**Actions**")
    headers[4].markdown("**Delete**")

    for i, inv in enumerate(st.session_state.inventory):
        cols = st.columns([3, 1, 1, 2, 1])
        cols[0].markdown(inv.get("item", ""))
        cols[1].markdown(str(inv.get("qty", 0)))
        cols[2].markdown(f"${inv.get('price', 0.00):.2f}")
        plus, minus = cols[3].columns(2)
        if plus.button("➕", key=f"plus_{i}"):
            st.session_state.inventory[i]["qty"] += 1
            st.rerun()
        if minus.button("➖", key=f"minus_{i}"):
            if st.session_state.inventory[i]["qty"] > 0:
                st.session_state.inventory[i]["qty"] -= 1
                st.rerun()
        if cols[4].button("🗑️", key=f"del_{i}"):
            st.session_state.inventory.pop(i)
            st.rerun()

    with st.expander("➕ Add Inventory Item"):
        with st.form("add_inventory_form"):
            name = st.text_input("Item Name")
            qty = st.number_input("Quantity", min_value=0, step=1)
            price = st.number_input("Price", min_value=0.0, step=0.01)
            if st.form_submit_button("Add Item"):
                st.session_state.inventory.append({"item": name, "qty": int(qty), "price": float(price)})
                st.success(f"Added: {name}")
                st.rerun()

# === TOOLS TAB ===
with tab2:
    st.subheader("Tools")
    with st.expander("➕ Add Tool"):
        with st.form("add_tool"):
            name = st.text_input("Tool Name")
            qty = st.number_input("Quantity", min_value=0, step=1, key="tool_qty")
            price = st.number_input("Price", min_value=0.0, step=0.01, key="tool_price")
            if st.form_submit_button("Add Tool"):
                st.session_state.tools.append({"item": name, "qty": int(qty), "price": float(price)})
                st.success(f"Added tool: {name}")
                st.rerun()
    for i, tool in enumerate(st.session_state.tools):
        st.write(f"{tool['item']} — Qty: {tool['qty']} — ${tool['price']:.2f}")
        if st.button("🗑️", key=f"del_tool_{i}"):
            st.session_state.tools.pop(i)
            st.rerun()

# === MATERIALS TAB ===
with tab3:
    st.subheader("Materials")
    with st.expander("➕ Add Material"):
        with st.form("add_material"):
            name = st.text_input("Material Name")
            qty = st.number_input("Quantity", min_value=0, step=1, key="mat_qty")
            price = st.number_input("Price", min_value=0.0, step=0.01, key="mat_price")
            if st.form_submit_button("Add Material"):
                st.session_state.materials.append({"item": name, "qty": int(qty), "price": float(price)})
                st.success(f"Added material: {name}")
                st.rerun()
    for i, mat in enumerate(st.session_state.materials):
        st.write(f"{mat['item']} — Qty: {mat['qty']} — ${mat['price']:.2f}")
        if st.button("🗑️", key=f"del_mat_{i}"):
            st.session_state.materials.pop(i)
            st.rerun()

# === JOB HOURS TAB ===
with tab4:
    st.subheader("Job Hours")
    desc = st.text_input("Task Description")
    if st.session_state.clock_start is None:
        if st.button("Start Clock"):
            st.session_state.clock_start = datetime.now()
    else:
        st.markdown(f"**Started:** {st.session_state.clock_start.strftime('%I:%M:%S %p')}")
        if st.button("End Clock"):
            end = datetime.now()
            duration = (end - st.session_state.clock_start).total_seconds() / 60
            st.session_state.job_logs.append({
                "desc": desc or "No description",
                "start": st.session_state.clock_start,
                "end": end,
                "minutes": int(duration)
            })
            st.session_state.clock_start = None
            st.success(f"Logged {int(duration)} minutes.")
            st.rerun()

    st.markdown("### Log History")
    now = datetime.now()
    week_total, month_total = 0, 0
    for i, log in enumerate(st.session_state.job_logs):
        start = log["start"]
        time_str = start.strftime('%m/%d %I:%M %p') if isinstance(start, datetime) else "Unknown"
        st.write(f"- {log['desc']} | {log['minutes']} min | {

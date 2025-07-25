import streamlit as st
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
    padding: 0.4rem 1rem;
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

# Initialize session state
for key in ["inventory", "tools", "materials", "job_logs"]:
    if key not in st.session_state:
        st.session_state[key] = []
if "clock_start" not in st.session_state:
    st.session_state.clock_start = None

# TABS
tab1, tab2, tab3, tab4 = st.tabs(["Inventory", "Tools", "Materials", "Job Hours"])

# === INVENTORY TAB ===
with tab1:
    st.subheader("Inventory")

    # Table Header
    header = st.columns([3, 1, 1, 2, 1])
    header[0].markdown("**Item**")
    header[1].markdown("**Qty**")
    header[2].markdown("**Price**")
    header[3].markdown("**Actions**")
    header[4].markdown("**Delete**")

    for i, item in enumerate(st.session_state.inventory):
        row = st.columns([3, 1, 1, 2, 1])
        row[0].write(item.get("item", ""))
        row[1].write(str(item.get("qty", 0)))
        row[2].write(f"${item.get('price', 0.00):.2f}")

        plus, minus = row[3].columns(2)
        if plus.button("➕", key=f"inv_plus_{i}"):
            item["qty"] += 1
            st.rerun()
        if minus.button("➖", key=f"inv_minus_{i}"):
            if item["qty"] > 0:
                item["qty"] -= 1
                st.rerun()

        if row[4].button("🗑️", key=f"inv_del_{i}"):
            st.session_state.inventory.pop(i)
            st.rerun()

    with st.expander("➕ Add Inventory Item"):
        with st.form("add_inventory"):
            name = st.text_input("Item Name")
            qty = st.number_input("Quantity", min_value=0, step=1)
            price = st.number_input("Price", min_value=0.0, step=0.01)
            if st.form_submit_button("Add Item") and name:
                st.session_state.inventory.append({
                    "item": name,
                    "qty": int(qty),
                    "price": float(price)
                })
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
            if st.form_submit_button("Add Tool") and name:
                st.session_state.tools.append({"item": name, "qty": int(qty), "price": float(price)})
                st.success(f"Added tool: {name}")
                st.rerun()
    for i, tool in enumerate(st.session_state.tools):
        st.write(f"{tool['item']} — Qty: {tool['qty']} — ${tool['price']:.2f}")
        if st.button("🗑️", key=f"tool_del_{i}"):
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
            if st.form_submit_button("Add Material") and name:
                st.session_state.materials.append({"item": name, "qty": int(qty), "price": float(price)})
                st.success(f"Added material: {name}")
                st.rerun()
    for i, mat in enumerate(st.session_state.materials):
        st.write(f"{mat['item']} — Qty: {mat['qty']} — ${mat['price']:.2f}")
        if st.button("🗑️", key=f"mat_del_{i}"):
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
            duration = int((end - st.session_state.clock_start).total_seconds() / 60)
            st.session_state.job_logs.append({
                "desc": desc or "No description",
                "start": st.session_state.clock_start,
                "end": end,
                "minutes": duration
            })
            st.session_state.clock_start = None
            st.success(f"Logged {duration} minutes.")
            st.rerun()

    st.markdown("### Log History")
    now = datetime.now()
    week_total = 0
    month_total = 0

    for i, log in enumerate(st.session_state.job_logs):
        task = log.get("desc", "No description")
        minutes = log.get("minutes", 0)
        start_time = log.get("start")
        time_str = start_time.strftime('%m/%d %I:%M %p') if isinstance(start_time, datetime) else "Unknown"
        st.write(f"- {task} | {minutes} min | {time_str}")
        if st.button("Delete", key=f"log_del_{i}"):
            st.session_state.job_logs.pop(i)
            st.rerun()
        if isinstance(start_time, datetime):
            if start_time.date() >= (now - timedelta(days=7)).date():
                week_total += minutes
            if start_time.month == now.month:
                month_total += minutes

    st.markdown(f"**This Week:** {round(week_total/60, 2)} hrs")
    st.markdown(f"**This Month:** {round(month_total/60, 2)} hrs")

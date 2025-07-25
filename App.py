import streamlit as st
from datetime import datetime, timedelta
from fractions import Fraction

st.set_page_config(page_title="All in One", layout="wide")

# Initialize session state
for key in ["inventory", "tools", "materials", "job_logs", "clock_start"]:
    if key not in st.session_state:
        st.session_state[key] = []

if "clock_start" not in st.session_state:
    st.session_state.clock_start = None

# --- Helper Functions ---
def render_table(data, key_prefix):
    headers = ["Item", "Qty", "Price", "Add", "Remove", "Delete"]
    header_cols = st.columns([2, 1, 1, 1, 1, 1])
    for col, header in zip(header_cols, headers):
        col.markdown(f"**{header}**")

    for i, entry in enumerate(data):
        cols = st.columns([2, 1, 1, 1, 1, 1])
        cols[0].markdown(entry["item"])
        cols[1].markdown(str(entry["qty"]))
        cols[2].markdown(f"${entry['price']:.2f}")

        if cols[3].button("+", key=f"{key_prefix}_add_{i}"):
            entry["qty"] += 1
        if cols[4].button("-", key=f"{key_prefix}_remove_{i}"):
            if entry["qty"] > 0:
                entry["qty"] -= 1
        if cols[5].button("Delete", key=f"{key_prefix}_delete_{i}"):
            data.pop(i)
            st.experimental_rerun()

def add_item_form(label, data_key):
    with st.expander(f"Add {label} Item"):
        with st.form(f"{data_key}_form"):
            item = st.text_input("Item Name", key=f"{data_key}_name")
            qty = st.number_input("Quantity", min_value=0, step=1, key=f"{data_key}_qty")
            price = st.number_input("Price", min_value=0.0, step=0.01, key=f"{data_key}_price")
            if st.form_submit_button("Add Item") and item:
                st.session_state[data_key].append({
                    "item": item,
                    "qty": int(qty),
                    "price": float(price)
                })
                st.success(f"{label} item added!")

# --- App Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Inventory", "Tools", "Materials", "Job Hours", "Calculator"])

# --- Inventory Tab ---
with tab1:
    st.header("Inventory")
    render_table(st.session_state.inventory, "inv")
    add_item_form("Inventory", "inventory")

# --- Tools Tab ---
with tab2:
    st.header("Tools")
    render_table(st.session_state.tools, "tool")
    add_item_form("Tool", "tools")

# --- Materials Tab ---
with tab3:
    st.header("Materials")
    render_table(st.session_state.materials, "mat")
    add_item_form("Material", "materials")

# --- Job Hours Tab ---
with tab4:
    st.header("Labor Log")
    desc = st.text_input("Job Description", key="job_desc")

    if st.session_state.clock_start is None:
        if st.button("Start Clock"):
            st.session_state.clock_start = datetime.now()
    else:
        st.write(f"**Started:** {st.session_state.clock_start.strftime('%I:%M:%S %p')}")
        if st.button("End Clock"):
            end_time = datetime.now()
            duration = end_time - st.session_state.clock_start
            minutes = round(duration.total_seconds() / 60)
            st.session_state.job_logs.append({
                "desc": desc if desc else "No description",
                "start": st.session_state.clock_start,
                "end": end_time,
                "minutes": minutes
            })
            st.session_state.clock_start = None
            st.success("Job logged!")

    st.markdown("### Job Log History")
    total_week = 0
    total_month = 0
    now = datetime.now()
    for i, log in enumerate(st.session_state.job_logs):
        st.write(f"- **{log['desc']}**: {log['minutes']} min ({log['start'].strftime('%m/%d %I:%M %p')})")
        if st.button("Delete", key=f"del_log_{i}"):
            st.session_state.job_logs.pop(i)
            st.experimental_rerun()
        if log["start"].date() >= (now - timedelta(days=7)).date():
            total_week += log["minutes"]
        if log["start"].month == now.month and log["start"].year == now.year:
            total_month += log["minutes"]

    st.markdown(f"**Total This Week:** {round(total_week/60, 2)} hrs")
    st.markdown(f"**Total This Month:** {round(total_month/60, 2)} hrs")

# --- Tape Measure Calculator ---
with tab5:
    st.header("Tape Measure Calculator")
    st.markdown("Add, subtract, multiply, or divide tape measure values like `3 1/4 + 1 1/8`")

    def parse_fraction(s):
        s = s.strip()
        if ' ' in s:
            whole, frac = s.split()
            return Fraction(int(whole)) + Fraction(frac)
        else:
            return Fraction(s)

    expr = st.text_input("Enter equation:", placeholder="e.g. 3 3/4 + 1 1/8")

    if expr:
        try:
            for op in ["+", "-", "*", "/"]:
                if op in expr:
                    left, right = expr.split(op)
                    a = parse_fraction(left)
                    b = parse_fraction(right)
                    result = eval(f"a {op} b")
                    inches = int(result)
                    frac = result - inches
                    # Convert to 1/16ths
                    rounded = round(frac * 16)
                    output = f"{inches} {rounded}/16" if inches > 0 else f"{rounded}/16"
                    st.success(f"Result: {output}")
                    break
        except:
            st.error("Invalid input. Use formats like `1/2`, `2 1/4`, etc.")

import streamlit as st
from fractions import Fraction
import re

st.set_page_config(page_title="All in One", layout="wide")
st.title("📋 All in One")

# --- Session State ---
if "inventory" not in st.session_state:
    st.session_state.inventory = []

if "tools" not in st.session_state:
    st.session_state.tools = []

if "job_logs" not in st.session_state:
    st.session_state.job_logs = []

# --- Tape Measurement Calculator ---
st.header("📏 Tape Measurement Calculator")

def parse_tape_input(s):
    s = s.strip().replace('"', '')
    parts = s.split()
    total = Fraction(0)
    for p in parts:
        if "'" in p:
            ft, rest = p.split("'")
            total += int(ft) * 12
            if rest:
                total += Fraction(rest)
        else:
            try:
                total += Fraction(p)
            except:
                pass
    return total

def format_inches(fraction_inch):
    inches = int(fraction_inch)
    frac = fraction_inch - inches
    if frac == 0:
        return f'{inches}"'
    return f'{inches} {frac}"' if inches > 0 else f'{frac}"'

calc_col1, calc_col2, calc_col3 = st.columns([3, 1, 3])

with calc_col1:
    val1 = st.text_input("First value", placeholder='e.g. 3 3/4"')
with calc_col2:
    operation = st.selectbox("Operation", ["+", "-", "×", "÷"])
with calc_col3:
    val2 = st.text_input("Second value", placeholder='e.g. 1 1/8"')

if st.button("Calculate"):
    try:
        f1 = parse_tape_input(val1)
        f2 = parse_tape_input(val2)
        if operation == "+":
            result = f1 + f2
        elif operation == "-":
            result = f1 - f2
        elif operation == "×":
            result = f1 * f2
        elif operation == "÷":
            result = f1 / f2
        st.success(f"Result: {format_inches(result)}")
    except:
        st.error("Invalid input")

# --- Inventory Tracking ---
st.header("📦 Inventory (A–Z)")

with st.expander("➕ Add Item to Inventory"):
    name = st.text_input("Item name")
    qty = st.number_input("Quantity", 1, step=1)
    price = st.number_input("Price", 0.0, step=1.0)
    status = st.selectbox("Status", ["For Sale", "Sold"])

    if st.button("Add Inventory Item"):
        if name:
            st.session_state.inventory.append({
                "name": name,
                "qty": qty,
                "price": price,
                "status": status
            })
            st.success("Item added.")

# Display Inventory
sorted_inventory = sorted(st.session_state.inventory, key=lambda x: x["name"].lower())

for i, item in enumerate(sorted_inventory):
    col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 1])
    col1.write(item["name"])
    col2.write(f'Qty: {item["qty"]}')
    col3.write(f'${item["price"]:.2f}')
    item["status"] = col4.selectbox("Status", ["For Sale", "Sold"], index=0 if item["status"] == "For Sale" else 1, key=f"status_{i}")
    if col5.button("🗑️", key=f"delete_{i}"):
        st.session_state.inventory.remove(item)
        st.experimental_rerun()

# --- Tools & Materials ---
st.header("🔧 Tool & Material Tracker")

with st.expander("➕ Add Tool or Material"):
    tm_name = st.text_input("Name", key="tm_name")
    tm_type = st.selectbox("Type", ["Tool", "Material"], key="tm_type")
    tm_notes = st.text_area("Notes", key="tm_notes")
    if st.button("Add Tool/Material"):
        st.session_state.tools.append({
            "name": tm_name,
            "type": tm_type,
            "notes": tm_notes
        })
        st.success("Added.")

# Display tools/materials
for tm in st.session_state.tools:
    st.markdown(f"- **{tm['type']}**: {tm['name']} – {tm['notes']}")

# --- Jobsite Logs ---
st.header("📸 Solo Jobsite Log")

with st.expander("➕ New Log Entry"):
    log_title = st.text_input("Log Title")
    log_notes = st.text_area("Notes")
    log_image = st.file_uploader("Photo (optional)", type=["png", "jpg", "jpeg"])
    if st.button("Add Log"):
        st.session_state.job_logs.append({
            "title": log_title,
            "notes": log_notes,
            "image": log_image
        })
        st.success("Log added.")

for log in st.session_state.job_logs[::-1]:
    with st.expander(log["title"]):
        st.write(log["notes"])
        if log["image"]:
            st.image(log["image"], use_column_width=True)

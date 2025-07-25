import streamlit as st from fractions import Fraction

st.set_page_config(page_title="All in One", layout="wide") st.title("📋 All in One")

--- Session State ---

if "inventory" not in st.session_state: st.session_state.inventory = []

if "tools" not in st.session_state: st.session_state.tools = []

if "materials" not in st.session_state: st.session_state.materials = []

if "job_logs" not in st.session_state: st.session_state.job_logs = []

if "calc_total" not in st.session_state: st.session_state.calc_total = Fraction(0)

--- Tape Measurement Calculator in Sidebar ---

st.sidebar.header("📏 Tape Measurement Calculator")

def parse_tape_input(s): s = s.strip().replace('"', '') parts = s.split() total = Fraction(0) for p in parts: if "'" in p: ft, rest = p.split("'") total += int(ft) * 12 if rest: total += Fraction(rest) else: try: total += Fraction(p) except: pass return total

def format_inches(fraction_inch): inches = int(fraction_inch) frac = fraction_inch - inches if frac == 0: return f'{inches}"' return f'{inches} {frac}"' if inches > 0 else f'{frac}"'

val1 = st.sidebar.text_input("First value", placeholder='e.g. 3 3/4"') operation = st.sidebar.selectbox("Operation", ["+", "-", "×", "÷"]) val2 = st.sidebar.text_input("Second value", placeholder='e.g. 1 1/8"')

if st.sidebar.button("Calculate"): try: f1 = parse_tape_input(val1) f2 = parse_tape_input(val2) if operation == "+": result = f1 + f2 elif operation == "-": result = f1 - f2 elif operation == "×": result = f1 * f2 elif operation == "÷": result = f1 / f2 st.session_state.calc_total += result st.sidebar.success(f"Result: {format_inches(result)}") except: st.sidebar.error("Invalid input")

st.sidebar.markdown(f"Running Total: {format_inches(st.session_state.calc_total)}")

--- Inventory Tracking ---

st.header("📦 Inventory") with st.expander("➕ Add Item to Inventory"): name = st.text_input("Item name") qty = st.number_input("Quantity", 1, step=1) price = st.number_input("Price", 0.0, step=1.0) status = st.selectbox("Status", ["For Sale", "Sold"])

if st.button("Add Inventory Item"):
    if name:
        st.session_state.inventory.append({
            "name": name,
            "qty": qty,
            "price": price,
            "status": status
        })
        st.success("Item added.")

Dropdown list of inventory

inv_names = [f"{item['name']} (Qty: {item['qty']}, ${item['price']}, {item['status']})" for item in st.session_state.inventory] st.selectbox("Inventory List:", options=["Select an item..."] + inv_names)

--- Tools Tracker ---

st.header("🔧 Tools") with st.expander("➕ Add Tool"): tool_name = st.text_input("Tool Name") tool_notes = st.text_area("Tool Notes") if st.button("Add Tool"): if tool_name: st.session_state.tools.append({ "name": tool_name, "notes": tool_notes }) st.success("Tool added.")

tool_names = [f"{tool['name']} – {tool['notes']}" for tool in st.session_state.tools] st.selectbox("Tool List:", options=["Select a tool..."] + tool_names)

--- Materials Tracker ---

st.header("🪵 Materials") with st.expander("➕ Add Material"): mat_name = st.text_input("Material Name") mat_notes = st.text_area("Material Notes") if st.button("Add Material"): if mat_name: st.session_state.materials.append({ "name": mat_name, "notes": mat_notes }) st.success("Material added.")

mat_names = [f"{mat['name']} – {mat['notes']}" for mat in st.session_state.materials] st.selectbox("Material List:", options=["Select a material..."] + mat_names)

--- Jobsite Logs ---

st.header("📸 Jobsite Log") with st.expander("➕ New Log Entry"): log_title = st.text_input("Log Title") log_notes = st.text_area("Notes") log_image = st.file_uploader("Photo (optional)", type=["png", "jpg", "jpeg"]) if st.button("Add Log"): st.session_state.job_logs.append({ "title": log_title, "notes": log_notes, "image": log_image }) st.success("Log added.")

for log in st.session_state.job_logs[::-1]: with st.expander(log["title"]): st.write(log["notes"]) if log["image"]: st.image(log["image"], use_column_width=True)


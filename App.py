import streamlit as st from fractions import Fraction from datetime import datetime, timedelta

st.set_page_config(page_title="All in One", layout="wide") st.title("📋 All in One")

--- Session State ---

if "inventory" not in st.session_state: st.session_state.inventory = [] if "tools" not in st.session_state: st.session_state.tools = [] if "materials" not in st.session_state: st.session_state.materials = [] if "job_logs" not in st.session_state: st.session_state.job_logs = [] if "calc_total" not in st.session_state: st.session_state.calc_total = Fraction(0) if "clock_entries" not in st.session_state: st.session_state.clock_entries = [] if "clock_start" not in st.session_state: st.session_state.clock_start = None

--- Sidebar Calculator ---

st.sidebar.header("📏 Tape Measurement Calculator")

def parse_tape_input(s): s = s.strip().replace('"', '') parts = s.split() total = Fraction(0) for p in parts: if "'" in p: ft, rest = p.split("'") total += int(ft) * 12 if rest: total += Fraction(rest) else: try: total += Fraction(p) except: pass return total

def format_inches(fraction_inch): inches = int(fraction_inch) frac = fraction_inch - inches if frac == 0: return f'{inches}"' return f'{inches} {frac}"' if inches > 0 else f'{frac}"'

val1 = st.sidebar.text_input("First value", placeholder='e.g. 3 3/4"') operation = st.sidebar.selectbox("Operation", ["+", "-", "×", "÷"]) val2 = st.sidebar.text_input("Second value", placeholder='e.g. 1 1/8"')

if st.sidebar.button("Calculate"): try: f1 = parse_tape_input(val1) f2 = parse_tape_input(val2) if operation == "+": result = f1 + f2 elif operation == "-": result = f1 - f2 elif operation == "×": result = f1 * f2 elif operation == "÷": result = f1 / f2 st.session_state.calc_total += result st.sidebar.success(f"Result: {format_inches(result)}") except: st.sidebar.error("Invalid input")

st.sidebar.markdown(f"Running Total: {format_inches(st.session_state.calc_total)}")

--- Main Tabs ---

tabs = st.tabs(["Inventory", "Tools", "Materials", "Labor Log"])

--- Inventory Tab ---

with tabs[0]: st.subheader("📦 Inventory") with st.expander("➕ Add Item"): name = st.text_input("Item Name", key="inv_name") qty = st.number_input("Quantity", 1, step=1, key="inv_qty") price = st.number_input("Price", 0.0, step=1.0, key="inv_price") status = st.selectbox("Status", ["For Sale", "Sold"], key="inv_status") if st.button("Add Inventory Item"): if name: st.session_state.inventory.append({ "name": name, "qty": qty, "price": price, "status": status }) st.success("Item added.")

sorted_inventory = sorted(st.session_state.inventory, key=lambda x: x["name"].lower())
inv_delete_index = None
for i, item in enumerate(sorted_inventory):
    col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 1])
    col1.write(item["name"])
    col2.write(f'Qty: {item["qty"]}')
    col3.write(f'${item["price"]:.2f}')
    item["status"] = col4.selectbox(
        "Status", ["For Sale", "Sold"],
        index=0 if item["status"] == "For Sale" else 1,
        key=f"inv_status_{item['name']}_{i}"
    )
    if col5.button("🗑️", key=f"inv_delete_{item['name']}_{i}"):
        inv_delete_index = i

if inv_delete_index is not None and inv_delete_index < len(st.session_state.inventory):
    del st.session_state.inventory[inv_delete_index]
    st.experimental_rerun()

--- Tools Tab ---

with tabs[1]: st.subheader("🔧 Tools") with st.expander("➕ Add Tool"): tool_name = st.text_input("Tool Name", key="tool_name") tool_notes = st.text_area("Tool Notes", key="tool_notes") if st.button("Add Tool"): if tool_name: st.session_state.tools.append({ "name": tool_name, "notes": tool_notes }) st.success("Tool added.") tool_delete_index = None for i, tool in enumerate(st.session_state.tools): col1, col2 = st.columns([6, 1]) col1.markdown(f"- {tool['name']}: {tool['notes']}") if col2.button("🗑️", key=f"tool_delete_{tool['name']}_{i}"): tool_delete_index = i if tool_delete_index is not None and tool_delete_index < len(st.session_state.tools): del st.session_state.tools[tool_delete_index] st.experimental_rerun()

--- Materials Tab ---

with tabs[2]: st.subheader("🪵 Materials") with st.expander("➕ Add Material"): mat_name = st.text_input("Material Name", key="mat_name") mat_notes = st.text_area("Material Notes", key="mat_notes") if st.button("Add Material"): if mat_name: st.session_state.materials.append({ "name": mat_name, "notes": mat_notes }) st.success("Material added.") mat_delete_index = None for i, mat in enumerate(st.session_state.materials): col1, col2 = st.columns([6, 1]) col1.markdown(f"- {mat['name']}: {mat['notes']}") if col2.button("🗑️", key=f"mat_delete_{mat['name']}_{i}"): mat_delete_index = i if mat_delete_index is not None and mat_delete_index < len(st.session_state.materials): del st.session_state.materials[mat_delete_index] st.experimental_rerun()

--- Labor Log Tab ---

with tabs[3]: st.subheader("📋 Labor Log") if st.session_state.clock_start is None: if st.button("Start Clock"): st.session_state.clock_start = datetime.now() st.success("Clock started.") else: st.info(f"Clock running since: {st.session_state.clock_start.strftime('%Y-%m-%d %H:%M:%S')}") if st.button("End Clock"): end_time = datetime.now() st.session_state.clock_entries.append({ "start": st.session_state.clock_start, "end": end_time }) st.session_state.clock_start = None st.success("Clock entry saved.")

# Show totals
now = datetime.now()
total_today = timedelta()
total_week = timedelta()
total_month = timedelta()
total_year = timedelta()

for entry in st.session_state.clock_entries:
    delta = entry["end"] - entry["start"]
    if entry["start"].date() == now.date():
        total_today += delta
    if entry["start"].isocalendar()[1] == now.isocalendar()[1] and entry["start"].year == now.year:
        total_week += delta
    if entry["start"].month == now.month and entry["start"].year == now.year:
        total_month += delta
    if entry["start"].year == now.year:
        total_year += delta

st.markdown(f"**Hours Today:** {round(total_today.total_seconds() / 3600, 2)} hrs")
st.markdown(f"**Hours This Week:** {round(total_week.total_seconds() / 3600, 2)} hrs")
st.markdown(f"**Hours This Month:** {round(total_month.total_seconds() / 3600, 2)} hrs")
st.markdown(f"**Hours This Year:** {round(total_year.total_seconds() / 3600, 2)} hrs")

# Manual Labor Log
with st.expander("➕ New Manual Log Entry"):
    log_title = st.text_input("Log Title", key="log_title")
    log_notes = st.text_area("Notes", key="log_notes")
    log_image = st.file_uploader("Photo (optional)", type=["png", "jpg", "jpeg"], key="log_img")
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

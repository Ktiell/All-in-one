import streamlit as st
import pandas as pd
from fractions import Fraction

st.set_page_config(page_title="All In One", layout="wide")

# --- Session State Setup ---
for key in ["inventory", "tools", "materials", "jobsite_logs"]:
    if key not in st.session_state:
        st.session_state[key] = []

if "calc_input" not in st.session_state:
    st.session_state.calc_input = ""

if "calc_result" not in st.session_state:
    st.session_state.calc_result = ""

# --- Helpers ---
def parse_tape_expr(expr):
    try:
        expr = expr.replace("×", "*").replace("÷", "/")
        tokens = expr.split()
        parsed = ""
        for token in tokens:
            if "/" in token:
                parsed += f"({Fraction(token)})"
            else:
                parsed += token
        result = eval(parsed)
        return result
    except:
        return None

def format_fraction_inches(value):
    try:
        total_inches = float(value)
        feet = int(total_inches) // 12
        remaining_inches = total_inches - (feet * 12)
        inches_whole = int(remaining_inches)
        fractional_part = remaining_inches - inches_whole
        frac = round(Fraction(fractional_part).limit_denominator(16) * 16) / 16
        frac = Fraction(frac).limit_denominator(16)
        inch_str = f"{inches_whole}"
        if frac != 0:
            inch_str += f" {frac}"
        return f"{feet}' {inch_str}\""
    except:
        return "Invalid"

# --- Styled Calculator Buttons ---
def tape_calculator():
    st.sidebar.markdown("## 📏 Tape Measure Calculator")

    st.sidebar.markdown(f"""
        <div style='
            font-size: 20px;
            font-weight: bold;
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
        '>{st.session_state.calc_input or "0"}</div>
    """, unsafe_allow_html=True)

    def button(label):
        if st.sidebar.button(label):
            if label == "=":
                result = parse_tape_expr(st.session_state.calc_input)
                if result is not None:
                    st.session_state.calc_result = format_fraction_inches(result)
                    st.session_state.calc_input = ""
                else:
                    st.session_state.calc_result = "Invalid"
            elif label == "C":
                st.session_state.calc_input = ""
                st.session_state.calc_result = ""
            else:
                st.session_state.calc_input += f"{label} "

    # Button rows
    rows = [
        ["7", "8", "9", "÷"],
        ["4", "5", "6", "×"],
        ["1", "2", "3", "-"],
        ["0", "/", "=", "+"],
        ["1/16", "1/8", "1/4", "3/8"],
        ["1/2", "5/8", "3/4", "7/8"],
        ["15/16", "C"]
    ]

    for row in rows:
        cols = st.sidebar.columns(len(row))
        for i, label in enumerate(row):
            with cols[i]:
                button(label)

    if st.session_state.calc_result:
        st.sidebar.markdown("### Result")
        st.sidebar.success(st.session_state.calc_result)

# --- Data Table Helpers ---
def display_table(data, section):
    if not data:
        st.info(f"No items added yet to {section}.")
        return
    df = pd.DataFrame(data)
    df = df.sort_values(by=df.columns[0], ascending=True)
    st.dataframe(df.style.set_properties(**{'text-align': 'left'}), use_container_width=True)

def add_item_form(state_key, labels):
    with st.form(f"form_{state_key}", clear_on_submit=True):
        cols = st.columns(len(labels))
        entry = {}
        for i, label in enumerate(labels):
            entry[label] = cols[i].text_input(label)
        submitted = st.form_submit_button("Add")
        if submitted and all(entry.values()):
            st.session_state[state_key].append(entry)

# --- Render Sidebar Calculator ---
tape_calculator()

# --- Main Tabs ---
tabs = st.tabs(["📋 Jobsite Log", "🔧 Tool Tracker", "🪵 Material Tracker", "📦 Inventory", "📐 Tape Calculator"])

with tabs[0]:
    st.subheader("Jobsite Log")
    add_item_form("jobsite_logs", ["Date", "Job Name", "Notes"])
    display_table(st.session_state.jobsite_logs, "Jobsite Log")

with tabs[1]:
    st.subheader("Tool Tracker")
    add_item_form("tools", ["Tool Name", "Location", "Condition"])
    display_table(st.session_state.tools, "Tool Tracker")

with tabs[2]:
    st.subheader("Material Tracker")
    add_item_form("materials", ["Material", "Quantity", "Location"])
    display_table(st.session_state.materials, "Material Tracker")

with tabs[3]:
    st.subheader("Inventory List")
    add_item_form("inventory", ["Item Name", "Qty", "Price", "Status (For Sale/Sold)"])
    display_table(st.session_state.inventory, "Inventory List")

with tabs[4]:
    st.subheader("📐 Tape Calculator")
    st.info("Use the full calculator in the sidebar →")

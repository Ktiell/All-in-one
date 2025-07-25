import streamlit as st
import pandas as pd
from fractions import Fraction

# Page setup
st.set_page_config(page_title="All In One", layout="wide")

# Data storage
for key in ["inventory", "tools", "materials", "jobsite_logs"]:
    if key not in st.session_state:
        st.session_state[key] = []

if "calculator_total" not in st.session_state:
    st.session_state.calculator_total = Fraction(0)

# Helpers
def format_fraction_inches(value):
    try:
        total_inches = float(value)
        feet = int(total_inches) // 12
        inches = total_inches - (feet * 12)
        frac_inches = Fraction(inches).limit_denominator(16)
        if feet > 0:
            return f"{feet}' {frac_inches}\""
        else:
            return f"{frac_inches}\""
    except:
        return "Invalid"

def parse_mixed_fraction(text):
    try:
        parts = text.strip().split()
        if len(parts) == 2:
            whole = int(parts[0])
            frac = Fraction(parts[1])
            return whole + frac
        elif len(parts) == 1:
            return Fraction(parts[0])
    except:
        return None
    return None

# Tape Measure Calculator
def tape_calc():
    st.sidebar.header("📏 Tape Measure Calculator")

    left = st.sidebar.text_input("First value (e.g. 3 1/2)", key="left_input")
    operator = st.sidebar.selectbox("Operation", ["+", "-", "*", "÷"], key="op")
    right = st.sidebar.text_input("Second value (e.g. 1/4)", key="right_input")

    col1, col2 = st.sidebar.columns([1, 1])
    equals = col1.button("Calculate")
    reset = col2.button("Reset Total")

    if reset:
        st.session_state.calculator_total = Fraction(0)

    if equals:
        a = parse_mixed_fraction(left)
        b = parse_mixed_fraction(right)

        if a is None or b is None:
            st.sidebar.error("Invalid input format. Try '3 1/4' or '1/8'")
        else:
            try:
                if operator == "+":
                    result = a + b
                elif operator == "-":
                    result = a - b
                elif operator == "*":
                    result = a * b
                elif operator == "÷":
                    result = a / b

                st.session_state.calculator_total += result
                st.sidebar.success(f"{left} {operator} {right} = {format_fraction_inches(result)}")
            except Exception as e:
                st.sidebar.error(f"Error in calculation: {e}")

    st.sidebar.markdown("### Running Total")
    st.sidebar.markdown(f"**{format_fraction_inches(st.session_state.calculator_total)}**")

# Table display
def display_table(data, section):
    if not data:
        st.info(f"No items added yet to {section}.")
        return
    df = pd.DataFrame(data)
    df = df.sort_values(by=df.columns[0], ascending=True)
    st.dataframe(df.style.set_properties(**{'text-align': 'left'}), use_container_width=True)

# Add item form
def add_item_form(state_key, labels):
    with st.form(f"form_{state_key}", clear_on_submit=True):
        cols = st.columns(len(labels))
        entry = {}
        for i, label in enumerate(labels):
            entry[label] = cols[i].text_input(label)
        submitted = st.form_submit_button("Add")
        if submitted and all(entry.values()):
            st.session_state[state_key].append(entry)

# Render app
tape_calc()

tabs = st.tabs(["📋 Jobsite Log", "🔧 Tool Tracker", "🪵 Material Tracker", "📦 Inventory"])

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

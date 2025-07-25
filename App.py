import streamlit as st
import pandas as pd
from fractions import Fraction

st.set_page_config(page_title="All In One", layout="wide")

# Data Storage
if "inventory" not in st.session_state:
    st.session_state.inventory = []

if "tools" not in st.session_state:
    st.session_state.tools = []

if "materials" not in st.session_state:
    st.session_state.materials = []

if "jobsite_logs" not in st.session_state:
    st.session_state.jobsite_logs = []

if "calculator_total" not in st.session_state:
    st.session_state.calculator_total = Fraction(0)

# Tape Measure Calculator
def parse_fraction(input_str):
    try:
        return Fraction(input_str)
    except:
        return None

def tape_calc():
    st.sidebar.header("📏 Tape Measure Calculator")
    col1, col2, col3 = st.sidebar.columns([4, 2, 1])
    with col1:
        user_input = st.text_input("Enter value (e.g. 3 1/4)", key="input")
    with col2:
        operation = st.selectbox("Op", ["+", "-", "*", "÷"], key="operation")
    with col3:
        calculate = st.button("=", key="calc_btn")

    if calculate and user_input:
        try:
            parts = user_input.strip().split()
            if len(parts) == 2:
                total_input = int(parts[0]) + Fraction(parts[1])
            else:
                total_input = Fraction(parts[0])
            if operation == "+":
                st.session_state.calculator_total += total_input
            elif operation == "-":
                st.session_state.calculator_total -= total_input
            elif operation == "*":
                st.session_state.calculator_total *= total_input
            elif operation == "÷":
                st.session_state.calculator_total /= total_input
        except:
            st.sidebar.error("Invalid format. Try '3 1/4'")

    st.sidebar.write("**Running Total:**", st.session_state.calculator_total)

# Inventory Display Function
def display_table(data, section):
    if not data:
        st.info(f"No items added yet to {section}.")
        return
    df = pd.DataFrame(data)
    df = df.sort_values(by=df.columns[0], ascending=True)
    st.dataframe(df.style.set_properties(**{'text-align': 'left'}), use_container_width=True)

# Add Item Form
def add_item_form(state_key, labels):
    with st.form(f"form_{state_key}", clear_on_submit=True):
        cols = st.columns(len(labels))
        entry = {}
        for i, label in enumerate(labels):
            entry[label] = cols[i].text_input(label)
        submitted = st.form_submit_button("Add")
        if submitted and all(entry.values()):
            st.session_state[state_key].append(entry)

# Main Tabs
tape_calc()
tabs = st.tabs(["📋 Jobsite Log", "🔧 Tool Tracker", "🪵 Material Tracker", "📦 Inventory"])

# Jobsite Log
with tabs[0]:
    st.subheader("Jobsite Log")
    add_item_form("jobsite_logs", ["Date", "Job Name", "Notes"])
    display_table(st.session_state.jobsite_logs, "Jobsite Log")

# Tool Tracker
with tabs[1]:
    st.subheader("Tool Tracker")
    add_item_form("tools", ["Tool Name", "Location", "Condition"])
    display_table(st.session_state.tools, "Tool Tracker")

# Material Tracker
with tabs[2]:
    st.subheader("Material Tracker")
    add_item_form("materials", ["Material", "Quantity", "Location"])
    display_table(st.session_state.materials, "Material Tracker")

# Inventory
with tabs[3]:
    st.subheader("Inventory List")
    add_item_form("inventory", ["Item Name", "Qty", "Price", "Status (For Sale/Sold)"])
    display_table(st.session_state.inventory, "Inventory List")

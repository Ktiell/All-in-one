import streamlit as st import datetime from fractions import Fraction

Set page config

st.set_page_config(page_title="All In One App", layout="wide") st.title("🧰 All In One Business Toolkit")

Sidebar Navigation

page = st.sidebar.radio("Navigate", [ "Calculator", "Inventory List", "Tool Tracker", "Material Tracker", "Jobsite Log" ])

Utility Functions

def parse_fraction(s): try: return float(sum(Fraction(part) for part in s.split())) except: return None

def format_fraction(value): return str(Fraction(value).limit_denominator(16))

Session State Defaults

for key in ["inventory", "tools", "materials", "jobsite_logs", "calc_total"]: if key not in st.session_state: st.session_state[key] = [] if key != "calc_total" else 0.0

Calculator Tab

if page == "Calculator": st.subheader("📏 Tape Measure Calculator") col1, col2, col3 = st.columns([3, 1, 3])

with col1:
    left = st.text_input("First Measurement", placeholder="e.g. 3 3/4")
with col2:
    operation = st.selectbox("Operation", ["+", "-", "x", "/"])
with col3:
    right = st.text_input("Second Measurement", placeholder="e.g. 1 1/8")

if st.button("Calculate"):
    left_val = parse_fraction(left)
    right_val = parse_fraction(right)
    result = None

    if left_val is not None and right_val is not None:
        if operation == "+":
            result = left_val + right_val
        elif operation == "-":
            result = left_val - right_val
        elif operation == "x":
            result = left_val * right_val
        elif operation == "/" and right_val != 0:
            result = left_val / right_val

        if result is not None:
            st.session_state.calc_total += result
            st.success(f"Result: {format_fraction(result)}\"")
    else:
        st.error("Invalid measurement input. Use format like '3 3/4'")

st.markdown(f"### Running Total: {format_fraction(st.session_state.calc_total)}\"")
if st.button("Reset Total"):
    st.session_state.calc_total = 0.0

Inventory List Tab

elif page == "Inventory List": st.subheader("📦 Inventory List") name = st.text_input("Item Name") qty = st.number_input("Quantity", step=1) status


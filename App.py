
import streamlit as st
import pandas as pd
from fractions import Fraction

st.set_page_config(page_title="All-in-One App", layout="wide")

# --- Initialize Session State ---
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "use_feet" not in st.session_state:
    st.session_state.use_feet = False

# --- Helper Functions ---
def parse_tape_measure(value):
    value = value.strip().replace('â€³', '').replace('"', '')
    if ' ' in value:
        whole, frac = value.split(' ')
        return Fraction(int(whole)) + Fraction(frac)
    elif '/' in value:
        return Fraction(value)
    else:
        return Fraction(int(value))

def format_inches(frac):
    rounded = round(frac * 16) / 16
    whole = int(rounded)
    remainder = rounded - whole
    if remainder == 0:
        return f"{whole}"
    else:
        return f"{whole} {Fraction(remainder).limit_denominator(16)}" if whole > 0 else f"{Fraction(remainder).limit_denominator(16)}"

def fraction_to_tape_string(value, use_feet=False):
    inches = float(value)
    if use_feet:
        feet = int(inches) // 12
        remaining_inches = inches - feet * 12
        return f"{feet}' {format_inches(Fraction(remaining_inches))}\""
    else:
        return f"{format_inches(Fraction(inches))}\""

def evaluate_expression(expr):
    try:
        expr = expr.replace("Ã—", "*").replace("Ã·", "/")
        parts = expr.split()
        parsed_expr = ""
        i = 0
        while i < len(parts):
            if '/' in parts[i]:
                if i > 0 and parts[i-1].isdigit():
                    parsed_expr = parsed_expr.rstrip() + f"+Fraction('{parts[i]}') "
                else:
                    parsed_expr += f"Fraction('{parts[i]}') "
            elif parts[i].isdigit():
                parsed_expr += f"{parts[i]} "
            else:
                parsed_expr += f"{parts[i]} "
            i += 1
        result = eval(parsed_expr, {"Fraction": Fraction})
        return fraction_to_tape_string(result, st.session_state.use_feet)
    except Exception:
        return "Error"

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["ðŸ“¦ Inventory", "ðŸ§° Tools", "ðŸªµ Materials", "ðŸ“‹ Jobsite Log", "ðŸ“ Calculator"])

with tab1:
    st.subheader("Inventory")
    st.write("Inventory list will go here.")

with tab2:
    st.subheader("Tools")
    st.write("Tool tracking list goes here.")

with tab3:
    st.subheader("Materials")
    st.write("Material tracking list goes here.")

with tab4:
    st.subheader("Jobsite Log")
    st.write("Jobsite logs and notes will go here.")

with tab5:
    st.subheader("Tape Measure Calculator")
    st.markdown("Enter measurements like `3 1/2 + 1 1/8` or use the buttons.")

    st.text_input("Calculation", st.session_state.expression, key="expression_display", label_visibility="collapsed")

    col1, col2, col3, col4 = st.columns(4)
    buttons = [
        ("7", "8", "9", "Ã·"),
        ("4", "5", "6", "Ã—"),
        ("1", "2", "3", "-"),
        ("0", "C", "=", "+")
    ]
    for row in buttons:
        cols = st.columns(4)
        for i, label in enumerate(row):
            if cols[i].button(label):
                if label == "C":
                    st.session_state.expression = ""
                elif label == "=":
                    st.session_state.expression = evaluate_expression(st.session_state.expression)
                else:
                    st.session_state.expression += f"{label} "

    st.markdown("### Tape Measure Fractions")
    frac_row1 = st.columns(5)
    frac_row2 = st.columns(5)
    fractions = ["1/16", "1/8", "1/4", "3/8", "1/2", "5/8", "3/4", "7/8", "15/16"]
    for i, frac in enumerate(fractions):
        row = frac_row1 if i < 5 else frac_row2
        if row[i % 5].button(frac):
            st.session_state.expression += f"{frac} "

    st.checkbox("Show in feet & inches", key="use_feet")

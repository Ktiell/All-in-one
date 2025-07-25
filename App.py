import streamlit as st
from fractions import Fraction
import re

st.set_page_config(page_title="Tape Measure Calculator", layout="centered")

# --- Session State ---
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "result" not in st.session_state:
    st.session_state.result = ""
if "use_feet" not in st.session_state:
    st.session_state.use_feet = False

# --- Parser for Mixed Numbers ---
def parse_mixed_expression(expr):
    expr = expr.replace("×", "*").replace("÷", "/")
    # Convert mixed numbers like 5 1/2 to (5+1/2)
    expr = re.sub(r'(\d+)\s+(\d+/\d+)', r'(\1+\2)', expr)
    # Convert all fractions to Fraction() for Python
    expr = re.sub(r'(\d+/\d+)', r'Fraction("\1")', expr)
    return expr

def evaluate_expression(expr):
    try:
        parsed = parse_mixed_expression(expr)
        result = eval(parsed, {"Fraction": Fraction})
        return result
    except:
        return "Error"

def format_result(val, use_feet=False):
    if val == "Error":
        return "Error"
    inches = float(val)
    rounded = round(inches * 16) / 16
    whole = int(rounded)
    remainder = rounded - whole
    fraction = Fraction(remainder).limit_denominator(16)
    if use_feet:
        feet = whole // 12
        inch = whole % 12
        result = f"{feet}'"
        if inch or fraction:
            result += f" {inch if inch else ''} {fraction if fraction else ''}\""
        return result.strip()
    else:
        return f"{whole if whole else ''} {fraction if fraction else ''}\"".strip()

# --- UI Layout ---
st.title("Tape Measure Calculator")

# Display field (disabled)
st.text_input("Input", value=st.session_state.expression, key="display", label_visibility="collapsed", disabled=True)

# Buttons
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "C", "+"],
    ["1/16", "1/8", "1/4", "="]
]

for row in buttons:
    cols = st.columns(len(row))
    for i, label in enumerate(row):
        if cols[i].button(label):
            if label == "C":
                st.session_state.expression = ""
                st.session_state.result = ""
            elif label == "=":
                raw = st.session_state.expression
                res = evaluate_expression(raw)
                st.session_state.result = format_result(res, st.session_state.use_feet)
            else:
                st.session_state.expression += f"{label} "

# Manual edit if needed
st.session_state.expression = st.text_input("Edit input:", value=st.session_state.expression, key="manual_edit")

# Result display
if st.session_state.result:
    st.success(f"Result: {st.session_state.result}")

# Feet/inches toggle
st.checkbox("Show feet & inches", key="use_feet")

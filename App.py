import streamlit as st
from fractions import Fraction

st.set_page_config(page_title="Tape Measure Calculator", layout="centered")

# --- Session State ---
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "result" not in st.session_state:
    st.session_state.result = ""
if "use_feet" not in st.session_state:
    st.session_state.use_feet = False

# --- Helper Functions ---
def parse_tape_measure(value):
    value = value.strip().replace('″', '').replace('"', '')
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
        expr = expr.replace("*", "*").replace("/", "/")
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

# --- UI ---
st.title("Tape Measure Calculator")
st.markdown("Type expressions like: `3 1/2 + 1 1/8 - 5/16 * 2`")

st.session_state.expression = st.text_input("Enter measurement math here:", value=st.session_state.expression)

if st.button("Calculate"):
    st.session_state.result = evaluate_expression(st.session_state.expression)

st.text_input("Result", value=st.session_state.result, disabled=True, label_visibility="collapsed")
st.checkbox("Show in feet & inches", key="use_feet")

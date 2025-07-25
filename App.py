import streamlit as st
from fractions import Fraction

st.set_page_config(page_title="Tape Measure Calculator", layout="centered")

# --- Initialize ---
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "result" not in st.session_state:
    st.session_state.result = ""

# --- Helpers ---
def parse_expression(expr):
    expr = expr.replace("*", "*").replace("/", "/")
    parts = expr.split()
    output = ""
    i = 0
    while i < len(parts):
        part = parts[i]
        if '/' in part:
            if i > 0 and parts[i-1].isdigit():
                output = output.rstrip() + f"+Fraction('{part}') "
            else:
                output += f"Fraction('{part}') "
        elif part.isdigit():
            output += f"{part} "
        elif part in "+-*()/":
            output += f"{part} "
        i += 1
    return output

def format_result(value, use_feet=False):
    inches = float(value)
    rounded = round(inches * 16) / 16
    whole = int(rounded)
    remainder = rounded - whole
    fraction = Fraction(remainder).limit_denominator(16)
    if use_feet:
        feet = whole // 12
        inch = whole % 12
        out = f"{feet}'"
        if inch or fraction:
            out += f" {inch if inch else ''} {fraction if fraction else ''}\""
        return out.strip()
    else:
        out = f"{whole if whole else ''}"
        if fraction:
            out += f" {fraction}"
        return out.strip() + "\""

def calculate(expr, use_feet):
    try:
        parsed = parse_expression(expr)
        result = eval(parsed, {"Fraction": Fraction})
        return format_result(result, use_feet)
    except:
        return "Error"

# --- UI ---
st.title("Tape Measure Calculator")

col1, col2 = st.columns([3, 1])
with col1:
    expr = st.text_input("Enter your tape math:", value=st.session_state.expression)
    st.session_state.expression = expr
with col2:
    use_feet = st.checkbox("Show feet", key="use_feet")

if st.button("Calculate"):
    st.session_state.result = calculate(expr, use_feet)

if st.session_state.result:
    st.success(f"Result: {st.session_state.result}")

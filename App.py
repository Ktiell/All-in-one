
import streamlit as st
from fractions import Fraction

st.set_page_config(page_title="All-in-One App", layout="wide")

# Session state for calculator
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "result" not in st.session_state:
    st.session_state.result = ""
if "use_feet" not in st.session_state:
    st.session_state.use_feet = False

# Helper functions
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

# Calculator Page Layout
st.title("Tape Measure Calculator")

center = st.columns([1, 2, 1])  # layout for centering
with center[1]:
    st.text_input("Expression", st.session_state.expression, key="expression_display", label_visibility="collapsed", disabled=True)
    st.text_input("Result", st.session_state.result, key="result_display", label_visibility="collapsed", disabled=True)

    for row in [["7", "8", "9", "Ã·"], ["4", "5", "6", "Ã—"], ["1", "2", "3", "-"], ["0", "C", "=", "+"]]:
        cols = st.columns(4)
        for i, label in enumerate(row):
            if cols[i].button(label):
                if label == "C":
                    st.session_state.expression = ""
                    st.session_state.result = ""
                elif label == "=":
                    st.session_state.result = evaluate_expression(st.session_state.expression)
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

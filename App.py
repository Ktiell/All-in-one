
import streamlit as st
from fractions import Fraction
import re

st.set_page_config(page_title="All-in-One App", layout="wide")

# ---------------- SESSION STATE ---------------- #
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "result" not in st.session_state:
    st.session_state.result = ""
if "use_feet" not in st.session_state:
    st.session_state.use_feet = False
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "tools" not in st.session_state:
    st.session_state.tools = []
if "materials" not in st.session_state:
    st.session_state.materials = []
if "logs" not in st.session_state:
    st.session_state.logs = []

# ---------------- CALCULATOR FUNCTIONS ---------------- #
def parse_mixed_expression(expr):
    expr = expr.replace("Ã—", "*").replace("Ã·", "/")
    expr = re.sub(r'(\d+)\s+(\d+/\d+)', r'(\1+\2)', expr)
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

# ---------------- TABS ---------------- #
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Inventory", "Tools", "Materials", "Jobsite Log", "Calculator"])

# ---------------- INVENTORY TAB ---------------- #
with tab1:
    st.subheader("Inventory")
    name = st.text_input("Item Name")
    qty = st.number_input("Quantity", min_value=0, step=1)
    if st.button("Add to Inventory"):
        st.session_state.inventory.append({"Item": name, "Qty": qty})
    if st.session_state.inventory:
        st.dataframe(st.session_state.inventory)

# ---------------- TOOLS TAB ---------------- #
with tab2:
    st.subheader("Tools")
    tool = st.text_input("Tool Name")
    cond = st.selectbox("Condition", ["New", "Used", "Needs Repair"])
    if st.button("Add Tool"):
        st.session_state.tools.append({"Tool": tool, "Condition": cond})
    if st.session_state.tools:
        st.dataframe(st.session_state.tools)

# ---------------- MATERIALS TAB ---------------- #
with tab3:
    st.subheader("Materials")
    mat = st.text_input("Material Type")
    amt = st.text_input("Amount (e.g. 3 boards, 2 sheets)")
    if st.button("Add Material"):
        st.session_state.materials.append({"Material": mat, "Amount": amt})
    if st.session_state.materials:
        st.dataframe(st.session_state.materials)

# ---------------- JOBSITE LOG TAB ---------------- #
with tab4:
    st.subheader("Jobsite Log")
    entry = st.text_area("Log Entry")
    if st.button("Save Log Entry"):
        st.session_state.logs.append(entry)
    if st.session_state.logs:
        for i, log in enumerate(st.session_state.logs[::-1]):
            st.markdown(f"**Entry {len(st.session_state.logs)-i}:** {log}")

# ---------------- CALCULATOR TAB ---------------- #
with tab5:
    st.subheader("Tape Measure Calculator")
    st.markdown("Use buttons or type expressions like `5 1/2 * 3 + 1/8`.")

    # Entry
    st.session_state.expression = st.text_input("Enter or edit input here:", value=st.session_state.expression)

    # Button Grid
    button_rows = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "C", "+"],
        ["1/16", "1/8", "1/4", "="]
    ]
    for row in button_rows:
        cols = st.columns(len(row))
        for i, label in enumerate(row):
            if cols[i].button(label, key=f"{row}_{i}"):
                if label == "C":
                    st.session_state.expression = ""
                    st.session_state.result = ""
                elif label == "=":
                    res = evaluate_expression(st.session_state.expression)
                    st.session_state.result = format_result(res, st.session_state.use_feet)
                else:
                    st.session_state.expression += f"{label} "

    if st.session_state.result:
        st.success(f"Result: {st.session_state.result}")
    st.checkbox("Show feet & inches", key="use_feet")

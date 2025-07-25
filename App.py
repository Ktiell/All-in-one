
import streamlit as st
from fractions import Fraction
import re
from datetime import datetime, timedelta

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
if "clock_start" not in st.session_state:
    st.session_state.clock_start = None
if "job_hours" not in st.session_state:
    st.session_state.job_hours = []

# ---------------- HELPER FUNCTIONS ---------------- #
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
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Inventory", "Tools", "Materials", "Job Hours", "Calculator"])

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

# ---------------- JOB HOURS TAB ---------------- #
with tab4:
    st.subheader("Job Hours Tracker")

    now = datetime.now()

    if st.session_state.clock_start is None:
        if st.button("Start Clock"):
            st.session_state.clock_start = now
            st.experimental_rerun()
    else:
        st.success(f"Clock started at {st.session_state.clock_start.strftime('%I:%M %p')}")
        desc = st.text_input("What are you working on?", key="job_desc")
        if st.button("End Clock"):
            end_time = datetime.now()
            duration = end_time - st.session_state.clock_start
            st.session_state.job_hours.append({
                "Start": st.session_state.clock_start,
                "End": end_time,
                "Duration": duration,
                "Description": desc
            })
            st.session_state.clock_start = None
            st.success(f"Session ended: {duration}")
            st.experimental_rerun()

    # Totals
    this_week = this_month = timedelta()
    for entry in st.session_state.job_hours:
        if entry["Start"].isocalendar()[1] == now.isocalendar()[1]:
            this_week += entry["Duration"]
        if entry["Start"].month == now.month and entry["Start"].year == now.year:
            this_month += entry["Duration"]

    st.markdown(f"**Total This Week:** {round(this_week.total_seconds() / 3600, 2)} hrs")
    st.markdown(f"**Total This Month:** {round(this_month.total_seconds() / 3600, 2)} hrs")

    if st.session_state.job_hours:
        st.write("Job History")
        history = [{
            "Start": e["Start"].strftime("%Y-%m-%d %I:%M %p"),
            "End": e["End"].strftime("%Y-%m-%d %I:%M %p"),
            "Hours": round(e["Duration"].total_seconds() / 3600, 2),
            "Description": e["Description"]
        } for e in st.session_state.job_hours]
        st.dataframe(history)

# ---------------- CALCULATOR TAB ---------------- #
with tab5:
    st.subheader("Tape Measure Calculator")
    st.markdown("ðŸ› ï¸ Calculator fix coming next... layout and lag improvements will be added.")

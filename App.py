import streamlit as st
import datetime
from fractions import Fraction

st.set_page_config(page_title="All in One", layout="wide")
st.markdown("<h1 style='text-align:center;'>All in One</h1>", unsafe_allow_html=True)

tabs = st.tabs(["Tools", "Materials", "Inventory", "Job Hours", "Tape Calculator"])

for key in ["tools", "materials", "inventory", "job_sessions", "active_job"]:
    if key not in st.session_state:
        st.session_state[key] = []

# -------------------- TOOLS --------------------
with tabs[0]:
    st.subheader("Tools")
    tool_input = st.text_input("Add Tool", key="tool_input")
    if st.button("➕ Add Tool"):
        if tool_input:
            st.session_state.tools.append(tool_input)

    for i, tool in enumerate(st.session_state.tools):
        col1, col2 = st.columns([6, 1])
        col1.write(tool)
        if col2.button("🗑️", key=f"tool_del_{i}"):
            st.session_state.tools.pop(i)
            st.rerun()

# -------------------- MATERIALS --------------------
with tabs[1]:
    st.subheader("Materials")
    col1, col2 = st.columns([3, 1])
    new_material = col1.text_input("Material Name", key="mat_name_input")
    new_qty = col2.number_input("Qty", min_value=0, step=1, value=1, key="mat_qty_input")

    if st.button("➕ Add Material"):
        if new_material:
            st.session_state.materials.append({"name": new_material, "qty": new_qty})

    st.markdown("#### Material List")
    for i, item in enumerate(st.session_state.materials):
        cols = st.columns([3, 1, 2])
        cols[0].write(item["name"])
        cols[1].write(str(item["qty"]))
        with cols[2]:
            b1, b2, b3 = st.columns(3)
            if b1.button("➕", key=f"mat_add_{i}"):
                item["qty"] += 1
                st.rerun()
            if b2.button("➖", key=f"mat_sub_{i}"):
                if item["qty"] > 0:
                    item["qty"] -= 1
                    st.rerun()
            if b3.button("🗑️", key=f"mat_del_{i}"):
                st.session_state.materials.pop(i)
                st.rerun()

# -------------------- INVENTORY --------------------
with tabs[2]:
    st.subheader("Inventory")
    col1, col2, col3 = st.columns([3, 1, 1])
    name = col1.text_input("Item Name", key="inv_name_input")
    qty = col2.number_input("Qty", value=1, min_value=0, step=1, key="inv_qty_input")
    price = col3.number_input("Price", value=0.0, min_value=0.0, step=0.01, key="inv_price_input")

    if st.button("➕ Add Inventory Item"):
        if name:
            st.session_state.inventory.append({"name": name, "qty": qty, "price": price})

    st.markdown("#### Inventory List")
    header_cols = st.columns([3, 1, 1, 2])
    header_cols[0].markdown("**Item**")
    header_cols[1].markdown("**Qty**")
    header_cols[2].markdown("**Price**")
    header_cols[3].markdown("**Actions**")

    for i, item in enumerate(st.session_state.inventory):
        cols = st.columns([3, 1, 1, 2])
        cols[0].write(item["name"])
        cols[1].write(item["qty"])
        cols[2].write(f"${item['price']:.2f}")
        with cols[3]:
            a1, a2, a3 = st.columns(3)
            if a1.button("➕", key=f"inv_plus_{i}"):
                st.session_state.inventory[i]["qty"] += 1
                st.rerun()
            if a2.button("➖", key=f"inv_minus_{i}"):
                if st.session_state.inventory[i]["qty"] > 0:
                    st.session_state.inventory[i]["qty"] -= 1
                    st.rerun()
            if a3.button("🗑️", key=f"inv_delete_{i}"):
                st.session_state.inventory.pop(i)
                st.rerun()

# -------------------- JOB HOURS --------------------
with tabs[3]:
    st.subheader("Job Hours Log")

    def get_total_hours():
        now = datetime.datetime.now()
        this_week = now.isocalendar().week
        week_hours = 0
        month_hours = 0
        for job in st.session_state.job_sessions:
            duration = (job["end"] - job["start"]).total_seconds() / 3600 if job["end"] else 0
            if job["start"].isocalendar().week == this_week:
                week_hours += duration
            if job["start"].month == now.month:
                month_hours += duration
        return round(week_hours, 2), round(month_hours, 2)

    desc = st.text_input("Task Description")
    if not st.session_state.active_job:
        if st.button("▶️ Start Clock"):
            st.session_state.active_job = {
                "start": datetime.datetime.now(),
                "desc": desc,
            }
    else:
        st.info(f"Started: {st.session_state.active_job['start'].strftime('%Y-%m-%d %H:%M:%S')} — {st.session_state.active_job['desc']}")
        if st.button("⏹️ End Clock"):
            job = st.session_state.active_job
            job["end"] = datetime.datetime.now()
            st.session_state.job_sessions.append(job)
            st.session_state.active_job = None
            st.rerun()

    week_total, month_total = get_total_hours()
    st.write(f"**Total Hours This Week:** {week_total} hrs")
    st.write(f"**Total Hours This Month:** {month_total} hrs")

    for i, job in enumerate(st.session_state.job_sessions):
        duration = (job["end"] - job["start"]).total_seconds() / 3600 if job["end"] else 0
        with st.expander(f"{job['desc']} — {round(duration, 2)} hrs"):
            st.write(f"Start: {job['start']}")
            st.write(f"End: {job['end']}")
            st.write(f"Duration: {round(duration, 2)} hrs")
            if st.button("🗑️ Delete", key=f"del_job_{i}"):
                st.session_state.job_sessions.pop(i)
                st.rerun()

# -------------------- TAPE CALCULATOR --------------------
with tabs[4]:
    st.subheader("Tape Measure Calculator")

    def parse_inches(text):
        try:
            text = text.strip()
            if ' ' in text:
                whole, frac = text.split()
                return int(whole) + float(Fraction(frac))
            elif '/' in text:
                return float(Fraction(text))
            elif text == "":
                return 0
            else:
                return float(text)
        except:
            return 0

    def format_inches(value):
        total = round(value * 16) / 16
        whole = int(total)
        frac = Fraction(total - whole).limit_denominator(16)
        if frac == 0:
            return f"{whole}\""
        elif whole == 0:
            return f"{frac}\""
        else:
            return f"{whole} {frac}\""

    ft1 = st.number_input("Feet (1st)", value=0, step=1)
    in1 = st.text_input("Inches (1st) — e.g. 3 1/4", "0")

    ft2 = st.number_input("Feet (2nd)", value=0, step=1)
    in2 = st.text_input("Inches (2nd) — e.g. 1 7/8", "0")

    operation = st.selectbox("Operation", ["+", "-", "×", "÷"])

    inches1 = ft1 * 12 + parse_inches(in1)
    inches2 = ft2 * 12 + parse_inches(in2)

    result = None
    if operation == "+":
        result = inches1 + inches2
    elif operation == "-":
        result = inches1 - inches2
    elif operation == "×":
        result = inches1 * inches2
    elif operation == "÷":
        if inches2 != 0:
            result = inches1 / inches2
        else:
            st.error("Can't divide by zero.")

    if result is not None:
        feet_out = int(result // 12)
        inch_out = format_inches(result % 12)
        st.success(f"Result: {feet_out} ft {inch_out}")

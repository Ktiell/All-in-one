import streamlit as st
import datetime
from fractions import Fraction
from collections import defaultdict

st.set_page_config(page_title="All in One", layout="wide")

st.markdown(
    """
    <style>
    .title { text-align: center; font-size: 3em; font-weight: bold; margin-bottom: 1em; }
    .inv-table th, .inv-table td { padding: 0.5em; text-align: center; }
    .inv-table input[type="number"] { width: 4em; }
    .button-cell button { margin-right: 0.3em; }
    .job-entry { border: 1px solid #ccc; padding: 0.5em; border-radius: 8px; margin-bottom: 0.5em; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="title">All in One</div>', unsafe_allow_html=True)

tabs = st.tabs(["Tools", "Materials", "Inventory", "Job Hours", "Tape Calculator"])

# SESSION STATE INIT
for key in ["tools", "materials", "inventory", "job_sessions", "active_job"]:
    if key not in st.session_state:
        st.session_state[key] = []

### TOOLS TAB
with tabs[0]:
    st.subheader("Tools")
    tool_name = st.text_input("Add Tool")
    if st.button("➕ Add Tool"):
        if tool_name:
            st.session_state.tools.append(tool_name)

    for i, tool in enumerate(st.session_state.tools):
        cols = st.columns([6, 1])
        cols[0].write(tool)
        if cols[1].button("🗑️", key=f"tool_del_{i}"):
            st.session_state.tools.pop(i)
            st.experimental_rerun()

### MATERIALS TAB
with tabs[1]:
    st.subheader("Materials")
    mat_name = st.text_input("Add Material")
    if st.button("➕ Add Material"):
        if mat_name:
            st.session_state.materials.append(mat_name)

    for i, mat in enumerate(st.session_state.materials):
        cols = st.columns([6, 1])
        cols[0].write(mat)
        if cols[1].button("🗑️", key=f"mat_del_{i}"):
            st.session_state.materials.pop(i)
            st.experimental_rerun()

### INVENTORY TAB
with tabs[2]:
    st.subheader("Inventory")

    def inventory_table():
        st.markdown("<table class='inv-table'><tr><th>Item</th><th>Qty</th><th>Price</th><th>Actions</th></tr>", unsafe_allow_html=True)
        for i, item in enumerate(st.session_state.inventory):
            st.markdown(f"""
                <tr>
                    <td>{item['name']}</td>
                    <td>{item['qty']}</td>
                    <td>${item['price']}</td>
                    <td class='button-cell'>
                        <form action='#' method='post'>
                            <button onclick="document.getElementById('inv_add_{i}').click();return false;">➕</button>
                            <button onclick="document.getElementById('inv_sub_{i}').click();return false;">➖</button>
                            <button onclick="document.getElementById('inv_del_{i}').click();return false;">🗑️</button>
                        </form>
                    </td>
                </tr>
                """, unsafe_allow_html=True)
            if st.button("", key=f"inv_add_{i}", help="Add", use_container_width=False):
                st.session_state.inventory[i]["qty"] += 1
            if st.button("", key=f"inv_sub_{i}", help="Subtract", use_container_width=False):
                if st.session_state.inventory[i]["qty"] > 0:
                    st.session_state.inventory[i]["qty"] -= 1
            if st.button("", key=f"inv_del_{i}", help="Delete", use_container_width=False):
                st.session_state.inventory.pop(i)
                st.experimental_rerun()
        st.markdown("</table>", unsafe_allow_html=True)

    inv_name = st.text_input("Item name")
    inv_qty = st.number_input("Quantity", step=1, value=1)
    inv_price = st.number_input("Price", step=1.0, value=0.0)
    if st.button("➕ Add Inventory Item"):
        st.session_state.inventory.append({"name": inv_name, "qty": inv_qty, "price": inv_price})
    inventory_table()

### JOB HOURS TAB
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
    if "active_job" not in st.session_state or not st.session_state.active_job:
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
            st.experimental_rerun()

    st.divider()
    week_total, month_total = get_total_hours()
    st.write(f"**Total Hours This Week:** {week_total} hrs")
    st.write(f"**Total Hours This Month:** {month_total} hrs")
    st.divider()

    for i, job in enumerate(st.session_state.job_sessions):
        duration = (job["end"] - job["start"]).total_seconds() / 3600 if job["end"] else 0
        with st.expander(f"{job['desc']} — {round(duration, 2)} hrs"):
            st.write(f"Start: {job['start']}")
            st.write(f"End: {job['end']}")
            st.write(f"Duration: {round(duration, 2)} hrs")
            if st.button("🗑️ Delete", key=f"del_job_{i}"):
                st.session_state.job_sessions.pop(i)
                st.experimental_rerun()

### TAPE CALCULATOR TAB
with tabs[4]:
    st.subheader("Tape Measure Calculator")

    def parse_fraction(value):
        if ' ' in value:
            whole, frac = value.split()
            return float(whole) + float(Fraction(frac))
        elif '/' in value:
            return float(Fraction(value))
        else:
            return float(value)

    def format_tape(value):
        inches = round(value * 16) / 16
        whole = int(inches)
        frac = Fraction(inches - whole).limit_denominator(16)
        return f"{whole} {frac}" if frac else f"{whole}"

    ft1 = st.number_input("Feet 1", step=1, value=0)
    in1 = st.text_input("Inches 1 (e.g. 3 1/2)", "0")
    op = st.selectbox("Operation", ["+", "-", "×", "÷"])
    ft2 = st.number_input("Feet 2", step=1, value=0)
    in2 = st.text_input("Inches 2 (e.g. 1 3/4)", "0")

    try:
        total1 = ft1 * 12 + parse_fraction(in1)
        total2 = ft2 * 12 + parse_fraction(in2)

        result = 0
        if op == "+":
            result = total1 + total2
        elif op == "-":
            result = total1 - total2
        elif op == "×":
            result = total1 * total2
        elif op == "÷":
            result = total1 / total2 if total2 != 0 else 0

        feet = int(result // 12)
        inches = format_tape(result % 12)
        st.success(f"Result: {feet} ft {inches} in")

    except Exception as e:
        st.error(f"Error: {e}")

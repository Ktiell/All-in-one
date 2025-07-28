import streamlit as st
from datetime import datetime, timedelta
from fractions import Fraction

st.set_page_config(page_title="All in One", layout="wide")

# ---------- INIT ----------
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "materials" not in st.session_state:
    st.session_state.materials = []
if "tools" not in st.session_state:
    st.session_state.tools = []
if "job_log" not in st.session_state:
    st.session_state.job_log = []
if "clock_running" not in st.session_state:
    st.session_state.clock_running = False
if "clock_start" not in st.session_state:
    st.session_state.clock_start = None

st.markdown("""
    <style>
        .title { font-size:40px; font-weight:700; margin-bottom:20px; }
        .inv-table th, .inv-table td { padding:8px 12px; text-align:center; border-bottom:1px solid #ddd; }
        .inv-table th { background-color:#f0f0f0; }
        .stButton>button { padding: 0.3em 0.8em; }
    </style>
""", unsafe_allow_html=True)

# ---------- TABS ----------
tabs = st.tabs(["📦 Inventory", "🧱 Materials", "🛠️ Tools", "⏱️ Job Hours", "📏 Tape Calculator"])

# ---------- SHARED FUNCTION ----------
def display_list(data_key, tab_title):
    st.markdown(f'<div class="title">{tab_title}</div>', unsafe_allow_html=True)
    data = st.session_state[data_key]

    for i, item in enumerate(data):
        col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
        with col1:
            st.write(item["name"])
        with col2:
            st.write(item["qty"])
        with col3:
            st.write(f"${item['price']:.2f}")
        with col4:
            c1, c2, c3 = st.columns(3)
            if c1.button("➕", key=f"{data_key}_add_{i}"):
                data[i]["qty"] += 1
            if c2.button("➖", key=f"{data_key}_sub_{i}"):
                data[i]["qty"] = max(0, data[i]["qty"] - 1)
            if c3.button("🗑️", key=f"{data_key}_del_{i}"):
                del data[i]
                st.rerun()

    if st.button("➕ Add New Item", key=f"{data_key}_add_btn"):
        st.session_state[f"{data_key}_form"] = True

    if st.session_state.get(f"{data_key}_form"):
        with st.form(f"{data_key}_form_inner", clear_on_submit=True):
            name = st.text_input("Item Name", key=f"{data_key}_name")
            qty = st.number_input("Quantity", min_value=0, step=1, key=f"{data_key}_qty")
            price = st.number_input("Price", min_value=0.0, step=0.01, format="%.2f", key=f"{data_key}_price")
            submitted = st.form_submit_button("Save Item")
            if submitted and name:
                data.append({"name": name, "qty": qty, "price": price})
                st.session_state[f"{data_key}_form"] = False
                st.rerun()

# ---------- INVENTORY ----------
with tabs[0]:
    display_list("inventory", "📦 Inventory")

# ---------- MATERIALS ----------
with tabs[1]:
    display_list("materials", "🧱 Materials")

# ---------- TOOLS ----------
with tabs[2]:
    display_list("tools", "🛠️ Tools")

# ---------- JOB HOURS ----------
with tabs[3]:
    st.markdown('<div class="title">⏱️ Job Hours</div>', unsafe_allow_html=True)

    job_desc = st.text_input("Job Description", key="job_desc")

    if not st.session_state.clock_running:
        if st.button("▶️ Start Clock"):
            st.session_state.clock_start = datetime.now()
            st.session_state.clock_running = True
            st.rerun()
    else:
        st.write(f"🟢 Clock started at: {st.session_state.clock_start.strftime('%H:%M:%S')}")
        if st.button("⏹️ End Clock"):
            end_time = datetime.now()
            elapsed = end_time - st.session_state.clock_start
            st.session_state.job_log.append({
                "desc": st.session_state.get("job_desc", ""),
                "start": st.session_state.clock_start,
                "end": end_time,
                "hours": round(elapsed.total_seconds() / 3600, 2)
            })
            st.session_state.clock_running = False
            st.rerun()

    st.subheader("Job Log")
    for i, entry in enumerate(st.session_state.job_log):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        with col1:
            st.write(entry["desc"])
        with col2:
            st.write(entry["start"].strftime('%m/%d %H:%M'))
        with col3:
            st.write(f"{entry['hours']} hrs")
        with col4:
            if st.button("🗑️", key=f"del_job_{i}"):
                del st.session_state.job_log[i]
                st.rerun()

    # Totals
    now = datetime.now()
    week_total = sum(e["hours"] for e in st.session_state.job_log if e["start"] > now - timedelta(days=7))
    month_total = sum(e["hours"] for e in st.session_state.job_log if e["start"] > now - timedelta(days=30))
    st.info(f"**This Week:** {week_total:.2f} hrs  |  **This Month:** {month_total:.2f} hrs")

# ---------- TAPE CALCULATOR ----------
with tabs[4]:
    st.markdown('<div class="title">📏 Tape Measure Calculator</div>', unsafe_allow_html=True)

    def parse_measure(text):
        try:
            text = text.strip().replace(' ', '+')
            parts = text.split('+')
            total = sum(float(Fraction(p)) for p in parts)
            return total
        except:
            return None

    col1, col2 = st.columns(2)
    with col1:
        val1 = st.text_input("Measurement 1 (e.g. 3 1/2 or 2+3/8)")
    with col2:
        val2 = st.text_input("Measurement 2")

    operation = st.selectbox("Operation", ["+", "-", "×", "÷"])
    feet_mode = st.checkbox("Include feet in output (e.g. 2ft 3 1/2in)")

    def format_result(inches):
        feet = int(inches // 12)
        rem = inches % 12
        fraction = Fraction(rem).limit_denominator(16)
        if feet_mode:
            return f"{feet}ft {fraction}\""
        else:
            return f"{fraction}\""

    if val1 and val2:
        n1 = parse_measure(val1)
        n2 = parse_measure(val2)
        if n1 is not None and n2 is not None:
            if operation == "+":
                result = n1 + n2
            elif operation == "-":
                result = n1 - n2
            elif operation == "×":
                result = n1 * n2
            elif operation == "÷" and n2 != 0:
                result = n1 / n2
            else:
                result = None

            if result is not None:
                st.success(f"**Result:** {format_result(result)}")
            else:
                st.error("Invalid calculation.")
        else:
            st.error("Couldn't parse one of the inputs.")

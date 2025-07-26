import streamlit as st
from datetime import datetime, timedelta
from fractions import Fraction
import math

st.set_page_config(page_title="All in One", layout="wide")

# Apply custom CSS
st.markdown("""
<style>
    .centered-title { text-align: center; font-size: 2em; font-weight: bold; margin-bottom: 1rem; }
    .inventory-table { border-collapse: collapse; width: 100%; }
    .inventory-table th, .inventory-table td { border: 1px solid #ddd; padding: 8px; text-align: center; }
    .inventory-table th { background-color: #f2f2f2; }
    .button-col button { margin: 0 0.2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="centered-title">All in One</div>', unsafe_allow_html=True)

# Initialize session state
for section in ['Inventory', 'Tools', 'Materials']:
    if f'{section.lower()}_data' not in st.session_state:
        st.session_state[f'{section.lower()}_data'] = []

if 'job_log' not in st.session_state:
    st.session_state.job_log = []

if 'clock_start' not in st.session_state:
    st.session_state.clock_start = None

# -------- Tabs ----------
tabs = st.tabs(["📦 Inventory", "🧰 Tools", "🪵 Materials", "🕒 Job Hours", "📐 Tape Measure Calculator"])

# -------- Inventory Tab ----------
with tabs[0]:
    st.subheader("Inventory")
    inv_data = st.session_state.inventory_data
    cols = st.columns([3, 1, 1, 2])

    with cols[0]: item = st.text_input("Item", key="inv_item")
    with cols[1]: qty = st.number_input("Qty", step=1, key="inv_qty")
    with cols[2]: price = st.number_input("Price", step=0.01, key="inv_price")
    with cols[3]:
        if st.button("Add Item", key="add_inv"):
            inv_data.append({"Item": item, "Qty": int(qty), "Price": float(price)})

    if inv_data:
        st.markdown('<table class="inventory-table"><tr><th>Item</th><th>Qty</th><th>Price</th><th>Actions</th></tr>', unsafe_allow_html=True)
        for i, row in enumerate(inv_data):
            st.markdown(f"""
                <tr>
                    <td>{row['Item']}</td>
                    <td>{row['Qty']}</td>
                    <td>${row['Price']:.2f}</td>
                    <td class="button-col">
                        <form action="" method="post">
                            <button type="submit" name="plus_{i}">+</button>
                            <button type="submit" name="minus_{i}">−</button>
                            <button type="submit" name="del_{i}">🗑️</button>
                        </form>
                    </td>
                </tr>
            """, unsafe_allow_html=True)
            if f'plus_{i}' in st.session_state:
                row['Qty'] += 1
            if f'minus_{i}' in st.session_state and row['Qty'] > 0:
                row['Qty'] -= 1
            if f'del_{i}' in st.session_state:
                inv_data.pop(i)
                break
        st.markdown("</table>", unsafe_allow_html=True)

# -------- Tools Tab ----------
with tabs[1]:
    st.subheader("Tools")
    tools = st.session_state.tools_data
    cols = st.columns([4, 1])

    with cols[0]: tool = st.text_input("Tool", key="tool_input")
    with cols[1]:
        if st.button("Add Tool"):
            tools.append(tool)

    for i, t in enumerate(tools):
        col1, col2 = st.columns([6, 1])
        col1.write(t)
        if col2.button("🗑️", key=f"del_tool_{i}"):
            tools.pop(i)
            break

# -------- Materials Tab ----------
with tabs[2]:
    st.subheader("Materials")
    mats = st.session_state.materials_data
    cols = st.columns([4, 1])

    with cols[0]: mat = st.text_input("Material", key="mat_input")
    with cols[1]:
        if st.button("Add Material"):
            mats.append(mat)

    for i, m in enumerate(mats):
        col1, col2 = st.columns([6, 1])
        col1.write(m)
        if col2.button("🗑️", key=f"del_mat_{i}"):
            mats.pop(i)
            break

# -------- Job Hours Tab ----------
with tabs[3]:
    st.subheader("Job Hours")
    description = st.text_input("Job Description")
    col1, col2 = st.columns(2)

    if st.session_state.clock_start is None:
        if col1.button("Start Clock"):
            st.session_state.clock_start = datetime.now()
            st.rerun()
    else:
        col1.write(f"Started at {st.session_state.clock_start.strftime('%I:%M:%S %p')}")
        if col2.button("End Clock"):
            end_time = datetime.now()
            duration = end_time - st.session_state.clock_start
            st.session_state.job_log.append({
                "desc": description,
                "start": st.session_state.clock_start,
                "end": end_time,
                "duration": duration
            })
            st.session_state.clock_start = None
            st.rerun()

    if st.session_state.job_log:
        st.write("### Logged Jobs")
        total_week = timedelta()
        total_month = timedelta()
        now = datetime.now()

        for i, job in enumerate(st.session_state.job_log):
            start = job['start']
            duration = job['duration']
            if start >= now - timedelta(days=7):
                total_week += duration
            if start.month == now.month and start.year == now.year:
                total_month += duration

            col1, col2, col3, col4 = st.columns([3, 3, 2, 1])
            col1.write(job['desc'])
            col2.write(f"{job['start'].strftime('%Y-%m-%d %I:%M %p')} → {job['end'].strftime('%I:%M %p')}")
            col3.write(f"{duration}")
            if col4.button("🗑️", key=f"del_job_{i}"):
                st.session_state.job_log.pop(i)
                st.rerun()

        st.markdown(f"**Total This Week:** {total_week}")
        st.markdown(f"**Total This Month:** {total_month}")

# -------- Tape Measure Calculator Tab ----------
with tabs[4]:
    st.subheader("Tape Measure Calculator")

    def parse_input(s):
        try:
            s = s.strip().replace(" ", "")
            if "'" in s or '"' in s:
                s = s.replace("'", "").replace('"', "")
            if '/' in s:
                return float(Fraction(s))
            return float(s)
        except:
            return None

    num1 = st.text_input("First Measurement (e.g. 3 3/4)", key="num1")
    operator = st.selectbox("Operation", ["+", "-", "×", "÷"])
    num2 = st.text_input("Second Measurement (e.g. 1 1/8)", key="num2")

    result_area = st.empty()
    if st.button("Calculate"):
        val1 = parse_input(num1)
        val2 = parse_input(num2)
        if val1 is not None and val2 is not None:
            if operator == "+":
                result = val1 + val2
            elif operator == "-":
                result = val1 - val2
            elif operator == "×":
                result = val1 * val2
            elif operator == "÷":
                result = val1 / val2 if val2 != 0 else None

            def format_fraction(x):
                whole = int(x)
                frac = Fraction(x - whole).limit_denominator(16)
                return f"{whole} {frac.numerator}/{frac.denominator}\"" if frac.numerator != 0 else f"{whole}\""

            if result is not None:
                result_area.markdown(f"### Result: `{format_fraction(result)}`")
            else:
                result_area.error("Division by zero.")
        else:
            result_area.error("Invalid input. Use format like 3 3/4")

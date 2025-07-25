import streamlit as st
import datetime

# App title
st.set_page_config(page_title="All in One", layout="wide")
st.markdown("<h1 style='text-align: center;'>All in One</h1>", unsafe_allow_html=True)

# Initialize session state
if 'inventory' not in st.session_state:
    st.session_state.inventory = []

if 'tools' not in st.session_state:
    st.session_state.tools = []

if 'materials' not in st.session_state:
    st.session_state.materials = []

if 'job_log' not in st.session_state:
    st.session_state.job_log = []

# Inventory tab
def inventory_tab():
    st.subheader("Inventory")
    with st.form(key="inventory_form"):
        item = st.text_input("Item")
        qty = st.number_input("Quantity", step=1, min_value=0)
        price = st.number_input("Price", step=0.01, min_value=0.0)
        submitted = st.form_submit_button("Add")
        if submitted and item:
            st.session_state.inventory.append({"item": item, "qty": qty, "price": price})

    st.markdown("### Current Inventory")
    headers = ["Item", "Qty", "Price", "Actions"]
    for col in st.columns(len(headers)):
        col.markdown(f"**{headers[st.columns(len(headers)).index(col)]}**")

    for i, inv in enumerate(st.session_state.inventory):
        cols = st.columns(4)
        cols[0].write(inv['item'])
        cols[1].write(inv['qty'])
        cols[2].write(f"${inv['price']:.2f}")
        with cols[3]:
            col1, col2, col3 = st.columns(3)
            if col1.button("➕", key=f"inc_{i}"):
                inv['qty'] += 1
            if col2.button("➖", key=f"dec_{i}") and inv['qty'] > 0:
                inv['qty'] -= 1
            if col3.button("🗑️", key=f"del_{i}"):
                st.session_state.inventory.pop(i)
                st.experimental_rerun()

# Tools tab
def tools_tab():
    st.subheader("Tools")
    with st.form(key="tools_form"):
        tool = st.text_input("Tool name")
        qty = st.number_input("Quantity", step=1, min_value=0, key="tool_qty")
        add = st.form_submit_button("Add")
        if add and tool:
            st.session_state.tools.append({"tool": tool, "qty": qty})

    st.markdown("### Tool List")
    for i, tool in enumerate(st.session_state.tools):
        cols = st.columns([4, 1, 1])
        cols[0].write(tool["tool"])
        cols[1].write(tool["qty"])
        if cols[2].button("🗑️", key=f"tool_del_{i}"):
            st.session_state.tools.pop(i)
            st.experimental_rerun()

# Materials tab
def materials_tab():
    st.subheader("Materials")
    with st.form(key="materials_form"):
        material = st.text_input("Material name")
        qty = st.number_input("Quantity", step=1, min_value=0, key="mat_qty")
        add = st.form_submit_button("Add")
        if add and material:
            st.session_state.materials.append({"material": material, "qty": qty})

    st.markdown("### Material List")
    for i, mat in enumerate(st.session_state.materials):
        cols = st.columns([4, 1, 1])
        cols[0].write(mat["material"])
        cols[1].write(mat["qty"])
        if cols[2].button("🗑️", key=f"mat_del_{i}"):
            st.session_state.materials.pop(i)
            st.experimental_rerun()

# Job Hours tab
def job_hours_tab():
    st.subheader("Job Hours")
    if "job_clock" not in st.session_state:
        st.session_state.job_clock = {"start": None}

    with st.form("job_entry_form"):
        desc = st.text_input("Job Description")
        start_btn = st.form_submit_button("Start Clock")
        if start_btn and desc:
            st.session_state.job_clock["start"] = datetime.datetime.now()
            st.session_state.job_clock["desc"] = desc
            st.experimental_rerun()

    if st.session_state.job_clock["start"]:
        end_btn = st.button("End Clock")
        if end_btn:
            end_time = datetime.datetime.now()
            start_time = st.session_state.job_clock["start"]
            duration = round((end_time - start_time).total_seconds() / 3600, 2)
            st.session_state.job_log.append({
                "desc": st.session_state.job_clock["desc"],
                "start": start_time,
                "end": end_time,
                "hours": duration
            })
            st.session_state.job_clock = {"start": None}
            st.experimental_rerun()

    # Show job log
    st.markdown("### Job History")
    total_week = 0
    total_month = 0
    today = datetime.datetime.now()
    for i, log in enumerate(st.session_state.job_log):
        log_date = log["start"]
        week_diff = (today - log_date).days < 7
        month_diff = (today - log_date).days < 31
        if week_diff:
            total_week += log["hours"]
        if month_diff:
            total_month += log["hours"]

        st.write(f"**{log['desc']}** — {log['start'].strftime('%Y-%m-%d %H:%M')} to {log['end'].strftime('%H:%M')} — {log['hours']} hrs")
        if st.button("🗑️ Delete", key=f"job_del_{i}"):
            st.session_state.job_log.pop(i)
            st.experimental_rerun()

    st.markdown(f"**Total hours this week:** {round(total_week, 2)}")
    st.markdown(f"**Total hours this month:** {round(total_month, 2)}")

# Sidebar navigation
tab = st.sidebar.radio("Navigate", ["Inventory", "Tools", "Materials", "Job Hours"])
if tab == "Inventory":
    inventory_tab()
elif tab == "Tools":
    tools_tab()
elif tab == "Materials":
    materials_tab()
elif tab == "Job Hours":
    job_hours_tab()

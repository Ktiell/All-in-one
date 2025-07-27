# All-in-One Streamlit App
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ---------- Custom CSS ----------
def local_css():
    st.markdown("""
        <style>
            .main {
                background-color: #f4f4f4;
            }
            .stButton>button {
                border-radius: 10px;
                margin: 2px;
            }
            .inventory-table td, .inventory-table th {
                padding: 6px 12px;
                text-align: left;
            }
        </style>
    """, unsafe_allow_html=True)

local_css()

# ---------- App Title ----------
st.title("🧰 All in One")

# ---------- Session State Setup ----------
for tab in ["Inventory", "Tools", "Materials", "Labor"]:
    if f"{tab}_df" not in st.session_state:
        st.session_state[f"{tab}_df"] = pd.DataFrame(columns=["Item", "Qty", "Price"])

if "Labor_log" not in st.session_state:
    st.session_state["Labor_log"] = []

if "clock_active" not in st.session_state:
    st.session_state["clock_active"] = False

if "start_time" not in st.session_state:
    st.session_state["start_time"] = None

# ---------- Helper Functions ----------
def render_table(tab_name):
    df = st.session_state[f"{tab_name}_df"]
    st.write(f"### {tab_name}")
    edited_rows = []
    for i, row in df.iterrows():
        cols = st.columns([4, 1, 1, 1, 1])
        cols[0].write(row["Item"])
        cols[1].write(row["Qty"])
        cols[2].write(row["Price"])
        if cols[3].button("➕", key=f"{tab_name}_add_{i}"):
            df.at[i, "Qty"] += 1
        if cols[4].button("➖", key=f"{tab_name}_sub_{i}"):
            if df.at[i, "Qty"] > 0:
                df.at[i, "Qty"] -= 1
        if cols[0].button("🗑️", key=f"{tab_name}_del_{i}"):
            edited_rows.append(i)
    for i in edited_rows:
        df.drop(index=i, inplace=True)
    df.reset_index(drop=True, inplace=True)

def add_item(tab_name):
    with st.form(f"add_{tab_name}"):
        item = st.text_input("Item Name", key=f"{tab_name}_item")
        qty = st.number_input("Quantity", min_value=0, value=1, key=f"{tab_name}_qty")
        price = st.number_input("Price", min_value=0.0, value=0.0, step=0.01, key=f"{tab_name}_price")
        submitted = st.form_submit_button("Add")
        if submitted and item:
            new_row = pd.DataFrame([{"Item": item, "Qty": qty, "Price": price}])
            st.session_state[f"{tab_name}_df"] = pd.concat([st.session_state[f"{tab_name}_df"], new_row], ignore_index=True)

def render_labor_log():
    st.write("### Labor Log")
    desc = st.text_input("Task Description", key="desc")
    if not st.session_state["clock_active"]:
        if st.button("▶️ Start Clock"):
            st.session_state["clock_active"] = True
            st.session_state["start_time"] = datetime.now()
            st.session_state["current_desc"] = desc
    else:
        if st.button("⏹️ End Clock"):
            end_time = datetime.now()
            duration = end_time - st.session_state["start_time"]
            st.session_state["Labor_log"].append({
                "Description": st.session_state["current_desc"],
                "Start": st.session_state["start_time"],
                "End": end_time,
                "Duration": duration
            })
            st.session_state["clock_active"] = False
            st.session_state["start_time"] = None

    total_week = timedelta()
    total_month = timedelta()
    now = datetime.now()
    for entry in st.session_state["Labor_log"]:
        if entry["Start"].isocalendar().week == now.isocalendar().week:
            total_week += entry["Duration"]
        if entry["Start"].month == now.month:
            total_month += entry["Duration"]

    st.success(f"**Total this week:** {str(total_week)} | **This month:** {str(total_month)}")

    for i, entry in enumerate(st.session_state["Labor_log"]):
        col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 1])
        col1.write(entry["Description"])
        col2.write(entry["Start"].strftime("%Y-%m-%d %H:%M"))
        col3.write(entry["End"].strftime("%Y-%m-%d %H:%M"))
        col4.write(str(entry["Duration"]))
        if col5.button("🗑️", key=f"del_log_{i}"):
            st.session_state["Labor_log"].pop(i)
            st.experimental_rerun()

# ---------- Tab Layout ----------
tab1, tab2, tab3, tab4 = st.tabs(["Inventory", "Tools", "Materials", "Labor"])

with tab1:
    render_table("Inventory")
    st.markdown("---")
    add_item("Inventory")

with tab2:
    render_table("Tools")
    st.markdown("---")
    add_item("Tools")

with tab3:
    render_table("Materials")
    st.markdown("---")
    add_item("Materials")

with tab4:
    render_labor_log()

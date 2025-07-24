import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

st.set_page_config(page_title="Board & Soul App", layout="wide")
st.title("Board & Soul Business Manager")
st.markdown("Easily track tools, job logs, and inventory for your woodworking business.")

# Initialize session state
if "tools" not in st.session_state:
    st.session_state.tools = []

if "logs" not in st.session_state:
    st.session_state.logs = []

if "inventory" not in st.session_state:
    st.session_state.inventory = []

# Tabs
tab1, tab2, tab3 = st.tabs(["🛠️ Tools & Materials", "📷 Job Logs", "📦 Inventory"])

# ---------- Tools Tab ----------
with tab1:
    st.header("Add Tool or Material")
    with st.form("tool_form", clear_on_submit=True):
        name = st.text_input("Name")
        category = st.selectbox("Type", ["Tool", "Material"])
        qty = st.number_input("Quantity", 1)
        notes = st.text_area("Notes")
        submit = st.form_submit_button("Add")
        if submit:
            st.session_state.tools.append({
                "id": str(uuid.uuid4()),
                "name": name,
                "category": category,
                "qty": qty,
                "notes": notes,
                "timestamp": datetime.now()
            })
            st.success("Item added!")

    if st.session_state.tools:
        df = pd.DataFrame(st.session_state.tools)
        st.dataframe(df[["name", "category", "qty", "notes", "timestamp"]])

# ---------- Logs Tab ----------
with tab2:
    st.header("Daily Job Log")
    with st.form("log_form", clear_on_submit=True):
        desc = st.text_area("Work Notes")
        photo = st.file_uploader("Photo (optional)", type=["jpg", "jpeg", "png"])
        log_submit = st.form_submit_button("Save Log")
        if log_submit:
            st.session_state.logs.append({
                "id": str(uuid.uuid4()),
                "desc": desc,
                "photo": photo.read() if photo else None,
                "timestamp": datetime.now()
            })
            st.success("Log saved!")

    for log in st.session_state.logs[::-1]:
        st.markdown(f"**Date:** {log['timestamp'].strftime('%Y-%m-%d %H:%M')}")
        st.markdown(log["desc"])
        if log["photo"]:
            st.image(log["photo"], width=300)
        st.markdown("---")

# ---------- Inventory Tab ----------
with tab3:
    st.header("Track Inventory")
    with st.form("inventory_form", clear_on_submit=True):
        item = st.text_input("Item Name")
        qty = st.number_input("Quantity", min_value=1, value=1)
        status = st.selectbox("Status", ["For Sale", "Sold"])
        image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        add_item = st.form_submit_button("Add")
        if add_item:
            st.session_state.inventory.append({
                "id": str(uuid.uuid4()),
                "item": item,
                "qty": qty,
                "status": status,
                "image": image.read() if image else None,
                "timestamp": datetime.now()
            })
            st.success("Inventory item added!")

    if st.session_state.inventory:
        st.subheader("Inventory List")
        for inv in st.session_state.inventory:
            cols = st.columns([2, 1, 1])
            with cols[0]:
                st.markdown(f"**{inv['item']}**")
                st.markdown(f"Qty: {inv['qty']}")
                st.markdown(f"Status: {inv['status']}")
                new_status = st.selectbox(
                    "Change Status",
                    ["For Sale", "Sold"],
                    index=0 if inv["status"] == "For Sale" else 1,
                    key=inv["id"]
                )
                if new_status != inv["status"]:
                    inv["status"] = new_status
                    st.success(f"Updated status to {new_status}")
            with cols[1]:
                if inv["image"]:
                    st.image(inv["image"], width=100)
            with cols[2]:
                if st.button("🗑️ Remove", key="del_" + inv["id"]):
                    st.session_state.inventory = [x for x in st.session_state.inventory if x["id"] != inv["id"]]
                    st.experimental_rerun()

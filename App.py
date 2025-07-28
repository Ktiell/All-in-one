import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="All in One", layout="wide")

st.sidebar.title("All in One")
page = st.sidebar.radio("Go to", ["Inventory", "Materials", "Job Hours", "Calculator", "Build Tracker"])

# ---------- Inventory ----------
if page == "Inventory":
    st.title("Inventory")
    if "inventory" not in st.session_state:
        st.session_state.inventory = pd.DataFrame(columns=["Item", "Qty", "Price"])

    st.subheader("Current Inventory")
    inventory_df = st.session_state.inventory
    edited_df = st.data_editor(
        inventory_df,
        num_rows="dynamic",
        use_container_width=True,
        key="inventory_editor"
    )
    st.session_state.inventory = edited_df

    with st.expander("➕ Add Item to Inventory"):
        col1, col2, col3 = st.columns(3)
        item = col1.text_input("Item Name")
        qty = col2.number_input("Quantity", step=1, value=1)
        price = col3.number_input("Price", step=1.0, value=0.0)
        if st.button("Add Item"):
            st.session_state.inventory = pd.concat([
                st.session_state.inventory,
                pd.DataFrame([{"Item": item, "Qty": qty, "Price": price}])
            ], ignore_index=True)
            st.success(f"Added {item} to inventory.")

# ---------- Materials ----------
elif page == "Materials":
    st.title("Materials")
    if "materials" not in st.session_state:
        st.session_state.materials = pd.DataFrame(columns=["Material", "Qty", "Cost"])

    st.subheader("Current Materials")
    materials_df = st.session_state.materials
    edited_df = st.data_editor(
        materials_df,
        num_rows="dynamic",
        use_container_width=True,
        key="materials_editor"
    )
    st.session_state.materials = edited_df

    with st.expander("➕ Add Material"):
        col1, col2, col3 = st.columns(3)
        material = col1.text_input("Material Name")
        qty = col2.number_input("Quantity", step=1, value=1, key="mat_qty")
        cost = col3.number_input("Cost", step=1.0, value=0.0, key="mat_cost")
        if st.button("Add Material"):
            st.session_state.materials = pd.concat([
                st.session_state.materials,
                pd.DataFrame([{"Material": material, "Qty": qty, "Cost": cost}])
            ], ignore_index=True)
            st.success(f"Added {material} to materials.")

# ---------- Job Hours ----------
elif page == "Job Hours":
    st.title("Labor Log")
    if "job_log" not in st.session_state:
        st.session_state.job_log = []

    with st.form("job_form"):
        desc = st.text_input("Task Description")
        if st.form_submit_button("Start Clock"):
            st.session_state.job_log.append({
                "desc": desc,
                "start": datetime.now(),
                "end": None
            })

    for i, job in enumerate(st.session_state.job_log):
        if job["end"] is None:
            if st.button(f"End Clock for: {job['desc']}", key=f"end_{i}"):
                st.session_state.job_log[i]["end"] = datetime.now()

    log_df = pd.DataFrame([
        {
            "Description": job["desc"],
            "Start": job["start"],
            "End": job["end"],
            "Hours": round((job["end"] - job["start"]).seconds / 3600, 2) if job["end"] else None
        } for job in st.session_state.job_log
    ])
    st.dataframe(log_df, use_container_width=True)
    week_total = log_df["Hours"].sum() if "Hours" in log_df else 0
    st.markdown(f"**Total Hours Worked:** {week_total:.2f}")

# ---------- Calculator ----------
elif page == "Calculator":
    st.title("Tape Measure Calculator")
    st.write("Coming soon!")

# ---------- Build Tracker ----------
elif page == "Build Tracker":
    st.title("Build Tracker")
    if "build_df" not in st.session_state:
        st.session_state.build_df = pd.DataFrame(
            columns=["Product", "Status", "Start Time", "End Time", "Hours"]
        )

    with st.expander("➕ Add / Update Product Status"):
        col1, col2 = st.columns(2)
        product = col1.selectbox(
            "Product",
            [
                "Rustic Entryway Shelf",
                "Mosaic Wall Art",
                "Compact Side Table",
            ],
        )
        status = col2.selectbox("Status", ["TO BUILD", "

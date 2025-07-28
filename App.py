
import streamlit as st
import pandas as pd
from datetime import datetime

# Sidebar navigation
st.sidebar.title("All in One")
page = st.sidebar.radio("Go to", ["Inventory", "Materials", "Job Hours", "Calculator", "Build Tracker"])

# ---------- Inventory ----------
if page == "Inventory":
    st.title("ðŸ§° Inventory")
    if "inventory" not in st.session_state:
        st.session_state.inventory = pd.DataFrame(columns=["Item", "Qty", "Price"])
    col1, col2, col3 = st.columns(3)
    item = col1.text_input("Item")
    qty = col2.number_input("Qty", step=1, value=1)
    price = col3.number_input("Price", step=1.0, value=0.0)
    if st.button("Add"):
        st.session_state.inventory = pd.concat([
            st.session_state.inventory,
            pd.DataFrame([{"Item": item, "Qty": qty, "Price": price}])
        ], ignore_index=True)
    st.dataframe(st.session_state.inventory, use_container_width=True)

# ---------- Materials ----------
elif page == "Materials":
    st.title("ðŸªµ Materials")
    if "materials" not in st.session_state:
        st.session_state.materials = pd.DataFrame(columns=["Material", "Qty", "Cost"])
    col1, col2, col3 = st.columns(3)
    material = col1.text_input("Material")
    qty = col2.number_input("Qty", step=1, value=1, key="mat_qty")
    cost = col3.number_input("Cost", step=1.0, value=0.0, key="mat_cost")
    if st.button("Add Material"):
        st.session_state.materials = pd.concat([
            st.session_state.materials,
            pd.DataFrame([{"Material": material, "Qty": qty, "Cost": cost}])
        ], ignore_index=True)
    st.dataframe(st.session_state.materials, use_container_width=True)

# ---------- Job Hours ----------
elif page == "Job Hours":
    st.title("â±ï¸ Labor Log")
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
    st.title("ðŸ“ Tape Measure Calculator")
    st.write("Feature coming soon!")

# ---------- Build Tracker ----------
elif page == "Build Tracker":
    st.subheader("ðŸ“¦ Product Build Tracker")
    if "build_df" not in st.session_state:
        st.session_state.build_df = pd.DataFrame(
            columns=["Product", "Status", "Start Time", "End Time", "Hours"]
        )

    with st.form("add_build"):
        col1, col2 = st.columns(2)
        product = col1.selectbox(
            "Product",
            [
                "Rustic Entryway Shelf",
                "Mosaic Wall Art",
                "Compact Side Table",
            ],
        )
        status = col2.selectbox("Status", ["TO BUILD", "IN PROGRESS", "DONE"])
        submit = st.form_submit_button("Save / Update")

    if submit:
        now = datetime.now()
        df = st.session_state.build_df
        if ((df["Product"] == product) & (df["Status"] != "DONE")).any():
            idx = df[(df["Product"] == product) & (df["Status"] != "DONE")].index[0]
            df.at[idx, "Status"] = status
            if status == "IN PROGRESS":
                df.at[idx, "Start Time"] = now
            if status == "DONE":
                df.at[idx, "End Time"] = now
                start = df.at[idx, "Start Time"]
                df.at[idx, "Hours"] = round((now - start).seconds / 3600, 2)
        else:
            st.session_state.build_df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        {
                            "Product": [product],
                            "Status": [status],
                            "Start Time": [now if status == "IN PROGRESS" else None],
                            "End Time": [None],
                            "Hours": [None],
                        }
                    ),
                ],
                ignore_index=True,
            )

    st.dataframe(
        st.session_state.build_df.sort_values(by=["Status", "Product"]),
        use_container_width=True,
        hide_index=True,
    )

    done = st.session_state.build_df[st.session_state.build_df["Status"] == "DONE"]
    st.markdown(
        f"**Total finished this month:** {done.shape[0]}  |  "
        f"**Total build hours:** {done['Hours'].sum():.2f}"
            )

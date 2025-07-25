
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
if "job_desc" not in st.session_state:
    st.session_state.job_desc = ""

# ---------------- TABS ---------------- #
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Inventory", "Tools", "Materials", "Job Hours", "Calculator"])

# ---------------- JOB HOURS TAB ---------------- #
with tab4:
    st.subheader("Job Hours Tracker")
    now = datetime.now()

    if st.session_state.clock_start is None:
        st.session_state.job_desc = st.text_input("What are you working on?")
        if st.button("Start Clock"):
            st.session_state.clock_start = now
    else:
        st.success(f"Clock started at {st.session_state.clock_start.strftime('%I:%M %p')}")
        st.write(f"Description: {st.session_state.job_desc}")
        if st.button("End Clock"):
            end_time = datetime.now()
            duration = end_time - st.session_state.clock_start
            st.session_state.job_hours.append({
                "Start": st.session_state.clock_start,
                "End": end_time,
                "Duration": duration,
                "Description": st.session_state.job_desc
            })
            st.session_state.clock_start = None
            st.session_state.job_desc = ""
            st.success(f"Session ended: {duration}")

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
        for i, entry in enumerate(reversed(st.session_state.job_hours)):
            idx = len(st.session_state.job_hours) - 1 - i
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(
                    f"**Start:** {entry['Start'].strftime('%Y-%m-%d %I:%M %p')} | "
                    f"**End:** {entry['End'].strftime('%Y-%m-%d %I:%M %p')} | "
                    f"**Hours:** {round(entry['Duration'].total_seconds() / 3600, 2)} | "
                    f"**Note:** {entry['Description']}"
                )
            with col2:
                if st.button("ðŸ—‘ï¸", key=f"del_{idx}"):
                    del st.session_state.job_hours[idx]
                    st.experimental_rerun()

# ---------------- CALCULATOR PLACEHOLDER ---------------- #
with tab5:
    st.subheader("Tape Measure Calculator")
    st.markdown("ðŸ› ï¸ Calculator fix coming next...")

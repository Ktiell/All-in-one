import streamlit as st import datetime

st.set_page_config(page_title="All-in-One App", layout="centered")

-------------------------------

INVENTORY TAB

-------------------------------

if 'inventory' not in st.session_state: st.session_state.inventory = []

Sidebar Navigation

selected_tab = st.selectbox("", ["Inventory", "Tools", "Materials", "Job Hours", "Calculator"], format_func=lambda x: x, index=0)

if selected_tab == "Inventory": st.title("Inventory") item_name = st.text_input("Item name") qty = st.number_input("Quantity", step=1, value=1) if st.button("Add to Inventory"): if item_name: st.session_state.inventory.append((item_name, qty))

if st.session_state.inventory:
    st.subheader("Items (A to Z)")
    for name, qty in sorted(st.session_state.inventory):
        st.write(f"{name}: {qty}")

-------------------------------

TOOLS TAB

-------------------------------

elif selected_tab == "Tools": st.title("Tools") if 'tools' not in st.session_state: st.session_state.tools = []

tool = st.text_input("Tool name")
if st.button("Add Tool"):
    if tool:
        st.session_state.tools.append(tool)

if st.session_state.tools:
    st.subheader("Tools List")
    for t in sorted(st.session_state.tools):
        st.write(t)

-------------------------------

MATERIALS TAB

-------------------------------

elif selected_tab == "Materials": st.title("Materials") if 'materials' not in st.session_state: st.session_state.materials = []

material = st.text_input("Material name")
if st.button("Add Material"):
    if material:
        st.session_state.materials.append(material)

if st.session_state.materials:
    st.subheader("Material List")

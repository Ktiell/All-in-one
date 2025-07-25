
import streamlit as st
import datetime

st.set_page_config(page_title="All in One", layout="wide")

# ---------- Inventory Tab ----------
st.title("All in One Â· App")

st.header("Inventory Management")

if "inventory" not in st.session_state:
    st.session_state.inventory = []

with st.expander("Add New Inventory Item"):
    item_name = st.text_input("Item Name", key="new_item_name")
    quantity = st.number_input("Quantity", min_value=0, step=1, key="new_quantity")
    price = st.number_input("Price", min_value=0.0, step=0.01, key="new_price")
    if st.button("Add Inventory Item"):
        st.session_state.inventory.append({
            "item": item_name,
            "qty": quantity,
            "price": price
        })
        st.success("Item added!")

st.subheader("Current Inventory")
if st.session_state.inventory:
    cols = st.columns([3, 2, 2, 1, 1, 1])
    headers = ["Item", "Qty", "Price", "Add", "Remove", "Delete"]
    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")

    for idx, entry in enumerate(st.session_state.inventory):
        cols = st.columns([3, 2, 2, 1, 1, 1])
        cols[0].markdown(entry["item"])
        cols[1].markdown(str(entry["qty"]))
        cols[2].markdown(f"${entry['price']:.2f}")
        if cols[3].button("+", key=f"add_{idx}"):
            entry["qty"] += 1
        if cols[4].button("-", key=f"remove_{idx}"):
            if entry["qty"] > 0:
                entry["qty"] -= 1
        if cols[5].button("X", key=f"delete_{idx}"):
            st.session_state.inventory.pop(idx)
            st.experimental_rerun()
else:
    st.info("No inventory items added yet.")

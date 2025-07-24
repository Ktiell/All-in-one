import streamlit as st
import uuid

st.set_page_config(page_title="All-in-One App", layout="wide")

# Initialize session state
if "inventory" not in st.session_state:
    st.session_state.inventory = []

st.title("🛠️ All-in-One App")
st.markdown("Manage your items, sales, and shop inventory.")

st.header("➕ Add Item")
with st.form("add_item_form"):
    name = st.text_input("Item Name")
    qty = st.number_input("Quantity", min_value=1, value=1)
    status = st.selectbox("Status", ["For Sale", "Sold"])
    submitted = st.form_submit_button("Add Item")
    if submitted and name:
        st.session_state.inventory.append({
            "id": str(uuid.uuid4()),
            "name": name,
            "qty": qty,
            "status": status
        })
        st.rerun()

# Divider
st.markdown("---")
st.header("📦 Inventory List")

# Show inventory
if not st.session_state.inventory:
    st.info("No items in inventory yet.")
else:
    for item in st.session_state.inventory:
        col1, col2, col3, col4 = st.columns([3, 2, 3, 2])
        with col1:
            st.markdown(f"**{item['name']}**")
        with col2:
            st.markdown(f"Qty: {item['qty']}")
        with col3:
            new_status = st.selectbox(
                "Change Status",
                ["For Sale", "Sold"],
                index=0 if item['status'] == "For Sale" else 1,
                key=item['id']
            )
            if new_status != item['status']:
                item['status'] = new_status
                st.rerun()
        with col4:
            if st.button("🗑️ Remove", key="remove_" + item['id']):
                st.session_state.inventory = [i for i in st.session_state.inventory if i['id'] != item['id']]
                st.rerun()

# -----------------------------
# INVENTORY TRACKER (with delete button)
# -----------------------------
with tab3:
    st.header("📦 Product Inventory")

    # Add new inventory item
    with st.form("inv_form"):
        item = st.text_input("Item Name")
        price = st.number_input("Price ($)", min_value=0.0)
        status = st.selectbox("Status", ["For Sale", "Sold"])
        inv_photo = st.file_uploader("Photo (optional)", type=["jpg", "png"])
        submit_inv = st.form_submit_button("Add to Inventory")
        if submit_inv and item:
            inv_row = {
                "Item": item,
                "Price": price,
                "Status": status,
                "Photo": inv_photo.name if inv_photo else "None"
            }
            st.session_state.setdefault("inventory", []).append(inv_row)
            st.success(f"Added: {item}")

    # Show inventory
    inventory_data = st.session_state.get("inventory", [])
    if inventory_data:
        st.subheader("Your Inventory")

        for idx, item in enumerate(inventory_data):
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
            col1.markdown(f"**{item['Item']}**")
            col2.write(f"${item['Price']:.2f}")
            col3.write(item["Status"])
            col4.write(item["Photo"])
            if col5.button("❌", key=f"del_{idx}"):
                del st.session_state["inventory"][idx]
                st.experimental_rerun()

        # Download updated CSV
        df = pd.DataFrame(inventory_data)
        inv_csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Inventory CSV", inv_csv, "inventory.csv", "text/csv")
    else:
        st.info("No inventory items yet.")

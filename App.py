# -----------------------------
# INVENTORY TRACKER (with delete)
# -----------------------------
with tab3:
    st.header("Product Inventory")

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
            st.success(f"Added to inventory: {item}")

    inv_df = pd.DataFrame(st.session_state.get("inventory", []))

    if not inv_df.empty:
        st.subheader("Current Inventory")

        # Create delete buttons for each item
        for i, row in inv_df.iterrows():
            cols = st.columns([4, 2, 2, 2, 1])
            cols[0].write(f"📦 {row['Item']}")
            cols[1].write(f"${row['Price']:.2f}")
            cols[2].write(row["Status"])
            cols[3].write(row["Photo"])
            if cols[4].button("🗑️", key=f"delete_{i}"):
                st.session_state["inventory"].pop(i)
                st.experimental_rerun()

        # Download updated table
        inv_csv = inv_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Inventory CSV", inv_csv, "inventory.csv", "text/csv")

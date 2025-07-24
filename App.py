# -----------------------------
# INVENTORY TRACKER (delete + status toggle)
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

    # Show inventory list
    inventory_data = st.session_state.get("inventory", [])
    if inventory_data:
        st.subheader("Your Inventory")

        for idx, item in enumerate(inventory_data):
            st.markdown("---")
            st.markdown(f"**🪵 {item['Item']}** — ${item['Price']:.2f}")
            st.text(f"Status: {item['Status']} | Photo: {item['Photo']}")

            col1, col2 = st.columns(2)
            if col1.button("❌ Delete", key=f"del_{idx}"):
                del st.session_state["inventory"][idx]
                st.experimental_rerun()

            toggle_label = "Mark as Sold" if item["Status"] == "For Sale" else "Mark as For Sale"
            if col2.button(toggle_label, key=f"toggle_{idx}"):
                st.session_state["inventory"][idx]["Status"] = (
                    "Sold" if item["Status"] == "For Sale" else "For Sale"
                )
                st.experimental_rerun()

        # Download updated CSV
        df = pd.DataFrame(inventory_data)
        inv_csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Inventory CSV", inv_csv, "inventory.csv", "text/csv")

    else:
        st.info("No inventory items yet.")

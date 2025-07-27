with tabs[1]:
    st.subheader("Materials")

    # Add material inputs
    col1, col2 = st.columns([4, 1])
    mat_name = col1.text_input("Material Name", key="mat_name_input")
    mat_qty = col2.number_input("Qty", min_value=0, step=1, value=1, key="mat_qty_input")

    if st.button("➕ Add Material"):
        if mat_name:
            st.session_state.materials.append({"name": mat_name, "qty": mat_qty})

    # Render table-style layout manually
    st.markdown("#### Material List")
    st.markdown(
        """
        <style>
        .material-table th, .material-table td {
            padding: 6px 12px;
            text-align: center;
            border-bottom: 1px solid #444;
        }
        .material-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<table class='material-table'><tr><th>Material</th><th>Qty</th><th colspan='3'>Actions</th></tr>", unsafe_allow_html=True)

    for i, item in enumerate(st.session_state.materials):
        st.markdown(
            f"<tr><td>{item['name']}</td><td>{item['qty']}</td><td>➕</td><td>➖</td><td>🗑️</td></tr>",
            unsafe_allow_html=True
        )
        cols = st.columns([1, 1, 1])
        with cols[0]:
            if st.button(" ", key=f"mat_plus_{i}", help="Add Qty"):
                item["qty"] += 1
                st.rerun()
        with cols[1]:
            if st.button(" ", key=f"mat_minus_{i}", help="Subtract Qty"):
                if item["qty"] > 0:
                    item["qty"] -= 1
                    st.rerun()
        with cols[2]:
            if st.button(" ", key=f"mat_delete_{i}", help="Delete Material"):
                st.session_state.materials.pop(i)
                st.rerun()

    st.markdown("</table>", unsafe_allow_html=True)

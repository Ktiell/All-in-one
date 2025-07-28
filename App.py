import streamlit as st
from datetime import datetime, timedelta
from fractions import Fraction

st.set_page_config(page_title="All in One", layout="wide")

# Custom CSS for clean look
st.markdown("""
    <style>
        .title { font-size:40px; font-weight:700; margin-bottom:20px; }
        .add-form { background:#f9f9f9; padding:15px; border-radius:12px; box-shadow:0 2px 5px rgba(0,0,0,0.1); }
        .inv-table th, .inv-table td { padding:6px 12px; text-align:center; border-bottom:1px solid #ddd; }
        .inv-table th { background-color:#f0f0f0; }
        .inv-table td button { margin: 0 2px; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "inventory" not in st.session_state:
    st.session_state.inventory = []

tabs = st.tabs(["📦 Inventory", "🧱 Materials", "🛠️ Tools", "⏱️ Job Hours", "📏 Tape Calculator"])

# ========== INVENTORY TAB ==========
with tabs[0]:
    st.markdown('<div class="title">📦 Inventory</div>', unsafe_allow_html=True)

    def render_inventory_table():
        st.markdown("<table class='inv-table'><thead><tr><th>Item</th><th>Qty</th><th>Price</th><th>Actions</th></tr></thead><tbody>", unsafe_allow_html=True)
        for idx, item in enumerate(st.session_state.inventory):
            st.markdown(f"""
                <tr>
                    <td>{item['name']}</td>
                    <td>{item['qty']}</td>
                    <td>${item['price']:.2f}</td>
                    <td>
                        <form action="" method="post">
                            <button type="submit" name="action" value="add-{idx}">➕</button>
                            <button type="submit" name="action" value="sub-{idx}">➖</button>
                            <button type="submit" name="action" value="del-{idx}">🗑️</button>
                        </form>
                    </td>
                </tr>
            """, unsafe_allow_html=True)
        st.markdown("</tbody></table>", unsafe_allow_html=True)

        # Handle actions
        action = st.experimental_get_query_params().get("action", [None])[0]
        if action:
            prefix, idx = action.split("-")
            idx = int(idx)
            if prefix == "add":
                st.session_state.inventory[idx]['qty'] += 1
            elif prefix == "sub" and st.session_state.inventory[idx]['qty'] > 0:
                st.session_state.inventory[idx]['qty'] -= 1
            elif prefix == "del":
                del st.session_state.inventory[idx]
            st.experimental_set_query_params()  # Clear query after action

    render_inventory_table()

    # Toggle add item form
    if st.button("➕ Add New Item"):
        st.session_state.show_add = True
    if st.session_state.get("show_add"):
        with st.container():
            st.markdown('<div class="add-form">', unsafe_allow_html=True)
            name = st.text_input("Item Name")
            qty = st.number_input("Quantity", min_value=0, step=1)
            price = st.number_input("Price", min_value=0.0, step=0.01, format="%.2f")
            if st.button("Save Item"):
                if name:
                    st.session_state.inventory.append({"name": name, "qty": qty, "price": price})
                    st.session_state.show_add = False
                    st.experimental_rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ========== PLACEHOLDERS FOR OTHER TABS ==========
with tabs[1]:
    st.header("🧱 Materials")
    st.info("Materials tab content goes here...")

with tabs[2]:
    st.header("🛠️ Tools")
    st.info("Tools tab content goes here...")

with tabs[3]:
    st.header("⏱️ Job Hours")
    st.info("Job hour logging interface coming next...")

with tabs[4]:
    st.header("📏 Tape Calculator")
    st.info("Tape measure calculator coming soon...")

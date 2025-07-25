def format_fraction_inches(value):
    try:
        total_inches = float(value)
        feet = int(total_inches) // 12
        inches = total_inches - (feet * 12)
        frac_inches = Fraction(inches).limit_denominator(16)
        if feet > 0:
            return f"{feet}' {frac_inches}\""
        else:
            return f"{frac_inches}\""
    except:
        return "Invalid"

def parse_mixed_fraction(text):
    try:
        parts = text.strip().split()
        if len(parts) == 2:
            whole = int(parts[0])
            frac = Fraction(parts[1])
            return whole + frac
        elif len(parts) == 1:
            return Fraction(parts[0])
        else:
            return None
    except:
        return None

def tape_calc():
    st.sidebar.header("📏 Tape Measure Calculator")

    if "calculator_total" not in st.session_state:
        st.session_state.calculator_total = Fraction(0)

    left = st.sidebar.text_input("First value (e.g. 3 1/2)", key="left_input")
    operator = st.sidebar.selectbox("Operation", ["+", "-", "*", "÷"], key="op")
    right = st.sidebar.text_input("Second value (e.g. 1/4)", key="right_input")

    col1, col2 = st.sidebar.columns([1, 1])
    equals = col1.button("Calculate", key="equals_btn")
    reset = col2.button("Reset Total", key="reset_btn")

    if reset:
        st.session_state.calculator_total = Fraction(0)

    if equals:
        a = parse_mixed_fraction(left)
        b = parse_mixed_fraction(right)

        if a is None or b is None:
            st.sidebar.error("Invalid input format. Try '3 1/4' or '1/8'")
        else:
            try:
                if operator == "+":
                    result = a + b
                elif operator == "-":
                    result = a - b
                elif operator == "*":
                    result = a * b
                elif operator == "÷":
                    result = a / b

                st.session_state.calculator_total += result
                st.sidebar.success(f"{left} {operator} {right} = {format_fraction_inches(result)}")
            except Exception as e:
                st.sidebar.error(f"Error in calculation: {e}")

    st.sidebar.markdown("### Running Total")
    st.sidebar.markdown(f"**{format_fraction_inches(st.session_state.calculator_total)}**")

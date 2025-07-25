def format_fraction_inches(value):
    feet = int(value) // 12
    inches = value - feet * 12
    frac_inches = Fraction(inches).limit_denominator(16)
    if feet > 0:
        return f"{feet}' {frac_inches}\""
    else:
        return f"{frac_inches}\""

def parse_mixed_fraction(text):
    try:
        parts = text.strip().split()
        if len(parts) == 2:  # e.g. "3 1/4"
            whole = int(parts[0])
            frac = Fraction(parts[1])
            return whole + frac
        elif len(parts) == 1:
            return Fraction(parts[0])
    except:
        return None
    return None

def tape_calc():
    st.sidebar.header("📏 Tape Measure Calculator")

    left = st.sidebar.text_input("First value (e.g. 3 1/2)", key="left_input")
    operator = st.sidebar.selectbox("Operation", ["+", "-", "*", "÷"], key="op")
    right = st.sidebar.text_input("Second value (e.g. 1/4)", key="right_input")
    col1, col2 = st.sidebar.columns([1, 1])
    equals = col1.button("Calculate", key="equals_btn")
    reset = col2.button("Reset Total", key="reset_btn")

    if reset:
        st.session_state.calculator_total = Fraction(0)

    result_display = ""
    if equals:
        a = parse_mixed_fraction(left)
        b = parse_mixed_fraction(right)
        if a is not None and b is not None:
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
                result_display = f"{left} {operator} {right} = {format_fraction_inches(result)}"
            except:
                result_display = "⚠️ Invalid operation."
        else:
            result_display = "⚠️ Invalid fraction format."

    if result_display:
        st.sidebar.markdown(f"**{result_display}**")
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Running Total:** {format_fraction_inches(st.session_state.calculator_total)}")

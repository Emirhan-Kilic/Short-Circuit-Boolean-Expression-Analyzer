import re
import itertools
import streamlit as st
import pandas as pd

def generate_short_circuit_tests(expression):
    # Find single-letter variables (skip "and","or", etc. by matching entire word boundaries)
    vars_found = sorted(set(re.findall(r"\b([a-zA-Z])\b", expression)))
    
    if not vars_found:
        return None, None  # Return None if no variables found
    
    # Replace single-letter words in expression with track('x') calls
    def replacer(m):
        letter = m.group(1)
        if letter in vars_found:
            return f"track('{letter}')"
        return letter

    transformed_expr = re.sub(r"\b([a-zA-Z])\b", replacer, expression)

    unique_patterns = set()

    def get_tracker(values, used):
        def track(var):
            used[var] = True
            return values[var]
        return track

    # Evaluate all 2^n combos for n variables
    for combo in itertools.product([False, True], repeat=len(vars_found)):
        values = dict(zip(vars_found, combo))
        used = dict.fromkeys(vars_found, False)

        try:
            # Use Python's short-circuit with eval
            _ = eval(transformed_expr, {}, {"track": get_tracker(values, used)})

            # Build result row
            row = []
            for v in vars_found:
                row.append('T' if used[v] and values[v] else
                          'F' if used[v] else '_')
            unique_patterns.add(tuple(row))
        except:
            st.error("Invalid expression. Please check your syntax.")
            return None, None

    # Return variables and patterns
    return vars_found, sorted(unique_patterns)

# Streamlit UI
st.title("Short Circuit Expression Analyzer")

st.write("""
This tool analyzes boolean expressions to show which variables are evaluated 
based on short-circuit behavior.

**Legend:**
- T: Variable was evaluated and is True
- F: Variable was evaluated and is False
- _: Variable was not evaluated (short-circuited)
""")

# Examples section moved above input
st.markdown("""
### Example expressions:
- `(a or b) and c`
- `(a and b) or (c and d)`
- `not a or (b and c)`
""")

# Input field with default example
default_expr = "(((a or b) and c) or d) and e"
expression = st.text_input(
    "Enter a boolean expression:",
    value=default_expr,
    help="Use 'and', 'or', 'not' operators and single-letter variables (e.g., 'a and b or c')"
)

if st.button("Analyze"):
    if expression:
        vars_found, patterns = generate_short_circuit_tests(expression)
        
        if vars_found and patterns:
            # Create DataFrame with 1-based index for all patterns
            df = pd.DataFrame(patterns, columns=vars_found)
            df.index = df.index + 1  # Make index start from 1
            
            # Style the table
            styled_df = df.style.set_properties(**{
                'text-align': 'center',
                'font-size': '16px',
                'padding': '5px'
            }).set_table_styles([
                {'selector': 'th', 'props': [
                    ('text-align', 'center'),
                    ('font-weight', 'bold'),
                    ('font-size', '16px'),
                    ('background-color', '#f0f2f6'),
                    ('padding', '5px')
                ]},
                {'selector': 'td, th', 'props': [
                    ('border', '1px solid #ddd')
                ]}
            ])
            
            # Display the full patterns table
            st.write("### All Possible Patterns:")
            st.write(styled_df)
            
            # Generate minimal test cases
            def select_minimal_test_cases(patterns, vars_found):
                patterns_list = list(patterns)
                n = len(vars_found)
                selected = []
                
                # Track coverage for each variable
                var_coverage = {var: {'T': False, 'F': False} for var in vars_found}
                
                # First pass: find patterns that give most T/F coverage
                for pattern in patterns_list:
                    if len(selected) >= n + 1:
                        break
                        
                    pattern_dict = dict(zip(vars_found, pattern))
                    coverage_added = False
                    
                    for var, val in pattern_dict.items():
                        if val in ['T', 'F'] and not var_coverage[var][val]:
                            var_coverage[var][val] = True
                            coverage_added = True
                    
                    if coverage_added:
                        selected.append(pattern)
                
                # If we need more patterns to reach n+1, add remaining patterns
                while len(selected) < n + 1 and patterns_list:
                    selected.append(patterns_list[0])
                    patterns_list.pop(0)
                
                return selected

            minimal_patterns = select_minimal_test_cases(patterns, vars_found)
            
            # Create and style minimal test cases table
            minimal_df = pd.DataFrame(minimal_patterns, columns=vars_found)
            minimal_df.index = minimal_df.index + 1
            
            styled_minimal_df = minimal_df.style.set_properties(**{
                'text-align': 'center',
                'font-size': '16px',
                'padding': '5px'
            }).set_table_styles([
                {'selector': 'th', 'props': [
                    ('text-align', 'center'),
                    ('font-weight', 'bold'),
                    ('font-size', '16px'),
                    ('background-color', '#f0f2f6'),
                    ('padding', '5px')
                ]},
                {'selector': 'td, th', 'props': [
                    ('border', '1px solid #ddd')
                ]}
            ])
            
            # Display the minimal test cases table
            st.write(f"""
            ### Minimal Test Cases (n+1 = {len(vars_found)+1} cases):
            These test cases ensure each variable has at least one True and one False evaluation when possible.
            """)
            st.write(styled_minimal_df)
            
            # Add explanation of the current expression
            st.markdown(f"""
            **Expression being analyzed:** `{expression}`
            
            The full table shows {len(patterns)} unique evaluation patterns for your expression.
            """)
        else:
            st.warning("Please enter a valid boolean expression with single-letter variables.")
    else:
        st.warning("Please enter an expression.")

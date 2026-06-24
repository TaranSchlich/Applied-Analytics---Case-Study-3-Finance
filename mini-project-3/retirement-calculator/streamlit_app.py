# =====================================================================
# Retirement Savings Calculator — Streamlit in Snowflake (warm-up)
# Introductory Streamlit activity. Compounds current savings plus monthly
# contributions to an estimated balance at retirement.
#
# Sample: age 24 -> 65, $1,000 start, $400/mo, 11% return  =>  ~$3,330,503.40
# =====================================================================

# Import python packages
import streamlit as st
import numpy as np

st.title('Retirement Savings Calculator')
st.write('This calculates our future retirement savings.')

current_age = st.number_input('Current Age', min_value=18, max_value=100, value=24)
retirement_age = st.number_input('Retirement Age', min_value=current_age + 1, max_value=101, value=65)
current_savings = st.number_input('Current Savings ($)', min_value=0.00, max_value=10_000_000.00, value=1000.00)
monthly_savings = st.number_input('Monthly Savings ($)', min_value=0.00, max_value=1_000_000.00, value=400.00)
annual_rate = st.slider('Expected Annual Rate of Return (%)', min_value=0.0, max_value=20.0, value=11.0)

# Calculate years and months to retirement.
years_to_retire = retirement_age - current_age
months_to_retire = years_to_retire * 12

# Calculate returns.
monthly_return_rate = (1 + annual_rate / 100) ** (1 / 12) - 1
total_savings = current_savings
for month in range(months_to_retire):
    total_savings = total_savings * (1 + monthly_return_rate) + monthly_savings

# Report returns to the user.
st.write(f"By the age of {retirement_age}, you will have saved approximately ${total_savings:,.2f}.")

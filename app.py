import streamlit as st
import openai
import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import json

st.set_page_config(page_title="Zeesolution AI Consultant", page_icon="📊", layout="wide")

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.sidebar.title("🏢 Zeesolution")
st.sidebar.markdown("### AI Strategic Advisory System")
st.sidebar.markdown("---")
st.sidebar.info("Professional Business Growth Intelligence")

st.title("Zeesolution AI Business Consultant")

mode = st.radio("Select your category:", ["Existing Business", "Start New Business"])
st.markdown("---")

def generate_chart(chart_data):
    revenue_data = chart_data["revenue_projection"]
    profit_data = chart_data["profit_projection"]

    df = pd.DataFrame({
        "Month": ["Month 1", "Month 3", "Month 6", "Month 12"],
        "Revenue": list(revenue_data.values()),
        "Profit": list(profit_data.values())
    })

    fig, ax = plt.subplots()
    ax.plot(df["Month"], df["Revenue"], marker="o", label="Revenue")
    ax.plot(df["Month"], df["Profit"], marker="o", label="Profit")
    ax.legend()
    st.pyplot(fig)

if mode == "Existing Business":
    col1, col2 = st.columns(2)

    with col1:
        business_type = st.selectbox("Business Type", ["Manufacturing", "Trading", "Services"])
        industry = st.text_input("Industry")
        revenue = st.number_input("Monthly Revenue", min_value=0.0)
        expenses = st.number_input("Monthly Expenses", min_value=0.0)

    with col2:
        marketing_budget = st.number_input("Marketing Budget", min_value=0.0)
        sales_channel = st.text_input("Sales Channel")
        problem = st.text_area("Describe Your Main Problem")

    if st.button("Analyze Business"):
        profit = revenue - expenses

        prompt = f"""
        Business Type: {business_type}
        Industry: {industry}
        Monthly Revenue: {revenue}
        Monthly Expenses: {expenses}
        Monthly Profit: {profit}
        Marketing Budget: {marketing_budget}
        Sales Channel: {sales_channel}
        Problem: {problem}

        Provide structured analysis and include JSON block named CHART_DATA.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Zeesolution AI Business Consultant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        result = response["choices"][0]["message"]["content"]
        st.markdown(result)

        if "CHART_DATA:" in result:
            try:
                json_part = result.split("CHART_DATA:")[-1].strip()
                chart_data = json.loads(json_part)
                generate_chart(chart_data)
            except:
                st.warning("Chart generation failed.")

elif mode == "Start New Business":
    col1, col2 = st.columns(2)

    with col1:
        idea = st.text_input("Business Idea")
        location = st.text_input("Target Location")
        budget = st.number_input("Starting Budget", min_value=0.0)

    with col2:
        experience = st.text_input("Experience Level")
        target_customer = st.text_input("Target Customer")
        concern = st.text_area("Main Concern")

    if st.button("Analyze Startup Plan"):
        prompt = f"""
        Business Idea: {idea}
        Location: {location}
        Starting Budget: {budget}
        Experience: {experience}
        Target Customer: {target_customer}
        Main Concern: {concern}

        Provide structured startup analysis and include JSON block named CHART_DATA.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Zeesolution AI Startup Consultant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )

        result = response["choices"][0]["message"]["content"]
        st.markdown(result)

        if "CHART_DATA:" in result:
            try:
                json_part = result.split("CHART_DATA:")[-1].strip()
                chart_data = json.loads(json_part)
                generate_chart(chart_data)
            except:
                st.warning("Chart generation failed.")

st.markdown("---")
st.markdown("Prepared by Zeesolution AI Strategic Advisory System")

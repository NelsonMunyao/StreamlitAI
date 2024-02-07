import streamlit as st
import pandas as pd
import os
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
import numpy as np
from dotenv import load_dotenv


st.title("Sales KPI Dashboard")
st.divider()

@st.cache_data()
def read_data():
    df = pd.read_csv('Data/supermarket_sales - Sheet1.csv')
    return df

df = pd.read_csv('Data/supermarket_sales - Sheet1.csv')

read_data()

tab1, tab2, tab3 = st.tabs(["Metrics","AI-Assistant","Fraud Detector*"])

Sales = df['Total'].sum().astype(float)

#Profits
profits = df['gross income'].sum()

#Transactions
transactions = df.shape[0]

#Sales by Products
Sales_by_prod = df.groupby('Product line')['Total'].sum()

#split month


Top_products_per_gender = df.groupby(['Gender', 'Product line'])['Total'].sum().reset_index()
asc_top_products_per_gender = Top_products_per_gender.sort_values(by=['Gender', 'Total'], ascending=[True, False])

with tab1:
    def kpi_card(title, value, unit):
        st.write(f"## {title}")
        st.write(f"{value} {unit}")

    card1, card2, card3, card4 = st.columns(4)

    # Replace these values with your actual data
    with card1:
        with st.container(height=150,):
            kpi_card("Sales", Sales, "USD")
            #add short sentence to describe increase/decrease from time period A to B

    with card2:
        with st.container(height=150):
            kpi_card("Orders", transactions , "Total orders")
            #add short sentence to describe increase/decrease from time period A to B

    with card3:
        with st.container(height=150):
            kpi_card("Profits", profits, "USD")
            #add short sentence to describe increase/decrease from time period A to B

    with card4:
        with st.container(height=150):
            kpi_card("Profits", profits, "USD")
            #add short sentence to describe increase/decrease from time period A to B
    with st.container(height=300,):
        st.write('write')

# llm = OpenAI(api_token="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")
# df = SmartDataframe(df, config={"llm": llm})
# Chatbot = df.chat("Give me an explanation of my what my dataset enails. how you can help analyse key KPIs for business intelligence. I do not know anything about data analysis so explain it to me as you would do to a businessperson. Be concise and offer explanations where necessary ")


llm = OpenAI(api_token="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")
cf = SmartDataframe(df, config={"llm": llm})
#AI button
with tab2:
    with st.expander('Data preview'):
        st.dataframe(df)

    #AI summary button
    ai_button = st.button("Generate AI Summary")
    if ai_button:
        llm = OpenAI(api_token="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")
        cf = SmartDataframe(df, config={"llm": llm})


    if ai_button:
        with st.expander("Complete! Click for more:"):
            response = cf.chat("Give me an explanation of my what my dataset is about. I do not know anything about data analysis so explain it to me as you would do to a businessperson in a yearly report. Be concise and offer explanations where necessary. Highlight trends in the data and potential causes. Then encourage me to Chat with you in the chatbox below for more insights into your data")
            st.spinner("Loading")
            st.write(response)

    #Chat with CSV textbox
    def question():
        user_question = st.text_input('Ask any question about your data.')
        Chatbot_response = cf.chat(user_question)
        with st.expander(label="Click for answer"):
            st.write(Chatbot_response)

    question()


#COGS: Cost of goods sold
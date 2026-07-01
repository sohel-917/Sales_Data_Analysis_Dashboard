import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("processed_data/master_sales_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

master_data = load_data()

st.title("📊 Sales Data Analysis Dashboard")

st.write(master_data.head())
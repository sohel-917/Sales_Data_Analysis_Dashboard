import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "processed_data",
        "master_sales_data_sample.csv"
    )

    print("Loading file from:", file_path)

    df = pd.read_csv(file_path, low_memory=False)

    print("Columns:", df.columns.tolist())

    df["date"] = pd.to_datetime(df["date"])

    return df

master_data = load_data()

st.markdown("""
# 📊 Store Sales Analytics Dashboard

### Business Intelligence Dashboard for Store Sales Forecasting

Analyze sales trends, promotions, store performance,
transactions and business insights.

---
""")
# ==========================
# KPI Calculations
# ==========================

total_sales = master_data["sales"].sum()

total_transactions = master_data["transactions"].sum()

total_stores = master_data["store_nbr"].nunique()

total_promotions = (master_data["Promotion"] == "Yes").sum()

average_sales = master_data["sales"].mean()
from datetime import datetime

st.caption(
    f"Last Updated: {datetime.now().strftime('%d %B %Y %I:%M %p')}"
)
# ==========================
# KPI Cards
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Sales",
        f"{total_sales/1_000_000_000:.2f} B"
    )

with col2:
    st.metric(
        "🛒 Transactions",
        f"{total_transactions/1_000_000_000:.2f} B"
    )

with col3:
    st.metric(
        "🏬 Stores",
        total_stores
    )

with col4:
    st.metric(
        "🎁 Promotions",
        f"{total_promotions:,}"
    )
    st.success(
    f"📈 Average Sales per Record : {average_sales:.2f}"
)
    st.divider()

st.sidebar.title("⚙ Dashboard Filters")
st.sidebar.info(
"""
This dashboard allows you to explore:

• Sales Trends

• Store Performance

• Product Categories

• Promotions

• Transactions
"""
)

st.sidebar.markdown("---")

selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(master_data["Year"].unique())
)
selected_month = st.sidebar.selectbox(
    "📅 Select Month",
    ["All"] + sorted(master_data["Month_Name"].unique().tolist())
)
selected_store = st.sidebar.selectbox(
    "🏬 Select Store",
    ["All"] + sorted(master_data["store_nbr"].unique().tolist())
)
selected_city = st.sidebar.selectbox(
    "🌍 Select City",
    ["All"] + sorted(master_data["city"].unique().tolist())
)
selected_family = st.sidebar.selectbox(
    "🛍 Product Category",
    ["All"] + sorted(master_data["family"].unique().tolist())
)
st.sidebar.markdown("---")

st.sidebar.success(
    f"""
### Selected Filters

📅 Year : {selected_year}

📅 Month : {selected_month}

🏬 Store : {selected_store}

🌍 City : {selected_city}

🛍 Category : {selected_family}
"""
)

filtered_data = master_data.copy()

filtered_data = filtered_data[
    filtered_data["Year"] == selected_year
]

if selected_month != "All":
    filtered_data = filtered_data[
        filtered_data["Month_Name"] == selected_month
    ]

if selected_store != "All":
    filtered_data = filtered_data[
        filtered_data["store_nbr"] == selected_store
    ]

if selected_city != "All":
    filtered_data = filtered_data[
        filtered_data["city"] == selected_city
    ]

if selected_family != "All":
    filtered_data = filtered_data[
        filtered_data["family"] == selected_family
    ]
import plotly.express as px
st.subheader("📊 Sales Performance Analysis")
st.write("Explore sales trends, monthly performance, product categories and top-performing stores.")
st.divider()
daily_sales = (
    filtered_data.groupby("date")["sales"]
    .sum()
    .reset_index()
)

fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Daily Sales Trend"
)

chart1, chart2 = st.columns(2)

with chart1:
    st.plotly_chart(fig, use_container_width=True)
monthly_sales = (
    filtered_data.groupby("Month_Name")["sales"]
    .sum()
    .reset_index()
)

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly_sales["Month_Name"] = pd.Categorical(
    monthly_sales["Month_Name"],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values("Month_Name")

fig = px.bar(
    monthly_sales,
    x="Month_Name",
    y="sales",
    title="📅 Monthly Sales Analysis"
)

with chart2:
    st.plotly_chart(fig, use_container_width=True)

chart3, chart4 = st.columns(2)
top_products = (
    filtered_data.groupby("family")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_products,
    x="family",
    y="sales",
    title="🛍 Top 10 Product Categories"
)

with chart3:
    st.plotly_chart(fig, use_container_width=True)
top_stores = (
    filtered_data.groupby("store_nbr")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_stores,
    x="store_nbr",
    y="sales",
    title="🏬 Top 10 Performing Stores"
)

with chart4:
    st.plotly_chart(fig, use_container_width=True)
st.subheader("📈 Additional Business Insights")
st.divider()
category_sales = (
    filtered_data.groupby("family")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.pie(
    category_sales,
    names="family",
    values="sales",
    title="🥧 Top 10 Product Category Distribution",
    hole=0.45
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

st.plotly_chart(fig, use_container_width=True)
city_sales = (
    filtered_data.groupby("city")["sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    city_sales,
    x="city",
    y="sales",
    title="🌍 Sales by City"
)

st.plotly_chart(fig, use_container_width=True)
promotion_sales = (
    filtered_data.groupby("Promotion")["sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    promotion_sales,
    x="Promotion",
    y="sales",
    title="🎁 Sales by Promotion Status"
)

st.plotly_chart(fig, use_container_width=True)
corr = filtered_data[
    ["sales", "transactions", "onpromotion"]
].corr()

fig = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        text=corr.round(2).values,
        texttemplate="%{text}",
        colorscale="Blues"
    )
)

fig.update_layout(
    title="🔥 Correlation Heatmap"
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("📋 Filtered Sales Data")

st.dataframe(
    filtered_data,
    use_container_width=True,
    hide_index=True
)
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_data.to_csv(index=False),
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)
st.divider()

st.markdown(
    """
    <div style='text-align:center; color:gray;'>
        <h4>📊 Store Sales Analytics Dashboard</h4>
        <p>Developed by <b>Sk Sohel</b></p>
        <p> Project | Python • Pandas • Plotly • Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)


import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Enterprise Analytics", layout="wide")
st.title("📊 Enterprise Sales Data Engineering & Analytics Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("cleaned_sales_data.csv")

df = load_data()

# Metrics Calculated
revenue_sum = df['sales'].sum()
profit_sum = df['profit'].sum()
margin_ratio = (profit_sum / revenue_sum) * 100

# Layout Dashboard Columns
c1, c2, c3 = st.columns(3)
c1.metric("Gross Revenue", f"${revenue_sum:,.2f}")
c2.metric("Net Profit", f"${profit_sum:,.2f}")
c3.metric("Operational Net Margin", f"{margin_ratio:.2f}%")

st.markdown("---")
left_chart, right_chart = st.columns(2)

with left_chart:
    st.subheader("Monthly Revenue Trajectory")
    df['order_date'] = pd.to_datetime(df['order_date'])
    monthly_series = df.groupby(df['order_date'].dt.to_period('M'))['sales'].sum().reset_index()
    monthly_series['order_date'] = monthly_series['order_date'].astype(str)
    fig1 = px.line(monthly_series, x='order_date', y='sales', markers=True, template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

with right_chart:
    st.subheader("Regional Operational Profitability Assessment")
    regional_aggregates = df.groupby('region')['profit'].sum().reset_index()
    fig2 = px.bar(regional_aggregates, x='region', y='profit', color='profit',
                 color_continuous_scale='RdYlGn', template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(page_title="Customer LTV Analysis Dashboard", layout="wide")
st.title("📈 Customer Lifetime Value (LTV) Exploratory Analysis Dashboard")

# Load data
file_path = "digital_wallet_ltv_dataset.csv"
df = pd.read_csv(file_path)

# Sidebar Navigation
st.sidebar.header("🔎 Navigation")
page = st.sidebar.radio("Go to", [
    "Boxplot Visualizations",
    "Correlation Heatmap",
    "Customer Demographics & Behaviour",
    "Customer Engagement Analysis"
])

# 1. Boxplot Visualizations
if page == "Boxplot Visualizations":
    st.header("📦 Boxplot Visualizations of Key Features")
    selected_cols = [
        'Total_Spent', 'Loyalty_Points_Earned', 'Referral_Count',
        'Cashback_Received', 'Customer_Satisfaction_Score', 'LTV'
    ]
    fig_box, ax_box = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df[selected_cols], ax=ax_box)
    ax_box.set_title("Boxplots of Important Features")
    st.pyplot(fig_box)

# 2. Correlation Heatmap
elif page == "Correlation Heatmap":
    st.header("📊 Correlation Heatmap")
    selected_cols = [
        'Total_Spent', 'Loyalty_Points_Earned', 'Referral_Count',
        'Cashback_Received', 'Customer_Satisfaction_Score', 'LTV'
    ]
    corr = df[selected_cols].corr()
    fig_corr, ax_corr = plt.subplots(figsize=(10, 7))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax_corr)
    ax_corr.set_title("Correlation Matrix of Selected Features")
    st.pyplot(fig_corr)

# 3. Customer Demographics & Behaviour
elif page == "Customer Demographics & Behaviour":
    st.header("👥 Customer Demographics and Behaviour Analysis")

    st.subheader("📌 Key Indicators")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Customers", f"{df['Customer_ID'].nunique()}")
    with col2:
        st.metric("Total Referral Count", f"{df['Referral_Count'].sum():,}")
    with col3:
        st.metric("Total Loyalty Points", f"{df['Loyalty_Points_Earned'].sum():,}")
    with col4:
        st.metric("Total Cashback Received", f"₹{df['Cashback_Received'].sum():,.2f}")

    st.subheader("🗺 Spending Distribution by Location")
    location_spent = df.groupby('Location')['Total_Spent'].sum().reset_index()
    fig_pie = px.pie(location_spent, names='Location', values='Total_Spent',
                     title="Total Spent Amount by Location", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("📈 Customer Count by Satisfaction Score")
    score_count = df['Customer_Satisfaction_Score'].value_counts().sort_index().reset_index()
    fig_bar = px.bar(score_count, x='index', y='Customer_Satisfaction_Score',
                     labels={'index': 'Satisfaction Score', 'Customer_Satisfaction_Score': 'Customer Count'},
                     title="Customers by Satisfaction Score")
    st.plotly_chart(fig_bar, use_container_width=True)

# 4. Customer Engagement Analysis
elif page == "Customer Engagement Analysis":
    st.header("📞 Customer Engagement Analysis")

    st.subheader("📌 Engagement Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Transactions", f"{df['Total_Transactions'].sum():,}")
    with col2:
        st.metric("Avg Issue Resolution Time (hrs)", f"{df['Issue_Resolution_Time'].mean():.2f}")

    st.subheader("📲 App Usage Frequency Distribution")
    app_usage = df['App_Usage_Frequency'].value_counts().reset_index()
    fig_usage = px.bar(app_usage, x='index', y='App_Usage_Frequency',
                       labels={'index': 'App Usage Frequency', 'App_Usage_Frequency': 'Number of Customers'},
                       title="App Usage Frequency among Customers")
    st.plotly_chart(fig_usage, use_container_width=True)

    st.subheader("🛠 Support Tickets vs Customer Satisfaction")
    support_satisfaction = df.groupby('Customer_Satisfaction_Score')['Support_Tickets_Raised'].sum().reset_index()
    fig_support = px.bar(support_satisfaction, x='Customer_Satisfaction_Score', y='Support_Tickets_Raised',
                         labels={'Customer_Satisfaction_Score': 'Satisfaction Score', 'Support_Tickets_Raised': 'Support Tickets'},
                         title="Support Tickets Raised by Satisfaction Score")
    st.plotly_chart(fig_support, use_container_width=True)

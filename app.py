
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(page_title="Customer LTV Analysis Dashboard", layout="wide")

# Simple login mechanism
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login to LTV Dashboard")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "Customer_LTV" and password == "Fintech":
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials.")
    st.stop()

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
    for col in selected_cols:
        st.subheader(f"Boxplot for {col}")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.boxplot(x=df[col], ax=ax)
        st.pyplot(fig)

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
        st.metric("Total Support Tickets", f"{df['Support_Tickets_Raised'].sum():,}")

    st.subheader("🗺 Spending Distribution by Location")
    location_spent = df.groupby('Location')['Total_Spent'].sum().reset_index()
    fig_pie = px.pie(
        location_spent,
        names='Location',
        values='Total_Spent',
        title="Total Spent Amount by Location",
        hole=0.4
    )
    fig_pie.update_layout(
        title_font_size=24,
        legend_font_size=20
    )
    fig_pie.update_traces(textfont_size=14)
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("📈 Customer Count by Satisfaction Score")
    score_count = df['Customer_Satisfaction_Score'].value_counts().sort_index().reset_index()
    score_count.columns = ['Customer_Satisfaction_Score', 'count']
    fig_bar = px.bar(
        score_count,
        x='Customer_Satisfaction_Score',
        y='count',
        labels={'Customer_Satisfaction_Score': 'Satisfaction Score', 'count': 'Customer Count'},
        title="No of Customers by Customer Satisfaction Score",
        text='count'
    )
    fig_bar.update_traces(textposition='outside', textfont_size=14)
    fig_bar.update_layout(
        title_font_size=24,
        xaxis_title_font_size=20,
        yaxis_title_font_size=20,
        xaxis_tickfont_size=18,
        yaxis_tickfont_size=18
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# 4. Customer Engagement Analysis
elif page == "Customer Engagement Analysis":
    st.header("📞 Customer Engagement Analysis")

    st.subheader("📌 Engagement Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Transactions", f"{df['Total_Transactions'].sum():,}")
    with col2:
        st.metric("Total Spent Amount", f"₹{df['Total_Spent'].sum():,.3f}")
    with col3:
        st.metric("Total Cashback Received", f"₹{df['Cashback_Received'].sum():,.3f}")
    with col4:
        st.metric("Avg Issue Resolution Time (hrs)", f"{df['Issue_Resolution_Time'].mean():.3f}")

    st.subheader("📲 App Usage Frequency Distribution")
    app_usage = df['App_Usage_Frequency'].value_counts().reset_index()
    app_usage.columns = ['App_Usage_Frequency', 'count']
    fig_usage = px.bar(app_usage, x='App_Usage_Frequency', y='count',
                       labels={'App_Usage_Frequency': 'App Usage Frequency', 'count': 'Number of Customers'},
                       title="App Usage Frequency by Customers", text='count')
    fig_usage.update_traces(textposition='outside', textfont_size=14)
    fig_usage.update_layout(
        title_font_size=24,
        xaxis_title_font_size=20,
        yaxis_title_font_size=20,
        xaxis_tickfont_size=18,
        yaxis_tickfont_size=18
    )
    st.plotly_chart(fig_usage, use_container_width=True)

    st.subheader("🛠 Support Tickets vs Customer Satisfaction")
    support_satisfaction = df.groupby('Customer_Satisfaction_Score')['Support_Tickets_Raised'].sum().reset_index()
    fig_support = px.bar(support_satisfaction, x='Customer_Satisfaction_Score', y='Support_Tickets_Raised',
                         labels={'Customer_Satisfaction_Score': 'Satisfaction Score', 'Support_Tickets_Raised': 'Support Tickets'},
                         title="Support Tickets Raised by Satisfaction Score", text='Support_Tickets_Raised')
    fig_support.update_traces(textposition='outside', textfont_size=14)
    fig_support.update_layout(
        title_font_size=24,
        xaxis_title_font_size=20,
        yaxis_title_font_size=20,
        xaxis_tickfont_size=18,
        yaxis_tickfont_size=18
    )
    st.plotly_chart(fig_support, use_container_width=True)

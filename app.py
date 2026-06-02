import streamlit as st
import pandas as pd
import plotly.express as px
from utils import ask_llm
from prompts import ANALYSIS_PROMPT, CHAT_PROMPT

st.set_page_config(page_title="AI Fulfillment Dashboard", layout="wide")

st.title("📦 AI Fulfillment Dashboard")
st.markdown("Analyze fulfillment performance and identify operational issues using AI")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    required_cols = [
        "order_id", "order_date", "warehouse", "delay_reason",
        "delay_days", "fulfilled_on_time"
    ]

    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        st.error(f"Missing required columns: {missing_cols}")
        st.stop()

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["fulfilled_on_time"] = df["fulfilled_on_time"].astype(bool)

    # -------------------- FILTERS --------------------
    st.subheader("🔍 Filters")

    col1, col2 = st.columns(2)

    with col1:
        selected_warehouse = st.selectbox(
            "Select Warehouse",
            ["All"] + sorted(df["warehouse"].dropna().unique().tolist())
        )

    with col2:
        selected_reason = st.selectbox(
            "Select Delay Reason",
            ["All"] + sorted(df["delay_reason"].dropna().unique().tolist())
        )

    filtered_df = df.copy()

    if selected_warehouse != "All":
        filtered_df = filtered_df[filtered_df["warehouse"] == selected_warehouse]

    if selected_reason != "All":
        filtered_df = filtered_df[filtered_df["delay_reason"] == selected_reason]

    st.caption(f"Filtered rows: {len(filtered_df)}")

    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
        st.stop()

    # -------------------- KPI METRICS --------------------
    st.subheader("📊 Key Metrics")

    total_orders = len(filtered_df)
    avg_delay = filtered_df["delay_days"].mean()
    on_time_rate = filtered_df["fulfilled_on_time"].mean() * 100

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Orders", f"{total_orders:,}")
    col2.metric("Avg Delay (days)", f"{avg_delay:.2f}")
    col3.metric("On-time Rate", f"{on_time_rate:.1f}%")

    # -------------------- VISUAL INSIGHTS --------------------
    st.subheader("📈 Visual Insights")

    col1, col2 = st.columns(2)

    with col1:
        fig_delay = px.histogram(
            filtered_df,
            x="delay_days",
            nbins=10,
            title="Delay Distribution",
            labels={"delay_days": "Delay Days", "count": "Orders"}
        )
        fig_delay.update_layout(height=420)
        st.plotly_chart(fig_delay, use_container_width=True)

    with col2:
        trend = (
            filtered_df
            .dropna(subset=["order_date"])
            .groupby(filtered_df["order_date"].dt.date)
            .size()
            .reset_index(name="orders")
        )

        trend.columns = ["order_date", "orders"]

        fig_trend = px.line(
            trend,
            x="order_date",
            y="orders",
            markers=True,
            title="Orders Over Time",
            labels={"order_date": "Order Date", "orders": "Orders"}
        )
        fig_trend.update_layout(height=420)
        st.plotly_chart(fig_trend, use_container_width=True)

    # -------------------- QUICK INSIGHTS --------------------
    st.subheader("🚨 Quick Insights")

    col1, col2 = st.columns(2)

    with col1:
        delay_by_wh = (
            filtered_df.groupby("warehouse")["delay_days"]
            .mean()
            .reset_index()
            .sort_values("delay_days", ascending=False)
            .head(5)
        )

        fig_wh = px.bar(
            delay_by_wh,
            x="delay_days",
            y="warehouse",
            orientation="h",
            title="Top Delay Warehouses",
            labels={"delay_days": "Avg Delay Days", "warehouse": "Warehouse"}
        )
        fig_wh.update_layout(height=360, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_wh, use_container_width=True)

    with col2:
        reason_count = (
            filtered_df["delay_reason"]
            .value_counts()
            .head(5)
            .reset_index()
        )
        reason_count.columns = ["delay_reason", "orders"]

        fig_reason = px.bar(
            reason_count,
            x="orders",
            y="delay_reason",
            orientation="h",
            title="Top Delay Reasons",
            labels={"orders": "Orders", "delay_reason": "Delay Reason"}
        )
        fig_reason.update_layout(height=360, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_reason, use_container_width=True)

    # -------------------- WHAT-IF SIMULATION --------------------
    st.subheader("🧪 What-if Simulation")

    reduction_pct = st.slider("Reduce delay by (%)", 0, 50, 10)

    simulated_df = filtered_df.copy()
    simulated_df["simulated_delay_days"] = simulated_df["delay_days"] * (1 - reduction_pct / 100)

    new_avg_delay = simulated_df["simulated_delay_days"].mean()
    new_on_time = (simulated_df["simulated_delay_days"] <= 0).mean() * 100

    col1, col2, col3 = st.columns(3)

    col1.metric("Current Avg Delay", f"{avg_delay:.2f}")
    col2.metric("New Avg Delay", f"{new_avg_delay:.2f}")
    col3.metric("New On-time Rate", f"{new_on_time:.1f}%")

    # -------------------- DATA PREVIEW --------------------
    with st.expander("📄 Data Preview"):
        st.dataframe(filtered_df.head(20), use_container_width=True)

    # -------------------- BUILD AI CONTEXT --------------------
    summary = f"""
    Total Orders: {len(filtered_df)}
    Avg Delay: {filtered_df['delay_days'].mean():.2f}
    On-time Rate: {filtered_df['fulfilled_on_time'].mean()*100:.1f}%

    Top Delay Warehouse:
    {filtered_df.groupby('warehouse')['delay_days'].mean().sort_values(ascending=False).head(3)}

    Top Delay Reasons:
    {filtered_df['delay_reason'].value_counts().head(3)}
    """

    simulation_summary = f"""
    If delay is reduced by {reduction_pct}%:
    - New Avg Delay: {new_avg_delay:.2f}
    - New On-time Rate: {new_on_time:.1f}%
    """

    sample_data = filtered_df.head(100).to_string()
    context = summary + "\n\n" + simulation_summary + "\n\nSample Data:\n" + sample_data

    # -------------------- AI ANALYSIS --------------------
    st.subheader("🤖 AI Analysis")

    if st.button("Run AI Analysis"):
        with st.spinner("Analyzing data... 🤖"):
            result = ask_llm(ANALYSIS_PROMPT, context)
            st.write(result)

    # -------------------- AI CHAT --------------------
    st.subheader("💬 Ask AI")

    question = st.text_input("Ask about your data")

    if st.button("Ask AI"):
        if question:
            with st.spinner("Thinking... 🤔"):
                answer = ask_llm(CHAT_PROMPT, context + "\n\nUser Question:\n" + question)
                st.write(answer)
        else:
            st.warning("Please enter a question")
else:
    st.info("Please upload a CSV file to start analysis.")

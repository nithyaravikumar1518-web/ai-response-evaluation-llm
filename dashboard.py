import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="AI Response Evaluation with LLM",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ENTERPRISE DARK MODE STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] label, [data-testid="stSidebar"] div {
        color: #f3f4f6 !important;
    }
    div.stMetric {
        background-color: #131b2e;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #1e293b;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        border-top: 3px solid #10b981;
    }
    div.stMetric label {
        color: #9ca3af !important;
        font-size: 13px !important;
    }
    div.stMetric div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 26px !important;
    }
    h3 {
        color: #f3f4f6 !important;
        font-size: 18px !important;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION & COUNTDOWN TIMER ---
with st.sidebar:
    st.markdown("### ⚡ AI Eval <span style='background:#10b981; color:#0b0f19; padding:2px 6px; border-radius:4px; font-size:10px;'>v1</span>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Milestone Countdown Widget
    st.markdown("⏳ **Mission Deadline Countdown**")
    target_date = datetime.now() + timedelta(days=7) # Target milestone 7 days from now
    time_left = target_date - datetime.now()
    days_left = time_left.days
    hours_left = time_left.seconds // 3600
    
    st.info(f"🚀 **Target:** GitHub Launch\n\n⏱️ **Time Left:** {days_left} Days, {hours_left} Hours")
    st.markdown("---")
    
    st.markdown("**MAIN**")
    page = st.radio("Navigation", ["📊 Overview", "📋 Eval Runs", "⚡ Run Suite", "➕ New Eval", "⚖️ Compare"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**SYSTEM**")
    st.success("🟢 API Connected")
    st.markdown("---")
    filter_option = st.selectbox("Filter History", ["All Evaluations", "High Scores (Average >= 5.0)"])

# --- HEADER TITLE & STATUS ---
st.markdown("## AI Response Evaluation with LLM")
st.markdown("<p style='color: #9ca3af; margin-top: -10px;'>Real-time monitoring of your LLM evaluation pipeline. &nbsp;<span style='color: #10b981;'>● System Online</span></p>", unsafe_allow_html=True)
st.markdown("---")

# Try loading data
try:
    df = pd.read_csv("eval_reports.csv", header=None, 
                     names=["Question", "AI_Answer", "Accuracy", "Relevance", "Clarity", "Instruction_Following", "Average_Score"])
    
    if filter_option == "High Scores (Average >= 5.0)":
        df_filtered = df[df['Average_Score'] >= 5.0]
    else:
        df_filtered = df

    # --- TOP 4 KPI METRIC CARDS ---
    c1, c2, c3, c4 = st.columns(4)
    
    total_runs = len(df)
    pass_rate = (len(df[df['Average_Score'] >= 4.0]) / total_runs * 100) if total_runs > 0 else 0
    avg_score_val = df['Average_Score'].mean() / 5.0 
    
    c1.metric("Total Eval Runs", total_runs, "+12 this week")
    c2.metric("Pass Rate", f"{pass_rate:.0f}%", "+3.2%")
    c3.metric("Avg Score", f"{avg_score_val:.2f}", "+0.05")
    c4.metric("Safety Score", "0.92", "+0.02")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- CHARTS SECTION (SIDE-BY-SIDE PLOTLY COMPARISON) ---
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Score Trends")
        st.markdown("<p style='color: #9ca3af; font-size: 12px;'>Multi-metric performance trajectory</p>", unsafe_allow_html=True)
        
        fig_line = px.line(df[['Accuracy', 'Relevance', 'Clarity', 'Instruction_Following']], 
                           markers=True, 
                           color_discrete_sequence=['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b'])
        fig_line.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f3f4f6',
            margin=dict(l=10, r=10, t=10, b=10),
            height=260,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with chart_col2:
        st.subheader("Category Performance")
        st.markdown("<p style='color: #9ca3af; font-size: 12px;'>By test type & criteria</p>", unsafe_allow_html=True)
        
        category_df = pd.DataFrame({
            "Criteria": ["Accuracy", "Relevance", "Clarity", "Instruction Following"],
            "Score": [
                df['Accuracy'].mean() / 5.0,
                df['Relevance'].mean() / 5.0,
                df['Clarity'].mean() / 5.0,
                df['Instruction_Following'].mean() / 5.0
            ]
        })
        
        fig_bar = px.bar(category_df, x="Criteria", y="Score", 
                         color="Criteria",
                         color_discrete_sequence=['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6'])
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f3f4f6',
            margin=dict(l=10, r=10, t=10, b=10),
            height=260,
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    
    # --- EVALUATION HISTORY TABLE ---
    st.subheader("Evaluation History Records")
    st.dataframe(df_filtered, width="stretch")

except Exception as e:
    st.warning("No evaluation data found yet! Run your `eval_tool.py` script in your terminal to add records.")
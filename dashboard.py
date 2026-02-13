# ============================================
# AI Water Intake Tracker — Ultra Premium UI
# ============================================

import streamlit as st
import pandas as pd
from datetime import datetime

# Backend Integrations
from src.agent import WaterIntakeAgent
from src.database import log_intake, get_intake_history


# ============================================
# Page Config
# ============================================

st.set_page_config(
    page_title="AI Water Tracker",
    page_icon="💧",
    layout="wide"
)


# ============================================
# Session State
# ============================================

if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

if "ai_feedback" not in st.session_state:
    st.session_state.ai_feedback = None


# ============================================
# 1️⃣ Welcome Screen
# ============================================

if not st.session_state.tracker_started:

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/728/728093.png",
            width=180
        )

    with col2:
        st.title("💧 AI Water Tracker")

        st.markdown("""
        ### Smart Hydration Monitoring

        Track your hydration with an **AI Health Assistant**.

        Monitor intake, analyze hydration, and stay healthy.
        """)

        if st.button("🚀 Start Tracking", use_container_width=True):
            st.session_state.tracker_started = True
            st.rerun()


# ============================================
# 2️⃣ Dashboard
# ============================================

else:

    st.title("💧 Water Intake Dashboard")
    st.markdown("Monitor hydration and receive AI insights.")

    st.divider()

    # ========================================
    # Sidebar Logger
    # ========================================

    st.sidebar.header("📝 Log Water Intake")

    user_id = st.sidebar.text_input(
        "User ID",
        value="user_123"
    )

    intake_ml = st.sidebar.number_input(
        "Intake (mL)",
        min_value=0,
        step=50,
        value=250
    )

    if st.sidebar.button("Submit Intake"):

        log_intake(user_id, intake_ml)

        agent = WaterIntakeAgent()
        feedback = agent.analyze_intake(intake_ml)

        st.session_state.ai_feedback = feedback

        st.sidebar.success(
            f"Logged {intake_ml} mL successfully ✅"
        )

        st.rerun()

    # ========================================
    # AI Feedback
    # ========================================

    if st.session_state.ai_feedback:

        st.subheader("🧠 AI Hydration Feedback")
        st.info(st.session_state.ai_feedback)
        st.divider()

    # ========================================
    # History Section
    # ========================================

    st.subheader("📊 Water Intake History")

    history = get_intake_history(user_id)

    if history:

        df = pd.DataFrame(
            history,
            columns=["Intake (mL)", "Date"]
        )

        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

        # ====================================
        # Metrics
        # ====================================

        total_intake = df["Intake (mL)"].sum()
        avg_intake = int(df["Intake (mL)"].mean())

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Intake", f"{total_intake} mL")

        with col2:
            st.metric("Average Intake", f"{avg_intake} mL")

        st.divider()

        # ====================================
        # Table
        # ====================================

        st.markdown("### 📋 Intake Records")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ====================================
        # 🏆 ULTRA PREMIUM GOAL ANALYTICS
        # ====================================

        st.markdown("## 🏆 Hydration Goal Center")

        goal = 3000
        today_total = total_intake

        progress = min(today_total / goal, 1.0)
        remaining = max(goal - today_total, 0)

        # Hydration Score
        hydration_score = int(progress * 100)

        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Consumed", f"{today_total} mL")
        col2.metric("Goal", f"{goal} mL")
        col3.metric("Remaining", f"{remaining} mL")
        col4.metric("Hydration Score", f"{hydration_score}/100")

        st.write("")

        # Animated Progress Bar Feel
        st.progress(progress)

        st.write(
            f"### {today_total} / {goal} mL completed"
        )

        # Glass Visualization
        st.markdown("#### 🥛 Glass Consumption")

        glass_ml = 250
        glasses = today_total // glass_ml

        glass_icons = "🥛" * int(glasses)

        if glass_icons:
            st.write(glass_icons)
        else:
            st.write("No glasses logged yet.")

        st.write(f"**{glasses} glasses consumed**")

        # Smart Status Feedback
        if hydration_score >= 100:
            st.success(
                "🎉 Excellent hydration! Goal achieved."
            )
        elif hydration_score >= 75:
            st.info(
                "👍 Great progress — almost there."
            )
        elif hydration_score >= 50:
            st.warning(
                "⚠️ Moderate hydration — drink more."
            )
        else:
            st.error(
                "🚨 Low hydration — increase intake urgently."
            )

        st.divider()

        # ====================================
        # Daily Comparison Chart
        # ====================================

        st.subheader("📅 Daily Intake Comparison")

        daily_df = (
            df.groupby("Date")["Intake (mL)"]
            .sum()
            .reset_index()
        )

        st.bar_chart(
            daily_df.set_index("Date")
        )

        # ====================================
        # Cumulative Chart
        # ====================================

        st.subheader("📈 Cumulative Hydration Growth")

        daily_df["Cumulative Intake"] = (
            daily_df["Intake (mL)"].cumsum()
        )

        st.area_chart(
            daily_df.set_index("Date")["Cumulative Intake"]
        )

    else:

        st.info(
            "No intake history found. "
            "Log water from the sidebar 🚰"
        )
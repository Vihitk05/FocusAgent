import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from backend.agent import plan_day, feedback_loop, generate_weekly_review, export_to_pdf, get_memory_snapshot, retrieve_preferences, save_static_preferences

st.set_page_config(page_title="🧠 FocusAgent AI", layout="centered")
st.title("🧠 FocusAgent: AI Task Planner")

# Onboarding - only if preferences not yet stored
prefs = retrieve_preferences()
if not prefs:
    st.subheader("👋 Welcome to FocusAgent!")
    st.write("Let’s quickly customize your preferences. When do you usually:")
    wake_time = st.time_input("Wake Up", value=None)
    lunch_time = st.time_input("Lunch", value=None)
    dinner_time = st.time_input("Dinner", value=None)
    if st.button("Save Preferences"):
        prefs = {
            "wake_time": str(wake_time),
            "lunch_time": str(lunch_time),
            "dinner_time": str(dinner_time)
        }
        save_static_preferences(prefs)
        st.success("Preferences saved and learned!")
        st.rerun()
    st.stop()

# Input
today_tasks = st.text_area("📝 What do you want to get done today?", "")

if st.button("🗕️ Plan My Day"):
    plan = plan_day(today_tasks)
    st.subheader("🔢 Suggested Schedule")
    st.markdown(plan)

if st.button("🖨️ Export Schedule to PDF"):
    path = export_to_pdf("FocusAgent Daily Plan", plan_day(today_tasks), "today_plan.pdf")
    st.success(f"PDF exported: {path}")

# Feedback
tasks_done = st.text_area("✅ What did you actually complete?", "")
if st.button("📤 Submit Feedback"):
    if tasks_done.strip():
        status = feedback_loop(tasks_done)
        st.success(status)
        st.info("Reinforcement insight stored.")
    else:
        st.warning("Please enter what you completed before submitting feedback.")

# Weekly Review
if st.button("📊 Generate Weekly Review"):
    summary = generate_weekly_review()
    st.subheader("🧠 Weekly Strategy Suggestions")
    st.markdown(summary)

# Memory Visualizer
if st.button("📚 Show Memory Snapshot"):
    mems = get_memory_snapshot()
    st.subheader("🧠 Memory Snapshot")
    for m in mems:
        st.markdown(f"- {m}")

# Preferences Editor (optional)
with st.expander("⚙️ Edit Preferences"):
    wake_time = st.time_input("Wake Up Time", value=None, key="wake")
    lunch_time = st.time_input("Lunch Time", value=None, key="lunch")
    dinner_time = st.time_input("Dinner Time", value=None, key="dinner")
    if st.button("Update Preferences"):
        prefs = {
            "wake_time": str(wake_time),
            "lunch_time": str(lunch_time),
            "dinner_time": str(dinner_time)
        }
        save_static_preferences(prefs)
        st.success("Preferences updated.")
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from backend.agent import plan_day, feedback_loop

st.title("💡 FocusAgent: Smarter Daily Planning")

st.header("🕊️ Input Your Tasks")
today_tasks = st.text_area("What do you want to get done today?", "Finish blog post, reply to emails, prep design review")

if st.button("📅 Plan My Day"):
    plan = plan_day(today_tasks)
    st.subheader("🔢 Suggested Schedule")
    st.write(plan)

st.header("✅ End-of-Day Feedback")
tasks_done = st.text_area("What did you actually complete today?")

if st.button("🚀 Submit Feedback"):
    result = feedback_loop(tasks_done)
    st.success(result)

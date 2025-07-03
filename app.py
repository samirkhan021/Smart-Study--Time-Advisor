import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Smart Study Time Advisor", layout="centered")

st.title("📚 Smart Study Time Advisor")
st.write("Let me help you create an effective study plan!")

# Step 1: Time Slots
st.header("1️⃣ Enter Your Free Time Slots")

slots = []
num_slots = st.number_input("How many free time slots do you have today?", min_value=1, max_value=10, step=1)

for i in range(num_slots):
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.time_input(f"Start time for Slot {i+1}")
    with col2:
        end_time = st.time_input(f"End time for Slot {i+1}")
    slots.append((start_time, end_time))

# Step 2: Subjects
st.header("2️⃣ Enter Subjects and Difficulty")

subjects = []
num_subjects = st.number_input("How many subjects do you want to study?", min_value=1, max_value=10, step=1)

difficulty_map = {"Easy": 1, "Medium": 2, "Hard": 3}

for i in range(num_subjects):
    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input(f"Subject {i+1}")
    with col2:
        difficulty = st.selectbox(f"Difficulty of {subject}", ["Easy", "Medium", "Hard"], key=i)
    if subject:
        subjects.append((subject, difficulty_map[difficulty]))

# Generate Plan
if st.button("📅 Generate Study Plan"):
    if not slots or not subjects:
        st.error("Please enter at least one slot and one subject.")
    else:
        # Sort subjects by difficulty (descending)
        subjects.sort(key=lambda x: x[1], reverse=True)
        
        plan = []
        subject_index = 0
        
        for i, (start, end) in enumerate(slots):
            start_dt = datetime.combine(datetime.today(), start)
            end_dt = datetime.combine(datetime.today(), end)
            duration = (end_dt - start_dt).seconds // 60

            if duration < 15:
                plan.append((f"Slot {i+1}", "Too short for study", ""))
                continue

            subject = subjects[subject_index % len(subjects)][0]
            plan.append((f"Slot {i+1}", subject, f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"))
            subject_index += 1

        # Display Study Plan
        st.success("Here's your recommended study plan!")
        df = pd.DataFrame(plan, columns=["Slot", "Subject", "Time"])
        st.table(df)

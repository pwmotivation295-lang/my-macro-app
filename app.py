import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(page_title="MacroTracker", page_icon="💪", layout="centered")

# Database Setup
DB_FILE = "macro_history.csv"
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["Date", "Calories (kcal)", "Protein (g)"])
    df.to_csv(DB_FILE, index=False)

def load_data():
    return pd.read_csv(DB_FILE)

def save_data(df):
    df.to_csv(DB_FILE, index=False)

history_df = load_data()

# Navigation tabs like an app
app_mode = st.radio("Nav", ["➕ Log Today", "📊 View History"], horizontal=True, label_visibility="collapsed")
st.markdown("---")

if "Log Today" in app_mode:
    st.markdown("### ➕ Add Daily Intake")
    with st.container(border=True):
        log_date = st.date_input("Date", date.today())
        calories = st.number_input("Calories (kcal)", min_value=0, step=50, value=0)
        protein = st.number_input("Protein (g)", min_value=0, step=5, value=0)
        submit_btn = st.button("Save Log", use_container_width=True, type="primary")
        
    if submit_btn:
        date_str = str(log_date)
        if date_str in history_df["Date"].astype(str).values:
            idx = history_df[history_df["Date"].astype(str) == date_str].index[0]
            history_df.at[idx, "Calories (kcal)"] += calories
            history_df.at[idx, "Protein (g)"] += protein
        else:
            new_row = pd.DataFrame({"Date": [date_str], "Calories (kcal)": [calories], "Protein (g)": [protein]})
            history_df = pd.concat([history_df, new_row], ignore_index=True)
        save_data(history_df)
        st.success("Saved successfully!")
        st.rerun()

elif "View History" in app_mode:
    st.markdown("### 📊 Logged History")
    if not history_df.empty:
        for index, row in history_df.sort_values(by="Date", ascending=False).iterrows():
            with st.container(border=True):
                st.markdown(f"**📅 {row['Date']}** — 🔥 `{row['Calories (kcal)']} kcal` | 🍗 `{row['Protein (g)']}g` ")
    else:
        st.info("No logs tracked yet.")
      

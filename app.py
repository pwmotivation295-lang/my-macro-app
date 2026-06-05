import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Optimize page settings for mobile and web view
st.set_page_config(page_title="Macro Tracker", layout="wide")

# Connect to your Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. FETCH DATA ON PAGE LOAD (ttl=0 forces a fresh pull from Google Sheets)
try:
    df = conn.read(ttl=0)
    # Ensure columns exist and clean up any empty rows
    df = df.dropna(subset=["date", "calories", "protein"])
except Exception:
    df = pd.DataFrame(columns=["calories", "protein", "date"])

# 2. CREATE TABS FOR CLEAN MOBILE NAVIGATION
tab1, tab2 = st.tabs(["📊 Analytics & History", "🥗 Add New Entry"])

# ==========================================
# TAB 1: ANALYTICS & HISTORICAL DATA LOG
# ==========================================
with tab1:
    st.subheader("📈 Analytics Workspace")
    
    if not df.empty:
        # Convert columns to numeric types for flawless charting
        df["calories"] = pd.to_numeric(df["calories"], errors='coerce').fillna(0)
        df["protein"] = pd.to_numeric(df["protein"], errors='coerce').fillna(0)
        df["date"] = df["date"].astype(str)
        
        # Calculate Quick Stats Summary
        total_entries = len(df)
        avg_calories = int(df["calories"].mean())
        avg_protein = int(df["protein"].mean())
        
        # Display Summary Cards
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Days Logged", f"{total_entries} Days")
        m2.metric("Average Energy", f"{avg_calories} kcal")
        m3.metric("Average Protein", f"{avg_protein} g")
        
        # Draw Live Progress Chart over time
        st.write("### Consumed Trends Over Time")
        st.line_chart(df, x="date", y=["calories", "protein"])
        
        # Show Spreadsheet Rows Table
        st.write("### 📋 Historical Data Log")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No saved tracking data found yet. Go to the 'Add New Entry' tab to start logging!")

# ==========================================
# TAB 2: INPUT FORM FOR NEW ENTRIES
# ==========================================
with tab2:
    st.subheader("📥 Add Nutrient Entry")
    
    with st.container(border=True):
        date_input = st.date_input("Target Recording Date")
        calories_input = st.number_input("Energy Value (kcal)", min_value=0, value=300, step=1)
        protein_input = st.number_input("Protein Substrate (g)", min_value=0, value=6, step=1)
        
        # Red theme submission button
        submit_button = st.button("Generate Cloud Sync Entry", type="primary", use_container_width=True)

    if submit_button:
        with st.spinner("Syncing your data securely with Google Sheets..."):
            # Construct the new entry row format
            new_entry = pd.DataFrame([{
                "calories": int(calories_input),
                "protein": int(protein_input),
                "date": str(date_input)
            }])
            
            # Combine historical data with our fresh entry row
            updated_data = pd.concat([df, new_entry], ignore_index=True)
            
            # Commit update directly live to your spreadsheet
            conn.update(data=updated_data)
            
            st.success("🎉 Successfully synced your entry to the MACRO TRACKER spreadsheet!")
            
            # Auto-reload app logic so Tab 1 immediately updates with the fresh data
            st.rerun()
            

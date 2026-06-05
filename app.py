import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Set page layout title
st.title("🥗 Add Nutrient Entry")

# Set up the input fields to match your UI layout
with st.container(border=True):
    date_input = st.date_input("Target Recording Date")
    calories_input = st.number_input("Energy Value (kcal)", min_value=0, value=300, step=1)
    protein_input = st.number_input("Protein Substrate (g)", min_value=0, value=6, step=1)

    # Big red sync button matching your theme
    submit_button = st.button("Generate Cloud Sync Entry", type="primary", use_container_width=True)

# Connect to Google Sheets using the Streamlit Connection API
conn = st.connection("gsheets", type=GSheetsConnection)

if submit_button:
    with st.spinner("Syncing entry to Google Cloud Spreadsheet..."):
        try:
            # 1. Fetch current data from the sheet to prevent overwriting
            existing_data = conn.read(ttl=0)
        except Exception:
            # If the sheet is blank, initialize empty dataframe with your lowercase columns
            existing_data = pd.DataFrame(columns=["calories", "protein", "date"])

        # 2. Create a row with user inputs matching your column names exactly
        new_entry = pd.DataFrame([{
            "calories": int(calories_input),
            "protein": int(protein_input),
            "date": str(date_input)
        }])

        # 3. Append the new entry row to your existing logs
        updated_data = pd.concat([existing_data, new_entry], ignore_index=True)

        # 4. Upload back to your Google Sheet live
        conn.update(data=updated_data)
        
        st.success("🎉 Successfully synced your entry to the MACRO TRACKER spreadsheet!")

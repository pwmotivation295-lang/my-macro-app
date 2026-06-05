import streamlit as st
import pandas as pd
from datetime import date

# --- 1. PRO EXECUTIVE APP INTERFACE CONFIG ---
st.set_page_config(page_title="MacroPro Labs", page_icon="👑", layout="centered", initial_sidebar_state="collapsed")

# Premium Custom UI Injection
st.markdown("""
    <style>
    div[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 800 !important; color: #10B981; }
    div[data-testid="stMetricLabel"] { font-size: 11px !important; text-transform: uppercase; letter-spacing: 1px; color: #9CA3AF; }
    div[data-testid="stVerticalBlockBorder"] { background-color: #111827; border-radius: 16px; padding: 20px !important; border: 1px solid #1F2937 !important; margin-bottom: 15px; }
    .stRadio div[role="radiogroup"] { background-color: #1F2937; padding: 6px; border-radius: 12px; border: 1px solid #374151; }
    .stRadio div[role="radiogroup"] label { font-weight: 600 !important; font-size: 14px !important; padding: 8px 16px !important; border-radius: 8px; margin: 0px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. USER CONFIGURATION ---
TARGET_CALORIES = 1600
TARGET_PROTEIN = 100
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ug8DSMVE7PTJnJfTXxl8XVlHrePmOWTWVF7dJV1pzKQ/edit?usp=drivesdk"

# --- 3. DATABASE CONVERSION SYSTEM ---
def get_csv_url(url):
    try:
        base_url = url.split("/edit")[0]
        return f"{base_url}/gviz/tq?tqx=out:csv"
    except:
        return None

CSV_URL = get_csv_url(GOOGLE_SHEET_URL)

def load_data():
    if not CSV_URL:
        return pd.DataFrame(columns=["Date", "Calories", "Protein"])
    try:
        df = pd.read_csv(CSV_URL)
        if "Date" not in df.columns:
            return pd.DataFrame(columns=["Date", "Calories", "Protein"])
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df
    except:
        return pd.DataFrame(columns=["Date", "Calories", "Protein"])

history_df = load_data()
today_date = date.today()

today_row = history_df[history_df["Date"] == today_date]
logged_cal = int(today_row["Calories"].sum()) if not today_row.empty else 0
logged_prot = int(today_row["Protein"].sum()) if not today_row.empty else 0

# --- 4. NAVIGATION TAB ---
selected_tab = st.radio("Nav", ["⚡ Overview", "🥗 Log Nutrition", "📈 Analytics Workspace"], horizontal=True, label_visibility="collapsed")
st.markdown("---")

# MODULE 1: OVERVIEW
if "Overview" in selected_tab:
    st.markdown(f"### ⚡ Daily Progress\n*{today_date.strftime('%A, %B %d, %Y')}*")
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric(label="Calories Consumed", value=f"{logged_cal} kcal", delta=f"{TARGET_CALORIES - logged_cal} remaining", delta_color="inverse")
    with m_col2:
        st.metric(label="Protein Target", value=f"{logged_prot} g", delta=f"{TARGET_PROTEIN - logged_prot} remaining", delta_color="inverse")
    
    cal_percentage = min(float(logged_cal / TARGET_CALORIES), 1.0) if TARGET_CALORIES > 0 else 0.0
    st.caption(f"🔥 **Energy Goal Fulfillment:** {int(cal_percentage * 100)}%")
    st.progress(cal_percentage)
    
    prot_percentage = min(float(logged_prot / TARGET_PROTEIN), 1.0) if TARGET_PROTEIN > 0 else 0.0
    st.caption(f"🍗 **Anabolic Muscle Support:** {int(prot_percentage * 100)}%")
    st.progress(prot_percentage)

# MODULE 2: LOG INTAKE
elif "Log Nutrition" in selected_tab:
    st.markdown("### 🥗 Add Nutrient Entry")
    with st.container(border=True):
        entry_date = st.date_input("Target Recording Date", date.today())
        input_cal = st.number_input("Energy Value (kcal)", min_value=0, max_value=10000, step=50, value=0)
        input_prot = st.number_input("Protein Substrate (g)", min_value=0, max_value=500, step=5, value=0)
        save_action = st.button("Generate Cloud Sync Entry", use_container_width=True, type="primary")
        
    if save_action:
        # Formulate direct sheet submission link
        form_date = str(entry_date)
        # Display cloud instruction for pure data persistence
        st.success("To completely automate writing back to Google Sheets, use the Streamlit Secrets tab to connect st.connection('gsheets'). For now, copy this row directly to your spreadsheet if it doesn't auto-sync:")
        st.code(f"{form_date},{input_cal},{input_prot}")

# MODULE 3: ANALYTICS
elif "Analytics Workspace" in selected_tab:
    st.markdown("### 📈 Historical Visual Logs")
    if len(history_df) >= 1:
        visual_df = history_df.sort_values(by="Date").set_index("Date")
        st.markdown("##### 📊 Caloric Tracking History")
        st.line_chart(visual_df["Calories"], color="#10B981")
        st.markdown("##### 📊 Protein Tracking History")
        st.area_chart(visual_df["Protein"], color="#6366F1")
    else:
        st.info("Your Google Sheet database appears empty. Add data to the Sheet to see charts.")
        

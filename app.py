import streamlit as st
import pandas as pd
from datetime import date
import os

# --- 1. PRO EXECUTIVE APP INTERFACE CONFIG ---
st.set_page_config(
    page_title="MacroPro Labs",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Premium Custom UI Injection (Bespoke Font Sizes & Component Spacing)
st.markdown("""
    <style>
    /* Premium Typography & Metric Styling */
    div[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 800 !important; color: #10B981; font-family: 'SF Pro Display', -apple-system, sans-serif; }
    div[data-testid="stMetricLabel"] { font-size: 11px !important; text-transform: uppercase; letter-spacing: 1px; color: #9CA3AF; }
    
    /* Clean Layout Containers */
    div[data-testid="stVerticalBlockBorder"] { background-color: #111827; border-radius: 16px; padding: 20px !important; border: 1px solid #1F2937 !important; margin-bottom: 15px; }
    
    /* Segmented Navigation Menu Styling */
    .stRadio div[role="radiogroup"] { background-color: #1F2937; padding: 6px; border-radius: 12px; border: 1px solid #374151; }
    .stRadio div[role="radiogroup"] label { font-weight: 600 !important; font-size: 14px !important; padding: 8px 16px !important; border-radius: 8px; margin: 0px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. USER MACRO PROFILE TARGETS ---
TARGET_CALORIES = 2200
TARGET_PROTEIN = 150

# --- 3. HARDWARE CORE DATABASE SETUP ---
DB_FILE = "macro_premium_history.csv"
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["Date", "Calories", "Protein"])
    df.to_csv(DB_FILE, index=False)

def load_data():
    df = pd.read_csv(DB_FILE)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    return df

def save_data(df):
    df.to_csv(DB_FILE, index=False)

history_df = load_data()
today_date = date.today()

# Safely extract calculations for the current calendar date
today_row = history_df[history_df["Date"] == today_date]
logged_cal = int(today_row["Calories"].sum()) if not today_row.empty else 0
logged_prot = int(today_row["Protein"].sum()) if not today_row.empty else 0

# --- 4. NAVIGATION TAB ELEMENT ---
selected_tab = st.radio(
    "Navigation System",
    ["⚡ Overview", "🥗 Log Nutrition", "📈 Analytics Workspace"],
    horizontal=True,
    label_visibility="collapsed"
)
st.markdown("---")

# ==========================================
# MODULE 1: PREMIUM PERFORMANCE DASHBOARD
# ==========================================
if "Overview" in selected_tab:
    st.markdown(f"### ⚡ Daily Progress\n*{today_date.strftime('%A, %B %d, %Y')}*")
    
    # Grid Layout for Core Performance Counters
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric(label="Calories Consumed", value=f"{logged_cal} kcal", delta=f"{TARGET_CALORIES - logged_cal} remaining", delta_color="inverse")
    with m_col2:
        st.metric(label="Protein Target", value=f"{logged_prot} g", delta=f"{TARGET_PROTEIN - logged_prot} remaining", delta_color="inverse")
    
    # Custom Dynamic Status Indicators
    cal_percentage = min(float(logged_cal / TARGET_CALORIES), 1.0) if TARGET_CALORIES > 0 else 0.0
    st.caption(f"🔥 **Energy Goal Fulfillment:** {int(cal_percentage * 100)}%")
    st.progress(cal_percentage)
    
    prot_percentage = min(float(logged_prot / TARGET_PROTEIN), 1.0) if TARGET_PROTEIN > 0 else 0.0
    st.caption(f"🍗 **Anabolic Muscle Support:** {int(prot_percentage * 100)}%")
    st.progress(prot_percentage)
    
    # Premium Notification Alerts
    st.markdown("##### 🛎️ Assistant Insights")
    if logged_cal == 0:
        st.info("Your performance log is clean today. Ready to record your first meal context?")
    elif logged_cal < TARGET_CALORIES and logged_prot < TARGET_PROTEIN:
        st.warning("Under target parameters. Prioritize clear protein sources for your upcoming nutritional intake.")
    else:
        st.success("Target saturation profile completed successfully! Excellent structural consistency.")

# ==========================================
# MODULE 2: PRODUCTION RECORD INTAKE
# ==========================================
elif "Log Nutrition" in selected_tab:
    st.markdown("### 🥗 Add Nutrient Entry")
    
    with st.container(border=True):
        entry_date = st.date_input("Target Recording Date", date.today())
        input_cal = st.number_input("Energy Value (kcal)", min_value=0, max_value=10000, step=50, value=0)
        input_prot = st.number_input("Protein Substrate (g)", min_value=0, max_value=500, step=5, value=0)
        
        save_action = st.button("Commit Food Item to Ledger", use_container_width=True, type="primary")
        
    if save_action:
        if entry_date in history_df["Date"].values:
            idx = history_df[history_df["Date"] == entry_date].index[0]
            history_df.at[idx, "Calories"] += input_cal
            history_df.at[idx, "Protein"] += input_prot
        else:
            new_entry = pd.DataFrame({"Date": [entry_date], "Calories": [input_cal], "Protein": [input_prot]})
            history_df = pd.concat([history_df, new_entry], ignore_index=True)
            
        save_data(history_df)
        st.toast("🧬 Database Ledger Updated", icon="✅")
        st.rerun()

# ==========================================
# MODULE 3: METRIC ANALYSIS WORKSPACE
# ==========================================
elif "Analytics Workspace" in selected_tab:
    st.markdown("### 📈 Chronological Historical Charts")
    
    if len(history_df) >= 2:
        visual_df = history_df.sort_values(by="Date").set_index("Date")
        
        # High Fidelity Interactive Trend-line Matrix Charts
        st.markdown("##### 📊 Historical Caloric Ceiling Metrics")
        st.line_chart(visual_df["Calories"], color="#10B981")
        
        st.markdown("##### 📊 Historical Protein Retention Curve")
        st.area_chart(visual_df["Protein"], color="#6366F1")
        
        # Full Audit Log Data Sheet Table View
        with st.expander("🛠️ Open Complete Historical Spreadsheet Data Log"):
            st.dataframe(history_df.sort_values(by="Date", ascending=False), use_container_width=True)
    else:
        st.info("Historical visual rendering requires a database volume of at least 2 entries across unique separate days.")
      

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Expense Tracker", layout="wide")
st.title("🧾 Smart Expense Tracker")

# --- Sidebar: Configuration & Filters ---
with st.sidebar:
    st.header("⚙️ Configuration")
    provider = st.selectbox("Select AI Provider", ["Local (Ollama)", "Gemini", "OpenAI", "Claude"])
    
    api_key = None
    if provider != "Local (Ollama)":
        api_key = st.text_input(f"Enter {provider} API Key", type="password")
    
    # --- NEW: Time Filter ---
    st.divider()
    st.header("📅 Analytics Filter")
    time_filter = st.radio("Show Expenses For:", ["All Time", "Last 30 Days", "Last 7 Days"])

    # Model Selection Logic
    available_models = []
    if provider == "Local (Ollama)" or (api_key and len(api_key) > 5):
        try:
            resp = requests.post(f"{API_URL}/models", data={"provider": provider, "api_key": api_key})
            if resp.status_code == 200:
                available_models = resp.json().get("models", [])
        except: pass
    selected_model = st.selectbox("Select Model", available_models) if available_models else st.text_input("Model Name", value="deepseek-ocr")

# --- Logic Helper ---
def upload_to_api(file_bytes, file_name, file_type):
    with st.spinner(f"Processing..."):
        try:
            files = {"file": (file_name, file_bytes, file_type)}
            data = {"provider": provider, "model": selected_model, "api_key": api_key or ""}
            response = requests.post(f"{API_URL}/scan", files=files, data=data)
            if response.status_code == 200:
                st.success("Success!")
                st.json(response.json())
                return True
            else:
                st.error(f"Failed: {response.text}")
                return False
        except Exception as e:
            st.error(f"Connection Error: {e}")
            return False

# --- Input Tabs ---
tab1, tab2, tab3 = st.tabs(["📤 Upload File", "📸 Camera Scan", "📊 Bulk Import"])
with tab1:
    uploaded_file = st.file_uploader("Upload Receipt", type=["jpg", "png", "jpeg", "pdf"])
    if uploaded_file and st.button("Scan File"):
        upload_to_api(uploaded_file.getvalue(), uploaded_file.name, uploaded_file.type)
with tab2:
    camera_img = st.camera_input("Take a picture")
    if camera_img and st.button("Process Photo"):
        upload_to_api(camera_img.getvalue(), "camera_capture.jpg", "image/jpeg")
with tab3:
    data_file = st.file_uploader("Upload Excel/CSV", type=["csv", "xlsx"])
    if data_file and st.button("Import Data"):
        upload_to_api(data_file.getvalue(), data_file.name, "application/octet-stream")

# --- Dashboard Section ---
st.divider()
st.subheader(f"💰 Expense Dashboard ({time_filter})")

try:
    response = requests.get(f"{API_URL}/expenses")
    if response.status_code == 200:
        expenses = response.json()
        if expenses:
            df = pd.DataFrame(expenses)
            
            # --- DATE FILTERING LOGIC ---
            # Convert date column to datetime objects
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
            # Filter based on selection
            if time_filter == "Last 30 Days":
                cutoff = datetime.now() - timedelta(days=30)
                df = df[df['date'] >= cutoff]
            elif time_filter == "Last 7 Days":
                cutoff = datetime.now() - timedelta(days=7)
                df = df[df['date'] >= cutoff]
            
            if not df.empty:
                # Metrics
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Spend", f"${df['total'].sum():.2f}")
                m2.metric("Transactions", len(df))
                m3.metric("Top Category", df['category'].mode()[0] if not df.empty else "N/A")
                
                # Download Button (Downloads ONLY the filtered view)
                csv = df.to_csv(index=False).encode('utf-8')
                m4.download_button(
                    label=f"📥 Download {time_filter} Report",
                    data=csv,
                    file_name=f"expenses_{time_filter.replace(' ', '_').lower()}.csv",
                    mime="text/csv",
                )

                # Charts
                c1, c2 = st.columns(2)
                with c1:
                    fig_cat = px.pie(df, names='category', values='total', title=f"Spending by Category ({time_filter})")
                    st.plotly_chart(fig_cat, width="stretch")
                with c2:
                    # Sort by date for the bar chart
                    df_sorted = df.sort_values(by="date")
                    fig_time = px.bar(df_sorted, x='date', y='total', title="Spending Timeline")
                    st.plotly_chart(fig_time, width="stretch")
                    
                st.dataframe(df, width="stretch")

                # --- AI Analysis (Aware of Filter) ---
                st.divider()
                st.subheader("🤖 AI Financial Advisor")
                if st.button(f"Analyze {time_filter} Data"):
                    # Convert Timestamps back to string for JSON serialization
                    df_to_send = df.copy()
                    df_to_send['date'] = df_to_send['date'].dt.strftime('%Y-%m-%d')
                    
                    with st.spinner("Analyzing..."):
                        payload = {
                            "expenses": df_to_send.to_dict(orient="records"),
                            "api_key": api_key if api_key else "",
                            "provider": provider,
                            "model": selected_model
                        }
                        res = requests.post(f"{API_URL}/analyze", json=payload)
                        if res.status_code == 200:
                            st.markdown(res.json()['advice'])
                        else:
                            st.error(res.text)
            else:
                st.warning(f"No expenses found for {time_filter}.")
        else:
            st.info("No expenses recorded yet.")
except Exception as e:
    st.error(f"Backend Error: {e}")
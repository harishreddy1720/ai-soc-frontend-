import streamlit as st
import pandas as pd
import requests

st.title("AI-Powered SOC Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload Network Logs (CSV)", type=["csv"])

# If a file is uploaded
if uploaded_file:
    # Send the file to the backend
    response = requests.post(
        "https://ai-powerd-soc.onrender.com/predict_anomaly/",
        files={"file": uploaded_file}
    )

    # Check if the request was successful
    if response.status_code == 200:
        try:
            alerts = response.json()
        except ValueError:
            st.error("❌ The response is not valid JSON.")
            st.stop()
    else:
        st.error(f"❌ Request failed with status code {response.status_code}")
        st.error(f"Response text: {response.text}")
        st.stop()

    # Display the results
    st.subheader("Detected Anomalies")
    if alerts:
        df_alerts = pd.DataFrame(alerts)
        st.dataframe(df_alerts)
    else:
        st.success("✅ No anomalies detected!")

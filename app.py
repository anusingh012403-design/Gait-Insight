import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Clinical Reverse Walking App",
    page_icon="🧠",
    layout="wide"
)

# ---------- SIDEBAR ----------
st.sidebar.title("🧠 Clinical Gait System")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home","📥 Upload & Analysis","📊 Visualization","📡 Live Monitoring","🧾 Clinical Report"]
)

# =====================================================
# HOME PAGE
# =====================================================

if page=="🏠 Home":

    st.title("🚶 Reverse Walking Clinical Analysis System")

    st.write("""
    Professional biomedical application for gait analysis.
    Upload patient gait reports to generate automatic analysis.
    """)

# =====================================================
# UPLOAD & ANALYSIS
# =====================================================

elif page=="📥 Upload & Analysis":

    st.title("📥 Upload Patient Data")

    file = st.file_uploader("Upload CSV")

    if file:

        data = pd.read_csv(file)

        st.session_state["data"] = data

        st.success("Data uploaded successfully")

        st.dataframe(data)

# =====================================================
# VISUALIZATION
# =====================================================

elif page=="📊 Visualization":

    st.title("📊 Advanced Visualization")

    if "data" in st.session_state:

        data = st.session_state["data"]

        parameters = [c for c in data.columns if c!="subject"]

        selected = st.selectbox("Select Parameter", parameters)

        fig, ax = plt.subplots()

        ax.bar(data["subject"], data[selected])

        st.pyplot(fig)

        # Radar
        angles = np.linspace(0,2*np.pi,len(parameters),endpoint=False)

        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)

        for i in range(len(data)):
            values = data.loc[i,parameters].tolist()
            values += values[:1]
            ang = np.concatenate((angles,[angles[0]]))

            ax.plot(ang,values,label=data.loc[i,"subject"])

        ax.set_xticks(angles)
        ax.set_xticklabels(parameters)
        ax.legend()

        st.pyplot(fig)

# =====================================================
# LIVE MONITORING
# =====================================================

elif page=="📡 Live Monitoring":

    st.title("📡 Live Gait Monitoring (Simulation)")

    chart = st.line_chart(np.random.randn(10,1))

    for i in range(30):

        new_data = np.random.randn(1,1)
        chart.add_rows(new_data)
        time.sleep(0.2)

# =====================================================
# CLINICAL REPORT
# =====================================================

elif page=="🧾 Clinical Report":

    st.title("🧾 Automatic Clinical Report")

    if "data" in st.session_state:

        data = st.session_state["data"]

        for i in range(len(data)):

            st.subheader(f"Patient: {data.loc[i,'subject']}")

            if "walking_speed" in data.columns and data.loc[i,"walking_speed"]<0.7:
                st.error("Reduced walking speed detected")

            if "stride_length" in data.columns and data.loc[i,"stride_length"]<1:
                st.warning("Short stride length observed")

            st.success("Analysis completed")

    else:

        st.warning("Upload data first.")

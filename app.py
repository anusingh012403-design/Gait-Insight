import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ---------- PAGE SETTINGS ----------
st.set_page_config(
    page_title="Clinical Gait Dashboard",
    layout="wide"
)

# ---------- SIDEBAR ----------
st.sidebar.title("🧠 Clinical Gait App")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📊 Clinical Dashboard"]
)

# ---------- HOME PAGE ----------
if page == "🏠 Home":

    st.title("🚶 Reverse Walking Clinical Analysis")

    st.write("""
    This professional clinical dashboard analyzes reverse walking gait parameters.

    Features:
    - Multi-subject comparison
    - Clinical metrics overview
    - Radar gait visualization
    - Automatic clinical interpretation
    """)

# ---------- DASHBOARD ----------
elif page == "📊 Clinical Dashboard":

    st.title("📊 Clinical Gait Dashboard")

    file = st.file_uploader("📁 Upload Reverse Walking CSV")

    if file:

        data = pd.read_csv(file)

        st.subheader("👀 Uploaded Data")
        st.dataframe(data)

        # Auto detect parameters
        parameters = [col for col in data.columns if col != "subject"]

        subjects = data["subject"]

        # ---------- METRIC CARDS ----------
        st.subheader("🩺 Clinical Metrics Overview")

        cols = st.columns(len(parameters))

        for i, param in enumerate(parameters):
            avg_value = data[param].mean()
            cols[i].metric(f"📌 {param}", round(avg_value,2))

        # ---------- TABS ----------
        tab1, tab2, tab3 = st.tabs(["📊 Graph View", "🕸 Radar Analysis", "🧾 Clinical Report"])

        # ---------- BAR GRAPH ----------
        with tab1:

            st.subheader("Multi-Parameter Comparison")

            fig, ax = plt.subplots()

            x = range(len(parameters))

            for i, subject in enumerate(subjects):
                values = data.loc[i, parameters]
                ax.bar([p + i*0.3 for p in x], values, width=0.3, label=subject)

            ax.set_xticks(list(x))
            ax.set_xticklabels(parameters, rotation=45)

            ax.legend()

            st.pyplot(fig)

        # ---------- RADAR CHART ----------
        with tab2:

            st.subheader("Radar Gait Analysis")

            angles = np.linspace(0, 2*np.pi, len(parameters), endpoint=False)

            fig = plt.figure()
            ax = fig.add_subplot(111, polar=True)

            for i, subject in enumerate(subjects):
                values = data.loc[i, parameters].tolist()
                values += values[:1]
                ang = np.concatenate((angles, [angles[0]]))

                ax.plot(ang, values, label=subject)

            ax.set_xticks(angles)
            ax.set_xticklabels(parameters)

            ax.legend()

            st.pyplot(fig)

        # ---------- CLINICAL REPORT ----------
        with tab3:

            st.subheader("Automatic Clinical Interpretation")

            for param in parameters:
                if data[param].iloc[0] > data[param].iloc[1]:
                    st.write(f"🔍 Subject {subjects.iloc[0]} shows higher {param}.")
                else:
                    st.write(f"🔍 Subject {subjects.iloc[1]} shows higher {param}.")

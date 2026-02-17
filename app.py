import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Clinical Gait Analyzer",
    page_icon="🧠",
    layout="wide"
)

# ---------- SIDEBAR NAVIGATION ----------
st.sidebar.title("🧠 Clinical Gait App")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📊 Analysis", "🧾 Clinical Report"]
)

# ---------- HOME PAGE ----------
if page == "🏠 Home":

    st.title("🚶 Reverse Walking Clinical Analysis System")

    st.markdown("""
    ### Advanced Biomedical Application

    Upload gait data and get automatic clinical analysis.

    Features:

    ✅ Multi-subject comparison  
    ✅ Interactive graphs  
    ✅ Radar biomechanical analysis  
    ✅ Automatic clinical report generation
    """)

# ---------- ANALYSIS PAGE ----------
elif page == "📊 Analysis":

    st.title("📊 Clinical Analysis Dashboard")

    file = st.file_uploader("Upload Reverse Walking CSV")

    if file:

        data = pd.read_csv(file)

        st.session_state["data"] = data

        st.subheader("📄 Uploaded Data")
        st.dataframe(data)

        parameters = [col for col in data.columns if col != "subject"]

        # METRIC CARDS
        st.subheader("📌 Key Metrics")

        cols = st.columns(len(parameters))

        for i,param in enumerate(parameters):
            cols[i].metric(param, round(data[param].mean(),2))

        # BAR GRAPH
        st.subheader("📊 Multi-Parameter Comparison")

        fig, ax = plt.subplots()

        for i in range(len(data)):
            values = data.loc[i, parameters]
            ax.bar(parameters, values, alpha=0.5, label=data.loc[i,"subject"])

        ax.legend()
        plt.xticks(rotation=45)

        st.pyplot(fig)

        # RADAR GRAPH
        st.subheader("🕸 Radar Biomechanical Visualization")

        angles = np.linspace(0, 2*np.pi, len(parameters), endpoint=False)

        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)

        for i in range(len(data)):

            values = data.loc[i, parameters].tolist()
            values += values[:1]
            ang = np.concatenate((angles, [angles[0]]))

            ax.plot(ang, values, label=data.loc[i,"subject"])

        ax.set_xticks(angles)
        ax.set_xticklabels(parameters)
        ax.legend()

        st.pyplot(fig)

# ---------- REPORT PAGE ----------
elif page == "🧾 Clinical Report":

    st.title("🧾 Automatic Clinical Report")

    if "data" in st.session_state:

        data = st.session_state["data"]

        for i in range(len(data)):

            st.markdown(f"## Patient: {data.loc[i,'subject']}")

            if data.loc[i,"walking_speed"] < 0.7:
                st.warning("⚠ Reduced walking speed detected")

            if data.loc[i,"stride_length"] < 1.0:
                st.warning("⚠ Reduced stride length")

            if data.loc[i,"cadence"] > 120:
                st.warning("⚠ High cadence compensation")

            st.success("Analysis completed.")

    else:
        st.info("Upload data first from Analysis page.")

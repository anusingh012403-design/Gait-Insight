import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------- PAGE CONFIG --------
st.set_page_config(
    page_title="Clinical Reverse Walking App",
    page_icon="🧠",
    layout="wide"
)

# -------- SIDEBAR --------
st.sidebar.title("🧠 Clinical Gait App")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home","📊 Analysis","📈 Visualization"]
)

# =================================================
# HOME PAGE
# =================================================

if page=="🏠 Home":

    st.title("🚶 Reverse Walking Clinical Analysis")

    st.subheader("Ultra Premium Biomedical Dashboard")

    st.write("""
    Upload reverse walking gait reports and receive automated clinical analysis.
    """)

    st.markdown("""
    ### Features

    ✅ Multi-subject comparison  
    ✅ Clinical metrics overview  
    ✅ Radar biomechanical visualization  
    ✅ Automatic clinical interpretation  
    """)

# =================================================
# ANALYSIS PAGE
# =================================================

elif page=="📊 Analysis":

    st.title("📊 Clinical Gait Parameter Analysis")

    uploaded_file = st.file_uploader("Upload Reverse Walking CSV")

    if uploaded_file:

        data = pd.read_csv(uploaded_file)

        st.session_state["data"] = data

        st.subheader("Uploaded Data")
        st.dataframe(data)

        # -------- Clinical Interpretation --------

        st.subheader("🧠 Clinical Report")

        report=""

        if "walking_speed" in data.columns:
            avg_speed = data["walking_speed"].mean()

            if avg_speed < 0.7:
                report+="⚠ Slow walking speed detected.\n"
            else:
                report+="✅ Walking speed within functional range.\n"

        if "stride_length" in data.columns:
            if data["stride_length"].mean()<1:
                report+="⚠ Reduced stride length.\n"

        st.success(report)

# =================================================
# VISUALIZATION PAGE (ADVANCED)
# =================================================

elif page=="📈 Visualization":

    st.title("📈 Advanced Biomechanical Visualization")

    if "data" in st.session_state:

        data = st.session_state["data"]

        parameters = [c for c in data.columns if c!="subject"]

        # PARAMETER SELECTOR
        selected_param = st.selectbox(
            "Select parameter",
            parameters
        )

        # BAR GRAPH
        st.subheader("Multi Subject Comparison")

        fig, ax = plt.subplots()
        ax.bar(data["subject"], data[selected_param])
        ax.set_ylabel(selected_param)
        st.pyplot(fig)

        # THRESHOLD LINE GRAPH
        st.subheader("Clinical Threshold View")

        fig, ax = plt.subplots()
        ax.plot(data["subject"], data[selected_param], marker='o')

        threshold = data[selected_param].mean()
        ax.axhline(threshold, linestyle='--')

        st.pyplot(fig)

        # RADAR PLOT
        st.subheader("Radar Biomechanical Profile")

        angles = np.linspace(0,2*np.pi,len(parameters),endpoint=False)

        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)

        for i in range(len(data)):
            values=data.loc[i,parameters].tolist()
            values+=values[:1]
            ang=np.concatenate((angles,[angles[0]]))

            ax.plot(ang,values,label=data.loc[i,"subject"])

        ax.set_xticks(angles)
        ax.set_xticklabels(parameters)
        ax.legend()

        st.pyplot(fig)

        # BOXPLOT
        st.subheader("Distribution Analysis")

        fig, ax = plt.subplots()
        data[parameters].boxplot(ax=ax)
        st.pyplot(fig)

        # CORRELATION HEATMAP
        st.subheader("Correlation Heatmap")

        corr=data[parameters].corr()

        fig, ax = plt.subplots()
        cax=ax.matshow(corr)

        plt.xticks(range(len(parameters)),parameters,rotation=90)
        plt.yticks(range(len(parameters)),parameters)

        fig.colorbar(cax)

        st.pyplot(fig)

    else:
        st.warning("Upload data first in Analysis page.")

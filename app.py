import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------- PAGE NAVIGATION ----------
page = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Clinical Dashboard"]
)

# ---------- HOME PAGE ----------
if page == "Home":

    st.title("Clinical Reverse Walking Analysis System")

    st.subheader("Biomechanical and Neuromuscular Gait Analysis")

    st.write("""
    This clinical web application allows analysis of forward and reverse walking.
    It provides visualization of temporal-spatial gait parameters and joint kinematics.
    """)

    st.success("Click Clinical Dashboard from sidebar to start analysis.")

# ---------- DASHBOARD PAGE ----------
elif page == "Clinical Dashboard":

    st.title("Clinical Gait Analysis Dashboard")

    forward_file = st.file_uploader("Upload Forward Walking Data")
    reverse_file = st.file_uploader("Upload Reverse Walking Data")

    if forward_file and reverse_file:

        forward = pd.read_csv(forward_file)
        reverse = pd.read_csv(reverse_file)

        st.subheader("Walking Speed Comparison")

        fig, ax = plt.subplots()

        ax.bar(["Forward","Reverse"],
               [forward["walking_speed"].mean(),
                reverse["walking_speed"].mean()])

        st.pyplot(fig)

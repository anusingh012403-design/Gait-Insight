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

    st.subheader("Biomechanical Gait Analysis Application")

    st.write("""
    This clinical web application analyzes reverse walking gait parameters.
    Upload reverse walking datasets of multiple subjects to compare clinical metrics.
    """)

# ---------- CLINICAL DASHBOARD ----------

elif page == "Clinical Dashboard":

    st.title("Reverse Walking Subject Comparison")

    file = st.file_uploader("Upload Reverse Walking CSV")

    if file:

        data = pd.read_csv(file)

        st.subheader("Uploaded Data")
        st.dataframe(data)

        # PARAMETERS (change names if your CSV has different column names)
        parameters = [
            "walking_speed",
            "stride_lenght",
            "cadence",
            "hip_rom"
        ]

        subjects = data["subject"]

        st.subheader("Multi-Parameter Clinical Comparison")

        fig, ax = plt.subplots()

        x = range(len(parameters))

        for i, subject in enumerate(subjects):
            values = data.loc[i, parameters]
            ax.bar([p + i*0.3 for p in x], values, width=0.3, label=subject)

        ax.set_xticks(x)
        ax.set_xticklabels(parameters)

        ax.legend()

        st.pyplot(fig)

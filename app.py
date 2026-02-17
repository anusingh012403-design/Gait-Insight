import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------- PAGE NAVIGATION --------

page = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Clinical Dashboard"]
)

# -------- HOME PAGE --------

if page == "Home":

    st.title("Clinical Reverse Walking Analysis System")

    st.subheader("Biomechanical Gait Analysis Application")

    st.write("""
    This clinical web application analyzes multiple gait parameters.
    Upload forward and reverse walking datasets to compare clinical metrics.
    """)

# -------- CLINICAL DASHBOARD --------

elif page == "Clinical Dashboard":

    st.title("Clinical Gait Parameter Analysis")

    # Upload files
    forward_file = st.file_uploader("Upload Forward Walking CSV")
    reverse_file = st.file_uploader("Upload Reverse Walking CSV")

    if forward_file and reverse_file:

        forward = pd.read_csv(forward_file)
        reverse = pd.read_csv(reverse_file)

        # PARAMETERS (change according to your CSV columns)
        parameters = [
            "walking_speed",
            "cadence",
            "step_length",
            "stride_time"
        ]

        results = []

        for p in parameters:
            f_val = forward[p].mean()
            r_val = reverse[p].mean()

            results.append([p, f_val, r_val])

        result_df = pd.DataFrame(
            results,
            columns=["Parameter","Forward","Reverse"]
        )

        # -------- TABLE --------

        st.subheader("Clinical Parameter Table")

        st.dataframe(result_df)

        # -------- GRAPH --------

        st.subheader("Multi Parameter Analysis Graph")

        fig, ax = plt.subplots()

        x = range(len(parameters))

        ax.bar(x, result_df["Forward"], label="Forward")
        ax.bar(x, result_df["Reverse"], label="Reverse")

        ax.set_xticks(x)
        ax.set_xticklabels(parameters, rotation=45)

        ax.legend()

        st.pyplot(fig)

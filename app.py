import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="Reverse Walking Clinical Platform",
    layout="wide",
    page_icon="🧬"
)

# ================= SIDEBAR =================

st.sidebar.title("🏥 Clinical Gait System")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📂 Upload & Analysis",
        "📊 Visualization Lab",
        "📡 Live Monitoring",
        "📑 Clinical Report"
    ]
)

# ================= HOME PAGE =================

if page == "🏠 Home":

    st.title("🚶 Reverse Walking Clinical Analysis Platform")
    st.subheader("Hospital-Level Biomedical Gait + EMG Analysis")

    st.markdown("""
    ✅ Reverse walking biomechanics  
    ✅ Joint ROM analysis  
    ✅ EMG muscle activation analysis  
    ✅ Clinical alerts system  
    ✅ Advanced visualization lab  
    ✅ Live monitoring simulation  
    """)

# ================= UPLOAD PAGE =================

elif page == "📂 Upload & Analysis":

    st.title("Upload Gait + EMG CSV")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.session_state["data"] = df
        st.success("Data uploaded successfully")
        st.dataframe(df)

        # ===== Clinical Alerts =====

        st.subheader("Clinical Alerts")

        def alert(val, low, high):
            if val < low:
                return "🔴 High Risk"
            elif val > high:
                return "🟡 Monitor"
            else:
                return "🟢 Normal"

        for i,row in df.iterrows():

            st.write(
                row["subject"],
                alert(row["walking_speed"],0.8,1.5),
                alert(row["hip_rom"],30,50)
            )

# ================= VISUALIZATION LAB =================

elif page == "📊 Visualization Lab":

    st.title("Advanced Gait + EMG Visualization")

    if "data" in st.session_state:

        df = st.session_state["data"]

        # BAR chart
        st.subheader("Parameter Comparison")
        fig = px.bar(df, x="subject", y=[
            "walking_speed","stride_length","cadence"
        ])
        st.plotly_chart(fig, use_container_width=True)

        # RADAR chart
        st.subheader("ROM Radar")

        for i,row in df.iterrows():
            radar = go.Figure()

            radar.add_trace(go.Scatterpolar(
                r=[
                    row["hip_rom"],
                    row["knee_rom"],
                    row["ankle_rom"]
                ],
                theta=["Hip","Knee","Ankle"],
                fill='toself',
                name=row["subject"]
            ))

            st.plotly_chart(radar)

        # EMG Visualization
        st.subheader("EMG Muscle Activation")

        emg_cols = ["emg_quad","emg_hamstring","emg_ta","emg_gastro"]

        if all(col in df.columns for col in emg_cols):

            fig2 = px.line(df, x="subject", y=emg_cols)
            st.plotly_chart(fig2, use_container_width=True)

        # BOX plot
        st.subheader("Distribution Analysis")
        st.plotly_chart(px.box(df,y=df.columns[1:]))

        # SCATTER matrix
        st.subheader("Correlation Matrix")
        st.plotly_chart(px.scatter_matrix(df))

    else:
        st.warning("Upload data first")

# ================= LIVE MONITORING =================

elif page == "📡 Live Monitoring":

    st.title("Live Gait + EMG Simulation")

    chart = st.line_chart()

    for i in range(50):

        new_data = pd.DataFrame(
            np.random.randn(1,3),
            columns=["EMG","Speed","ROM"]
        )

        chart.add_rows(new_data)
        time.sleep(0.1)

# ================= CLINICAL REPORT =================

elif page == "📑 Clinical Report":

    st.title("Automated Clinical Report Generator")

    if "data" in st.session_state:

        df = st.session_state["data"]

        name = st.text_input("Patient Name")
        age = st.number_input("Age",0,100)
        diagnosis = st.text_input("Diagnosis")

        if st.button("Generate Clinical Interpretation"):

            st.subheader("Clinical Interpretation")

            avg_speed = df["walking_speed"].mean()
            avg_hip = df["hip_rom"].mean()

            st.write(f"Patient: {name}")
            st.write(f"Age: {age}")

            if avg_speed < 1:
                st.error("Reduced walking speed detected")
            else:
                st.success("Walking speed within functional range")

            if avg_hip < 35:
                st.warning("Hip ROM limitation observed")

            if "emg_quad" in df.columns:
                st.write("EMG muscle activation included in analysis.")

    else:
        st.warning("Upload data first")

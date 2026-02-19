import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="Reverse Walking Clinical Platform",
    page_icon="🚶",
    layout="wide"
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
        "🧾 Clinical Report"
    ]
)

# ================= HOME =================

if page == "🏠 Home":

    st.title("🚶 Reverse Walking Clinical Analysis Platform")

    st.subheader("Hospital-Level Biomedical Gait Analysis System")

    st.markdown("""
    ✅ Reverse walking biomechanics  
    ✅ Joint ROM analysis  
    ✅ Clinical alerts system  
    ✅ Advanced visualization  
    ✅ Live monitoring simulation  
    """)

# ================= UPLOAD =================

elif page == "📂 Upload & Analysis":

    st.header("Upload Patient CSV")

    file = st.file_uploader("Upload gait CSV")

    if file:
        data = pd.read_csv(file)
        st.session_state["data"] = data
        st.success("Data uploaded successfully")
        st.dataframe(data)

# ================= VISUALIZATION =================

elif page == "📊 Visualization Lab":

    st.header("Advanced Visualization")

    if "data" not in st.session_state:
        st.warning("Upload data first")

    else:

        data = st.session_state["data"]

        parameters = [
            "walking_speed",
            "stride_length",
            "cadence",
            "hip_rom",
            "knee_rom",
            "ankle_rom"
        ]

        param = st.selectbox("Select Parameter", parameters)

        # Bar chart
        bar = px.bar(data, x="subject", y=param, color="subject")
        st.plotly_chart(bar, use_container_width=True)

        # Radar chart
        radar = go.Figure()

        for i in range(len(data)):
            radar.add_trace(go.Scatterpolar(
                r=data.loc[i, parameters],
                theta=parameters,
                fill='toself',
                name=data.loc[i,"subject"]
            ))

        st.plotly_chart(radar, use_container_width=True)

        # Heatmap
        heat = px.imshow(data[parameters])
        st.plotly_chart(heat, use_container_width=True)

# ================= LIVE MONITORING =================

elif page == "📡 Live Monitoring":

    st.header("Live Gait Monitoring (Simulation)")

    chart = st.empty()

    x = []
    y = []

    for i in range(50):

        x.append(i)
        y.append(np.sin(i/3) + np.random.normal(0,0.1))

        fig = px.line(x=x, y=y, labels={"x":"Time","y":"Gait Signal"})
        chart.plotly_chart(fig, use_container_width=True)

        time.sleep(0.1)

# ================= CLINICAL REPORT =================

elif page == "🧾 Clinical Report":

    st.header("Automated Clinical Report")

    if "data" not in st.session_state:
        st.warning("Upload data first")

    else:

        data = st.session_state["data"]

        col1,col2 = st.columns(2)

        with col1:
            name = st.text_input("Patient Name")
            age = st.number_input("Age")
        with col2:
            gender = st.selectbox("Gender",["Male","Female"])
            diagnosis = st.text_input("Diagnosis")

        if st.button("Generate Clinical Report"):

            st.subheader("Patient Information")

            st.write(f"Name: {name}")
            st.write(f"Age: {age}")
            st.write(f"Gender: {gender}")
            st.write(f"Diagnosis: {diagnosis}")

            st.subheader("Gait Parameters")

            st.dataframe(data)

            st.subheader("Clinical Alerts")

            for i in range(len(data)):

                subject = data.loc[i,"subject"]
                speed = data.loc[i,"walking_speed"]

                if speed < 0.8:
                    st.error(f"{subject}: LOW walking speed")
                elif speed < 1.1:
                    st.warning(f"{subject}: Moderate performance")
                else:
                    st.success(f"{subject}: Normal performance")

            st.subheader("Clinical Interpretation")

            st.write("""
            Reverse walking analysis indicates biomechanical performance.
            Reduced speed or ROM values may indicate neuromuscular or rehabilitation needs.
            """)

            csv = data.to_csv(index=False)

            st.download_button(
                "Download Clinical Report",
                csv,
                "clinical_report.csv",
                "text/csv"
            )

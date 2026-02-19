import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Reverse Walking Clinical Analysis",
    page_icon="🧠",
    layout="wide"
)

# ================= SIDEBAR =================
st.sidebar.title("🏥 Clinical Gait System")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home",
     "📤 Upload & Analysis",
     "📊 Visualization Lab",
     "📡 Live Monitoring",
     "📄 Clinical Report"]
)

# ================= HOME PAGE =================
if page == "🏠 Home":

    st.title("🚶 Reverse Walking Clinical Analysis Platform")
    st.subheader("Advanced Biomedical Gait Assessment System")

    st.markdown("""
    Hospital-grade clinical system for:
    - Reverse walking evaluation  
    - Joint ROM assessment  
    - Clinical risk alerts  
    - Automated reporting  
    - Rehabilitation monitoring  
    """)

    st.image(
        "https://images.unsplash.com/photo-1581091870627-3f89f0d2d3f9",
        use_container_width=True
    )

    st.success("Use sidebar to start clinical workflow.")

# ================= UPLOAD PAGE =================
elif page == "📤 Upload & Analysis":

    st.title("📤 Upload Patient Reverse Walking Data")

    uploaded_file = st.file_uploader("Upload CSV File")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.subheader("📋 Uploaded Data")
        st.dataframe(df)

        st.session_state["data"] = df

        # ===== METRIC CARDS =====
        st.subheader("📈 Key Clinical Metrics")

        col1, col2, col3 = st.columns(3)

        col1.metric("Walking Speed (m/s)", round(df["walking_speed"].mean(),2))
        col2.metric("Stride Length (m)", round(df["stride_length"].mean(),2))
        col3.metric("Cadence (steps/min)", round(df["cadence"].mean(),2))

        col4, col5, col6 = st.columns(3)

        col4.metric("Hip ROM (°)", round(df["hip_rom"].mean(),2))
        col5.metric("Knee ROM (°)", round(df["knee_rom"].mean(),2))
        col6.metric("Ankle ROM (°)", round(df["ankle_rom"].mean(),2))

        # ===== CLINICAL ALERT SYSTEM =====
        st.subheader("🚨 Clinical Risk Alert")

        speed = df["walking_speed"].mean()

        if speed < 0.6:
            st.error("🔴 High Risk – Abnormal Walking Speed")
        elif speed < 0.9:
            st.warning("🟡 Moderate Risk – Borderline Speed")
        else:
            st.success("🟢 Normal Walking Speed")

# ================= VISUALIZATION PAGE =================
elif page == "📊 Visualization Lab":

    st.title("📊 Advanced Gait Visualization")

    if "data" in st.session_state:

        df = st.session_state["data"]

        # Bar Chart
        st.subheader("📊 Multi-Parameter Comparison")

        fig = px.bar(
            df,
            x="subject",
            y=["walking_speed","stride_length","cadence"],
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Radar Chart
        st.subheader("🕸 ROM Radar Analysis")

        categories = ["hip_rom","knee_rom","ankle_rom"]

        for i in range(len(df)):
            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=df.loc[i, categories].values,
                theta=categories,
                fill='toself',
                name=df.loc[i,"subject"]
            ))

            fig.update_layout(polar=dict(radialaxis=dict(visible=True)))
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Upload data first.")

# ================= LIVE MONITORING PAGE =================
elif page == "📡 Live Monitoring":

    st.title("📡 Live Gait Monitoring Simulation")

    chart = st.line_chart(np.random.randn(10,1))

    for i in range(50):
        new_data = np.random.randn(1,1)
        chart.add_rows(new_data)
        time.sleep(0.1)

    st.success("Live Simulation Complete")

# ================= CLINICAL REPORT PAGE =================
elif page == "📄 Clinical Report":

    st.title("📄 Automated Clinical Report")

    if "data" in st.session_state:

        df = st.session_state["data"]

        name = st.text_input("Patient Name")
        age = st.number_input("Age", 1, 100)
        gender = st.selectbox("Gender", ["Male","Female"])
        diagnosis = st.text_input("Diagnosis")

        if st.button("Generate Report"):

            speed = df["walking_speed"].mean()
            stride = df["stride_length"].mean()
            cadence = df["cadence"].mean()
            hip = df["hip_rom"].mean()
            knee = df["knee_rom"].mean()
            ankle = df["ankle_rom"].mean()

            st.subheader("📋 Clinical Interpretation")

            st.write(f"Patient: {name}")
            st.write(f"Age: {age}")
            st.write(f"Gender: {gender}")
            st.write(f"Diagnosis: {diagnosis}")

            st.write("---- Gait Summary ----")

            st.write(f"Average Walking Speed: {round(speed,2)} m/s")
            st.write(f"Average Stride Length: {round(stride,2)} m")
            st.write(f"Average Cadence: {round(cadence,2)} steps/min")
            st.write(f"Hip ROM: {round(hip,2)}°")
            st.write(f"Knee ROM: {round(knee,2)}°")
            st.write(f"Ankle ROM: {round(ankle,2)}°")

            # PDF GENERATION
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200,10,"Reverse Walking Clinical Report",ln=True)

            pdf.cell(200,10,f"Name: {name}",ln=True)
            pdf.cell(200,10,f"Age: {age}",ln=True)
            pdf.cell(200,10,f"Gender: {gender}",ln=True)
            pdf.cell(200,10,f"Diagnosis: {diagnosis}",ln=True)

            pdf.cell(200,10,f"Walking Speed: {round(speed,2)} m/s",ln=True)
            pdf.cell(200,10,f"Stride Length: {round(stride,2)} m",ln=True)
            pdf.cell(200,10,f"Cadence: {round(cadence,2)} steps/min",ln=True)
            pdf.cell(200,10,f"Hip ROM: {round(hip,2)}°",ln=True)
            pdf.cell(200,10,f"Knee ROM: {round(knee,2)}°",ln=True)
            pdf.cell(200,10,f"Ankle ROM: {round(ankle,2)}°",ln=True)

            pdf.output("clinical_report.pdf")

            with open("clinical_report.pdf","rb") as f:
                st.download_button("📥 Download PDF Report", f, "clinical_report.pdf")

    else:
        st.warning("Upload patient data first.")

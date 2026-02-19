import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Clinical Reverse Walking System",
    page_icon="🏥",
    layout="wide"
)

# ------------------ SIDEBAR ------------------
st.sidebar.title("🏥 Clinical Gait System")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home",
     "📤 Upload & Analysis",
     "📊 Visualization",
     "📡 Live Monitoring",
     "📑 Clinical Report"]
)

# ------------------ SESSION STORAGE ------------------
if "data" not in st.session_state:
    st.session_state.data = None

if "patient_info" not in st.session_state:
    st.session_state.patient_info = {}

# =====================================================
# 🏠 HOME PAGE
# =====================================================
if page == "🏠 Home":

    st.title("🚶 Reverse Walking Clinical Analysis Platform")

    col1, col2 = st.columns([1.2,1])

    with col1:
        st.markdown("""
        ### Advanced Biomedical Gait Analysis System

        Hospital-grade platform designed for:

        ✅ Reverse walking biomechanics  
        ✅ Motion capture assessment  
        ✅ Rehabilitation monitoring  
        ✅ Clinical risk interpretation  
        ✅ Automated report generation  

        This system analyzes gait CSV files and generates professional clinical insights.
        """)

        st.success("Use the sidebar to begin clinical workflow.")

    with col2:
        st.image(
            "https://images.unsplash.com/photo-1580281658629-1a0e9cb9a1c3",
            use_column_width=True
        )

    st.markdown("---")

    st.subheader("🚨 Clinical Risk Classification")

    st.info("""
    🟢 Green → Normal gait  
    🟡 Yellow → Moderate deviation  
    🔴 Red → High clinical concern
    """)

# =====================================================
# 📤 UPLOAD & ANALYSIS
# =====================================================
elif page == "📤 Upload & Analysis":

    st.title("📤 Upload Patient Reverse Walking Data")

    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("Patient Name")

    with col2:
        age = st.number_input("Age", 1, 100)

    with col3:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    uploaded_file = st.file_uploader("Upload Reverse Walking CSV")

    if uploaded_file:

        data = pd.read_csv(uploaded_file)
        st.session_state.data = data
        st.session_state.patient_info = {
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Date": datetime.now().strftime("%d-%m-%Y")
        }

        st.subheader("Uploaded Data Preview")
        st.dataframe(data)

        st.markdown("---")
        st.subheader("🚨 Clinical Alerts")

        if "walking_speed" in data.columns:

            speed = data["walking_speed"].mean()

            if speed < 0.7:
                st.error("🔴 HIGH RISK: Slow gait detected — Clinical attention required")

            elif speed < 1.0:
                st.warning("🟡 MODERATE RISK: Gait below optimal range")

            else:
                st.success("🟢 NORMAL: Healthy walking speed detected")

# =====================================================
# 📊 VISUALIZATION
# =====================================================
elif page == "📊 Visualization":

    st.title("📊 Gait Visualization Dashboard")

    if st.session_state.data is not None:

        data = st.session_state.data

        numeric_cols = data.select_dtypes(include=np.number).columns

        selected = st.multiselect(
            "Select parameters to visualize",
            numeric_cols,
            default=list(numeric_cols)
        )

        if selected:

            fig = px.bar(
                data,
                x="subject" if "subject" in data.columns else data.index,
                y=selected,
                barmode="group",
                title="Multi-Parameter Comparison"
            )
            st.plotly_chart(fig, use_container_width=True)

            # Radar Chart
            st.subheader("🔵 Radar Biomechanical Profile")

            categories = selected

            fig2 = go.Figure()

            for i in range(len(data)):
                fig2.add_trace(go.Scatterpolar(
                    r=data.loc[i, selected].values,
                    theta=categories,
                    fill='toself',
                    name=str(data.loc[i, "subject"]) if "subject" in data.columns else f"Subject {i+1}"
                ))

            fig2.update_layout(polar=dict(radialaxis=dict(visible=True)))
            st.plotly_chart(fig2, use_container_width=True)

    else:
        st.warning("Please upload data first.")

# =====================================================
# 📡 LIVE MONITORING
# =====================================================
elif page == "📡 Live Monitoring":

    st.title("📡 Live Gait Monitoring Simulation")

    chart = st.line_chart()

    for i in range(30):
        new_data = np.random.randn(1,1)
        chart.add_rows(new_data)

    st.success("Live monitoring simulation running...")

# =====================================================
# 📑 CLINICAL REPORT
# =====================================================
elif page == "📑 Clinical Report":

    st.title("📑 Clinical Report Generator")

    if st.session_state.data is not None:

        data = st.session_state.data
        info = st.session_state.patient_info

        st.subheader("Patient Information")
        st.write(info)

        st.subheader("Clinical Interpretation")

        interpretation = ""

        if "walking_speed" in data.columns:
            speed = data["walking_speed"].mean()

            if speed < 0.7:
                interpretation += "Patient shows reduced walking speed indicating possible neuromuscular weakness.\n"
            elif speed < 1.0:
                interpretation += "Patient gait slightly below optimal range; monitoring recommended.\n"
            else:
                interpretation += "Walking speed within normal biomechanical range.\n"

        if "stride_length" in data.columns:
            stride = data["stride_length"].mean()
            interpretation += f"Average stride length recorded: {stride:.2f} m.\n"

        st.text(interpretation)

        report_text = f"""
        REVERSE WALKING CLINICAL REPORT
        --------------------------------
        Name: {info.get("Name")}
        Age: {info.get("Age")}
        Gender: {info.get("Gender")}
        Date: {info.get("Date")}

        Clinical Interpretation:
        {interpretation}
        """

        st.download_button(
            label="📥 Download Clinical Report",
            data=report_text,
            file_name="Clinical_Report.txt"
        )

    else:
        st.warning("Upload patient data first.")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Clinical Reverse Walking Platform",
    page_icon="🏥",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🏥 Clinical Gait System")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home",
     "📤 Upload & Analysis",
     "📊 Visualization",
     "📡 Live Monitoring",
     "📑 Clinical Report"]
)

# ---------------- SESSION STATE ----------------
if "data" not in st.session_state:
    st.session_state.data = None

if "patient" not in st.session_state:
    st.session_state.patient = {}

# ===================================================
# 🏠 HOME
# ===================================================
if page == "🏠 Home":

    col1, col2 = st.columns([1.2,1])

    with col1:
        st.title("🚶 Reverse Walking Clinical Analysis Platform")

        st.markdown("""
        ### Hospital-grade Biomedical Gait Analysis

        ✔ Motion capture clinical evaluation  
        ✔ Reverse walking biomechanical analysis  
        ✔ Clinical risk prediction  
        ✔ Automated interpretation  
        ✔ Research-grade visualization  

        Designed for rehabilitation, biomechanics and clinical research.
        """)

    with col2:
        st.image(
            "https://images.unsplash.com/photo-1580281658629-1a0e9cb9a1c3",
            use_column_width=True
        )

    st.markdown("---")

    st.subheader("🚨 Clinical Alert System")

    st.success("🟢 GREEN — Normal gait")
    st.warning("🟡 YELLOW — Moderate deviation")
    st.error("🔴 RED — High risk clinical gait")

# ===================================================
# 📤 UPLOAD & ANALYSIS
# ===================================================
elif page == "📤 Upload & Analysis":

    st.title("📤 Upload Patient Reverse Walking Data")

    col1,col2,col3 = st.columns(3)

    with col1:
        name = st.text_input("Patient Name")

    with col2:
        age = st.number_input("Age",1,100)

    with col3:
        gender = st.selectbox("Gender",["Male","Female","Other"])

    file = st.file_uploader("Upload CSV")

    if file:

        data = pd.read_csv(file)
        st.session_state.data = data

        st.session_state.patient = {
            "Name":name,
            "Age":age,
            "Gender":gender,
            "Date":datetime.now().strftime("%d-%m-%Y")
        }

        st.dataframe(data)

        # -------- CLINICAL ALERT --------
        if "walking_speed" in data.columns:

            speed = data["walking_speed"].mean()

            if speed < 0.7:
                st.error("🔴 HIGH RISK — Slow gait detected")

            elif speed < 1.0:
                st.warning("🟡 Moderate deviation")

            else:
                st.success("🟢 Normal gait")

        # -------- SYMMETRY INDEX --------
        if "left_step" in data.columns and "right_step" in data.columns:

            sym = abs(data["left_step"].mean() - data["right_step"].mean())

            st.info(f"Symmetry Index: {sym:.3f}")

# ===================================================
# 📊 VISUALIZATION
# ===================================================
elif page == "📊 Visualization":

    st.title("📊 Clinical Visualization Dashboard")

    if st.session_state.data is not None:

        data = st.session_state.data

        numeric = data.select_dtypes(include=np.number).columns

        selected = st.multiselect("Select Parameters",numeric,default=list(numeric))

        if selected:

            fig = px.bar(
                data,
                x="subject" if "subject" in data.columns else data.index,
                y=selected,
                barmode="group",
                title="Multi-Parameter Comparison"
            )
            st.plotly_chart(fig,use_container_width=True)

            # Radar Chart
            st.subheader("Radar Biomechanical Analysis")

            fig2 = go.Figure()

            for i in range(len(data)):
                fig2.add_trace(go.Scatterpolar(
                    r=data.loc[i,selected],
                    theta=selected,
                    fill="toself",
                    name=str(data.loc[i,"subject"]) if "subject" in data.columns else f"S{i+1}"
                ))

            st.plotly_chart(fig2,use_container_width=True)

    else:
        st.warning("Upload data first.")

# ===================================================
# 📡 LIVE MONITORING
# ===================================================
elif page == "📡 Live Monitoring":

    st.title("📡 Live Gait Monitoring Simulation")

    chart = st.line_chart()

    for i in range(40):
        chart.add_rows(np.random.randn(1,1))

    st.success("Real-time monitoring simulation active.")

# ===================================================
# 📑 CLINICAL REPORT
# ===================================================
elif page == "📑 Clinical Report":

    st.title("📑 Automated Clinical Report")

    if st.session_state.data is not None:

        data = st.session_state.data
        patient = st.session_state.patient

        st.subheader("Patient Info")
        st.write(patient)

        interpretation=""

        if "walking_speed" in data.columns:

            speed = data["walking_speed"].mean()

            if speed <0.7:
                interpretation+="Slow walking speed suggests neuromuscular deficit.\n"
            elif speed<1.0:
                interpretation+="Moderate gait deviation observed.\n"
            else:
                interpretation+="Normal walking speed.\n"

        if "stride_length" in data.columns:
            interpretation+=f"Average stride length: {data['stride_length'].mean():.2f} m.\n"

        st.subheader("Clinical Interpretation")
        st.text(interpretation)

        report=f"""
        REVERSE WALKING CLINICAL REPORT
        --------------------------------
        Name: {patient.get("Name")}
        Age: {patient.get("Age")}
        Gender: {patient.get("Gender")}
        Date: {patient.get("Date")}

        Interpretation:
        {interpretation}
        """

        st.download_button(
            "📥 Download Report",
            report,
            "Clinical_Report.txt"
        )

    else:
        st.warning("Upload patient data first.")

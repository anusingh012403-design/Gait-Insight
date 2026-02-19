import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import random
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Clinical Reverse Walking System",
    page_icon="🧬",
    layout="wide"
)

# ================= SIDEBAR =================
st.sidebar.title("🧬 Clinical Gait System")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📤 Upload & Analysis",
        "📊 Visualization",
        "📡 Live Monitoring",
        "📄 Clinical Report"
    ]
)

# ================= HOME =================
if page == "🏠 Home":
    st.title("🚶 Reverse Walking Clinical Analysis Platform")

    st.markdown("""
    ### GOD-MODE Biomedical Dashboard

    A hospital-grade clinical gait analysis system designed for  
    **research, rehabilitation & biomechanical assessment**

    #### Key Capabilities:
    ✅ AI-style clinical interpretation  
    ✅ Multi-subject biomechanical comparison  
    ✅ Radar gait visualization  
    ✅ Live gait monitoring simulation  
    ✅ Downloadable clinical report
    """)

    st.info("Use the sidebar to start clinical analysis workflow.")

# ================= UPLOAD =================
elif page == "📤 Upload & Analysis":
    st.title("📤 Upload Patient Gait CSV")

    file = st.file_uploader("Upload Reverse Walking CSV", type=["csv"])

    if file:
        data = pd.read_csv(file)
        st.session_state["data"] = data

        st.success("Patient data uploaded successfully")
        st.subheader("Uploaded Data")
        st.dataframe(data)

# ================= VISUALIZATION =================
elif page == "📊 Visualization":
    st.title("📊 Advanced Gait Visualization")

    if "data" not in st.session_state:
        st.warning("Upload data first.")
    else:
        data = st.session_state["data"]
        numeric_cols = data.select_dtypes(include="number").columns

        param = st.selectbox("Select Parameter", numeric_cols)

        fig = px.bar(
            data,
            x="subject",
            y=param,
            color="subject",
            title=f"{param} Comparison"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🧠 Biomechanical Radar Analysis")

        radar_fig = go.Figure()
        for i in range(len(data)):
            radar_fig.add_trace(go.Scatterpolar(
                r=data.loc[i, numeric_cols],
                theta=numeric_cols,
                fill='toself',
                name=data.loc[i, "subject"]
            ))

        radar_fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=True
        )

        st.plotly_chart(radar_fig, use_container_width=True)

# ================= LIVE MONITORING =================
elif page == "📡 Live Monitoring":
    st.title("📡 Live Gait Monitoring (Simulation)")

    placeholder = st.empty()
    values = []

    for i in range(40):
        values.append(random.uniform(0.6, 1.4))
        fig = px.line(values, title="Real-time Walking Speed")
        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.2)

# ================= CLINICAL REPORT =================
elif page == "📄 Clinical Report":
    st.title("📄 Automatic Clinical Report")

    if "data" not in st.session_state:
        st.warning("Upload data first.")
    else:
        data = st.session_state["data"]

        avg_speed = data["walking_speed"].mean()

        if avg_speed < 0.7:
            status = "Reduced gait speed detected"
            risk = "High Risk"
        elif avg_speed < 1.0:
            status = "Moderate gait performance"
            risk = "Moderate Risk"
        else:
            status = "Normal gait pattern"
            risk = "Low Risk"

        st.success("Clinical Interpretation Generated")

        st.markdown(f"""
        ### 🧠 Clinical Summary

        - Average Walking Speed: **{avg_speed:.2f} m/s**
        - Gait Status: **{status}**
        - Risk Level: **{risk}**

        **Clinical Recommendation**
        • Continue gait monitoring  
        • Assess ROM parameters  
        • Consider rehabilitation protocol if needed
        """)

        # ===== PDF GENERATION =====
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Clinical Gait Analysis Report", ln=True)
        pdf.ln(5)
        pdf.cell(200, 10, txt=f"Average Walking Speed: {avg_speed:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Gait Status: {status}", ln=True)
        pdf.cell(200, 10, txt=f"Risk Level: {risk}", ln=True)

        pdf.output("clinical_report.pdf")

        with open("clinical_report.pdf", "rb") as f:
            st.download_button(
                "⬇️ Download Clinical Report (PDF)",
                f,
                file_name="Clinical_Gait_Report.pdf"
            )

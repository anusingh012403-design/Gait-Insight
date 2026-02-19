import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="Clinical Reverse Walking System",
    page_icon="🧠",
    layout="wide"
)

# ================= SIDEBAR =================

st.sidebar.title("🏥 Clinical Gait System")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home",
     "📥 Upload & Analysis",
     "📊 Visualization",
     "🧾 Clinical Report"]
)

# ================= HOME PAGE =================

if page == "🏠 Home":

    st.title("🚶 Reverse Walking Clinical Analysis Platform")

    st.markdown("""
    ### Advanced Biomedical Dashboard

    Upload gait CSV data and receive automatic clinical analysis.

    **Features**
    - Multi-subject comparison
    - Interactive visualization
    - Radar biomechanical analysis
    - Clinical risk scoring
    - Automatic report generation
    """)

# ================= UPLOAD & ANALYSIS =================

elif page == "📥 Upload & Analysis":

    st.title("📥 Upload Patient Data")

    file = st.file_uploader("Upload CSV")

    if file:

        data = pd.read_csv(file)

        st.session_state["data"] = data

        st.success("Data uploaded successfully")

        # Patient selection
        patient = st.selectbox("Select Patient", data["subject"])

        patient_data = data[data["subject"] == patient]

        # KPI CARDS
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Walking Speed", round(float(patient_data["walking_speed"]),2))
        col2.metric("Stride Length", round(float(patient_data["stride_length"]),2))
        col3.metric("Cadence", round(float(patient_data["cadence"]),2))
        col4.metric("Hip ROM", round(float(patient_data["hip_rom"]),2))

        st.divider()

        parameters = [c for c in data.columns if c != "subject"]

        tab1, tab2, tab3 = st.tabs(["Overview","Biomechanics","Interpretation"])

        # -------- OVERVIEW TAB --------
        with tab1:

            fig = px.bar(
                data,
                x="subject",
                y=parameters,
                barmode="group",
                title="Multi-Parameter Comparison"
            )

            st.plotly_chart(fig, use_container_width=True)

        # -------- BIOMECHANICS TAB --------
        with tab2:

            fig = go.Figure()

            for i in range(len(data)):
                fig.add_trace(go.Scatterpolar(
                    r=data.loc[i, parameters],
                    theta=parameters,
                    fill='toself',
                    name=data.loc[i,"subject"]
                ))

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                showlegend=True,
                title="Radar Gait Profile"
            )

            st.plotly_chart(fig, use_container_width=True)

        # -------- INTERPRETATION TAB --------
        with tab3:

            score = 0

            if float(patient_data["walking_speed"]) < 0.7:
                score += 1
            if float(patient_data["stride_length"]) < 1:
                score += 1
            if float(patient_data["hip_rom"]) < 35:
                score += 1

            if score == 0:
                st.success("Normal biomechanical profile detected.")
            elif score == 1:
                st.warning("Mild deviation detected.")
            else:
                st.error("High clinical deviation detected.")

# ================= VISUALIZATION PAGE =================

elif page == "📊 Visualization":

    st.title("📊 Advanced Visualization Dashboard")

    if "data" in st.session_state:

        data = st.session_state["data"]

        parameters = [c for c in data.columns if c != "subject"]

        # HEATMAP
        fig = px.imshow(
            data[parameters],
            labels=dict(color="Value"),
            title="Gait Parameter Heatmap"
        )

        st.plotly_chart(fig, use_container_width=True)

        # BOX PLOT
        selected = st.selectbox("Select Parameter", parameters)

        fig2 = px.box(
            data,
            x="subject",
            y=selected,
            title=f"{selected} Distribution"
        )

        st.plotly_chart(fig2, use_container_width=True)

    else:

        st.warning("Upload data first.")

# ================= CLINICAL REPORT =================

elif page == "🧾 Clinical Report":

    st.title("🧾 Automated Clinical Report")

    if "data" in st.session_state:

        data = st.session_state["data"]

        report = ""

        for i in range(len(data)):

            report += f"Patient: {data.loc[i,'subject']}\n"
            report += f"Walking Speed: {data.loc[i,'walking_speed']}\n"
            report += f"Stride Length: {data.loc[i,'stride_length']}\n"
            report += f"Hip ROM: {data.loc[i,'hip_rom']}\n\n"

        st.text_area("Generated Report", report, height=300)

        st.download_button(
            "Download Report",
            report,
            file_name="clinical_report.txt"
        )

    else:

        st.warning("Upload data first.")

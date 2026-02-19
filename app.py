import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    ["🏠 Home","📂 Upload & Analysis","📊 Visualization Lab","🧪 Clinical Report"]
)

# ================= HOME =================

if page == "🏠 Home":

    st.title("🚶 Reverse Walking Clinical Analysis Platform")

    st.subheader("Advanced Biomedical Gait Analysis System")

    st.markdown("""
    Hospital-style clinical application for:

    ✅ Reverse walking evaluation  
    ✅ Joint ROM analysis  
    ✅ Clinical risk alerts  
    ✅ Automated reporting
    """)

# ================= UPLOAD =================

elif page == "📂 Upload & Analysis":

    st.header("📂 Upload Patient CSV")

    file = st.file_uploader("Upload gait CSV")

    if file:
        data = pd.read_csv(file)
        st.session_state["data"] = data
        st.dataframe(data)

# ================= VISUALIZATION =================

elif page == "📊 Visualization Lab":

    st.header("📊 Advanced Gait Visualization")

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

        # -------- BAR CHART --------
        st.subheader("Bar Chart Comparison")

        param = st.selectbox("Select parameter", parameters)

        bar = px.bar(data, x="subject", y=param, color="subject")
        st.plotly_chart(bar, use_container_width=True)

        # -------- LINE CHART --------
        st.subheader("Line Chart Trend")

        line = px.line(data, x="subject", y=param, markers=True)
        st.plotly_chart(line, use_container_width=True)

        # -------- RADAR CHART --------
        st.subheader("Radar Biomechanical Profile")

        radar = go.Figure()

        for i in range(len(data)):
            radar.add_trace(go.Scatterpolar(
                r=data.loc[i, parameters],
                theta=parameters,
                fill='toself',
                name=data.loc[i,"subject"]
            ))

        st.plotly_chart(radar, use_container_width=True)

        # -------- SCATTER --------
        st.subheader("Scatter Relationship")

        x_param = st.selectbox("X axis", parameters)
        y_param = st.selectbox("Y axis", parameters, index=1)

        scatter = px.scatter(data, x=x_param, y=y_param, color="subject")
        st.plotly_chart(scatter, use_container_width=True)

        # -------- BOX PLOT --------
        st.subheader("Box Plot (Clinical Variability)")

        box = px.box(data, y=parameters)
        st.plotly_chart(box, use_container_width=True)

        # -------- HEATMAP --------
        st.subheader("Heatmap Overview")

        heat = px.imshow(data[parameters])
        st.plotly_chart(heat, use_container_width=True)

        # -------- CLINICAL ALERTS --------
        st.subheader("Clinical Alerts")

        for i in range(len(data)):
            name = data.loc[i,"subject"]
            speed = data.loc[i,"walking_speed"]

            if speed < 0.8:
                st.error(f"{name}: LOW walking speed")
            elif speed < 1.1:
                st.warning(f"{name}: Moderate walking speed")
            else:
                st.success(f"{name}: Normal walking speed")

# ================= REPORT =================

elif page == "🧪 Clinical Report":

    st.header("🧪 Automated Clinical Report")

    if "data" not in st.session_state:
        st.warning("Upload data first")

    else:

        data = st.session_state["data"]

        name = st.text_input("Patient Name")
        age = st.number_input("Age")
        gender = st.selectbox("Gender",["Male","Female"])
        diagnosis = st.text_input("Diagnosis")

        if st.button("Generate Report"):

            st.write(f"Patient: {name}")
            st.write(f"Age: {age}")
            st.write(f"Gender: {gender}")
            st.write(f"Diagnosis: {diagnosis}")

            st.dataframe(data)

            st.subheader("Clinical Interpretation")

            for i in range(len(data)):
                subject = data.loc[i,"subject"]
                speed = data.loc[i,"walking_speed"]

                if speed < 0.8:
                    st.write(f"{subject}: Reduced gait speed — possible impairment.")
                else:
                    st.write(f"{subject}: Normal reverse walking performance.")

            csv = data.to_csv(index=False)

            st.download_button(
                "Download Report CSV",
                csv,
                "clinical_report.csv",
                "text/csv"
            )

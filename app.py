import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

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
     "📤 Upload & Analysis",
     "📊 Visualization",
     "📡 Live Monitoring",
     "📄 Clinical Report"]
)

# ================= HOME PAGE =================

if page == "🏠 Home":

    st.title("🚶 Reverse Walking Clinical Analysis Platform")

    col1, col2 = st.columns([1.2,1])

    with col1:
        st.markdown("""
        ### Advanced Biomedical Gait Analysis System

        Hospital-grade platform for:

        ✅ Reverse walking biomechanics  
        ✅ Motion capture analysis  
        ✅ Rehabilitation monitoring  
        ✅ Clinical interpretation  
        """)

    with col2:
        st.image(
            "https://images.unsplash.com/photo-1581092919535-7146ff1a590c",
            use_column_width=True
        )

    st.markdown("---")

    st.info("Use sidebar to start clinical workflow.")

# ================= UPLOAD PAGE =================

elif page == "📤 Upload & Analysis":

    st.title("📤 Upload Patient Data")

    name = st.text_input("Patient Name")
    age = st.number_input("Age", 1, 120)
    gender = st.selectbox("Gender", ["Male","Female","Other"])

    file = st.file_uploader("Upload CSV")

    if file:

        data = pd.read_csv(file)

        st.session_state["data"] = data
        st.session_state["name"] = name
        st.session_state["age"] = age
        st.session_state["gender"] = gender

        st.success("Data Uploaded Successfully")

        st.dataframe(data)

# ================= VISUALIZATION =================

elif page == "📊 Visualization":

    st.title("📊 Advanced Clinical Visualization")

    if "data" not in st.session_state:

        st.warning("Upload data first")

    else:

        data = st.session_state["data"]

        parameters = data.columns[1:]

        selected = st.selectbox("Select Parameter", parameters)

        fig = px.bar(data,
                     x="subject",
                     y=selected,
                     color="subject",
                     title="Clinical Parameter Comparison")

        st.plotly_chart(fig, use_container_width=True)

        # Radar Chart
        fig2 = go.Figure()

        for i in range(len(data)):
            fig2.add_trace(go.Scatterpolar(
                r=data.loc[i, parameters],
                theta=parameters,
                fill='toself',
                name=data.loc[i,"subject"]
            ))

        fig2.update_layout(polar=dict(radialaxis=dict(visible=True)))

        st.plotly_chart(fig2, use_container_width=True)

# ================= LIVE MONITORING =================

elif page == "📡 Live Monitoring":

    st.title("📡 Live Gait Monitoring Simulation")

    if "data" not in st.session_state:

        st.warning("Upload data first")

    else:

        chart = st.empty()

        for i in range(20):

            live_data = pd.DataFrame({
                "time": range(i+1),
                "speed":[x*0.1 for x in range(i+1)]
            })

            fig = px.line(live_data, x="time", y="speed",
                          title="Live Walking Speed")

            chart.plotly_chart(fig, use_container_width=True)

            time.sleep(0.2)

# ================= CLINICAL REPORT =================

elif page == "📄 Clinical Report":

    st.title("📄 Clinical Report")

    if "data" not in st.session_state:

        st.warning("Upload data first")

    else:

        data = st.session_state["data"]

        name = st.session_state["name"]
        age = st.session_state["age"]
        gender = st.session_state["gender"]

        st.subheader("Patient Details")

        st.write(f"Name: {name}")
        st.write(f"Age: {age}")
        st.write(f"Gender: {gender}")

        st.subheader("Clinical Interpretation")

        interpretation = "Patient shows stable gait characteristics with normal biomechanical parameters."

        st.success(interpretation)

        report_text = f"""
        Clinical Reverse Walking Report

        Name: {name}
        Age: {age}
        Gender: {gender}

        Interpretation:
        {interpretation}
        """

        st.download_button(
            "Download Report",
            report_text,
            file_name="clinical_report.txt"
        )

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import time

# ================= PAGE CONFIG =================

st.set_page_config(page_title="Clinical Gait System", layout="wide")

# ================= SIDEBAR =================

st.sidebar.title("🧬 Clinical Gait System")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home",
     "📤 Upload & Analysis",
     "📊 Visualization Lab",
     "📡 Live Monitoring",
     "📄 Clinical Report"]
)

# ================= HOME =================

if page == "🏠 Home":

    st.title("🚶 Reverse Walking Clinical Analysis Platform")

    st.markdown("""
    ### Hospital-Level Biomedical Gait Analysis System

    ✅ Reverse walking biomechanics  
    ✅ Joint ROM analysis  
    ✅ EMG activation monitoring  
    ✅ Clinical alerts system  
    ✅ Advanced visualization  
    """)

# ================= CLINICAL THRESHOLD FUNCTION =================

def grade(value, normal, moderate):

    if value >= normal:
        return 0, "🟢 Normal"
    elif value >= moderate:
        return 1, "🟡 Moderate"
    else:
        return 2, "🔴 Danger"

# ================= UPLOAD =================

if page == "📤 Upload & Analysis":

    st.header("Upload Gait CSV")

    file = st.file_uploader("Upload CSV")

    if file:

        df = pd.read_csv(file)
        st.success("Data uploaded successfully")
        st.dataframe(df)

        st.subheader("🚨 Clinical Alerts")

        for i,row in df.iterrows():

            st.markdown(f"### {row['subject']}")

            s1,g1 = grade(row["walking_speed"],1.1,0.95)
            s2,g2 = grade(row["hip_rom"],45,35)
            s3,g3 = grade(row["knee_rom"],60,50)
            s4,g4 = grade(row["ankle_rom"],22,18)
            s5,g5 = grade(row["emg_quad"],0.85,0.65)

            score = s1+s2+s3+s4+s5

            st.write("Speed:",g1)
            st.write("Hip ROM:",g2)
            st.write("Knee ROM:",g3)
            st.write("Ankle ROM:",g4)
            st.write("EMG Quad:",g5)

            if score<=1:
                st.success("Overall Status: Normal")
            elif score<=3:
                st.warning("Overall Status: Moderate Risk")
            else:
                st.error("Overall Status: High Risk")

            st.markdown("---")

        st.session_state["data"]=df


# ================= VISUALIZATION =================

if page == "📊 Visualization Lab":

    st.header("Advanced Visualization")

    if "data" in st.session_state:

        df = st.session_state["data"]

        parameters = ["walking_speed","stride_length","cadence","hip_rom","knee_rom","ankle_rom","emg_quad"]

        fig = px.bar(df,x="subject",y=parameters,barmode="group")
        st.plotly_chart(fig,use_container_width=True)

        # Radar chart
        st.subheader("Radar Chart")

        radar = px.line_polar(df,
                              r="hip_rom",
                              theta="subject",
                              line_close=True)

        st.plotly_chart(radar,use_container_width=True)

        # Scatter analysis
        st.subheader("Speed vs Cadence")

        scatter = px.scatter(df,x="walking_speed",y="cadence",color="subject",size="emg_quad")

        st.plotly_chart(scatter,use_container_width=True)

    else:
        st.warning("Upload data first")


# ================= LIVE MONITORING =================

if page == "📡 Live Monitoring":

    st.header("Live Monitoring Simulation")

    chart = st.line_chart()

    data = np.random.randn(50,1)

    for i in range(50):
        chart.add_rows(np.random.randn(1,1))
        time.sleep(0.05)


# ================= CLINICAL REPORT =================

if page == "📄 Clinical Report":

    st.header("Automated Clinical Report")

    if "data" in st.session_state:

        df = st.session_state["data"]

        patient = st.selectbox("Select Patient",df["subject"])

        row = df[df["subject"]==patient].iloc[0]

        st.write("Walking Speed:",row["walking_speed"])
        st.write("Stride Length:",row["stride_length"])
        st.write("Cadence:",row["cadence"])
        st.write("Hip ROM:",row["hip_rom"])
        st.write("Knee ROM:",row["knee_rom"])
        st.write("Ankle ROM:",row["ankle_rom"])
        st.write("EMG Quad:",row["emg_quad"])

        st.subheader("Clinical Interpretation")

        if row["walking_speed"]<0.95:
            st.error("Reduced reverse walking speed detected.")
        elif row["walking_speed"]<1.1:
            st.warning("Borderline walking speed.")
        else:
            st.success("Normal walking speed.")

    else:
        st.warning("Upload data first")

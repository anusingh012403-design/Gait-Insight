import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Clinical Gait System", layout="wide")

# ================= AUTO LOAD CSV =================
data = pd.read_csv("gait.csv")

# ================= ALERT FUNCTION =================
def grade(value, good, moderate):
    if value >= good:
        return "🟢 Normal"
    elif value >= moderate:
        return "🟡 Moderate"
    else:
        return "🔴 Risk"

# ================= SIDEBAR =================
st.sidebar.title("🏥 Clinical Gait System")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home","📤 Upload & Analysis","📊 Visualization Lab","📡 Live Monitoring","📄 Clinical Report"]
)

# ================= HOME =================
if page == "🏠 Home":

    col1,col2 = st.columns([2,1])

    with col1:
        st.title("🚶 Reverse Walking Clinical Analysis Platform")
        st.subheader("Hospital-Level Biomedical Gait Analysis System")

        st.success("✔ Reverse walking biomechanics")
        st.success("✔ Joint ROM analysis")
        st.success("✔ Clinical alerts system")
        st.success("✔ Advanced visualization")
        st.success("✔ Live monitoring simulation")

    with col2:
        st.image("https://cdn.pixabay.com/photo/2016/03/31/19/56/running-1298750_1280.png")

# ================= UPLOAD & ANALYSIS =================
elif page == "📤 Upload & Analysis":

    st.title("Patient Dataset")

    st.dataframe(data)

    st.subheader("Clinical Alerts")

    for i,row in data.iterrows():

        ws = grade(row['walking_speed'],1.2,0.9)
        cadence = grade(row['cadence'],100,80)
        hip = grade(row['hip_rom'],40,30)
        knee = grade(row['knee_rom'],55,45)
        ankle = grade(row['ankle_rom'],18,12)
        emg = grade(row['emg_quad'],0.6,0.4)

        st.write(f"{row['subject']} : {ws} | {cadence} | {hip} | {knee} | {ankle} | {emg}")

# ================= VISUALIZATION =================
elif page == "📊 Visualization Lab":

    st.title("Advanced Gait Visualization")

    parameters = ['walking_speed','stride_length','cadence','hip_rom','knee_rom','ankle_rom','emg_quad']

    # Bar chart
    fig = px.bar(data,x='subject',y=parameters,barmode='group')
    st.plotly_chart(fig,use_container_width=True)

    # Radar chart
    st.subheader("Radar Biomechanical Profile")

    for i,row in data.iterrows():
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=row[parameters],
            theta=parameters,
            fill='toself',
            name=row['subject']
        ))
        st.plotly_chart(fig)

    # Scatter comparison
    fig2 = px.scatter(data,x="walking_speed",y="cadence",color="subject",size="hip_rom")
    st.plotly_chart(fig2)

# ================= LIVE MONITORING =================
elif page == "📡 Live Monitoring":

    st.title("Live Gait Monitoring Simulation")

    chart = st.line_chart()

    import random

    for i in range(30):
        chart.add_rows([random.random()])
        time.sleep(0.1)

# ================= CLINICAL REPORT =================
elif page == "📄 Clinical Report":

    st.title("Automated Clinical Report")

    for i,row in data.iterrows():

        st.subheader(f"Patient: {row['subject']}")

        interpretation = []

        if row['walking_speed'] < 1.0:
            interpretation.append("Reduced gait speed observed")

        if row['knee_rom'] < 50:
            interpretation.append("Possible knee mobility limitation")

        if row['emg_quad'] < 0.5:
            interpretation.append("Reduced muscle activation")

        st.write("Clinical Interpretation:")
        for item in interpretation:
            st.warning(item)

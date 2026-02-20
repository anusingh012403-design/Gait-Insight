import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Clinical Gait System", layout="wide")

# ================= AUTO LOAD CSV =================
data = pd.read_csv("gait.csv")

# ================= STATUS FUNCTION =================
def get_status(value, good, moderate):
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
    ["🏠 Home","📊 Dashboard","📈 Visualization Lab","📡 Live Monitoring","📄 Clinical Report"]
)

# ================= HOME =================
if page == "🏠 Home":

    col1, col2 = st.columns([2,1])

    with col1:
        st.title("🚶 Reverse Walking Clinical Analysis Platform")
        st.subheader("Hospital-Level Biomedical Gait Assessment")

        st.success("✔ Reverse Walking Biomechanics")
        st.success("✔ Joint ROM Analysis")
        st.success("✔ EMG Muscle Activity Monitoring")
        st.success("✔ Clinical Risk Alerts")
        st.success("✔ Advanced Visualization & Reporting")

    with col2:
        st.image("https://cdn.pixabay.com/photo/2016/03/31/19/56/running-1298750_1280.png")

# ================= DASHBOARD =================
elif page == "📊 Dashboard":

    st.title("Clinical Overview Dashboard")

    col1,col2,col3 = st.columns(3)

    col1.metric("Average Speed", round(data["walking_speed"].mean(),2))
    col2.metric("Average Cadence", round(data["cadence"].mean(),2))
    col3.metric("Average EMG", round(data["emg_quad"].mean(),2))

    st.dataframe(data)

# ================= VISUALIZATION =================
elif page == "📈 Visualization Lab":

    st.title("Advanced Gait Visualization")

    parameters = ['walking_speed','stride_length','cadence','hip_rom','knee_rom','ankle_rom','emg_quad']

    # Bar Chart
    st.subheader("Multi-Parameter Comparison")
    fig_bar = px.bar(data,x='subject',y=parameters,barmode='group')
    st.plotly_chart(fig_bar,use_container_width=True)

    # Radar Chart
    st.subheader("Radar Biomechanical Profile")
    for i,row in data.iterrows():
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=row[parameters],
            theta=parameters,
            fill='toself',
            name=row['subject']
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True)))
        st.plotly_chart(fig,use_container_width=True)

    # Scatter Plot
    st.subheader("Speed vs Cadence Analysis")
    fig_scatter = px.scatter(
        data,
        x="walking_speed",
        y="cadence",
        color="subject",
        size="hip_rom"
    )
    st.plotly_chart(fig_scatter,use_container_width=True)

# ================= LIVE MONITORING =================
elif page == "📡 Live Monitoring":

    st.title("Live Gait Monitoring Simulation")

    chart = st.line_chart()

    for i in range(40):
        chart.add_rows([random.uniform(0.8,1.5)])
        time.sleep(0.1)

# ================= CLINICAL REPORT =================
elif page == "📄 Clinical Report":

    st.title("Automated Clinical Report")

    report_text = ""

    for i,row in data.iterrows():

        st.subheader(f"Patient: {row['subject']}")

        ws = get_status(row['walking_speed'],1.2,0.9)
        cadence = get_status(row['cadence'],100,80)
        hip = get_status(row['hip_rom'],40,30)
        knee = get_status(row['knee_rom'],55,45)
        ankle = get_status(row['ankle_rom'],18,12)
        emg = get_status(row['emg_quad'],0.6,0.4)

        # Parameter Summary
        st.write("### Parameter Summary")
        st.write(f"Walking Speed: {row['walking_speed']} m/s ({ws})")
        st.write(f"Cadence: {row['cadence']} steps/min ({cadence})")
        st.write(f"Hip ROM: {row['hip_rom']}° ({hip})")
        st.write(f"Knee ROM: {row['knee_rom']}° ({knee})")
        st.write(f"Ankle ROM: {row['ankle_rom']}° ({ankle})")
        st.write(f"EMG Quadriceps: {row['emg_quad']} ({emg})")

        # Interpretation
        st.write("### Clinical Interpretation")

        interpretation = []

        if "🔴" in ws:
            interpretation.append("Reduced walking speed detected.")
        if "🔴" in knee:
            interpretation.append("Knee mobility limitation observed.")
        if "🔴" in emg:
            interpretation.append("Reduced quadriceps activation.")

        if len(interpretation) == 0:
            interpretation.append("All parameters within functional range.")

        for item in interpretation:
            st.warning(item)

        # Graph for patient
        st.write("### Patient Parameter Graph")

        patient_df = pd.DataFrame({
            "Parameter":["Speed","Cadence","Hip ROM","Knee ROM","Ankle ROM","EMG"],
            "Value":[
                row['walking_speed'],
                row['cadence'],
                row['hip_rom'],
                row['knee_rom'],
                row['ankle_rom'],
                row['emg_quad']
            ]
        })

        fig_patient = px.bar(patient_df,x="Parameter",y="Value")
        st.plotly_chart(fig_patient,use_container_width=True)

        st.markdown("---")

        # Build text report
        report_text += f"""
Patient: {row['subject']}
---------------------------------
Walking Speed: {row['walking_speed']} ({ws})
Cadence: {row['cadence']} ({cadence})
Hip ROM: {row['hip_rom']} ({hip})
Knee ROM: {row['knee_rom']} ({knee})
Ankle ROM: {row['ankle_rom']} ({ankle})
EMG: {row['emg_quad']} ({emg})

Clinical Interpretation:
{', '.join(interpretation)}

=================================
"""

    # Download button
    st.download_button(
        label="⬇ Download Full Clinical Report",
        data=report_text,
        file_name="Clinical_Gait_Report.txt",
        mime="text/plain"
    )

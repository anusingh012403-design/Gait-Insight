import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time

# ---------------- PAGE CONFIG ----------------

st.set_page_config(page_title="Clinical Gait System", layout="wide")

# ---------------- SIDEBAR ----------------

st.sidebar.title("🏥 Clinical Gait System")

page = st.sidebar.radio("Navigation",
[
"🏠 Home",
"📂 Upload & Analysis",
"📊 Visualization Lab",
"❤️ Live Monitoring",
"📄 Clinical Report"
])

# ---------------- HOME ----------------

if page=="🏠 Home":

    st.title("🚶 Reverse Walking Clinical Analysis Platform")

    st.subheader("Hospital-Level Biomedical Gait Analysis System")

    st.success("✔ Reverse walking biomechanics")
    st.success("✔ Joint ROM analysis")
    st.success("✔ Clinical alerts system")
    st.success("✔ Advanced visualization")
    st.success("✔ Live monitoring simulation")

    st.markdown("---")
    st.subheader("🚨 Clinical Alerts Legend")

    st.error("🔴 High Risk")
    st.warning("🟡 Moderate Risk")
    st.success("🟢 Normal")

# ---------------- UPLOAD ----------------

elif page=="📂 Upload & Analysis":

    uploaded = st.file_uploader("Upload CSV")

    if uploaded:

        df = pd.read_csv(uploaded)

        st.session_state["data"]=df

        st.dataframe(df)

        def risk_score(row):

            score=0

            if row["walking_speed"]<0.8: score+=1
            if row["stride_length"]<1.0: score+=1
            if row["cadence"]<90: score+=1
            if row["hip_rom"]<30: score+=1
            if row["knee_rom"]<50: score+=1
            if row["ankle_rom"]<20: score+=1

            if score>=4:
                return "High Risk"
            elif score>=2:
                return "Moderate"
            else:
                return "Normal"

        df["Risk"]=df.apply(risk_score,axis=1)

        st.subheader("🚨 Clinical Alerts")

        for i,row in df.iterrows():

            if row["Risk"]=="High Risk":
                st.error(f"{row['subject']} : HIGH RISK")
            elif row["Risk"]=="Moderate":
                st.warning(f"{row['subject']} : Moderate Risk")
            else:
                st.success(f"{row['subject']} : Normal")

# ---------------- VISUALIZATION ----------------

elif page=="📊 Visualization Lab":

    if "data" in st.session_state:

        df=st.session_state["data"]

        st.header("Advanced Visualization")

        st.plotly_chart(px.bar(df,x="subject",y=["walking_speed","stride_length","cadence"]))

        st.plotly_chart(px.scatter(df,x="walking_speed",y="stride_length",color="subject"))

        st.plotly_chart(px.box(df,y=["hip_rom","knee_rom","ankle_rom"]))

        corr=df.corr(numeric_only=True)
        st.plotly_chart(px.imshow(corr,text_auto=True,title="Correlation Heatmap"))

        # radar
        for i,row in df.iterrows():

            fig=go.Figure()

            fig.add_trace(go.Scatterpolar(
            r=[row["walking_speed"],row["stride_length"],row["cadence"],row["hip_rom"],row["knee_rom"],row["ankle_rom"]],
            theta=["speed","stride","cadence","hip","knee","ankle"],
            fill='toself'))

            fig.update_layout(title=row["subject"])

            st.plotly_chart(fig)

# ---------------- LIVE ----------------

elif page=="❤️ Live Monitoring":

    st.header("Live Clinical Simulation")

    chart=st.empty()

    data=np.random.randn(20)

    for i in range(30):

        data=np.append(data,np.random.randn())
        fig=px.line(y=data)
        chart.plotly_chart(fig)
        time.sleep(0.3)

# ---------------- REPORT ----------------

elif page=="📄 Clinical Report":

    if "data" in st.session_state:

        df=st.session_state["data"]

        patient=st.selectbox("Select Subject",df["subject"])

        row=df[df["subject"]==patient].iloc[0]

        st.header("Automated Clinical Report")

        st.write(row)

        if row["Risk"]=="High Risk":

            st.error("Clinical Interpretation: Abnormal gait detected. Immediate evaluation recommended.")

        elif row["Risk"]=="Moderate":

            st.warning("Clinical Interpretation: Mild deviation observed.")

        else:

            st.success("Clinical Interpretation: Normal gait pattern.")

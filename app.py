import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Clinical Gait Analyzer",
    page_icon="🧠",
    layout="wide"
)

# -------- SIDEBAR ----------
st.sidebar.title("🧠 Clinical Gait App")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard","📊 Analysis","📈 Visualization","🧾 AI Report"]
)

# -------- DASHBOARD ----------
if page == "🏠 Dashboard":

    st.title("🚶 Reverse Walking Clinical Analysis")

    col1,col2,col3 = st.columns(3)

    col1.metric("👣 Subjects","2")
    col2.metric("📊 Parameters","5")
    col3.metric("🧠 Clinical Mode","Active")

    st.info("Upload gait data from Analysis tab.")

# -------- ANALYSIS ----------
elif page == "📊 Analysis":

    st.title("📊 Upload Clinical Data")

    file = st.file_uploader("Upload Reverse Walking CSV")

    if file:

        data = pd.read_csv(file)

        st.session_state["data"] = data

        st.success("Data uploaded successfully")

        st.dataframe(data)

# -------- VISUALIZATION ----------
elif page == "📈 Visualization":

    st.title("📈 Advanced Visualization")

    if "data" in st.session_state:

        data = st.session_state["data"]

        parameters = [c for c in data.columns if c!="subject"]

        # BAR GRAPH
        fig, ax = plt.subplots()

        for i in range(len(data)):
            ax.bar(parameters,data.loc[i,parameters],alpha=0.5,label=data.loc[i,"subject"])

        ax.legend()
        plt.xticks(rotation=45)

        st.pyplot(fig)

        # RADAR
        angles=np.linspace(0,2*np.pi,len(parameters),endpoint=False)

        fig=plt.figure()
        ax=fig.add_subplot(111,polar=True)

        for i in range(len(data)):
            values=data.loc[i,parameters].tolist()
            values+=values[:1]
            ang=np.concatenate((angles,[angles[0]]))
            ax.plot(ang,values,label=data.loc[i,"subject"])

        ax.set_xticks(angles)
        ax.set_xticklabels(parameters)
        ax.legend()

        st.pyplot(fig)

    else:
        st.warning("Upload data first")

# -------- AI REPORT ----------
elif page == "🧾 AI Report":

    st.title("🧾 Automatic Clinical Interpretation")

    if "data" in st.session_state:

        data = st.session_state["data"]

        for i in range(len(data)):

            st.subheader(f"Patient: {data.loc[i,'subject']}")

            if data.loc[i,"walking_speed"] < 0.7:
                st.error("Reduced walking speed detected")

            if data.loc[i,"stride_length"] < 1.0:
                st.warning("Short stride length")

            if data.loc[i,"cadence"] > 120:
                st.warning("High cadence compensation")

            st.success("Analysis completed")

    else:
        st.warning("Upload data first")

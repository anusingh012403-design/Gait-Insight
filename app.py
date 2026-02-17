import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Clinical Gait Analyzer",
    page_icon="🧠",
    layout="wide"
)

# ---------- PREMIUM MEDICAL CSS ----------
st.markdown("""
<style>
body {
    background-color:#0f172a;
    color:white;
}

.main {
    background-color:#0f172a;
}

.metric-container {
    background: #1e293b;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.4);
    transition:0.3s;
}

.metric-container:hover {
    transform:scale(1.05);
}

h1, h2, h3 {
    color:#38bdf8;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("🧠 Clinical System")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📊 Analysis", "🧾 Clinical Report"]
)

# ---------- HOME ----------
if page == "🏠 Home":

    st.title("🚶 Reverse Walking Clinical Analysis")

    st.markdown("""
### Ultra Premium Biomedical Dashboard

Upload gait reports and get automatic clinical analysis.

Features:

- AI-style clinical report
- Radar biomechanical analysis
- Professional medical UI
""")

# ---------- ANALYSIS ----------
elif page == "📊 Analysis":

    st.title("📊 Clinical Analysis Dashboard")

    file = st.file_uploader("Upload Reverse Walking CSV")

    if file:

        data = pd.read_csv(file)

        st.session_state["data"] = data

        st.subheader("📄 Dataset Preview")
        st.dataframe(data)

        parameters = [col for col in data.columns if col != "subject"]

        # ---------- METRIC CARDS ----------
        st.subheader("📌 Clinical Metrics")

        cols = st.columns(len(parameters))

        for i,param in enumerate(parameters):

            with cols[i]:
                st.markdown(f"""
                <div class="metric-container">
                <h3>📌 {param}</h3>
                <h2>{round(data[param].mean(),2)}</h2>
                </div>
                """, unsafe_allow_html=True)

        # ---------- TABS ----------
        tab1, tab2 = st.tabs(["📊 Comparison", "🕸 Radar"])

        with tab1:

            fig, ax = plt.subplots()

            for i in range(len(data)):
                values = data.loc[i, parameters]
                ax.bar(parameters, values, alpha=0.6, label=data.loc[i,"subject"])

            ax.legend()
            plt.xticks(rotation=45)

            st.pyplot(fig)

        with tab2:

            angles = np.linspace(0, 2*np.pi, len(parameters), endpoint=False)

            fig = plt.figure()
            ax = fig.add_subplot(111, polar=True)

            for i in range(len(data)):

                values = data.loc[i, parameters].tolist()
                values += values[:1]
                ang = np.concatenate((angles, [angles[0]]))

                ax.plot(ang, values, label=data.loc[i,"subject"])

            ax.set_xticks(angles)
            ax.set_xticklabels(parameters)
            ax.legend()

            st.pyplot(fig)

# ---------- CLINICAL REPORT ----------
elif page == "🧾 Clinical Report":

    st.title("🧾 Automatic Clinical Report")

    if "data" in st.session_state:

        data = st.session_state["data"]

        for i in range(len(data)):

            st.markdown(f"## 👤 {data.loc[i,'subject']}")

            if data.loc[i,"walking_speed"] < 0.7:
                st.error("🔴 Reduced walking speed")

            if data.loc[i,"stride_length"] < 1.0:
                st.warning("🟡 Reduced stride length")

            if data.loc[i,"cadence"] > 120:
                st.info("🔵 High cadence compensation")

            st.success("🟢 Clinical analysis complete")

    else:
        st.info("Upload data from Analysis page first.")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Reverse Walking Clinical System",
    page_icon="🏥",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🏥 Clinical Gait System")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📤 Upload", "📊 Dashboard", "📄 Clinical Report"]
)

# ---------------- SESSION STORAGE ----------------
if "data" not in st.session_state:
    st.session_state.data = None

# =====================================================
# 🏠 HOME
# =====================================================
if page == "🏠 Home":

    col1,col2 = st.columns([1.3,1])

    with col1:
        st.title("🚶 Reverse Walking Clinical Analysis Platform")

        st.markdown("""
        ### Biomedical Gait Analysis System

        Hospital-style clinical application for:

        ✅ Reverse walking evaluation  
        ✅ Joint ROM analysis  
        ✅ Clinical risk alerts  
        ✅ Automated reporting  
        """)

    with col2:
        st.image(
        "https://images.unsplash.com/photo-1580281658629-1a0e9cb9a1c3",
        use_column_width=True
        )

    st.markdown("---")

# =====================================================
# 📤 UPLOAD PAGE
# =====================================================
elif page == "📤 Upload":

    st.title("📤 Upload Reverse Walking CSV")

    file = st.file_uploader("Upload CSV")

    if file:

        st.session_state.data = pd.read_csv(file)

        st.success("Data Loaded Successfully")

        st.dataframe(st.session_state.data)

# =====================================================
# 📊 DASHBOARD
# =====================================================
elif page == "📊 Dashboard":

    if st.session_state.data is None:

        st.warning("Upload data first.")

    else:

        data = st.session_state.data

        st.title("📊 Clinical Dashboard")

        # ---------- Clinical Alerts ----------
        st.subheader("🚨 Clinical Alerts")

        for i in range(len(data)):

            name = data.loc[i,"subject"]
            speed = data.loc[i,"walking_speed"]

            if speed < 0.7:
                st.error(f"{name}: 🔴 High Risk — Slow gait detected")

            elif speed < 0.9:
                st.warning(f"{name}: 🟡 Moderate risk")

            else:
                st.success(f"{name}: 🟢 Normal gait")

        # ---------- Parameter Selection ----------
        param = st.selectbox(
            "Select Parameter",
            ["walking_speed","stride_length","cadence","hip_rom","knee_rom","ankle_rom"]
        )

        fig = px.bar(data,x="subject",y=param,color="subject")

        st.plotly_chart(fig,use_container_width=True)

        # ---------- Radar Chart ----------
        st.subheader("Radar Biomechanical Comparison")

        categories=["walking_speed","stride_length","cadence","hip_rom","knee_rom","ankle_rom"]

        fig2=go.Figure()

        for i in range(len(data)):
            fig2.add_trace(go.Scatterpolar(
                r=data.loc[i,categories],
                theta=categories,
                fill="toself",
                name=data.loc[i,"subject"]
            ))

        fig2.update_layout(polar=dict(radialaxis=dict(visible=True)))

        st.plotly_chart(fig2,use_container_width=True)

# =====================================================
# 📄 REPORT PAGE
# =====================================================
elif page == "📄 Clinical Report":

    if st.session_state.data is None:

        st.warning("Upload data first.")

    else:

        data = st.session_state.data

        st.title("📄 Clinical Report")

        report_text=""

        for i in range(len(data)):

            name=data.loc[i,"subject"]
            speed=data.loc[i,"walking_speed"]

            report_text+=f"\nSubject: {name}\n"

            report_text+=f"Walking Speed: {speed}\n"
            report_text+=f"Stride Length: {data.loc[i,'stride_length']}\n"
            report_text+=f"Cadence: {data.loc[i,'cadence']}\n"
            report_text+=f"Hip ROM: {data.loc[i,'hip_rom']}\n"
            report_text+=f"Knee ROM: {data.loc[i,'knee_rom']}\n"
            report_text+=f"Ankle ROM: {data.loc[i,'ankle_rom']}\n"

            if speed < 0.7:
                report_text+="Interpretation: Reduced gait speed.\n"
            elif speed < 0.9:
                report_text+="Interpretation: Moderate gait performance.\n"
            else:
                report_text+="Interpretation: Normal gait.\n"

        st.text_area("Generated Report",report_text,height=400)

        st.download_button(
            "⬇ Download Clinical Report",
            report_text,
            "Clinical_Report.txt"
        )

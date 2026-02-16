import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Reverse Walking Analysis Dashboard")

st.header("Upload Gait Data")

forward_file = st.file_uploader("Upload Forward Walking Data")
reverse_file = st.file_uploader("Upload Reverse Walking Data")

if forward_file and reverse_file:

    forward = pd.read_csv(forward_file)
    reverse = pd.read_csv(reverse_file)

    st.subheader("Data Preview")
    st.write("Forward Walking")
    st.dataframe(forward)

    st.write("Reverse Walking")
    st.dataframe(reverse)

    st.subheader("Walking Speed Comparison")

    fig, ax = plt.subplots()

    ax.bar(["Forward","Reverse"],
           [forward["walking_speed"].mean(),
            reverse["walking_speed"].mean()])

    st.pyplot(fig)
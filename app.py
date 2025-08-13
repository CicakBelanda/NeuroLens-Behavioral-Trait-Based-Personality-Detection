import streamlit as st
import base64

# Config halaman (harus paling atas)
st.set_page_config(page_title="NeuroLens", page_icon="🧠", layout="wide")

# Load & convert image to Base64
file_path = "./static/personality.jpg"
with open(file_path, "rb") as f:
    data = f.read()
img_base64 = base64.b64encode(data).decode()

# Hero Section
st.markdown("<h1 style='text-align: center;'>Welcome to NeuroLens</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Smart Personality & Behavioral Analysis Tool</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Centered Image
st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="data:image/jpeg;base64,{img_base64}" style="max-width:70%; height:auto;">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Call to action
st.markdown(
    """
    <style>
    div.stButton {
        display: flex;
        justify-content: center;
    }
    div.stButton > button {
        padding: 20px 50px !important; /* Perbesar tombol */
    }
    div.stButton > button p {
        font-size: 25px !important;   /* Perbesar teks tombol */
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("🚀 Predict My Personality"):
    st.switch_page("pages/1_predict.py")

st.write("---")

# Features
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("📊 AI Personality Analysis")
    st.write("Analyze human personality traits with cutting-edge machine learning models.")
with col2:
    st.subheader("⚡ Fast & Accurate")
    st.write("Real-time predictions with optimized algorithms.")
with col3:
    st.subheader("🌐 Accessible Anywhere")
    st.write("Run directly in your browser with no installation needed.")

st.write("---")

# Contact Form
st.subheader("📩 Contact Us")
with st.form(key="contact_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    submit = st.form_submit_button("Send")
    if submit:
        st.success("Your message has been sent!")

# Footer
st.markdown("<p style='text-align: center;'>© 2025 Kevin Joseph. All rights reserved.</p>", unsafe_allow_html=True)

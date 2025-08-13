import streamlit as st
import joblib
import numpy as np

st.set_page_config(page_title="Personality Test", page_icon="🧠", layout="wide")

# Load model pkl
model = joblib.load("model.pkl")  # ganti sesuai nama file model kamu

# Pertanyaan Likert
questions = [
    "I feel energized after spending time at a party with many people.",
    "I enjoy spending entire days alone without feeling lonely.",
    "I often find myself starting conversations with strangers.",
    "I frequently spend time thinking deeply about life and my experiences.",
    "I feel at ease speaking and contributing in group settings.",
    "I look forward to attending parties and large social events.",
    "I give my full attention when someone is speaking to me.",
    "I prefer having a clear plan and structure for my day.",
    "I feel confident taking the lead in group activities or projects.",
    "I am willing to take risks even if there is a chance of failure.",
    "I feel comfortable speaking in front of a large audience.",
    "I am eager to learn new things just for the sake of knowing them.",
    "I prefer having a consistent daily routine over frequent changes.",
    "I actively look for thrilling or stimulating experiences.",
    "I easily make new friends wherever I go.",
    "I usually plan my activities well in advance.",
    "I often make decisions on the spot without much planning.",
    "I enjoy trying activities that are new and slightly risky.",
    "I read books or articles regularly in my free time.",
    "I enjoy participating in or watching sports.",
    "I spend a significant amount of my free time on social media.",
    "I want to visit many different countries in my lifetime.",
    "I frequently use gadgets or tech devices throughout the day.",
    "I work better when I collaborate with others rather than alone.",
    "I usually make decisions quickly without prolonged hesitation."
]

# Mapping personality labels dan penjelasan
personality_labels = {
    0: ("Ambivert", "Balanced between introversion and extroversion. Comfortable in social situations but also enjoy time alone."),
    1: ("Extrovert", "Energized by social interactions, outgoing, talkative, and often seek excitement."),
    2: ("Introvert", "Prefer solitude or small groups, reflective, and often feel drained after extended social interaction.")
}

# Simpan jawaban di session_state
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)

# Simpan halaman sekarang di session_state
if "page" not in st.session_state:
    st.session_state.page = 0

# Tentukan jumlah pertanyaan per halaman
questions_per_page = 5
start_q = st.session_state.page * questions_per_page
end_q = start_q + questions_per_page

# Hitung progress
total_pages = (len(questions) - 1) // questions_per_page + 1
current_progress = (st.session_state.page) / (total_pages - 1)

# Tambah di awal untuk state hasil
if "result" not in st.session_state:
    st.session_state.result = None

st.title("🧠 Personality Test")
st.write("Answer the following statements according to your level of agreement:")
st.write("1 = Strongly Disagree | 2 = Disagree | 3 = Neutral | 4 = Agree | 5 = Strongly Agree")

# Form input
with st.form(key=f"page_form_{st.session_state.page}"):
    for i in range(start_q, end_q):
        if i < len(questions):
            st.session_state.answers[i] = st.radio(
                questions[i],
                options=[1, 2, 3, 4, 5],
                index=None,
                horizontal=True,
                key=f"q_{i}"
            )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.session_state.page > 0:
            if st.form_submit_button("⬅️ Previous"):
                st.session_state.page -= 1
                st.rerun()

    with col2:
        if end_q < len(questions):
            if st.form_submit_button("Next ➡️"):
                if all(st.session_state.answers[start_q:end_q]):
                    st.session_state.page += 1
                    st.rerun()
                else:
                    st.warning("Please answer all questions before proceeding.")

    with col3:
        if end_q >= len(questions):
            if st.form_submit_button("✅ Submit"):
                if all(st.session_state.answers):
                    transformed_answers = [(2 * x) - 1 for x in st.session_state.answers]
                    input_array = np.array(transformed_answers).reshape(1, -1)
                    prediction = model.predict(input_array)[0]
                    label, explanation = personality_labels.get(prediction, ("Unknown", "No explanation available."))

                    st.success("Your answers have been submitted!")

                    # Simpan hasil ke session_state
                    st.session_state.result = {
                        "label": label,
                        "explanation": explanation
                    }
                    st.rerun()
                else:
                    st.warning("Please answer all questions before submitting.")

st.progress(current_progress)

if st.session_state.result:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="
            background-color: #1e1e1e;
            border: 2px solid #444;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
            text-align: center;
            color: #f5f5f5;
        ">
            <h2 style="color: #00ff99; margin-bottom: 10px;">🧩 Personality Type: {st.session_state.result['label']}</h2>
            <p style="font-size: 16px; color: #e0e0e0;">{st.session_state.result['explanation']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        div.stButton {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        div.stButton > button {
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if st.button("🏠 Back to Homepage", use_container_width=False):
    st.session_state.clear()
    st.switch_page("app.py")

import streamlit as st
from groq import Groq
import json
import os
from prompt import build_prompt

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
labels = {
    "English": {
        "department": "Go to Department",
        "documents": "Documents to Bring",
        "scheme": "Say This at Billing Counter",
        "questions": "Ask Your Doctor",
        "ready": "Your hospital card is ready!"
    },
    "Tamil": {
        "department": "இந்த பிரிவுக்கு செல்லவும்",
        "documents": "கொண்டு வர வேண்டிய ஆவணங்கள்",
        "scheme": "பில்லிங் கவுண்டரில் இதை சொல்லுங்கள்",
        "questions": "மருத்துவரிடம் கேளுங்கள்",
        "ready": "உங்கள் மருத்துவமனை அட்டை தயார்!"
    },
    "Hindi": {
        "department": "इस विभाग में जाएं",
        "documents": "साथ लाने वाले दस्तावेज़",
        "scheme": "बिलिंग काउंटर पर यह कहें",
        "questions": "डॉक्टर से पूछें",
        "ready": "आपका हॉस्पिटल कार्ड तैयार है!"
    }
}

st.set_page_config(page_title="SAHAYAK", page_icon="🌿")
st.title("🌿 Sahayak")
st.caption("Visit Prep Assistant — Know before you go")

with st.form("patient_form"):
    symptoms = st.text_area("Describe your symptoms", placeholder="e.g. chest pain, difficulty breathing for 2 days")
    hospital = st.selectbox("Select Hospital", [
        "Rajiv Gandhi General Hospital, Chennai",
        "Stanley Government Hospital, Chennai"
    ])
    age = st.number_input("Patient Age", min_value=1, max_value=120, value=40)
    language = st.selectbox("Preferred Language", ["Tamil", "English", "Hindi"])
    scheme = st.selectbox("Insurance / Scheme Card", [
        "None",
        "Ayushman Bharat (PMJAY)",
        "CMCHIS (Tamil Nadu)"
    ])
    submitted = st.form_submit_button("Generate My Hospital Card →")

if submitted:
    if not symptoms.strip():
        st.error("Please describe your symptoms.")
    else:
        with st.spinner("Creating your hospital card..."):
            prompt = build_prompt(symptoms, hospital, age, language, scheme)

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )

            raw = response.choices[0].message.content
            clean = raw.replace("```json", "").replace("```", "").strip()

            try:
                result = json.loads(clean)

                st.success(labels[language]["ready"])
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader(labels[language]["department"])
                    st.info(result["department"])
                    st.subheader(labels[language]["documents"])
                    for doc in result["documents"]:
                        st.write(f"• {doc}")
                with col2:
                    st.subheader(labels[language]["scheme"])
                    st.success(result["scheme_script"])
                    st.subheader(labels[language]["questions"])
                    for q in result["doctor_questions"]:
                        st.write(f"• {q}")

            except json.JSONDecodeError:
                st.error("Something went wrong. Please try again.")
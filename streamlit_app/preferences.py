import streamlit as st
import requests

#backend API URL
BACKEND_URL = "http://127.0.0.1:5000" 

# Language Dictionary (Static Text)
translations = {
    "en": {
        "title": "⚙ Preferences",
        "description": "Please fill out the form to personalize your learning experience.",
        "grade": "What is your current grade/class level?",
        "stream": "Which stream are you in?",
        "degree": "Which degree are you pursuing?",
        "subjects_help": "Which subjects do you need the most help with?",
        "preferred_lang": "What is your preferred language for learning?",
        "hobbies": "What are your hobbies?",
        "career_asp": "Do you have any career aspirations?",
        "real_world_application": "Would you like to relate studies to real-world applications?",
        "study_hours": "How many hours per day do you study?",
        "preparing_for_exam": "Are you preparing for any upcoming exams?",
        "exam_options": "Which exam(s) are you preparing for?",
        "study_challenges": "Do you face any challenges while studying?",
        "challenge_options": "What is your biggest challenge in studying?",
        "submit": "Save Preferences"
    },
    "hi": {  # Hindi Translations
        "title": "⚙ प्राथमिकताएँ",
        "description": "कृपया अपने सीखने के अनुभव को व्यक्तिगत बनाने के लिए फ़ॉर्म भरें।",
        "grade": "आप वर्तमान में किस कक्षा में हैं?",
        "stream": "आप किस स्ट्रीम में हैं?",
        "degree": "आप कौन सी डिग्री कर रहे हैं?",
        "subjects_help": "आपको किन विषयों में सबसे अधिक सहायता की आवश्यकता है?",
        "preferred_lang": "आपकी पसंदीदा भाषा क्या है?",
        "hobbies": "आपके शौक क्या हैं?",
        "career_asp": "क्या आपके पास कोई करियर आकांक्षा है?",
        "real_world_application": "क्या आप अपने अध्ययन को वास्तविक दुनिया से जोड़ना चाहेंगे?",
        "study_hours": "आप प्रति दिन कितने घंटे पढ़ाई करते हैं?",
        "preparing_for_exam": "क्या आप किसी आगामी परीक्षा की तैयारी कर रहे हैं?",
        "exam_options": "आप कौन सी परीक्षा की तैयारी कर रहे हैं?",
        "study_challenges": "क्या आपको अध्ययन में कोई कठिनाई होती है?",
        "challenge_options": "अध्ययन में आपकी सबसे बड़ी चुनौती क्या है?",
        "submit": "प्राथमिकताएँ सहेजें"
    },
    "ta": {  # Tamil Translations
        "title": "⚙ முன்னுரிமைகள்",
        "description": "உங்கள் கற்றல் அனுபவத்தை தனிப்பயனாக்க தயவுசெய்து படிவத்தை நிரப்பவும்.",
        "grade": "நீங்கள் எந்த வகுப்பில் உள்ளீர்கள்?",
        "stream": "நீங்கள் எந்த பிரிவில் இருக்கிறீர்கள்?",
        "degree": "நீங்கள் எந்தப் பட்டத்தைப் படிக்கிறீர்கள்?",
        "subjects_help": "உங்களுக்கு அதிகமாக உதவி தேவையான பாடங்கள் என்ன?",
        "preferred_lang": "உங்களுக்குப் பிடித்த மொழி எது?",
        "hobbies": "உங்கள் பொழுதுபோக்குகள் என்ன?",
        "career_asp": "உங்களுக்கு ஏதேனும் தொழில் இலக்குகள் உள்ளனவா?",
        "real_world_application": "உங்கள் கல்வியை உண்மையான உலகப் பயன்பாடுகளுடன் தொடர்புபடுத்த விரும்புகிறீர்களா?",
        "study_hours": "நீங்கள் ஒரு நாளைக்கு எவ்வளவு நேரம் படிக்கிறீர்கள்?",
        "preparing_for_exam": "நீங்கள் வரவிருக்கும் தேர்வுக்குத் தயாராகுகிறீர்களா?",
        "exam_options": "நீங்கள் எந்த தேர்வுக்குத் தயாராகிறீர்கள்?",
        "study_challenges": "உங்களுக்கு படிப்பதில் ஏதேனும் சிக்கல்கள் உள்ளனவா?",
        "challenge_options": "உங்கள் படிப்பில் மிகப்பெரிய சிக்கல் எது?",
        "submit": "முன்னுரிமைகளைச் சேமிக்கவும்"
    }
}

def preferences_page():
    # Select Language
    lang_options = {"English": "en", "हिन्दी": "hi", "தமிழ்": "ta"}
    lang_choice = st.sidebar.selectbox("🌍 Select Language:", list(lang_options.keys()))
    selected_lang = lang_options[lang_choice]

    st.title(translations[selected_lang]["title"])
    st.write(translations[selected_lang]["description"])

    # User Inputs
    grade = st.selectbox(translations[selected_lang]["grade"], [
        "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th",
        "9th", "10th", "11th", "12th", "Undergraduate", "Postgraduate"
    ])

    # Stream & Degree
    stream, degree = "None", "None"
    if grade in ["11th", "12th"]:
        stream = st.selectbox(translations[selected_lang]["stream"], ["Science", "Commerce", "Arts"])
    elif grade == "Undergraduate":
        degree = st.selectbox(translations[selected_lang]["degree"], ["B.Tech", "BBA", "B.Com", "B.Sc"])
    elif grade == "Postgraduate":
        degree = st.selectbox(translations[selected_lang]["degree"], ["M.Tech", "MBA", "M.Com", "M.Sc"])

    subjects_help = st.text_input(translations[selected_lang]["subjects_help"])
    preferred_lang = st.text_input(translations[selected_lang]["preferred_lang"])
    hobbies = st.text_input(translations[selected_lang]["hobbies"])
    career_asp = st.text_input(translations[selected_lang]["career_asp"])
    real_world_application = st.radio(translations[selected_lang]["real_world_application"], ["Yes", "No"])
    study_hours = st.radio(translations[selected_lang]["study_hours"], ["<1 hour", "1-2 hours", "2-4 hours", ">4 hours"])
    preparing_for_exam = st.radio(translations[selected_lang]["preparing_for_exam"], ["Yes", "No"])
    selected_exams = st.multiselect(translations[selected_lang]["exam_options"], ["JEE", "NEET", "UPSC", "CUET"]) if preparing_for_exam == "Yes" else []

    study_challenges = st.radio(translations[selected_lang]["study_challenges"], ["Yes", "No"])
    challenges_list = st.multiselect(translations[selected_lang]["challenge_options"], [
        "Time management", "Understanding concepts", "Memorization", "Practice problems", "Lack of motivation", "Distractions"
    ]) if study_challenges == "Yes" else []

    # Check if user is logged in
    if "user" in st.session_state:
        username = st.session_state["user"]["username"]

        # Submit Preferences
        if st.button(translations[selected_lang]["submit"]):
            preferences_data = {
                "grade": grade,
                "stream": stream,
                "degree": degree,
                "subjects_help": subjects_help,
                "preferred_lang": preferred_lang,
                "hobbies": hobbies,
                "career_asp": career_asp,
                "real_world_application": real_world_application,
                "study_hours": study_hours,
                "preparing_for_exam": preparing_for_exam,
                "selected_exams": selected_exams,
                "study_challenges": study_challenges,
                "challenges_list": challenges_list
            }
            
            response = requests.post(f"{BACKEND_URL}/save_preference", json={"username": username, **preferences_data})
            st.success("✅ Preferences saved successfully!" if response.status_code == 200 else "❌ Error saving preferences.")
    else:
        st.warning("Please log in to save your preferences.")


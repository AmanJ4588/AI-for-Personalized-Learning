import streamlit as st
import requests 

BACKEND_URL = "http://127.0.0.1:5000"

# Language Dictionary (Static Text)
LANGUAGES = {
    "English": {
        "title": "📝 Generate a Custom Quiz",
        "description": "Fill in the details below to generate a personalized quiz.",
        "subject": "Enter the subject for the quiz (e.g., Math, Science, History)",
        "topic": "Enter the specific topic within the subject (e.g., Algebra, Newton's Laws)",
        "easy_questions": "How many easy questions?",
        "medium_questions": "How many medium questions?",
        "hard_questions": "How many hard questions?",
        "generate_button": "Generate Quiz",
        "quiz_generated": "✅ Quiz Generated for",
        "error": "❌ Please enter both the subject and topic to proceed.",
        "no_data": "⚠️ No quiz data received. Please try again.",
        "submit": "Submit Answers",
        "correct": "✅ Correct!",
        "incorrect": "❌ Incorrect! The correct answer is",
        "no_answer": "⚠️ No answer selected!",
        "score": "🎯 You scored",
    },
    "हिन्दी": {
        "title": "📝 एक कस्टम क्विज़ बनाएं",
        "description": "एक व्यक्तिगत क्विज़ उत्पन्न करने के लिए नीचे विवरण भरें।",
        "subject": "क्विज़ के लिए विषय दर्ज करें (जैसे, गणित, विज्ञान, इतिहास)",
        "topic": "विषय के भीतर विशिष्ट टॉपिक दर्ज करें (जैसे, बीजगणित, न्यूटन के नियम)",
        "easy_questions": "आसान प्रश्न कितने चाहिए?",
        "medium_questions": "मध्यम कठिनाई के प्रश्न कितने चाहिए?",
        "hard_questions": "कठिन प्रश्न कितने चाहिए?",
        "generate_button": "क्विज़ बनाएं",
        "quiz_generated": "✅ क्विज़ उत्पन्न किया गया",
        "error": "❌ कृपया विषय और टॉपिक दोनों दर्ज करें।",
        "no_data": "⚠️ कोई क्विज़ डेटा प्राप्त नहीं हुआ। कृपया पुनः प्रयास करें।",
        "submit": "उत्तर सबमिट करें",
        "correct": "✅ सही!",
        "incorrect": "❌ गलत! सही उत्तर है",
        "no_answer": "⚠️ कोई उत्तर चयनित नहीं किया गया!",
        "score": "🎯 आपका स्कोर",
    },
    "தமிழ்": {
        "title": "📝 தனிப்பயன் வினாடிவினா உருவாக்கவும்",
        "description": "தனிப்பட்ட வினாடிவினா உருவாக்க கீழே உள்ள விவரங்களை நிரப்பவும்.",
        "subject": "பாடத்தை உள்ளிடவும் (எ.கா., கணிதம், அறிவியல், வரலாறு)",
        "topic": "குறிப்பிட்ட தலைப்பை உள்ளிடவும் (எ.கா., கணித கோட்பாடு, நியூட்டனின் விதிகள்)",
        "easy_questions": "எளிய கேள்விகள் எத்தனை?",
        "medium_questions": "நடுத்தரக் கடினம் எத்தனை?",
        "hard_questions": "கடினமான கேள்விகள் எத்தனை?",
        "generate_button": "வினாடிவினா உருவாக்கவும்",
        "quiz_generated": "✅ வினாடிவினா உருவாக்கப்பட்டது",
        "error": "❌ தயவுசெய்து பாடத்தையும் தலைப்பையும் உள்ளிடவும்.",
        "no_data": "⚠️ வினாடிவினா தரவு கிடைக்கவில்லை. தயவுசெய்து முயற்சிக்கவும்.",
        "submit": "பதில்களை சமர்ப்பிக்கவும்",
        "correct": "✅ சரியான பதில்!",
        "incorrect": "❌ தவறான பதில்! சரியான பதில்",
        "no_answer": "⚠️ எந்த பதிலும் தேர்ந்தெடுக்கப்படவில்லை!",
        "score": "🎯 உங்கள் மதிப்பெண்",
    }
}

def quiz_page():
    # Language selection dropdown
    lang_options = {"English": "en", "हिन्दी": "hi", "தமிழ்": "ta"}
    lang_choice = st.sidebar.selectbox("🌍 Select Language:", list(lang_options.keys()))
    

    lang = LANGUAGES[lang_choice]

    st.title(lang["title"])
    st.write(lang["description"])

    # Subject and topic inputs
    subject = st.text_input(lang["subject"])
    topic = st.text_input(lang["topic"])

    # Number of questions per difficulty level
    easy_questions = st.number_input(lang["easy_questions"], min_value=0, step=1, value=5)
    medium_questions = st.number_input(lang["medium_questions"], min_value=0, step=1, value=5)
    hard_questions = st.number_input(lang["hard_questions"], min_value=0, step=1, value=5)

    # Initialize session state for answers and submission
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = []
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}

    # Generate quiz button
    if st.button(lang["generate_button"]):
        if not subject or not topic:
            st.error(lang["error"])
        else:
            payload = {
                "subject": subject,
                "topic": topic,
                "easy_questions": easy_questions,
                "medium_questions": medium_questions,
                "hard_questions": hard_questions
            }

            try:
                response = requests.post(f"{BACKEND_URL}/generate_quiz", json=payload)
                if response.status_code == 200:
                    st.session_state.quiz_data = response.json().get("quiz", [])
                    st.session_state.user_answers = {}  # Reset previous answers
                    if st.session_state.quiz_data:
                        st.success(f"{lang['quiz_generated']} {subject} - {topic}")
                    else:
                        st.error(lang["no_data"])

                else:
                    st.error(f"❌ Error: {response.json().get('error', 'Unknown error')}")

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Server connection failed: {e}")

    # Display quiz if available
    if st.session_state.quiz_data:
        st.subheader("📌 " + lang["title"])
        for i, q in enumerate(st.session_state.quiz_data, 1):
            st.write(f"**Q{i}: {q['question']}**")
            st.session_state.user_answers[i] = st.radio(
                f"Q{i}:",
                options=list(q["options"].keys()),
                format_func=lambda x: f"{x}: {q['options'][x]}",
                index=None,
                key=f"q{i}"
            )
            st.markdown("---")

        # Submit answers button
        if st.button(lang["submit"]):
            score = 0
            total = len(st.session_state.quiz_data)
            for i, q in enumerate(st.session_state.quiz_data, 1):
                selected = st.session_state.user_answers.get(i)
                correct = q["correct_option"]
                if selected:
                    if selected == correct:
                        score += 1
                        st.success(f"✅ Q{i}: {lang['correct']}")
                    else:
                        st.error(f"❌ Q{i}: {lang['incorrect']} {correct}: {q['options'][correct]}")
                else:
                    st.warning(f"⚠️ Q{i}: {lang['no_answer']}")

            st.info(f"🎯 {lang['score']} **{score}/{total}**!")


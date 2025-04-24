import streamlit as st
import requests

def chat_page(): 
    # Language Dictionary (Static Text)
    LANGUAGES = {
        "en": {
            "title": "Chat with AI",
            "input_placeholder": "Ask me anything...",
            "user": "You",
            "bot": "AI Bot",
            "select_language": "Select Language",
            "error": "Error getting response"
        },
        "hi": {
            "title": "एआई के साथ चैट करें",
            "input_placeholder": "मुझसे कुछ भी पूछें...",
            "user": "आप",
            "bot": "एआई बॉट",
            "select_language": "भाषा चुनें",
            "error": "उत्तर प्राप्त करने में त्रुटि"
        },
        "ta": {
            "title": "ஏஐயுடன் உரையாடவும்",
            "input_placeholder": "என்னையும் கேளுங்கள்...",
            "user": "நீங்கள்",
            "bot": "ஏஐ போட்",
            "select_language": "மொழியைத் தேர்ந்தெடுக்கவும்",
            "error": "பதில் பெறுவதில் பிழை"
        }
    }

    # Select Language
    lang_options = {"English": "en", "हिन्दी": "hi", "தமிழ்": "ta"}
    lang_choice = st.sidebar.selectbox("🌍 Select Language:", list(lang_options.keys()))
    selected_lang = lang_options[lang_choice]

    # Display title in selected language
    st.title(LANGUAGES[selected_lang]["title"])

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["parts"][0]["text"])

    # Get user input
    user_input = st.chat_input(LANGUAGES[selected_lang]["input_placeholder"])

    if user_input:
        # Display user input immediately
        with st.chat_message("user"):
            st.write(user_input)

        # Store user message
        st.session_state.messages.append({"role": "user", "parts": [{"text": user_input}]})

        # Check if user is logged in
        if "user" in st.session_state:
            username = st.session_state["user"]["username"]

            # Send request to backend
            response = requests.post("http://127.0.0.1:5000/chat", json={"username": username, "messages": st.session_state.messages})

            if response.status_code == 200:
                bot_reply = response.json().get("response", LANGUAGES[selected_lang]["error"])

                # Store bot's reply
                st.session_state.messages.append({"role": "model", "parts": [{"text": bot_reply}]})

                with st.chat_message("model"):
                    st.write(bot_reply)

            else:
                st.error(LANGUAGES[selected_lang]["error"])
        else:
            st.warning("Please log in to chat with the AI.")

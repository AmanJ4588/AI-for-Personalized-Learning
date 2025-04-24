import streamlit as st
import requests

# Backend API URL
BACKEND_URL = "http://127.0.0.1:5000"

# Language Dictionary (Static Text)
LANGUAGES = {
    "English": {
        "title": "Welcome to the App",
        "login": "Login",
        "signup": "Sign Up",
        "first_name": "First Name",
        "last_name": "Last Name",
        "email": "Email Address",
        "password": "Password",
        "signup_button": "Sign Up",
        "signup_success": "Account created successfully!",
        "signup_error": "An unknown error occurred",
        "login_title": "Login to Your Account",
        "login_button": "Login",
        "login_success": "Welcome back",
        "login_error": "Invalid email or password"
    },
    "हिन्दी": {
        "title": "ऐप में आपका स्वागत है",
        "login": "लॉगिन करें",
        "signup": "साइन अप करें",
        "first_name": "पहला नाम",
        "last_name": "अंतिम नाम",
        "email": "ईमेल पता",
        "password": "पासवर्ड",
        "signup_button": "साइन अप करें",
        "signup_success": "खाता सफलतापूर्वक बनाया गया!",
        "signup_error": "एक अज्ञात त्रुटि हुई",
        "login_title": "अपने खाते में लॉगिन करें",
        "login_button": "लॉगिन करें",
        "login_success": "वापसी पर स्वागत है",
        "login_error": "अमान्य ईमेल या पासवर्ड"
    },
    "தமிழ்": {
        "title": "ஆப்புக்கு வரவேற்கிறோம்",
        "login": "உள்நுழையவும்",
        "signup": "பதிவு செய்யவும்",
        "first_name": "முதல் பெயர்",
        "last_name": "கடைசி பெயர்",
        "email": "மின்னஞ்சல் முகவரி",
        "password": "கடவுச்சொல்",
        "signup_button": "பதிவு செய்யவும்",
        "signup_success": "கணக்கு வெற்றிகரமாக உருவாக்கப்பட்டது!",
        "signup_error": "ஒரு அறியப்படாத பிழை ஏற்பட்டது",
        "login_title": "உங்கள் கணக்கில் உள்நுழையவும்",
        "login_button": "உள்நுழையவும்",
        "login_success": "திரும்ப வருகை நல்வரவு",
        "login_error": "தவறான மின்னஞ்சல் அல்லது கடவுச்சொல்"
    }
}

def profile_page():
    # Language Selection
    lang_options = {"English": "en", "हिन्दी": "hi", "தமிழ்": "ta"}
    lang_choice = st.sidebar.selectbox("🌍 Select Language:", list(lang_options.keys()))
    text = LANGUAGES[lang_choice]

    st.title(text["title"])

    # Retrieve session data from query parameters
    query_params = st.query_params
    if "user" in query_params:
        user_data = query_params["user"].split(",")  
        if len(user_data) == 4:
            st.session_state["user"] = {
                "first_name": user_data[0],
                "last_name": user_data[1],
                "email": user_data[2],
                "username": user_data[3]
            }
        else:
            st.warning("User data is incomplete or corrupted. Please log in again.")
            st.query_params.clear() 

    if "user" in st.session_state:
        user = st.session_state["user"]
        st.write(f"Welcome, {user['first_name']}!")
        
        # Display user profile details
        st.subheader("Profile Details")
        st.write(f"**First Name:** {user['first_name']}")
        st.write(f"**Last Name:** {user['last_name']}")
        st.write(f"**Username:** {user['username']}")
        st.write(f"**Email:** {user['email']}")

        # Fetch user preferences
        response = requests.get(f"{BACKEND_URL}/get_preferences", params={"username": user["username"]})
        if response.status_code == 200:
            preferences = response.json().get("preferences", {})
            st.subheader("User Preferences")
            st.write(preferences)
        else: 
            st.error("Error fetching user preferences") 
        
        # Add a logout button
        if st.button("Logout"):
            del st.session_state["user"]
            st.query_params.clear()  # Clear query parameters
            st.rerun()
    else:
        # Create tabs for Login and Sign Up
        tab1, tab2 = st.tabs([text["login"], text["signup"]])

        # Sign Up Tab
        with tab2:
            st.header(text["signup"])
            with st.form(key='signup_form', clear_on_submit=True):
                first_name = st.text_input(text["first_name"])
                last_name = st.text_input(text["last_name"])
                username = st.text_input("Username")
                email = st.text_input(text["email"])
                password = st.text_input(text["password"], type="password")
                submit_button = st.form_submit_button(label=text["signup_button"])

                if submit_button:
                    payload = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "password": password,
                        "username": username
                    }
                    response = requests.post(f"{BACKEND_URL}/signup", json=payload)
                    data = response.json()

                    if data.get("success"):
                        st.success(text["signup_success"])
                        st.balloons()
                    else:
                        st.error(data.get("error", text["signup_error"]))

        # Login Tab
        with tab1:
            st.header(text["login_title"])
            with st.form(key='login_form', clear_on_submit=True):
                login_email = st.text_input(text["email"])
                login_password = st.text_input(text["password"], type="password")
                login_button = st.form_submit_button(label=text["login_button"])

                if login_button:
                    payload = {"email": login_email, "password": login_password}
                    response = requests.post(f"{BACKEND_URL}/login", json=payload)
                    data = response.json()

                    if data.get("success"):
                        st.success(f"{text['login_success']}, {data['user']['first_name']}!")
                        st.session_state["user"] = data["user"]
                       
                        st.query_params["user"] = ",".join([data["user"]["first_name"], data["user"]["last_name"], data["user"]["email"], data["user"]["username"]])

                        st.rerun()
                    else:
                        st.error(text["login_error"])

if __name__ == "__main__":
    profile_page()

from flask import Flask, request, jsonify 
import google.generativeai as genai
import threading
import os
import json
import re
import firebase_admin
from firebase_admin import auth, credentials, firestore
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("C:/Users/Aman/Downloads/ai-for-students-firebase-adminsdk-fbsvc-1d893ff58e.json")  # Load service account key
firebase_admin.initialize_app(cred)

# Initialize Firestore Database
db = firestore.client()

# Global dictionary to cache user preferences
user_preferences_cache = {}

# Global list to store chat messages
messages = []

def run_streamlit():
    #Function to run Streamlit app in a separate thread.
    os.system("streamlit run streamlit_app/main.py --server.port 8501 --server.headless true")

# Start Streamlit when Flask starts
threading.Thread(target=run_streamlit, daemon=True).start()

# Configure Gemini API
genai.configure(api_key="AIzaSyB_FZUX2L87MWS561tti3qyoN1qsvRHWpc")
# Use Gemini API for response
model = genai.GenerativeModel("gemini-pro")

# User Registration Endpoint
@app.route("/signup", methods=["POST"])
def signup():
    #Endpoint to handle user registration.
    data = request.json
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")
    username = data.get("username")

    try:
        # Create user in Firebase Authentication with username as UID
        user = auth.create_user(uid=username, email=email, password=password)

        # Store additional user details in Firestore
        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "username": username,
            "created_at": str(datetime.now())
        }
        db.collection("users").document(username).collection("profile_data").document("details").set(user_data)

        return jsonify({"success": True, "message": "Account created successfully!"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# User Login Endpoint
@app.route("/login", methods=["POST"])
def login():
    #Endpoint to handle user login.
    data = request.json
    email = data.get("email")
    password = data.get("password")

    try:
        # Get user by email (Firebase Admin SDK does not provide password authentication)
        user = auth.get_user_by_email(email)
        
        # Fetch user details from Firestore
        user_data = db.collection("users").document(user.uid).collection("profile_data").document("details").get().to_dict()

        # Fetch user preferences from Firestore
        preferences_data = db.collection("users").document(user.uid).collection("user_preferences").document("preferences").get().to_dict()

        return jsonify({"success": True, "user": user_data, "preferences": preferences_data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": "Invalid email or password"}), 401

def generate_custom_prompt(preferences_data):
    #Generate a structured prompt for AI to understand the student profile.
    return f"""
    Here is my learning profile and preferences:

    - My Grade/Class Level: {preferences_data.get('grade')}
    - My Stream (if applicable): {preferences_data.get('stream')}
    - My Degree (if applicable): {preferences_data.get('degree')}
    - Subjects I need help with: {preferences_data.get('subjects_help')}
    - My Preferred Language for Learning: {preferences_data.get('preferred_lang')}
    - My Hobbies: {preferences_data.get('hobbies')}
    - My Career Aspirations: {preferences_data.get('career_asp')}
    - Am I interested in real-world applications? {preferences_data.get('real_world_application')}
    - My Study Hours per day: {preferences_data.get('study_hours')}
    - Am I preparing for exams? {preferences_data.get('preparing_for_exam')}
    - Exam(s) I'm preparing for: {", ".join(preferences_data.get('selected_exams', []))}
    - Challenges I face while studying: {", ".join(preferences_data.get('study_challenges', []))}

    Based on this, please provide me with personalized learning guidance and study recommendations that match my academic needs and interests.
    """

@app.route("/chat", methods=["POST"])
def chat():
    #Endpoint to handle chat with AI.
    global messages

    data = request.json
    username = data.get("username")  # Retrieve username from JSON data
    user_messages = data.get("messages", [])

    if not username:
        return jsonify({"error": "Username is required"}), 400

    # Check if preferences are already in cache
    if username not in user_preferences_cache:
        # Fetch user preferences from Firestore
        preferences_doc = db.collection("users").document(username).collection("user_preferences").document("preferences").get()
        preferences_data = preferences_doc.to_dict() if preferences_doc.exists else None

        if preferences_data:
            # Store preferences in cache
            user_preferences_cache[username] = preferences_data

            # Generate a structured prompt for AI to understand the student profile
            custom_prompt = generate_custom_prompt(preferences_data)

            # Add custom prompt to the context and store it's response 
            messages.append({"role": "user", "parts": [{"text": custom_prompt}]})
            response = model.generate_content(messages)
            reply = response.text
            messages.append({"role": "model", "parts": [{"text": reply}]})

    # Add user messages to the context
    messages.extend(user_messages)

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    try:
        response = model.generate_content(messages)
        reply = response.text
        # Store AI response in messages for context
        messages.append({"role": "model", "parts": [{"text": reply}]})
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"response": reply})

@app.route("/save_preference", methods=["POST"])
def save_preference():
    #Endpoint to save user preferences.
    data = request.json
    username = data.get("username")

    try:
        # Save preferences data in Firestore
        db.collection("users").document(username).collection("user_preferences").document("preferences").set(data)
        # Update cache
        user_preferences_cache[username] = data
        return jsonify({"message": "Preferences saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_preferences", methods=["GET"])
def get_preferences():
    #Endpoint to get user preferences.
    username = request.args.get("username")

    try:
        # Fetch user preferences from Firestore
        preferences_data = db.collection("users").document(username).collection("user_preferences").document("preferences").get().to_dict()
        return jsonify({"preferences": preferences_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    #Endpoint to generate a custom quiz.
    try:
        # Get JSON data from Streamlit request
        data = request.json
        subject = data.get("subject")
        topic = data.get("topic")
        easy_questions = data.get("easy_questions", 0)
        medium_questions = data.get("medium_questions", 0)
        hard_questions = data.get("hard_questions", 0)

        if not subject or not topic:
            return jsonify({"error": "Subject and topic are required"}), 400

        total_questions = easy_questions + medium_questions + hard_questions

        # Construct prompt
        prompt = f"""
        Generate a multiple-choice quiz on the subject "{subject}" focusing on the topic "{topic}".  
        The quiz should contain exactly {total_questions} questions.  

        Each question must follow this format:  
        1. A clear and concise question statement.  
        2. Four answer choices labeled (A), (B), (C), and (D).  
        3. The correct answer indicated separately as a letter ("A", "B", "C", or "D").  

        ### Output Format:
        Return only a valid JSON array without explanations, extra text, or formatting issues.

        Example Output:
        [
            {{
                "question": "What is 2 + 2?",
                "options": {{"A": "3", "B": "4", "C": "5", "D": "6"}},
                "correct_option": "B"
            }},
            ...
        ]
        """

        # Call AI model
        response = model.generate_content([{"role": "user", "parts": [{"text": prompt}]}])
        ai_response = response.text.strip()  # Remove extra spaces

        # Extract only JSON using regex (if AI adds extra text)
        json_match = re.search(r"\[.*\]", ai_response, re.DOTALL)
        if (json_match):
            ai_response = json_match.group(0)  # Extract only JSON part

        # Validate and parse AI response
        try:
            quiz_questions = json.loads(ai_response)
            if not isinstance(quiz_questions, list):  # Ensure it's a list
                raise ValueError("Expected a JSON array but got something else.")
        except json.JSONDecodeError as e:
            return jsonify({"error": "Invalid JSON response from AI", "details": str(e)}), 500

        return jsonify({"quiz": quiz_questions})

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

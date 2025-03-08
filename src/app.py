import streamlit as st
import pyrebase
import json
import requests
import time

from commons import redirect

# Firebase Configuration (Replace with your Firebase project details)
firebase_config = {
    # "apiKey": "YOUR_FIREBASE_API_KEY",
    # "authDomain": "YOUR_FIREBASE_AUTH_DOMAIN",
    # "projectId": "YOUR_FIREBASE_PROJECT_ID",
    # "storageBucket": "YOUR_FIREBASE_STORAGE_BUCKET",
    # "messagingSenderId": "YOUR_FIREBASE_MESSAGING_SENDER_ID",
    # "appId": "YOUR_FIREBASE_APP_ID",
    # "databaseURL": ""

    "apiKey": "AIzaSyB_2S_25STjUF1LWyl3iITsaF3Lm2Jt87I",
    "authDomain": "by227auth.firebaseapp.com",
    "projectId": "by227auth",
    "storageBucket": "by227auth.firebasestorage.app",
    "messagingSenderId": "197615196385",
    "appId": "1:197615196385:web:fd5b2df8846ce2dfe23fa0",
    "databaseURL": ""
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

st.set_page_config(page_title="User Authentication", layout="centered")

# 🔹 Manage Authentication State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None

# 🔹 Authentication Logic
def login_page():
    st.title("🔐 Login to Your Account")

    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", placeholder="Enter your password", type="password")

    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success(f"✅ Logged in as {email}")

            print(f"Session in log in: {st.session_state}")

            time.sleep(2)
            redirect("home")  # Redirect to home page
        except Exception as e:
            st.error(f"⚠️ Login failed: Invalid Credentials. Register if new user.")
    
    if st.button("Register"):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            st.success("✅ Registration successful! You can now log in.")
        except Exception as e:
            st.error(f"⚠️ Error: {json.loads(e.args[1])['error']['message']}")

# 🔹 Page Navigation
page = st.query_params.get("page", ["login"])[0]

if st.session_state.logged_in:
    redirect("home")  # Redirect to home if logged in
elif page == "home":
    home_page()
elif page == "unauthorized":
    unauthorized_page()
else:
    login_page()

import streamlit as st
import pyrebase
import json
import requests
import time

from commons.utils import UiUtils as ui

class Authentication:

    # Firebase Configuration
    firebase_config = {
        "apiKey": "AIzaSyB_2S_25STjUF1LWyl3iITsaF3Lm2Jt87I",
        "authDomain": "by227auth.firebaseapp.com",
        "projectId": "by227auth",
        "storageBucket": "by227auth.firebasestorage.app",
        "messagingSenderId": "197615196385",
        "appId": "1:197615196385:web:fd5b2df8846ce2dfe23fa0",
        "databaseURL": ""
    }

    def __init__(self):
        # Initialize Firebase
        self.firebase = pyrebase.initialize_app(Authentication.firebase_config)
        self.auth = self.firebase.auth()

    # 🔹 Authentication Logic
    def login_page(self):
        st.title("🔐 Login to Your Account")

        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", placeholder="Enter your password", type="password")

        if st.button("Login", type="primary"):
            try:
                user = self.auth.sign_in_with_email_and_password(email, password)
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success(f"✅ Logged in as {email}")

                print(f"Session in log in: {st.session_state}")

                time.sleep(2)
                # st.switch_page('pages/home.py')
                ui.redirect("pages/home")  # Redirect to home page
            except Exception as e:
                st.error(f"⚠️ Login failed: Invalid Credentials. Register if new user.")
                print(e)
        
        if st.button("Register"):
            ui.redirect('pages/register')

    # Registration
    def register(self, email, password):
        ret_flag = "Failure"
        try:
            user = self.auth.create_user_with_email_and_password(email, password)
            ret_flag = "✅ Registration successful! You can now log in."
        except Exception as e:
            ret_flag = e
        
        return ret_flag
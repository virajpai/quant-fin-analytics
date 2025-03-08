import streamlit as st
import pyrebase
import json
import requests
import time

from commons.utils import UiUtils as ui
from commons.auth import Authentication

st.set_page_config(page_title="User Authentication", layout="wide")

ui.hide_nav()

# 🔹 Manage Authentication State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None

if st.session_state.logged_in:
    redirect("pages/home")  # Redirect to home if logged in
else:
    auth = Authentication()
    auth.login_page()


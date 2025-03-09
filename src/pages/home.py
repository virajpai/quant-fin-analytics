import streamlit as st
import time

from commons.utils import UiUtils as ui

print(f'Home session: {st.session_state}')

st.set_page_config(page_title="Home", layout="wide")

# 🔹 Manage Authentication State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None
    ui.redirect("pages/unauthorized")

st.title("🏠 Welcome to Home Page")
st.success(f"Logged in as {st.session_state.user_email}")

if st.button("Build Portfolio"):
    ui.redirect("pages/build_portfolio")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.success("🔓 Logged out successfully!")
    time.sleep(2)
    ui.redirect("app")

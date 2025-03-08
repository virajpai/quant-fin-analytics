import streamlit as st
import time

from commons import redirect

print(f'Home session: {st.session_state}')

# 🔹 Manage Authentication State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None
    redirect("unauthorized")

st.title("🏠 Welcome to Home Page")
st.success(f"Logged in as {st.session_state.user_email}")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.success("🔓 Logged out successfully!")
    time.sleep(2)
    redirect("")

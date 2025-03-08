import streamlit as st
from commons import redirect

st.title("🚫 Unauthorized Access")
st.warning("You need to log in to access this page.")

if st.button("Go to Login"):
    redirect("")

if st.button("Register"):
    redirect("register")
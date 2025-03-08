import streamlit as st
from commons.utils import UiUtils as ui

st.set_page_config(page_title="Unauthorized", layout="wide")
st.title("🚫 Unauthorized Access")
st.warning("You need to log in to access this page.")

if st.button("Go to Login"):
    ui.redirect("app")
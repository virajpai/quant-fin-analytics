import streamlit as st
import time

# 🔹 Redirect Function
def redirect(url):
    st.markdown(f'<meta http-equiv="refresh" content="0; url=/{url}">', unsafe_allow_html=True)
    time.sleep(1)
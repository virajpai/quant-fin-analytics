import streamlit as st
import time

class UiUtils:
    # Hide sidebar navigation
    @staticmethod
    def hide_nav():
        st.markdown(
            """
            <style>
                /* Hide the sidebar */
                section[data-testid="stSidebar"] {display: none !important;}
                
                /* Hide the hamburger menu */
                button[kind="header"] {display: none !important;}
            </style>
            """,
            unsafe_allow_html=True,
        )

    # 🔹 Redirect Function
    @staticmethod
    def redirect(url):
        st.switch_page(f'{url}.py')
        time.sleep(1)
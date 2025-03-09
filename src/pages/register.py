import streamlit as st
from commons.auth import Authentication
import json


def register():
    try:
        auth = Authentication()

        username = st.text_input("Username", placeholder="Enter a username")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", placeholder="Enter your password", type="password")
        confirm_password = st.text_input("Confirm Password", placeholder="Confirm your password", type="password")

        if st.button("Register"):    
            if password == confirm_password:
                ret_flag = auth.register(email, password)
                
                if type(ret_flag) == str:
                    if ret_flag == "Failure":
                        st.error("Unknown Error - Please try again later!")
                    else:
                        st.success(ret_flag)
                else:
                    st.error(f"Error in creating account: {json.loads(ret_flag.args[1])['error']['message']}")
            else:
                st.error("Password & Confirm Password must be same!")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        print(type(e))

register()

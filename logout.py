import streamlit as st
from auth import cookies

def show_logout_page():
    st.markdown("## 👋 Logged Out")
    if st.button("🔁 Return to Login"):
        cookies["user_email"] = ""  # Clear cookie
        st.session_state.authenticated = False
        st.session_state.user_email = ""
        st.rerun()

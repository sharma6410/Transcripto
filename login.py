import streamlit as st
from auth import register_user, login_user, cookies

def show_login_page():
    st.markdown("""
        <h1 style='text-align: center; font-size: 60px; color: #4B8BBE;'>🚀 Transcripto</h1>
        <h3 style='text-align: center; font-weight: normal;'>Summarize Smarter. Save Time. Stay Informed.</h3>
        <hr>
    """, unsafe_allow_html=True)

    st.subheader("🔐 Register or Login")

    mode = st.radio("Choose mode", ["Register", "Login"])
    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")

    if st.button(mode):
        if not email or not password:
            st.error("⚠️ Please enter both email and password.")
        elif mode == "Register":
            success, msg = register_user(email, password)
            if success:
                st.success(msg)
            else:
                st.error(msg)
        elif mode == "Login":
            success, msg = login_user(email, password)
            if success:
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

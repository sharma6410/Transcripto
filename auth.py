import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

# Initialize cookie manager
cookies = EncryptedCookieManager(
    prefix="transcripto/",
    password="your-secret-password"  # Replace with a secure value in production
)

if not cookies.ready():
    st.stop()

# Simulated user database
if "user_db" not in st.session_state:
    st.session_state.user_db = {}

def register_user(email, password):
    if email in st.session_state.user_db:
        return False, "User already exists."
    st.session_state.user_db[email] = {"password": password}
    return True, "Registration successful."

def login_user(email, password):
    user = st.session_state.user_db.get(email)
    if user and user["password"] == password:
        cookies["user_email"] = email  # Store login in cookie
        return True, "Login successful."
    return False, "Invalid credentials."

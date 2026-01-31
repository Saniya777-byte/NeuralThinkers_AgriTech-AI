import streamlit as st
import sqlite3
import hashlib

def connect_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

def authenticate(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return True if user else False

def register_page():
    st.title("Create Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register"):
            if username and password and password == confirm_password:
                register_user(username, password)
                st.success("Registered successfully! Please login.")
                # Logic to switch back to login
                st.session_state.page = "login"
                st.rerun()
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                st.error("Please fill in all fields.")
    with col2:
        if st.button("Back to Login"):
            st.session_state.page = "login"
            st.rerun()

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", type="primary"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.session_state.page = "welcome"
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.write("---")
    st.write("Don't have an account?")
    if st.button("Go to Register"):
        st.session_state.page = "register"
        st.rerun()

def welcome_page():
    st.title(f"Welcome!")
    st.success("You are now logged in.")
    st.write("This is your private dashboard content.")
    
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.page = "login"
        st.rerun()

def main():
    connect_db()

    # Initialize session states
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'page' not in st.session_state:
        st.session_state.page = "login"

    # Route the user to the correct page
    if st.session_state.authenticated:
        welcome_page()
    else:
        if st.session_state.page == "login":
            login_page()
        elif st.session_state.page == "register":
            register_page()

if __name__ == "__main__":
    main()
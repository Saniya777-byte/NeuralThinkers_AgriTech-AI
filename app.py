import streamlit as st
import sqlite3
import hashlib
from streamlit_js_eval import get_geolocation
<<<<<<< Updated upstream
=======
from farmer_dashboard import show_farmer_dashboard
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AgriTech AI - Farmer Dashboard", layout="wide", page_icon="🌾")
>>>>>>> Stashed changes


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
    c.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, hashed_password)
    )
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


@st.dialog("Location Permission Request")
def location_alert():
    st.write(
        "To provide accurate weather, soil analytics, and crop suggestions, "
        "we need your location permission."
    )
    if st.button("I understand, let's proceed"):
        st.session_state.location_allowed = True
        st.rerun()


def welcome_page():
    if 'location_allowed' not in st.session_state:
        st.session_state.location_allowed = False

    st.title("Welcome to your Farm Dashboard!")

    if not st.session_state.location_allowed:
        location_alert()
        st.info("Please respond to the location permission request to proceed.")
        st.stop()

    # Import wrapper here to avoid circular imports or early rendering issues
    from environment_data.wrapper import get_environmental_context
    from src.ai_logic import get_expert_analysis

    # Check if we already have data to avoid re-fetching on every rerun
    if 'env_data' not in st.session_state:
        with st.spinner("Analyzing your field environment (Weather + Soil)..."):
            env_data = get_environmental_context()
            
            # Simple validation: if we didn't get coordinates, we can't do much
            if not env_data['location']:
                 st.warning("Could not detect precise location. Please ensure location is enabled.")
                 st.stop()
                 
            st.session_state.env_data = env_data
            
            # Get AI Analysis
            analysis = get_expert_analysis(env_data['weather'], env_data['soil'])
            st.session_state.ai_analysis = analysis

<<<<<<< Updated upstream
        if lat is not None and lon is not None:
            st.success(f" Location identified: {lat}, {lon}")
        else:
            st.warning("Location detected, but coordinates are unavailable.")

        st.divider()
        st.subheader("Field & Crop Information")

        with st.form("farmer_data_form"):
            col1, col2 = st.columns(2)

            with col1:
                soil_type = st.selectbox(
                    "Select Soil Type",
                    ["Clay", "Silt", "Sandy", "Black Soil", "Loamy","Red soil"]
                )
                crop_type = st.selectbox(
                    "Crop Type",
                    ["Rice", "Wheat", "Cotton", "Sugarcane", "Maize"]
                )

            with col2:
                ph_level = st.number_input(
                    "Soil pH Level",
                    min_value=0.0,
                    max_value=14.0,
                    value=7.0,
                    step=0.1
                )
                st.caption("Standard pH for most crops is 6.0 - 7.5")

            fert_used = st.toggle("Did you use fertilizer?")
            if fert_used:
                f_amount = st.number_input("Amount (ml per unit)", min_value=0.0)

            submitted = st.form_submit_button("Get AI Recommendations")

            if submitted:
                st.info("AI Agent is analyzing your field context...")
=======
    # Display Data
    env_data = st.session_state.env_data
    analysis = st.session_state.get('ai_analysis', {})
>>>>>>> Stashed changes

    if env_data.get('location') and env_data['location'].get('latitude'):
        st.success(f" Location identified: {env_data['location']['latitude']:.4f}, {env_data['location']['longitude']:.4f}")
    else:
        st.warning(" Location identified but coordinates unavailable.")

    # Weather & Soil Context Cards
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(" Weather Context")
        w = env_data['weather']
        st.write(f"**Temp:** {w['temperature_c']}°C")
        st.write(f"**Humidity:** {w['humidity']}%")
        if w['weather_alert']:
            st.error(f" {w['weather_alert']}")
        else:
            st.info("No active weather alerts.")

    with col2:
        st.subheader(" Soil Composition")
        s = env_data['soil']
        st.write(f"**Type:** {s['soil_type'] or 'Unknown'}")
        st.write(f"**Est. pH:** {s['soil_ph'] or 'N/A'}")
        st.write(f"**Moisture:** {s['soil_moisture'] or 'N/A'}%")

    st.divider()
    
    st.subheader("AI Recommendations")
    
    if analysis.get('soil_analysis'):
        st.caption(analysis['soil_analysis'])

    with st.form("farmer_data_form"):
        st.write("Based on your location and conditions, we recommend:")
        
        suggested_crops = analysis.get('suggested_crops', ["Rice", "Wheat", "Maize"])
        
        c1, c2 = st.columns(2)
        with c1:
            selected_crop = st.selectbox("Select Crop", suggested_crops)
        with c2:
            # Allow overriding soil type if sensor data is wrong
            detected_soil = list([s['soil_type']]) if s['soil_type'] else []
            all_soils = detected_soil + ["Clay", "Silt", "Sandy", "Black Soil", "Loamy", "Red soil"]
            # Remove duplicates while preserving order
            all_soils = list(dict.fromkeys(all_soils))
            
            selected_soil = st.selectbox("Confirm Soil Type", all_soils)

        # Allow pH override
        ph_val = s['soil_ph'] if s['soil_ph'] else 7.0
        ph_level = st.number_input("Soil pH Level", value=float(ph_val), step=0.1)

        submitted = st.form_submit_button("Launch Dashboard ")

        if submitted:
            st.session_state.soil_type = selected_soil
            st.session_state.crop_type = selected_crop
            st.session_state.ph_level = ph_level
            st.session_state.weather_alert = env_data['weather']['weather_alert']
            
            # Store action plan for dashboard
            st.session_state.action_plan = analysis.get('action_plan', [])
            
            st.session_state.page = "dashboard"
            st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.page = "login"
        st.session_state.location_allowed = False
        st.rerun()


def main():
    connect_db()

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'page' not in st.session_state:
        st.session_state.page = "login"

    if st.session_state.authenticated:
        welcome_page()
    else:
        if st.session_state.page == "login":
            login_page()
        elif st.session_state.page == "register":
            register_page()


if __name__ == "__main__":
    main()

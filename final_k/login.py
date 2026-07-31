import streamlit as st
from pymongo import MongoClient
import bcrypt

# --- STREAMLIT PAGE CONFIGURATION ---
st.set_page_config(page_title="Login / Register", layout="wide")

# --- MongoDB Setup ---
MONGO_URI = "mongodb+srv://adeorabe23:bnZ1sHEdOITni0hy@cluster0.d1b46.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["nic_code_db"]
users_collection = db["users"]
queries_collection = db["user_queries"]



# --- INITIALIZE SESSION STATE ---
if "history" not in st.session_state:
    st.session_state["history"] = []
if "voice_input" not in st.session_state:
    st.session_state["voice_input"] = ""
if "is_authenticated" not in st.session_state:
    st.session_state["is_authenticated"] = False
    st.session_state["user_email"] = "anonymous"

# --- SIDEBAR (WITH LOGO & HISTORY) ---
st.sidebar.image("GovINTEL.AI.png", use_container_width=True)
st.sidebar.title("📜 Search History")

if st.session_state["is_authenticated"]:
    # Fetch history from DB
    history_records = list(queries_collection.find({"user": st.session_state["user_email"]}).sort("timestamp", -1))
    if history_records:
        for i, entry in enumerate(history_records, start=1):
            st.sidebar.markdown(f"**{i}.** {entry['user_input']}  \n🚀 *{entry['nic_code_result']}*")
    else:
        st.sidebar.info("No history yet.")
else:
    st.sidebar.info("Login to see your history.")

# --- Clear History ---
if st.sidebar.button("Clear History"):
    if st.session_state["is_authenticated"]:
        queries_collection.delete_many({"user": st.session_state["user_email"]})
        st.sidebar.success("Your history cleared!")
    else:
        st.sidebar.warning("Login first to clear history!")

# --- PAGE TITLE ---
st.title("Login & Register")

st.write("""To access all features of **NIC Code Finder**, please log in or create an account.""")

# --- Helper Functions ---
def create_user(email, password):
    if users_collection.find_one({"_id": email}):
        return False
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({"_id": email, "password_hash": hashed_pw})
    return True

def authenticate_user(email, password):
    user = users_collection.find_one({"_id": email})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password_hash"]):
        return True
    return False

# --- LAYOUT: LOGIN & REGISTER FORMS SIDE-BY-SIDE ---
col1, col2 = st.columns(2)

# --- LOGIN FORM ---
with col1:
    st.markdown("### **Existing Users - Login**")
    login_email = st.text_input("Email", key="login_email", placeholder="Enter your email")
    login_password = st.text_input("Password", key="login_password", placeholder="Enter your password", type="password")
    if st.button("Login", key="login_button"):
        if login_email and login_password:
            if authenticate_user(login_email, login_password):
                st.session_state["is_authenticated"] = True
                st.session_state["user_email"] = login_email
                st.success(f"Welcome back, {login_email}!")
                st.rerun()
            else:
                st.warning("Invalid email or password.")
        else:
            st.warning("Please enter both email and password!")

# --- REGISTER FORM ---
with col2:
    st.markdown("### **New Users - Register**")
    reg_email = st.text_input("Email", key="reg_email", placeholder="Enter your email")
    reg_password = st.text_input("Password", key="reg_password", placeholder="Create a password", type="password")
    if st.button("Register", key="register_button"):
        if reg_email and reg_password:
            if create_user(reg_email, reg_password):
                st.success(f"Account created successfully for {reg_email}! Please login.")
            else:
                st.warning("User already exists! Try logging in.")
        else:
            st.warning("Please fill all fields!")

# --- FOOTER ---
st.markdown("**Your account gives you access to exclusive features in NIC Code Finder.**")
# Sidebar: Font Selection
font_choice = st.sidebar.selectbox("🔤 Choose Font Style:", ["Default", "Dyslexic-Friendly"])

# Store the selected font in session state
if "font_style" not in st.session_state:
    st.session_state["font_style"] = font_choice
else:
    st.session_state["font_style"] = font_choice

# Define font URLs
dyslexic_font_url = "https://fonts.cdnfonts.com/css/opendyslexic"

# Apply CSS dynamically based on the selected font
if st.session_state["font_style"] == "Dyslexic-Friendly":
    font_css = f"""
        <style>
        @import url('{dyslexic_font_url}');
        * {{
            font-family: 'OpenDyslexic', sans-serif !important;
        }}
        </style>
    """
else:
    font_css = """
        <style>
        * {
            font-family: 'Arial', sans-serif !important;
        }
        </style>
    """

st.markdown(font_css, unsafe_allow_html=True)
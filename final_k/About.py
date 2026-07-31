import streamlit as st

st.set_page_config(page_title="About Us", layout="wide")

st.title("About the Project")

st.write("""
The **NIC Code Finder** is an AI-powered tool designed to simplify the process of identifying the correct **National Industrial Classification (NIC) code** for businesses.
""")

st.markdown("### **Challenges with Traditional Methods**")
st.write("""
- Required exact keyword matches, making searches difficult.
- Prone to human error, leading to misclassification.
- Time-consuming and inefficient.
""")

st.markdown("### **Our Solution**")
st.write("""
Our AI model:
- Understands natural language descriptions.
- Handles synonyms and alternative phrasing.
- Provides fast and accurate predictions.
""")

st.markdown("### **Future Scope**")
st.write("""
- Integration with government portals.
- Improved AI models for better accuracy.
- Support for multiple languages.
""")

st.markdown("**Developed for accuracy. Built for efficiency. Powered by AI.**")

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
import streamlit as st

st.set_page_config(page_title="Contact Us", layout="wide")

st.title("Contact Us")

name = st.text_input("Your Name")
email = st.text_input("Your Email")
feedback = st.text_area("Your Feedback")

if st.button("Submit"):
    if name and email and feedback:
        st.success("Thank you for your feedback! We'll get back to you soon.")
    else:
        st.warning("Please fill in all fields before submitting.")

st.write("📞 Phone: +91-9999084117")
st.write("📧 Email: karora4_be23@thapar.edu")
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
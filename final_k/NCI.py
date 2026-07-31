import streamlit as st
import pandas as pd

# Set page title
st.set_page_config(page_title="CSV Viewer", layout="wide")

# Title
st.title("NIC Codes 📊")

# Read the CSV file (Update the path accordingly)
csv_file_path = "NIC_5digit.csv"
df = pd.read_csv(csv_file_path)

# Set the index to start from 1 instead of 0
df.index = df.index + 1

# Display the dataframe as a table
st.dataframe(df, use_container_width=True)


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
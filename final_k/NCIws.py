import streamlit as st
import pandas as pd

# Set page title
st.set_page_config(page_title="NIC Code Viewer", layout="wide")

# Load NIC CSV File
csv_file_path = "C:\\Users\\KRIVI ARORA\\Desktop\\hackathon_final\\NIC_5digit.csv"
df = pd.read_csv(csv_file_path)

# Set the index to start from 1 instead of 0
df.index = df.index + 1

# Retrieve selected NIC code from URL parameters
query_params = st.query_params
selected_nic = query_params.get("code", [""])[0]

# Ensure NIC code is valid
if selected_nic and selected_nic.isdigit():
    first_digit = selected_nic[0]  # Extract first digit

    # Filter NIC codes that start with this digit
    filtered_df = df[df["NICcode"].astype(str).str.startswith(first_digit)]

    # Highlight the selected NIC code
    def highlight_selected(val):
        return "background-color: yellow" if str(val) == selected_nic else ""

    # Display Results
    st.subheader(f"🔍 Showing NIC Codes Starting with {first_digit}")
    st.dataframe(filtered_df.style.applymap(highlight_selected, subset=["NICcode"]), use_container_width=True)

else:
    st.warning("Invalid NIC code provided.")
import streamlit as st

# Here we declared NOVA's  page config
st.set_page_config(page_title="NOVA - Organizational Assistant", layout="wide")

# Title of the project
st.title("NOVA - Your Organizational Assistant")

# Import page modules and functions called from different pages to main file
from info import display_info
from login import login_process
from chat import chat_interface


pages = {
    "Home": display_info,
    "Login": login_process,
    "Chat": chat_interface,
}

# Sidebar
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Load the selected page
if selection:
    pages[selection]()

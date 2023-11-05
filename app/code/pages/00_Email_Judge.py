import os, sys, time
import re
import streamlit as st

try:

    st.set_page_config(
        page_title="Phishing Detection App",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a *phishing* detection app!"
        }
    )

    st.text("email judge")

except Exception as e:
    st.error(f"An error occurred: {e}")

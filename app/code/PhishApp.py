import os, sys, time
import re
import streamlit as st

from streamlit.source_util import (
    page_icon_and_name, 
    calc_md5, 
    get_pages,
    _on_pages_changed
)

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

try:

    # Use local CSS
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css("share/style.css")

    # ---- LOAD ASSETS ----


    # ---- HEADER SECTION ----
    with st.container():
        st.subheader("Welcome to the phishing email and url detection website :wave:")
        st.write("[Contact Us? >](<email addr>)")

    # ---- OUR MISSION ----
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("Our Mission :fire:")
            st.write("##")
            st.write(
                """
                Our mission is to empower individuals and organizations by providing cutting-edge tools to detect and thwart phishing attacks. We are dedicated to creating a safer online environment through innovative technology and education. By staying ahead of evolving cyber threats, we strive to be a trusted ally in the ongoing battle against phishing scams. Join us in our commitment to cybersecurity, where every click counts in the fight against online fraud. Together, let's build a more secure digital future.
                """
            )
        #with right_column: #for demo video !!!!
            #st.video("")

except Exception as e:
    st.error(f"An error occurred: {e}")

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
        st.subheader("Welcome to the phishing email detection website :wave:")
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
                -
                -
                -
                -
                """
            )
        #with right_column: #for demo video !!!!
            #st.video("")

except Exception as e:
    st.error(f"An error occurred: {e}")

import os, sys, time
import re
import streamlit as st

from streamlit.source_util import (
    page_icon_and_name, 
    calc_md5, 
    get_pages,
    _on_pages_changed
)

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

    st.text("this is a home page")

except Exception as e:
    st.error(f"An error occurred: {e}")

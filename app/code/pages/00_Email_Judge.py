import os, sys, time
import re
import streamlit as st
import requests
from PIL import Image
from io import StringIO

def read_file(file):
    with open(input, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
        st.write(text)

try:

    st.set_page_config(
        page_title="Phishing Detection App",
        page_icon="🎣",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a *phishing* detection app!"
        }
    )


    # emoji cheatsheet https://www.webfx.com/tools/emoji-cheat-sheet/


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

    # ---- PROJECTS ----
    with st.container():
        st.write("---")
        st.header("Our Projects 🛫")
        st.write("##")
        
        left_column, right_column = st.columns(2)
        with right_column:
            uploaded_file = st.file_uploader("Choose a EML file", accept_multiple_files=False)
            if uploaded_file and st.button("Process"):
             #        result = your_processing_script.process_content(uploaded_file)
                st.write("Processing result:")
                # st.write(type(uploaded_file))
                # read_file(uploaded_file)

                # To convert to a string based IO:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                st.write(type(stringio))
                string_data = stringio.read()
                st.write(string_data)
                # download_button = st.button("Download Processed File")
            # pass to script accordingly
            
    #download button
    #         if download_button:
    #            with open(result_path, "rb") as file:
    #                data = file.read()
    #            st.download_button(label="Click to download", data=data, key="processed_file.txt", file_name="processed_file.txt")

        with left_column:
            st.subheader("Email Content Analysis 📧")
            st.write(
                """
                <Description>
                """
            )
            st.markdown("[How to extract the email as a file...](<video_link>)")
    with st.container():
        st.write("******")
        left_column, right_column = st.columns((2))
        with right_column:
    #        link_form = """
    #            <form action="localhost" method="POST">
    #            <textarea name="url" placeholder="URL to analyze" required></textarea>
    #            <button type="submit">Send</button>
    #            </form>
    #            """
    #        st.markdown(link_form, unsafe_allow_html=True)
            user_input = st.text_input("Enter a URL to be analyzed:")
            if st.button("Submit"):
                if user_input:
                    st.write(f"You submitted the following link: {user_input}")
                    #pass the url to script, return result
                else:
                    st.warning("Please enter a valid link.")
            
        
        with left_column:
            st.subheader("URL Analysis (if any) 🔗")
            st.write(
                """
                <Description>
                """
            )


except Exception as e:
    st.error(f"An error occurred: {e}")

import streamlit as st
from PIL import Image
from io import StringIO
from Utilities.cli import is_phishing_url, is_phishing_email

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


    

    # ---- PROJECTS ----
    with st.container():
        # st.write("---")
        # st.header("Our Projects 🛫")
        # st.write("##")
        st.write("******")
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


except Exception as e:
    st.error(f"An error occurred: {e}")

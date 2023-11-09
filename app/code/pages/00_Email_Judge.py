import streamlit as st
from PIL import Image
from io import StringIO
from Utilities.cli import is_phishing_url, is_phishing_email
from Utilities.email_modeling.read_email import read_eml_string
from Utilities.email_modeling.preprocess import preprocess


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
            uploaded_file = st.file_uploader("Choose a EML file", accept_multiple_files=False, type="eml")
            if uploaded_file and st.button("Process"):
                st.write("Processing result:")

                # To convert to a string based IO:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                string_data = stringio.read()
                try:
                    subject, sender, links, email_content, has_attachments = read_eml_string(string_data)
                    if is_phishing_email(string_data):
                        st.warning("This file may be a phishing attempt!")
                    else:
                        st.success("This file is safe.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

                # download_button = st.button("Download Processed File")
            
        with left_column:
            st.subheader("Phishing Email Detector 📧")
            st.write(
                """
                This is a powerful tool designed for quick and accurate 
                .EML file analysis. Leveraging advanced machine learning models, 
                it swiftly determines whether an email is phishing or safe. 
                Simply upload your .EML file to receive instant insights, 
                enhancing your email security with efficiency and precision.
                """
            )
            st.markdown("[How to extract the email as a file from Gmail...](https://help.salesforce.com/s/articleView?id=000389554&type=1)")
            st.markdown("[How to extract the email as a file from Outlook...](https://help.technosis.biz/email-office/how-to-save-an-email-as-a-msg-or-eml-file)")


except Exception as e:
    st.error(f"An error occurred: {e}")

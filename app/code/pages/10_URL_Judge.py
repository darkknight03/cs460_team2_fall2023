import streamlit as st
from Utilities.cli import is_phishing_url, is_phishing_email


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
                # Validate user_input
                if user_input:
                    st.write(f"You submitted the following link: {user_input}")
                    if is_phishing_url(user_input):
                        st.error("This URL may be a phishing attempt!")
                    else:
                        st.success("This URL is safe.")
                else:
                    st.warning("Please enter a valid link.")
            
        
        with left_column:
            st.subheader("URL Analysis 🔗")
            st.write(
                """
                We prioritize your safety online. Our URL analysis feature is designed to meticulously scrutinize web addresses embedded in emails or messages, helping you make informed decisions about their legitimacy. By employing advanced algorithms, we assess URLs for potential phishing, malware, or fraudulent activities.
                """
            )

except Exception as e:
    st.error(f"An error occurred: {e}")

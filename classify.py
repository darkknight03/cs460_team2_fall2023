# Description: This file contains the code to classify an email as phishing or not phishing.
import joblib
from email_modeling.preprocess import preprocess
from url_modeling.preprocess_html import read_html


def classify_email(email):
    # Preprocess the email text
    print("Preprocessing email...")
    preprocessed_email = preprocess(email)

    # Load your trained model, label encoder, and TF-IDF vectorizer
    print("Loading model...")
    loaded_model = joblib.load('email_modeling/logistic.pkl')
    label_encoder = joblib.load('email_modeling/label_encoder.pkl')
    tfidf_vectorizer = joblib.load('email_modeling/tfidf_vectorizer.pkl')

    print("Classifying email...")
    # Transform the preprocessed email text using the same vectorizer
    email_vector = tfidf_vectorizer.transform([preprocessed_email])

    # Make a prediction using the loaded model
    predicted_class = loaded_model.predict(email_vector)

    # Convert the predicted class back to its original label
    predicted_label = label_encoder.inverse_transform(predicted_class)

    return predicted_label == 'Phishing Email'


def classify_url(url):
    # Preprocess the html text
    print("Preprocessing html...")
    preprocessed_html = read_html(url)

    # Load your trained mode and TF-IDF vectorizer
    print("Loading model...")
    loaded_model = joblib.load('url_modeling/model_svc.pkl')
    tfidf_vectorizer = joblib.load('url_modeling/tfidf_vectorizer_html.pkl')

    print("Classifying html...")
    # Transform the preprocessed html text using the same vectorizer
    html_vector = tfidf_vectorizer.transform([preprocessed_html])

    # Make a prediction using the loaded model
    predicted_class = loaded_model.predict(html_vector)

    return predicted_class == 'p'

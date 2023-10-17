# Description: This file contains the code to classify an email as phishing or not phishing.
import joblib
from preprocess import preprocess


def classify_email(email):
    # Preprocess the email text
    print("Preprocessing email...")
    preprocessed_email = preprocess(email)

    # Load your trained model, label encoder, and TF-IDF vectorizer
    print("Loading model...")
    loaded_model = joblib.load('/Users/wolf/dev/cs460/dev/logistic.pkl')
    label_encoder = joblib.load('/Users/wolf/dev/cs460/dev/label_encoder.pkl')
    tfidf_vectorizer = joblib.load('/Users/wolf/dev/cs460/dev/tfidf_vectorizer.pkl')

    print("Classifying email...")
    # Transform the preprocessed email text using the same vectorizer
    email_vector = tfidf_vectorizer.transform([preprocessed_email])

    # Make a prediction using the loaded model
    predicted_class = loaded_model.predict(email_vector)

    # Convert the predicted class back to its original label
    predicted_label = label_encoder.inverse_transform(predicted_class)

    # TODO:return boolean value for phishing or not phishing
    if predicted_label[0] == 'Safe Email':
        return False
    else:
        return True


def classify_url(url):
    return False

# print(f"Predicted Email Class: {label[0]}")

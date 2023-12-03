import os
from bs4 import BeautifulSoup
import urllib3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import joblib
import requests, re

def preprocess_html(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    text = re.sub('[\n]+', '\n', text)
    return text

def read_html(url):

    if url[:7] != 'http://' and url[:8] != 'https://':
        try: # try default https
            response = requests.get('https://' + url)

            html_content = response.text
            html_data = preprocess_html(html_content)
            return html_data
        except:
            pass

        # try http
        response = requests.get('http://' + url)

        html_content = response.text
        html_data = preprocess_html(html_content)
        return html_data

    response = requests.get(url)

    html_content = response.text
    html_data = preprocess_html(html_content)
    return html_data

def classify(tfidf, model, data):
    test = tfidf.transform([data])
    pred = model.predict(test)
    return pred

training_phish_dir = 'db/htmls/training/Phish/'
training_not_phish_dir = 'db/htmls/training/NotPhish/'
validation_phish_dir = 'db/htmls/validation/Phish/'
validation_not_phish_dir = 'db/htmls/validation/NotPhish/'

# fetch filenames
training_files_phish = [os.path.join(training_phish_dir, filename) for filename in os.listdir(training_phish_dir)]
training_files_not_phish = [os.path.join(training_not_phish_dir, filename) for filename in os.listdir(training_not_phish_dir)]
validation_files_phish = [os.path.join(validation_phish_dir, filename) for filename in os.listdir(validation_phish_dir)]
validation_files_not_phish = [os.path.join(validation_not_phish_dir, filename) for filename in os.listdir(validation_not_phish_dir)]

# Preprocess the training and validation data
training_data = []
training_labels = []
for file_path in training_files_phish:
    try:
        training_data.append(preprocess_html(open(file_path, 'r').read()))
        training_labels.append('p')
    except:
        continue
for file_path in training_files_not_phish:
    try:
        training_data.append(preprocess_html(open(file_path, 'r').read()))
        training_labels.append('n')
    except:
        continue

validation_data = []
validation_labels = []
for file_path in validation_files_phish:
    try:
        validation_data.append(preprocess_html(open(file_path, 'r').read()))
        validation_labels.append('p')
    except:
        continue
for file_path in validation_files_not_phish:
    try:
        validation_data.append(preprocess_html(open(file_path, 'r').read()))
        validation_labels.append('n')
    except:
        continue

# TF-IDF vectorization
tfidf_vectorizer = TfidfVectorizer(max_features=1000)
X_train = tfidf_vectorizer.fit_transform(training_data)
X_valid = tfidf_vectorizer.transform(validation_data)

# Train an SVM model
model_svc = SVC()
model_svc.fit(X_train, training_labels)
# Validation
validation_predictions = model_svc.predict(X_valid)

# Results
accuracy = accuracy_score(validation_labels, validation_predictions)
report = classification_report(validation_labels, validation_predictions)

print(f"Accuracy: {accuracy:.2f}")
print(report)

# Save the model
joblib.dump(model_svc, 'model_svc.pkl')
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer_html.pkl')
# Description: This file contains the code for the ML regression model.

import time
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV
import joblib
from project.email.preprocess import preprocess


# Regression Model
def regression_model(dataset='phishing.csv'):
    # Load your dataset into a DataFrame
    data = pd.read_csv(dataset)
    
    # Preprocess text data
    data['Text'] = data['Email Text'].apply(lambda text: preprocess(text))

    print("Preprocessing complete.")

    # Encode labels into numerical values
    label_encoder = LabelEncoder()
    data['Type'] = label_encoder.fit_transform(data['Email Type'])
    data.drop(['Email Type', 'Unnamed: 0'], axis=1, inplace=True)


    # Split the dataset into training, validation, and test sets
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
    val_data, test_data = train_test_split(test_data, test_size=0.5, random_state=42)
    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(max_features=5000)

    # Fit and transform the vectorizer on the training data
    X_train = tfidf_vectorizer.fit_transform(train_data['Text'])
    X_val = tfidf_vectorizer.transform(val_data['Text'])
    X_test = tfidf_vectorizer.transform(test_data['Text'])

    # Get the corresponding labels
    y_train = train_data['Type']
    y_val = val_data['Type']
    y_test = test_data['Type']

    # Define the model
    model = LogisticRegression(max_iter=1000)

    # Define hyperparameters to tune
    param_grid = {
        'C': [0.0001, 0.01, 0.1, 1, 10],  # Add a very small value for 'C'
        'penalty': ['l2']
    }

    # Create a GridSearchCV object
    grid_search = GridSearchCV(model, param_grid, cv=3, n_jobs=-1, verbose=2)

    # Perform hyperparameter tuning
    grid_search.fit(X_train, y_train)

    # Get the best hyperparameters
    best_params = grid_search.best_params_
    print("Best Hyperparameters:", best_params)

    # Get the best model
    best_model = grid_search.best_estimator_

    # Make predictions on the validation set
    val_preds = best_model.predict(X_val)

    # Evaluate the best model on the validation set
    accuracy = accuracy_score(y_val, val_preds)
    report = classification_report(y_val, val_preds)
    print(f'Validation Accuracy: {accuracy}')
    print(report)

    # Evaluate the best model on the test set
    test_preds = best_model.predict(X_test)
    test_accuracy = accuracy_score(y_test, test_preds)
    print(f'Final Test Accuracy: {test_accuracy}')

    return best_model, label_encoder, tfidf_vectorizer

# Show time and progress
print("Start time: ", time.ctime())
print("Training the model...")

# Train the model
best_model, label_encoder, tfidf_vectorizer = regression_model()

print("End time: ", time.ctime())

# Save the model to a .pkl file
joblib.dump(best_model, 'logistic.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.pkl')

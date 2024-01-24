import numpy as np
from sklearn.datasets import load_iris, load_wine, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib

def train_and_evaluate_model(X, y, model_name):
    try:
        # Preprocessing & scaling
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Splitting the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        # Training the model
        model = LogisticRegression()
        model.fit(X_train, y_train)

        # Model evaluation
        accuracy = model.score(X_test, y_test)
        print(f"{model_name} model accuracy: {accuracy}")

        # Save the model
        joblib.dump(model, f'{model_name}_model.pkl')

        # Load the model
        loaded_model = joblib.load(f'{model_name}_model.pkl')

        # Make predictions using the loaded model
        predictions = loaded_model.predict(X_test)
        print(f"{model_name} model predictions:", predictions)

    except Exception as e:
        print(f"An error occurred in {model_name} model processing: {e}")

def main():
    # Load the datasets
    iris = load_iris()
    X_iris, y_iris = iris.data, iris.target

    wine = load_wine()
    X_wine, y_wine = wine.data, wine.target

    cancer = load_breast_cancer()
    X_cancer, y_cancer = cancer.data, cancer.target

    # Train and evaluate models for each dataset
    train_and_evaluate_model(X_iris, y_iris, "Iris")
    train_and_evaluate_model(X_wine, y_wine, "Wine")
    train_and_evaluate_model(X_cancer, y_cancer, "Breast Cancer")

if __name__ == "__main__":
    main()

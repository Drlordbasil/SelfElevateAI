from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd

class StemCellAI:
    def __init__(self):
        self.model = LogisticRegression(solver='liblinear', multi_class='auto')

    def train(self, X_train, y_train):
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            raise Exception(f"An error occurred during training: {e}")

    def predict(self, X_test):
        try:
            return self.model.predict(X_test)
        except Exception as e:
            raise Exception(f"An error occurred during prediction: {e}")

    def save_model(self, filename):
        try:
            joblib.dump(self.model, filename)
        except Exception as e:
            raise Exception(f"An error occurred while saving the model: {e}")

    def load_model(self, filename):
        try:
            self.model = joblib.load(filename)
        except Exception as e:
            raise Exception(f"An error occurred while loading the model: {e}")

def main():
    try:
        wine_data = datasets.load_wine()
        df = pd.DataFrame(data=wine_data.data, columns=wine_data.feature_names)
        df['target'] = wine_data.target

        X = df.drop('target', axis=1)
        y = df['target']

        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        ai_model = StemCellAI()
        ai_model.train(X_train, y_train)
        ai_model.save_model("stemcell_model.pkl")  # Save model after training
        loaded_model = StemCellAI()  # Create a new instance to load the model
        loaded_model.load_model("stemcell_model.pkl")  # Load saved model
        predictions = loaded_model.predict(X_test)  # Use the loaded model for predictions

        accuracy = accuracy_score(y_test, predictions)
        print(f"Model accuracy: {accuracy}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

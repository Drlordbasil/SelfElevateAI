import numpy as np
import joblib
from sklearn.datasets import load_iris, load_wine, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class QLearningModel:
    def __init__(self, n_states, n_actions, learning_rate=0.01, gamma=0.9, epsilon=1.0, decay_rate=0.005, good_state_action_pairs=None):
        self.q_table = np.zeros((n_states, n_actions))
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.decay_rate = decay_rate
        self.state_action_frequency = np.zeros((n_states, n_actions))
        self.good_state_action_pairs = good_state_action_pairs if good_state_action_pairs is not None else set()

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.choice(len(self.q_table[state, :]))
        else:
            action = np.argmax(self.q_table[state, :])
        return action

    def learn(self, state, action, reward, next_state):
        self.state_action_frequency[state, action] += 1
        adjusted_reward = reward + (0.5 / (1 + self.state_action_frequency[state, action])) + (0.3 if (state, action) in self.good_state_action_pairs else 0)
        predict = self.q_table[state, action]
        target = adjusted_reward + self.gamma * np.max(self.q_table[next_state, :])
        self.q_table[state, action] += self.learning_rate / (1 + self.state_action_frequency[state, action] * self.decay_rate) * (target - predict)
        self.adjust_epsilon()

    def adjust_epsilon(self):
        self.epsilon = self.epsilon * (1 - self.decay_rate) if self.epsilon > 0.01 else 0.01
def train_and_evaluate_model(X, y, model_name):
    try:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        n_states = X_train.shape[0]
        n_actions = len(np.unique(y_train))

        model = QLearningModel(n_states, n_actions)

        for epoch in range(100):
            for i in range(len(X_train)):
                current_state = i
                action = model.choose_action(current_state)
                reward = 1 if action == y_train[i] else 0
                next_state = (i + 1) % len(X_train)
                model.learn(current_state, action, reward, next_state)

        accuracy = sum([1 if model.choose_action(i) == y_test[i] else 0 for i in range(len(X_test))]) / len(X_test)
        print(f"{model_name} model accuracy: {accuracy}")

        joblib.dump(model, f'{model_name}_model.pkl')

        loaded_model = joblib.load(f'{model_name}_model.pkl')
        predictions = [loaded_model.choose_action(i) for i in range(len(X_test))]
        print(f"{model_name} model predictions:", predictions)

    except Exception as e:
        print(f"An error occurred in {model_name} model processing: {e}")

def main():
    iris = load_iris()
    X_iris, y_iris = iris.data, iris.target

    wine = load_wine()
    X_wine, y_wine = wine.data, wine.target

    cancer = load_breast_cancer()
    X_cancer, y_cancer = cancer.data, cancer.target

    train_and_evaluate_model(X_iris, y_iris, "Iris")
    train_and_evaluate_model(X_wine, y_wine, "Wine")
    train_and_evaluate_model(X_cancer, y_cancer, "Breast Cancer")

if __name__ == "__main__":
    main()

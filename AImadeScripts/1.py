import numpy as np

class AdaptiveAI:
    def __init__(self, input_size, output_size):
        self.weights = np.random.rand(input_size, output_size)
        self.bias = np.random.rand(1, output_size)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def train(self, inputs, outputs, epochs):
        for _ in range(epochs):
            weighted_sum = np.dot(inputs, self.weights) + self.bias     
            activated_output = self.sigmoid(weighted_sum)

            error = outputs - activated_output
            adjustments = error * self.sigmoid_derivative(activated_output)

            self.weights += np.dot(inputs.T, adjustments)
            self.bias += np.sum(adjustments, axis=0, keepdims=True)     

    def predict(self, inputs):
        weighted_sum = np.dot(inputs, self.weights) + self.bias
        return self.sigmoid(weighted_sum)

# Example usage:
input_data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
output_data = np.array([[0], [1], [1], [0]])

adaptive_ai = AdaptiveAI(input_size=2, output_size=1)
adaptive_ai.train(input_data, output_data, epochs=10000)

print(adaptive_ai.predict(input_data))

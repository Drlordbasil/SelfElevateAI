import numpy as np
import logging
import datetime

class FoundationalAI:
    def __init__(self, input_size, output_size):
        self.weights = np.random.rand(input_size, output_size)
        self.bias = np.random.rand(output_size)
        self.version = 1  # Model version
        self.last_trained = datetime.datetime.now()  # Timestamp of last training

    def train(self, inputs, targets, learning_rate):
        try:
            predicted = np.dot(inputs, self.weights) + self.bias        
            errors = targets - predicted
            self.weights += learning_rate * np.dot(inputs.T, errors)    
            self.bias += learning_rate * np.mean(errors, axis=0)        
            self.last_trained = datetime.datetime.now()  # Update training timestamp
            self.version += 1  # Increment model version
            logging.info(f"Model trained successfully. Version: {self.version}, Timestamp: {self.last_trained}")
        except Exception as e:
            logging.error(f"Error occurred during training: {str(e)}")  

    def predict(self, inputs):
        try:
            return np.dot(inputs, self.weights) + self.bias
        except Exception as e:
            logging.error(f"Error occurred during prediction: {str(e)}")
            return None

    def save_model(self, path):
        try:
            np.savez(path, weights=self.weights, bias=self.bias, version=self.version, last_trained=self.last_trained)
            logging.info(f"Model saved to: {path}")
        except Exception as e:
            logging.error(f"Error occurred while saving model: {str(e)}")

    @staticmethod
    def load_model(path):
        try:
            data = np.load(path)
            model = FoundationalAI(input_size=data['weights'].shape[0], output_size=data['weights'].shape[1])
            model.weights = data['weights']
            model.bias = data['bias']
            model.version = data['version']
            model.last_trained = data['last_trained']
            logging.info(f"Model loaded from: {path}, Version: {model.version}, Last trained: {model.last_trained}")
            return model
        except Exception as e:
            logging.error(f"Error occurred while loading model: {str(e)}")
            return None

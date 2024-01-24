import numpy as np

class OrganicAICell:
    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size
        # Initialize layers with proper weight initialization method    
        # Here we use the Xavier initialization for weights
        self.layers = [
            np.random.randn(input_size, input_size) * np.sqrt(1. / input_size),
            np.random.randn(input_size, output_size) * np.sqrt(1. / input_size)
        ]

    def predict(self, inputs):
        inputs = np.asarray(inputs)
        if inputs.ndim != 1 or len(inputs) != self.input_size:
            raise ValueError(f"Expected input to be a 1D array of size {self.input_size}, but got {len(inputs)}.")

        return self._forward_propagation(inputs)

    def train(self, training_data, labels, epochs, learn_rate=0.01, verbose=False):
        training_data = np.asarray(training_data)
        labels = np.asarray(labels)

        if training_data.shape[1] != self.input_size:
            raise ValueError("Training data does not match input size of the model.")
        if labels.shape[1] != self.output_size:
            raise ValueError("Labels do not match output size of the model.")
        if training_data.shape[0] != labels.shape[0]:
            raise ValueError("Number of training examples must match number of labels.")

        for epoch in range(epochs):
            total_loss = 0.
            for i in range(training_data.shape[0]):
                outputs = self._forward_propagation(training_data[i])   
                error = labels[i] - outputs
                self._backpropagate(error, training_data[i], learn_rate)
                total_loss += np.mean(np.square(error))

            # Verbose logic
            if verbose and (epoch == 0 or (epoch + 1) % max(1, epochs // 10) == 0):
                average_loss = total_loss / training_data.shape[0]      
                print(f"Epoch {epoch + 1}/{epochs}, Loss: {average_loss:.4f}")

    def evolve(self, new_layer_size=None):
        if not self.layers:
            raise ValueError("Cannot evolve an AI cell with no existing layers.")

        new_layer_size = new_layer_size or np.random.randint(2, 5)      
        prev_output_size = self.layers[-1].shape[1]
        new_layer = np.random.randn(prev_output_size, new_layer_size) * np.sqrt(1. / prev_output_size)

        self.layers.append(new_layer)

    def _forward_propagation(self, inputs):
        activations = inputs
        for layer in self.layers:
            activations = self.activate(np.dot(activations, layer))     
        return activations

    def _backpropagate(self, error, input_data, learn_rate):
        # Calculate adjustments for the output layer
        delta = error * self.activate_derivative(self._forward_propagation(input_data))
        adjustment = learn_rate * np.outer(input_data, delta)

        # Update the last layer weights with the new adjustments        
        self.layers[-1] -= adjustment

        for i in reversed(range(len(self.layers) - 1)):
            layer = self.layers[i]
            next_layer = self.layers[i + 1]

            # Error for the current layer is the delta of the next layer dot the weight matrix of the next layer
            error = delta.dot(next_layer.T)

            # Activation for the current layer to calculate the delta   
            input_to_layer = np.dot(input_data, layer)
            delta = error * self.activate_derivative(input_to_layer)    

            if i != 0:
                # If it is not the input layer, prepare the input_data for next iteration
                input_data = self.activate(np.dot(input_data, self.layers[i-1]))

            # Calculate adjustment based on this layer's delta
            adjustment = learn_rate * np.outer(input_data, delta)       
            self.layers[i] -= adjustment

    @staticmethod
    def activate(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def activate_derivative(x):
        return OrganicAICell.activate(x) * (1 - OrganicAICell.activate(x))

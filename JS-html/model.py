import numpy as np

# Define the sigmoid activation function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Define the neural network class
class SimpleNeuralNetwork:
    def __init__(self):
        # Initialize weights with a random value
        self.weight = np.random.rand()

    def forward(self, x):
        # Compute the weighted sum and apply the activation function
        weighted_sum = self.weight * x
        output = sigmoid(weighted_sum)
        return output

# Instantiate the neural network
simple_nn = SimpleNeuralNetwork()

# Input value
input_value = 1.0

# Forward pass to get the predicted output
predicted_output = simple_nn.forward(input_value)

# Print the result
print("Input:", input_value)
print("Weight:", simple_nn.weight)
print("Predicted Output:", predicted_output)

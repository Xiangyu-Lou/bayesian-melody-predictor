import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.utils import shuffle


class MelodySelector:
    def __init__(self, window_size=32, batch_size=300):         # Adjusted window size and batch size depending on the memory
        # Define the GP kernel with specific length scale bounds, higher is more flexible
        kernel = RBF(length_scale=5, length_scale_bounds=(1e-8, 1e2))

        # Initialize the Gaussian Process Regressor
        self.gp = GaussianProcessRegressor(
            kernel=kernel,
            alpha=1e-9,                     # Small noise level to avoid numerical issues
            random_state=42,
            optimizer='fmin_l_bfgs_b',      # Optimizer to use, L-BFGS-B is efficient for GP
            n_restarts_optimizer=5,         # Number of restarts for optimizer
            normalize_y=True                # Normalize the output values
        )
        # Set the window size and batch size
        self.window_size = window_size
        self.batch_size = batch_size
        
    def prepare_training_data(self, data_frame):
        # Convert 'Normalized Pitch' data into a numpy array of floats
        data_frame['Data'] = data_frame['Normalized Pitch'].apply(lambda x: np.array([float(i) for i in x.split(',')]))

        # Initialize the training data
        X_train = []
        y_train = []

        # Loop through each row in the data frame
        for _, row in data_frame.iterrows():
            sequence = row['Data']
            # If the sequence is longer than the window size, we can apply a sliding window
            if len(sequence) > self.window_size:
                for i in range(0, len(sequence) - self.window_size):
                    # Add the windowed sequence to X_train and the next value to y_train
                    X_train.append(sequence[i:i + self.window_size])
                    y_train.append(sequence[i + self.window_size])

        # Convert the lists to numpy arrays for training
        return np.array(X_train), np.array(y_train)
    

    def train_model(self, X_train, y_train):
        # Number of epochs for training
        n_epochs = 3

        for epoch in range(n_epochs):

            print(f"Epoch {epoch + 1}/{n_epochs}")

            # Shuffle the training data before each epoch
            X_train, y_train = shuffle(X_train, y_train, random_state=42)
            
            # Loop through the training data in batches
            for start in range(0, len(X_train), self.batch_size):
                end = start + self.batch_size
                batch_X = X_train[start:end]
                batch_y = y_train[start:end]
                
                # Fit the GP model to the current batch
                self.gp.fit(batch_X, batch_y)

                # Print the progress of the training
                current_batch_size = start // self.batch_size + 1
                if current_batch_size % 100 == 0:
                    print(f"Batch Completed: {current_batch_size}/{len(X_train) // self.batch_size + 1}")
        

    def select_best_option(self, test_input, options):
        print("Option Evaluation:")
        option_scores = []
        
        # Loop through each option to evaluate its performance
        for idx, option in enumerate(options):
            # Initialize the sliding window with the last `window_size` values of the test input sequence
            current_window = test_input[-self.window_size:].copy()
            predictions = []
            prediction_stds = []
            
            # Predict each step of the option sequence
            for step in range(len(option)):
                window_input = current_window.reshape(1, -1)                            # Reshape the window for prediction
                pred_mean, pred_std = self.gp.predict(window_input, return_std=True)    # Predict the next value
                
                predictions.append(pred_mean[0])
                prediction_stds.append(pred_std[0])
                
                # Update the sliding window with the predicted value, 1 per step
                current_window = np.roll(current_window, -1)
                current_window[-1] = pred_mean[0]
            
            predictions = np.array(predictions)
            prediction_stds = np.array(prediction_stds)                                 # The standard deviation of the predictions
            
            # 1. prediction_error between the option and the predictions
            prediction_error = np.mean((predictions - option) ** 2)
            
            # 2. Variance difference between predicted and actual sequences
            variance_diff = abs(np.var(option) - np.var(predictions))
            
            # 3. Contour similarity (difference in pitch changes)
            pred_contour = np.diff(predictions)
            option_contour = np.diff(option)
            contour_similarity = np.mean((pred_contour - option_contour) ** 2)
            
            # 4. Confidence interval score (how many predictions fall within the 95% confidence interval)
            confidence_interval_width = 1.96 * prediction_stds                          # 95% confidence interval
            lower_bound = predictions - confidence_interval_width
            upper_bound = predictions + confidence_interval_width
            in_interval = np.logical_and(option >= lower_bound, option <= upper_bound)
            confidence_score = 1.0 - np.mean(in_interval)                               # penalize for points outside the interval
            
            # 5. Uncertainty penalty (average standard deviation of predictions)
            uncertainty_penalty = np.mean(prediction_stds)
            
            # Combine the scores with specific weights
            combined_score = (
                0.3 * prediction_error +        # Prediction error weight
                0.2 * variance_diff +           # Variance difference weight
                0.2 * contour_similarity +      # Contour similarity weight
                0.15 * confidence_score +       # Confidence score weight
                0.15 * uncertainty_penalty      # Uncertainty penalty weight
            )
            
            option_scores.append(combined_score)
            
            # Set the print options for numpy arrays
            np.set_printoptions(suppress=True, precision=6)
            # Print the evaluation results for each option
            print(f"\nOption {idx}:")
            print(f"Ground Truth: {option}")
            print(f"Predicted Sequence: {predictions}")
            print(f"Prediction Stds: {prediction_stds}")
            print(f"Mean Prediction Error: {prediction_error:.4f}")
            print(f"Variance Difference: {variance_diff:.4f}")
            print(f"Contour Similarity: {contour_similarity:.4f}")
            print(f"Confidence Score: {confidence_score:.4f}")
            print(f"Uncertainty Penalty: {uncertainty_penalty:.4f}")
            print(f"Combined Score: {combined_score:.4f}")
            print(f"Points in Confidence Interval: {np.sum(in_interval)}/{len(option)}")
            print("-" * 50)
        
        best_option_index = np.argmin(option_scores)
        print(f"\nSelected Option {best_option_index} with score {option_scores[best_option_index]:.4f}")
        
        return best_option_index

def main():
    # read training data
    training_data = pd.read_csv('dataset/gregorian_chant_pitch.csv')
    
    # initialize the melody selector
    melody_selector = MelodySelector()
    
    # prepare training data
    X_train, y_train = melody_selector.prepare_training_data(training_data)
    
    # train the model
    melody_selector.train_model(X_train, y_train)
    
    # Test data
    test_data = {
    "Test Input": [
    0.2500, 0.2500, 0.1786, 0.0714, 0.1786, 0.2500, 0.2500, 0.2500, 0.1786, 0.2500,
    0.3571, 0.4286, 0.3571, 0.3214, 0.2500, 0.1786, 0.2500, 0.2500, 0.2500, 0.2500,
    0.2500, 0.5000, 0.5000, 0.4286, 0.3571, 0.4286, 0.5000, 0.3571, 0.3214, 0.2500,
    0.1786, 0.2500, 0.2500, 0.2500, 0.2500, 0.3571, 0.3214, 0.2500, 0.3214, 0.3571,
    0.2500, 0.2500, 0.1429, 0.1786, 0.2500, 0.2500, 0.2500, 0.2500, 0.5000, 0.5000,
    0.4286, 0.3571, 0.4286, 0.5000, 0.5000, 0.4286, 0.3571, 0.4286, 0.3214, 0.2500,
    0.4286, 0.5000, 0.4286, 0.5000, 0.6071, 0.6071, 0.6071, 0.6071, 0.5000, 0.5000,
    0.3571, 0.4286, 0.5000, 0.4286, 0.5000, 0.5000, 0.4286, 0.5000, 0.5000, 0.4286,
    0.5000, 0.6071, 0.4286, 0.5000, 0.5000, 0.4286, 0.4286, 0.3571, 0.3214, 0.3571,
    0.3214, 0.3571, 0.4286, 0.5000, 0.4286, 0.4286, 0.4286, 0.4286, 0.4286, 0.5000,
    0.5000, 0.5000, 0.4286, 0.3571, 0.4286, 0.5000, 0.5000, 0.4286, 0.4286, 0.5000,
    0.4286, 0.4286, 0.5000, 0.4286, 0.4286, 0.5000, 0.6071, 0.5714, 0.6071, 0.6786,
    0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.4286, 0.5000, 0.6071, 0.5000, 0.3571,
    0.3571, 0.3571, 0.3214, 0.3571, 0.3571, 0.4286, 0.5000, 0.5000, 0.4286, 0.5000,
    0.4286, 0.3214
],
    # Options 0 is the correct continuation of the sequence
    "Option 0": [0.3571, 0.3214, 0.2500, 0.3571, 0.1786, 0.1786, 0.0714, 0.1786, 0.2500, 0.2500],
    "Option 1": [0.6786, 0.6071, 0.6071, 0.6786, 0.7500, 0.7857, 0.8571, 0.7857, 0.7500, 0.6786],
    "Option 2": [0.6071, 0.6786, 0.7500, 0.7857, 0.7857, 0.7857, 0.7500, 0.6786, 0.6071, 0.6071],
    "Option 3": [0.3214, 0.2500, 0.2500, 0.3214, 0.3214, 0.3571, 0.3214, 0.6071, 0.5000, 0.6786]

}
    
    # convert data to numpy arrays
    test_input = np.array(test_data["Test Input"])
    options = [
        np.array(test_data["Option 0"]),
        np.array(test_data["Option 1"]),
        np.array(test_data["Option 2"]),
        np.array(test_data["Option 3"])
    ]
    
    # select the best option
    best_option_index = melody_selector.select_best_option(test_input, options)
    
    print(f"\nBest option: Option {best_option_index}")

if __name__ == "__main__":
    main()

    
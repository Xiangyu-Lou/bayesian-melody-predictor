import numpy as np
import pandas as pd
from joblib import dump, load
import os
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.utils import shuffle


class MelodySelector:
    """
    Melody Selector class that trains a Gaussian Process model to predict the next note in a melody sequence.
    
    The model is trained on a dataset of melodies and can be used to select the best continuation of a given melody sequence from a set of options.
    """
    def __init__(self, window_size=32, batch_size=200, model_path='models/gp_5epoch.joblib'):
        # Define the GP kernel with specific length scale bounds, higher is more flexible
        kernel = RBF(length_scale=0.2, length_scale_bounds=(1e-4, 1e2))

        # Initialize the Gaussian Process Regressor
        self.gp = GaussianProcessRegressor(
            kernel=kernel,
            alpha=1e-9,
            random_state=42,
            optimizer='fmin_l_bfgs_b',
            n_restarts_optimizer=5,
            normalize_y=True,
        )
        # Set the window size and batch size
        self.window_size = window_size
        self.batch_size = batch_size
        self.model_path = model_path
        
    def prepare_training_data(self, data_frame):
        # Convert 'Normalized Pitch' data into a numpy array of floats
        # data_frame['Data'] = data_frame['normalized_pitch_sequence'].apply(lambda x: np.array([float(i) for i in x.strip('[]').split(',')]))
        data_frame['Data'] = data_frame['normalized_pitch_sequence'].apply(
            lambda x: np.array([round(float(i), 4) for i in x.strip('[]').split(',')])
        )

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
        n_epochs = 30

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

        # Save the model after training            
        print("\nSaving model...")
        dump(self.gp, self.model_path)
        print(f"Model saved to {self.model_path}")

    def load_model(self):
        """Load a previously trained model if it exists"""
        if os.path.exists(self.model_path):
            print(f"Loading existing model from {self.model_path}")
            self.gp = load(self.model_path)
            return True
        return False

    def select_best_option(self, test_input, options):
        # print("Option Evaluation:")
        option_scores = []
        
        # Loop through each option to evaluate its performance
        for idx, option in enumerate(options):
            # Initialize the sliding window with the last `window_size` values of the test input sequence
            current_window = test_input[-self.window_size:].copy()
            predictions = []
            prediction_stds = []
            
            # Predict each step of the option sequence
            for step in range(len(option)):
                window_input = current_window.reshape(1, -1)
                pred_mean, pred_std = self.gp.predict(window_input, return_std=True)
                
                predictions.append(pred_mean[0])
                prediction_stds.append(pred_std[0])
                
                # Update the sliding window with the predicted value, 1 per step
                current_window = np.roll(current_window, -1)
                current_window[-1] = pred_mean[0]
            
            predictions = np.array(predictions)
            prediction_stds = np.array(prediction_stds)
            
            # 1. prediction_error between the option and the predictions
            prediction_error = np.mean((predictions - option) ** 2)
            
            # 2. Variance difference between predicted and actual sequences
            variance_diff = abs(np.var(option) - np.var(predictions))
            
            # 3. Contour similarity (difference in pitch changes)
            pred_contour = np.diff(predictions)
            option_contour = np.diff(option)
            contour_similarity = np.mean((pred_contour - option_contour) ** 2)
            
            # 4. Confidence interval score (how many predictions fall within the 95% confidence interval)
            confidence_interval_width = 1.96 * prediction_stds
            lower_bound = predictions - confidence_interval_width
            upper_bound = predictions + confidence_interval_width
            in_interval = np.logical_and(option >= lower_bound, option <= upper_bound)
            confidence_score = 1.0 - np.mean(in_interval)
            
            # New Feature 1: Moving Average (MA) Similarity
            option_ma = np.convolve(option, np.ones(3) / 3, mode='valid')
            pred_ma = np.convolve(predictions, np.ones(3)/ 3, mode='valid')
            ma_similarity = np.mean((option_ma - pred_ma) ** 2)
            
            combined_score = (
                ma_similarity
            )

            option_scores.append(combined_score)
            
            # Set the print options for numpy arrays
            np.set_printoptions(suppress=True, precision=6)
        
        best_option_index = np.argmin(option_scores)
        
        return best_option_index

def main():
    # read training data
    training_data = pd.read_csv('dataset/dataset_train.csv')
    
    # initialize the melody selector
    melody_selector = MelodySelector()
    
    # prepare training data
    X_train, y_train = melody_selector.prepare_training_data(training_data)
    
    # train the model
    melody_selector.train_model(X_train, y_train)

if __name__ == "__main__":
    main()

    
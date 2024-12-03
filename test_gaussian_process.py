import numpy as np
import pandas as pd
from train_gaussian_process import MelodySelector

def evaluate_test_cases(test_data_path):
    # Initialize the melody selector
    melody_selector = MelodySelector()
    
    # Load the trained model
    if not melody_selector.load_model():
        raise Exception("No trained model found! Please run training first.")
    
    # Read test data
    test_df = pd.read_csv(test_data_path)
    
    total_cases = len(test_df)
    option1_selections = 0
    
    # Process each test case
    for idx, row in test_df.iterrows():
        # Convert input string to numpy array
        test_input = np.array([float(x) for x in row['input_pitch'].strip('[]').split(',')])
        
        # Convert options to numpy arrays
        options = []
        for i in (1, 10):  # Assuming 10 options columns
            option_col = f'option_{i}'
            option = np.array([float(x) for x in row[option_col].strip('[]').split(',')])
            options.append(option)
        
        # Select best option
        best_option_index = melody_selector.select_best_option(test_input, options)
        
        # Count if Option1 was selected
        if best_option_index == 1:
            option1_selections += 1
        
        # print(f"Test case {idx + 1}: Selected Option {best_option_index}")
    
    # Calculate probability
    option1_probability = option1_selections / total_cases
    print(f"\nResults:")
    print(f"Total test cases: {total_cases}")
    print(f"Option 1 selections: {option1_selections}")
    print(f"Probability of selecting Option 1: {option1_probability:.2%}")

if __name__ == "__main__":
    test_data_path = 'dataset/dataset_test_filled(rough).csv'  # test_path
    evaluate_test_cases(test_data_path)
import numpy as np
import pandas as pd
from train_gaussian_process import MelodySelector

TEST_DATASET_PATH = 'dataset/test.csv'
RESULT_PATH = 'result/output.csv'

def evaluate_test_cases(test_data_path, output_path):
    """
    Evaluate the test cases using the trained model and write the results to a CSV file.
    
    Args:
    - test_data_path: Path to the test data CSV file
    - output_path: Path to save the output CSV file
    
    Returns:
    - None
    """
    # Initialize the melody selector
    melody_selector = MelodySelector()
    
    # Load the trained model
    if not melody_selector.load_model():
        raise Exception("No trained model found! Please run training first.")
    
    # Read test data
    test_df = pd.read_csv(test_data_path)
    
    total_cases = len(test_df)
    option_selections = {f'option_{i}': 0 for i in range(1, 11)}

    results = []
    
    # Process each test case
    for idx, row in test_df.iterrows():
        # Convert input string to numpy array
        test_input = np.array([float(x) for x in row['input_pitch'].strip('[]').split(',')])
        
        # Convert options to numpy arrays
        options = []
        for i in range(1, 11):
            option_col = f'option_{i}'
            option = np.array([float(x) for x in row[option_col].strip('[]').split(',')])
            options.append(option)
        
        # Select best option
        best_option_index = melody_selector.select_best_option(test_input, options)
        option_selections[f'option_{best_option_index + 1}'] += 1
        
        # Store result
        results.append({
            'test_case': idx + 1,
            'selected_option': best_option_index + 1
        })
    
    # Calculate probability
    option1_probability = option_selections['option_1'] / total_cases
    print(f"\nResults:")
    print(f"Total test cases: {total_cases}")

    for i in range(1, 11):
        print(f"Option {i} selections: {option_selections[f'option_{i}']}")
    print(f"Probability of selecting Option 1: {option1_probability:.2%}")
    
    # Write results to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    evaluate_test_cases(TEST_DATASET_PATH, RESULT_PATH)
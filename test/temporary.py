import pandas as pd
import ast
import math

def denormalize_pitch_sequence(normalized_sequence):
    """
    Denormalize a list of normalized pitch values.

    Inputs:
        normalized_sequence (list): list of normalized pitch values (floats)

    Returns:
        denormalized_sequence (list): list of original pitch values (integers)
    """
    min_pitch = 21
    max_pitch = 108
    range_pitch = max_pitch - min_pitch

    denormalized_sequence = [int(round(normalized_value * range_pitch + min_pitch)) for normalized_value in normalized_sequence]
    return denormalized_sequence

def normalize_pitch_sequence(pitch_sequence):
    """
    Normalize a list of pitch values.

    Inputs:
        pitch_sequence (list): list of pitch values (integers)

    Returns:
        normalized_sequence (list): list of normalized pitch values (floats)
    """
    min_pitch = 55
    max_pitch = 84
    range_pitch = max_pitch - min_pitch

    normalized_sequence = [(pitch - min_pitch) / range_pitch for pitch in pitch_sequence]
    return normalized_sequence

if __name__ == "__main__":
    # Read the dataset
    file_path = "dataset_test_filled(rough).csv"
    data = pd.read_csv(file_path)

    data["pitch_sequence_original"] = data["normalized_pitch_sequence"].apply(lambda x: denormalize_pitch_sequence(ast.literal_eval(x)) if isinstance(x, str) and not pd.isna(x) else x)
    data["input_pitch_original"] = data["input_pitch"].apply(lambda x: denormalize_pitch_sequence(ast.literal_eval(x)) if isinstance(x, str) and not pd.isna(x) else x)

    
    # Parse and denormalize the `option_2` to `option_10` columns
    for i in range(1, 11):
        column_name = f'option_{i}'
        new_column_name = f'{column_name}_original'
        data[new_column_name] = data[column_name].apply(lambda x: denormalize_pitch_sequence(ast.literal_eval(x)) if isinstance(x, str) and not pd.isna(x) else x)

    
    min_value = float('inf')
    max_value = float('-inf')
    
    for i in range(1, 11):
        column_name = f'option_{i}_original'
        column_min = data[column_name].apply(lambda x: min(x) if isinstance(x, list) else float('inf')).min()
        column_max = data[column_name].apply(lambda x: max(x) if isinstance(x, list) else float('-inf')).max()
        min_value = min(min_value, column_min)
        max_value = max(max_value, column_max)

    print(f"Minimum value in option_1_original to option_10_original: {min_value}")
    print(f"Maximum value in option_1_original to option_10_original: {max_value}")
    
    data["pitch_sequence_normalized"] = data["pitch_sequence"].apply(lambda x: normalize_pitch_sequence(x) if isinstance(x, list) else x)
    data["input_pitch_normalized"] = data["input_pitch"].apply(lambda x: normalize_pitch_sequence(x) if isinstance(x, list) else x)
     
    # Normalize the `option_1_original` to `option_10_original` columns
    for i in range(1, 11):
        column_name = f'option_{i}_original'
        normalized_column_name = f'{column_name}_normalized'
        data[normalized_column_name] = data[column_name].apply(lambda x: normalize_pitch_sequence(x) if isinstance(x, list) else x)
        
        
    # Save the results back to a new CSV file
    output_file_path = "dataset_test_denormalized.csv"
    data.to_csv(output_file_path, index=False)
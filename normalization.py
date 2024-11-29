import pandas as pd

def normalize_pitch_data(input_file_path, output_file_path, min_value=55, max_value=83):
    """
    Normalize pitch data in the input CSV file using a global standard and save the result to an output CSV file.

    Args:
        input_file_path (str): Path to the input CSV file containing pitch data.
        output_file_path (str): Path to save the output CSV file with normalized pitch data.
        min_value (int): The minimum value used for normalization (default is 55).
        max_value (int): The maximum value used for normalization (default is 83).

    Returns:
        None
    """
    # Read the input CSV file
    data = pd.read_csv(input_file_path)

    # Define a normalization function
    def normalize(pitch_data, min_val, max_val):
        pitches = list(map(int, pitch_data.split(',')))
        normalized = [(p - min_val) / (max_val - min_val) for p in pitches]
        return ','.join(map(str, normalized))

    # Apply the normalization function to the Pitch Data column
    data['Normalized Pitch Data'] = data['Pitch Data'].apply(
        lambda x: normalize(x, min_value, max_value)
    )

    # Save the normalized data to the output file
    data.to_csv(output_file_path, index=False)

    print(f"Normalized pitch data has been saved to {output_file_path}.")

    
if __name__ == "__main__":
    input_file_path = "dataset/gregorian_chant_pitch.csv"
    output_file_path = "dataset/gregorian_chant_pitch_normalized.csv"
    normalize_pitch_data(input_file_path, output_file_path)
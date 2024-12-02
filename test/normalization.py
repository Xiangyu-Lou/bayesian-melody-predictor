import pandas as pd

def normalize_pitch_data(file_path, input_colum_name, min_value, max_value):
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
    df = pd.read_csv(file_path)

    # Apply the normalization directly within the lambda function
    df['Normalized Pitch'] = df[input_colum_name].apply(
        lambda x: ','.join([f"{(int(p) - min_value) / (max_value - min_value):.4f}" for p in x.split(',')])
    )

    # Save the normalized data to the output file
    df.to_csv(file_path, index=False)

    print(f"Normalized pitch data has been saved to {file_path}.")
    
def reverse_normalization(file_path, colum_name, min_value, max_value):
    """
    Reverse the normalization process to convert normalized values back to their original pitches.

    Args:
        file_path (str): Path to the CSV file containing normalized pitch data.
        min_value (int): The minimum value used during normalization (default is 55).
        max_value (int): The maximum value used during normalization (default is 83).

    Returns:
        None
    """
    # Read the input CSV file
    df = pd.read_csv(file_path)

    # Apply the reverse normalization
    df['Reverse Normalization'] = df[colum_name].apply(
        lambda x: ','.join([str(int(round(float(p) * (max_value - min_value) + min_value))) for p in x.split(',')])
    )

    # Save the data with reverse normalization to the output file
    df.to_csv(file_path, index=False)

    print(f"Reverse normalized pitch data has been saved to {file_path}.")

def normalize_multiple_columns(file_path, columns, min_value, max_value):
    """
    Normalize multiple columns of data in the input CSV file using global standards and save the result to a new output CSV file.

    Args:
        file_path (str): Path to the input CSV file containing data to be normalized.
        columns (list): List of column names to normalize.
        min_values (int): The minimum value used during normalization.
        max_values (int): The minimum value used during normalization.

    Returns:
        None
    """
    # Read the input CSV file
    df = pd.read_csv(file_path)

    # Normalize each column and add a new column with the normalized values
    for col in columns:
        df[f'normalized_{col}'] = df[col].apply(
            lambda x: ','.join([f"{(int(p) - min_value) / (max_value - min_value):.4f}" for p in x.split(',')])
        )

    # Save the data with normalized columns to the output file
    df.to_csv(file_path, index=False)

    print(f"Normalized data for columns {columns} has been saved to {file_path}.")
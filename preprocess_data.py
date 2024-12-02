import pandas as pd
import ast
from sklearn.model_selection import train_test_split

def melody_to_pitch_sequence(melody, note_mapping):
    """
    Convert melody string directly into a pitch sequence without generating a MIDI file.

    Inputs:
        melody (str): melody string
        note_mapping (dict): mapping of note characters to MIDI note numbers

    Returns:
        pitch_sequence (list): list of MIDI pitch values (integers)
    """
    if '6------6' in melody:
        return 'skip'

    pitch_sequence = []
    i = 0
    while i < len(melody):
        if melody[i:i+3] == '---':
            pitch_sequence.append(None)
            i += 3
        elif melody[i:i+2] == '--': 
            pitch_sequence.append(None)
            i += 2
        elif melody[i] == '-':
            pitch_sequence.append(None)
            i += 1
        elif melody[i].lower() in note_mapping:
            note = note_mapping[melody[i].lower()]
            if isinstance(note, int):
                pitch_sequence.append(note)
            i += 1
        elif melody[i:i+4] == '---4':
            break
        else:
            i += 1

    pitch_sequence = [pitch for pitch in pitch_sequence if pitch is not None]

    return pitch_sequence

def normalize_pitch_sequence(pitch_sequence):
    """
    Normalize a list of pitch values.

    Inputs:
        pitch_sequence (list): list of pitch values (integers)

    Returns:
        normalized_sequence (list): list of normalized pitch values (floats)
    """
    min_pitch = 21
    max_pitch = 108
    range_pitch = max_pitch - min_pitch

    normalized_sequence = [(pitch - min_pitch) / range_pitch for pitch in pitch_sequence]
    return normalized_sequence

def clean_dataset(df):
    """
    Clean the dataset by removing rows with 'skip' in the melody column and reindexing.

    Inputs:
        df (DataFrame): input DataFrame

    Returns:
        DataFrame: cleaned DataFrame
    """
    # Remove rows where the melody column contains 'skip'
    df = df[df['pitch_sequence'] != 'skip']

    # Convert pitch_sequence from string representation of list to actual list
    df['pitch_sequence'] = df['pitch_sequence'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    # Remove rows where the pitch_sequence list length is less than 40
    df = df[df['pitch_sequence'].apply(lambda x: len(x) >= 40 if isinstance(x, list) else False)]

    df.reset_index(drop=True, inplace=True)

    return df

def split_dataset(df, test_size=0.3, seed=522117):
    """
    Split the dataset into training and testing sets.

    Inputs:
        df (DataFrame): input DataFrame
        test_size (float): proportion of the dataset to include in the test split
        random_state (int): random seed for reproducibility

    Returns:
        train_df (DataFrame): training set DataFrame
        test_df (DataFrame): testing set DataFrame
    """
    # Split the dataset
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=seed)

    return train_df, test_df

def process_test_dataframe(df_test):
    """
    Process the test DataFrame by adding new columns and split the normalized_pitch_sequence to input_pitch and option_1.

    Inputs:
        df_test (DataFrame): input test DataFrame

    Returns:
        DataFrame: processed test DataFrame with new columns
    """
    # Add new columns with default values
    df_test['input_pitch'] = None
    for i in range(1, 11):
        df_test[f'option_{i}'] = None

    # Process each row to split normalized_pitch_sequence
    for index, row in df_test.iterrows():
        normalized_sequence = row['normalized_pitch_sequence']
        if isinstance(normalized_sequence, str):
            normalized_sequence = ast.literal_eval(normalized_sequence)

        input_pitch = normalized_sequence[:32]
        option_1 = normalized_sequence[32:40]
        df_test.at[index, 'input_pitch'] = input_pitch
        df_test.at[index, 'option_1'] = option_1

    return df_test
    
if __name__ == "__main__":
    # note mapping
    note_mapping = {
        '9': 55,  # G3
        'a': 57,  # A3
        'b': 59,  # B3
        'c': 60,  # C4
        'd': 62,  # D4
        'e': 64,  # E4
        'f': 65,  # F4
        'g': 67,  # G4
        'h': 69,  # A4
        'j': 71,  # B4
        'k': 72,  # C5
        'l': 74,  # D5
        'm': 76,  # E5
        'n': 77,  # F5
        'o': 79,  # G5
        'p': 81,  # A5
        'q': 83,  # B5
        'r': 84,  # C6
        's': 86,  # D6
        '---4': 'end',
        '---3': 'end',
        '1--': 'start',
        '---': 'word_pause',
        '--': 'syllable_pause',
        '-': 'neume_pause', 
        '7': 'line_break',
        '777': 'page_break',
    }
    
    # Read the dataset
    df_main = pd.read_csv('dataset/dataset_all.csv')

    # Process each melody and add the pitch sequence to a new column
    df_main['pitch_sequence'] = df_main['melody'].apply(lambda x: melody_to_pitch_sequence(x, note_mapping))

    # Clean the dataset by removing rows with 'skip' in the melody column and reindexing
    df_cleaned = clean_dataset(df_main)
    
    # Normalize the pitch sequences
    df_cleaned['normalized_pitch_sequence'] = df_main['pitch_sequence'].apply(lambda x: normalize_pitch_sequence(x) if isinstance(x, list) else x)
    
    # Save the cleaned dataframe to a new CSV file
    df_cleaned.to_csv('dataset/dataset_all.csv', index=False)
    
    # # Split the dataset into training and testing sets
    df_train, df_test = split_dataset(df_cleaned)

    # Process the test DataFrame by adding new columns and split the normalized_pitch_sequence to input_pitch and option_1
    df_test = process_test_dataframe(df_test)

    # # Save the training and testing sets to CSV files
    df_train.to_csv('dataset/dataset_train.csv', index=False)
    df_test.to_csv('dataset/dataset_test.csv', index=False)    
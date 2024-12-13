import pandas as pd
def validate_option_1(data):
    """
    Validate that for each row:
    a) `option_1` is a slice of `normalized_pitch_sequence` with start_index = 32 and end_index = 40, OR
    b) If `normalized_pitch_sequence` has fewer than 40 values, `option_1` matches the last 8 notes of `normalized_pitch_sequence`.
    """
    validation_results = []  
    for index, row in data.iterrows():
        try:
            normalized_sequence = eval(row['normalized_pitch_sequence'])
            option_1_sequence = eval(row['option_1'])
            if len(normalized_sequence) >= 40:
                is_valid = normalized_sequence[32:40] == option_1_sequence
            else:
                is_valid = normalized_sequence[-8:] == option_1_sequence
            validation_results.append((index, is_valid))
        except (SyntaxError, TypeError):
            validation_results.append((index, False))
    return validation_results
data = pd.read_csv('updated_pop.csv')
validation_results = validate_option_1(data)
validation_df = pd.DataFrame(validation_results, columns=['Row', 'Is_Valid'])
validation_df.to_csv('validation_results.csv', index=False)
print(validation_df)

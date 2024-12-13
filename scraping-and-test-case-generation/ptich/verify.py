import pandas as pd
import ast
import sys
import argparse
def parse_list(cell):
    """
    Safely parse a string representation of a list into an actual Python list.
    Returns None if parsing fails.
    """
    try:
        return ast.literal_eval(cell)
    except (ValueError, SyntaxError):
        return None
def validate_csv(input_file):
    """
    Validates the 'option_1' column in the CSV file based on the 'pitch_sequence' column.
    Conditions:
    a) If 'pitch_sequence' has 40 or more numbers, 'pitch_sequence[32:40]' must match 'option_1'.
    b) If 'pitch_sequence' has fewer than 40 numbers, the last 8 values of 'pitch_sequence' must match 'option_1'.
    Prints a summary of the validation results.
    """
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
        sys.exit(1)
    total_rows = len(df)
    matched_rows = 0
    mismatched_rows = 0
    failed_parsing = 0
    mismatches = []
    for index, row in df.iterrows():
        pitch_seq_str = row.get('pitch_sequence', '')
        option_1_str = row.get('option_1', '')
        pitch_seq = parse_list(pitch_seq_str)
        option_1 = parse_list(option_1_str)
        if pitch_seq is None or option_1 is None:
            failed_parsing += 1
            mismatches.append({
                'Row': index + 2,  
                'Issue': 'Parsing error in pitch_sequence or option_1'
            })
            continue
        if len(pitch_seq) >= 40:
            expected_option_1 = pitch_seq[32:40]
            condition = 'A (pitch_sequence[32:40] matches option_1)'
        else:
            expected_option_1 = pitch_seq[-8:] if len(pitch_seq) >= 8 else pitch_seq
            condition = 'B (last 8 of pitch_sequence matches option_1)'
        if expected_option_1 == option_1:
            matched_rows += 1
        else:
            mismatched_rows += 1
            mismatches.append({
                'Row': index + 2,  
                'Condition': condition,
                'Expected option_1': expected_option_1,
                'Actual option_1': option_1
            })
    print(f"\nValidation Summary for '{input_file}':")
    print(f"---------------------------------------")
    print(f"Total Rows Checked           : {total_rows}")
    print(f"Rows Passed Validation      : {matched_rows}")
    print(f"Rows Failed Validation      : {mismatched_rows}")
    print(f"Rows with Parsing Issues    : {failed_parsing}\n")
    if mismatched_rows > 0:
        print("Detailed Mismatches:")
        print("--------------------")
        for mismatch in mismatches:
            row_num = mismatch['Row']
            issue = mismatch.get('Issue', '')
            condition = mismatch.get('Condition', '')
            expected = mismatch.get('Expected option_1', '')
            actual = mismatch.get('Actual option_1', '')
            if issue:
                print(f"Row {row_num}: {issue}")
            else:
                print(f"Row {row_num}: {condition}")
                print(f"  Expected option_1: {expected}")
                print(f"  Actual option_1  : {actual}\n")
    else:
        print("All rows passed the validation!")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate 'option_1' in a CSV file based on 'pitch_sequence'.")
    parser.add_argument('input_csv', help='Path to the input CSV file.')
    args = parser.parse_args()
    validate_csv(args.input_csv)

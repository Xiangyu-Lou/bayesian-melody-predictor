import csv
import ast
def parse_float_sequence(seq_str):
    return ast.literal_eval(seq_str.strip())
def build_conversion_map(input_file):
    """Build a dictionary mapping normalized values (float) to pitch values (int)."""
    conversion_map = {}
    with open(input_file, "r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            pitch_sequence = ast.literal_eval(row["pitch_sequence"])
            normalized_sequence = ast.literal_eval(row["normalized_pitch_sequence"])
            for norm, pitch in zip(normalized_sequence, pitch_sequence):
                conversion_map[norm] = pitch
    return conversion_map
def find_nearest(value, conversion_map):
    """Find the nearest key in the conversion map for a given normalized value."""
    return min(conversion_map.keys(), key=lambda k: abs(k - value))
def apply_conversion(row, conversion_map, columns):
    """Convert normalized values to pitch values in the specified columns using nearest-match logic."""
    for column in columns:
        if column in row and row[column].strip():
            normalized_list = ast.literal_eval(row[column])
            converted_list = [conversion_map.get(find_nearest(norm, conversion_map), norm) for norm in normalized_list]
            row[column] = str(converted_list)
def main(input_file="output_2.csv", output_file="updated_pop.csv"):
    conversion_map = build_conversion_map(input_file)
    with open(input_file, "r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
        fieldnames = reader.fieldnames
    columns_to_update = ["normalized_pitch_sequence", "input_pitch"] + [f"option_{i}" for i in range(1, 11)]
    for row in rows:
        apply_conversion(row, conversion_map, columns_to_update)
    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Conversion complete. Updated data saved to {output_file}")
if __name__ == "__main__":
    main()

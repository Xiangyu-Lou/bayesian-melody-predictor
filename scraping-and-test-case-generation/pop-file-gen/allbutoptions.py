import pickle
import csv
class Melody:
    def __init__(self, name, pitch_sequence):
        self.name = name
        self.pitch_sequence = pitch_sequence
    def __repr__(self):
        return f"Melody(name={self.name}, pitch_sequence={self.pitch_sequence})"
class MelodyStore:
    def __init__(self):
        self.melodies = []
    def add_melody(self, melody):
        self.melodies.append(melody)
    def __repr__(self):
        return f"MelodyStore(melodies={self.melodies})"
def build_normalization_map(input_csv_file):
    """Build a dictionary mapping pitch values to normalized values."""
    normalization_map = {}
    with open(input_csv_file, "r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            try:
                pitch_sequence = [int(x.strip()) for x in row["pitch_sequence"].split(",") if x.strip().isdigit()]
                normalized_sequence = [float(x.strip()) for x in row["normalized_pitch_sequence"].strip('[]').split(",") if x.strip()]
                for pitch, norm in zip(pitch_sequence, normalized_sequence):
                    normalization_map[pitch] = norm
            except (KeyError, ValueError):
                print(f"Skipping row due to invalid data: {row}")
    return normalization_map
def filter_and_transform_csv(input_csv_file, output_csv_file):
    """Filter rows and add new columns to the CSV file."""
    with open(input_csv_file, "r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames or []
        extended_fieldnames = fieldnames[:]
        if "option_1" in extended_fieldnames:
            idx = extended_fieldnames.index("option_1")
            extended_fieldnames.insert(idx, "input_pitch")
            for i in range(2, 11):
                extended_fieldnames.append(f"option_{i}")
        with open(output_csv_file, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=extended_fieldnames)
            writer.writeheader()
            for row in reader:
                if row.get("option_1") == "NOT_ENOUGH_NOTES":
                    continue
                normalized_sequence = [float(x.strip()) for x in row["normalized_pitch_sequence"].strip('[]').split(",") if x.strip()]
                if len(normalized_sequence) > 8:
                    row["input_pitch"] = str(normalized_sequence[:-8])
                else:
                    row["input_pitch"] = "[]"
                for i in range(2, 11):
                    row[f"option_{i}"] = ""
                writer.writerow(row)
    print(f"Filtered and transformed data saved to {output_csv_file}")
def main():
    input_csv_file = "output.csv"  
    output_csv_file = "output_2.csv"  
    filter_and_transform_csv(input_csv_file, output_csv_file)
    print(f"CSV file saved to {output_csv_file}")
if __name__ == "__main__":
    main()

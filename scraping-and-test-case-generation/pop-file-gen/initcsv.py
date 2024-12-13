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
def build_conversion_map(input_csv_file):
    """Build a dictionary mapping pitch values to normalized values from input.csv."""
    conversion_map = {}
    with open(input_csv_file, "r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            pitch_sequence = [int(x.strip()) for x in row["pitch_sequence"].strip("[]").split(",") if x.strip().isdigit()]
            normalized_sequence = [float(x.strip()) for x in row["normalized_pitch_sequence"].strip("[]").split(",") if x.strip()]
            for pitch, norm in zip(pitch_sequence, normalized_sequence):
                conversion_map[pitch] = norm
    return conversion_map
def normalize_pitch_sequence(pitch_sequence, conversion_map):
    """Convert pitch values to normalized values using the conversion map."""
    return [conversion_map.get(pitch, 0.0) for pitch in pitch_sequence]
def save_to_csv_from_pickle(pickle_file, normalization_map, output_csv_file):
    """Process melodies.pkl and generate the output CSV file."""
    with open(pickle_file, 'rb') as file:
        melody_store = pickle.load(file)
    fieldnames = ["melody", "pitch_sequence", "normalized_pitch_sequence", "option_1"]
    filled_option_1_count = 0
    with open(output_csv_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for melody in melody_store.melodies:
            pitch_sequence = melody.pitch_sequence
            normalized_sequence = normalize_pitch_sequence(pitch_sequence, normalization_map)
            if len(normalized_sequence) > 12:
                option_1 = normalized_sequence[-8:]
                filled_option_1_count += 1
            else:
                option_1 = "NOT_ENOUGH_NOTES"
            writer.writerow({
                "melody": melody.name,
                "pitch_sequence": pitch_sequence,
                "normalized_pitch_sequence": normalized_sequence,
                "option_1": option_1,
            })
    print(f"Total filled option_1 entries: {filled_option_1_count}")
    print(f"CSV file saved to {output_csv_file}")
def main():
    pickle_file = "melodies_midi.pkl"  
    input_csv_file = "input.csv"  
    output_csv_file = "output.csv"  
    normalization_map = build_conversion_map(input_csv_file)
    save_to_csv_from_pickle(pickle_file, normalization_map, output_csv_file)
if __name__ == "__main__":
    main()

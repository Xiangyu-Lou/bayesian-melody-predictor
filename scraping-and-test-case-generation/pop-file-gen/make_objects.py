import pickle
import re
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
def parse_file(file_path):
    melody_store = MelodyStore()
    with open(file_path, 'r') as file:
        for line in file:
            match = re.match(r"(\S+):\s*[\u201c\"](.+?)[\u201d\"]", line.strip())
            if match:
                name = match.group(1)
                try:
                    sequence_str = match.group(2).replace(' ', ',')
                    pitch_sequence = [int(p) for p in sequence_str.split(',') if p.strip().isdigit()]
                    melody = Melody(name, pitch_sequence)
                    melody_store.add_melody(melody)
                except ValueError as e:
                    print(f"Error processing line: {line.strip()} - {e}")
    return melody_store
def save_to_pickle(data, pickle_file):
    with open(pickle_file, 'wb') as file:
        pickle.dump(data, file)
if __name__ == "__main__":
    input_file = "pitchsequences.txt"  
    output_pickle_file = "melodies.pkl"
    melody_store = parse_file(input_file)
    save_to_pickle(melody_store, output_pickle_file)
    print(f"All melodies have been saved to {output_pickle_file}")

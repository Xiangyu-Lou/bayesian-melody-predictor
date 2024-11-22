import pretty_midi
import csv
import os

def extract_pitch(output_folder, output_csv):
    """
    Extract pitch data from all MIDI files in the specified folder and write to CSV.

    Inputs:
        output_folder (str): path to folder containing MIDI files
        output_csv (str): path to output CSV file
    
    Returns:
        None
    """
    with open(output_csv, "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["File Name", "Pitch Data"])

    for i in range(1, 1584):
        filename = f"{i}.mid"
        midi_file_path = os.path.join(output_folder, filename)
        
        if os.path.exists(midi_file_path):
            print(f"Processing file: {midi_file_path}")
            midi_data = pretty_midi.PrettyMIDI(midi_file_path)

            pitch_sequence = []
            
            for instrument in midi_data.instruments:
                for note in instrument.notes:
                    pitch_sequence.append(note.pitch)
            
            if pitch_sequence:
                with open(output_csv, "a", newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    pitch_data_str = ','.join(map(str, pitch_sequence))
                    csvwriter.writerow([filename, pitch_data_str])
                print(f"Processed {midi_file_path} and added pitch data to {output_csv}")
            else:
                print(f"No pitch data found in file: {midi_file_path}")
        else:
            print(f"File {midi_file_path} does not exist.")

    print("Processing complete.")

if __name__ == "__main__":
    output_folder = "dataset/gregorian_chant_pitch_midi"
    output_csv = "dataset/gregorian_chant_pitch.csv"
    extract_pitch(output_folder, output_csv)
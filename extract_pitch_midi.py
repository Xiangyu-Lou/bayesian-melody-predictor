import pretty_midi
import csv
import os

def extract_pitch(input_folder, output_csv):
    """
    Extract pitch data from all MIDI files in the specified folder and write to CSV.

    Inputs:
        input_folder (str): path to folder containing MIDI files
        output_csv (str): path to output CSV file
    
    Returns:
        None
    """
    with open(output_csv, "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Index", "Pitch"])

    # count number of MIDI files in the folder
    midi_files = [f for f in os.listdir(input_folder) if f.endswith('.mid')]
    file_count = len(midi_files)
    valid_index = 1
    
    for index in range(1, file_count + 1):
        filename = f"{index}.mid"
        midi_file_path = os.path.join(input_folder, filename)
        
        if os.path.exists(midi_file_path):
            print(f"Processing file: {midi_file_path}")
            midi_data = pretty_midi.PrettyMIDI(midi_file_path)

            pitch_sequence = []
            
            for instrument in midi_data.instruments:
                for note in instrument.notes:
                    pitch_sequence.append(note.pitch)
                    
            # Debugging: Print the length of pitch_sequence
            print(f"Length of pitch sequence for {midi_file_path}: {len(pitch_sequence)}")
                
            if len(pitch_sequence) >= 32:
                with open(output_csv, "a", newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    pitch_data_str = ','.join(map(str, pitch_sequence))
                    csvwriter.writerow([valid_index, pitch_data_str])
                print(f"Processed {midi_file_path} and added pitch data to {output_csv}")
                valid_index += 1
            else:
                print(f"Pitch sequence in file {midi_file_path} is shorter than 32 and was discarded.")
        else:
            print(f"File {midi_file_path} does not exist.")

    print("Processing complete.")

if __name__ == "__main__":
    midis_files_path = "dataset/gregorian_chant_pitch_midi"
    output_csv = "dataset/gregorian_chant_pitch.csv"
    extract_pitch(midis_files_path, output_csv)
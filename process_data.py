import pandas as pd
import convert_transcripts as ct
import extract_pitch_midi as epm
import normalization as norm

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

origional_data_path = "dataset/gregorian_chant_origional.csv"
midis_files_path = "dataset/gregorian_chant_pitch_midi"
pitch_data_path = "dataset/gregorian_chant_pitch.csv"
test_data_path = "dataset/test_dataset.csv"

# read transcription data
df_origional = pd.read_csv(origional_data_path)

# convert transcriptions to MIDI files
output_index = 1
for index, row in df_origional.iterrows():
    melody = row['volpiano']
    if pd.isna(melody):
        print(f"Sample {index} is missing, skipping.")
        continue
    melody = str(melody)
    if ct.parse_melody(melody, note_mapping = note_mapping) == 'skip':
        print(f"Sample {index} is incomplete, skipping.")
        continue
    output_file = f"dataset/gregorian_chant_pitch_midi/{output_index}.mid"
    ct.create_midi(melody, note_mapping = note_mapping, output_file = output_file)
    output_index += 1
    
# extract pitch data from MIDI files
epm.extract_pitch(input_folder = midis_files_path, output_csv = pitch_data_path)

# extract the minimum and maximum pitch values
df_pitch = pd.read_csv(pitch_data_path)

all_pitches = []
for index, row in df_pitch.iterrows():
    pitches = list(map(int, row['Pitch'].split(',')))
    all_pitches.extend(pitches)

min_value = min(all_pitches)
max_value = max(all_pitches)
print(f"Minimum pitch value: {min_value}")
print(f"Maximum pitch value: {max_value}")

# normalize pitch data
norm.normalize_pitch_data(file_path = pitch_data_path, colum_name = 'Pitch', min_value = min_value, max_value = max_value)

# reverse normalization
# norm.reverse_normalization(file_path = test_data_path, colum_name = , min_value = min_value, max_value = max_value)
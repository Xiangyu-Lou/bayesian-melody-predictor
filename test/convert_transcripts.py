import pandas as pd
from mido import Message, MidiFile, MidiTrack

def parse_melody(melody, note_mapping):
    """
    Parse melody string into notes and durations.

    Inputs:
        melody (str): melody string
        note_mapping (dict): mapping of note characters to MIDI note numbers

    Returns:
        notes (list): list of tuples (note, duration)
    """
    # check if melody is complete and longer engough
    if '6------6' in melody:
        return 'skip'
    
    notes = []
    i = 0
    duration_map = {
        'word_pause': 0,
        'syllable_pause': 0,
        'neume_pause': 0,
    }
    while i < len(melody):
        if melody[i:i+3] == '---':
            notes.append((None, duration_map['word_pause']))
            i += 3
        elif melody[i:i+2] == '--': 
            notes.append((None, duration_map['syllable_pause']))
            i += 2
        elif melody[i] == '-':
            notes.append((None, duration_map['neume_pause']))
            i += 1
        elif melody[i].lower() in note_mapping:
            note = note_mapping[melody[i].lower()]
            if isinstance(note, int):
                notes.append((note, 480))
            i += 1
        elif melody[i:i+4] == '---4':
            break
        else:
            i += 1

    return notes

def create_midi(melody, note_mapping, output_file="output.mid"):
    """
    Create MIDI file.
    
    Inputs:
        melody (str): melody string
        output_file (str): output file path
        
    Returns:
        Saves MIDI file to output_file.
    """
    notes = parse_melody(melody, note_mapping)
    
    if notes == 'skip':
        print(f"{output_file} is incomplete, skipping.")
        return

    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)

    for note, duration in notes:
        if note is not None and isinstance(note, int):
            track.append(Message('note_on', note=note, velocity=64, time=0))
            track.append(Message('note_off', note=note, velocity=64, time=duration))
        elif note is None:  # 停顿
            track.append(Message('note_off', note=0, velocity=0, time=duration))

    midi.save(output_file)
    print(f"MIDI file saved as {output_file}")

if __name__ == '__main__':
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
    
    # read data
    df = pd.read_csv('dataset/gregorian_chant_origional.csv')

    # traverse all samples
    output_index = 1
    for index, row in df.iterrows():
        melody = row['volpiano']
        if pd.isna(melody):
            print(f"Sample {index} is missing, skipping.")
            continue
        melody = str(melody)
        if parse_melody(melody, note_mapping = note_mapping) == 'incomplete':
            print(f"Sample {index} is incomplete, skipping.")
            continue
        output_file = f"dataset/gregorian_chant_pitch_midi/{output_index}.mid"
        create_midi(melody, output_file)
        output_index += 1
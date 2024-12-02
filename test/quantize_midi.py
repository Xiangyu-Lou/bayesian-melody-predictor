import pretty_midi

def quantize_midi(input_midi_path, output_midi_path, quantization_level=1/32):
    """
    Quantizes the timing of notes in a MIDI file and saves the quantized MIDI file.

    Parameters
    ----------
    input_midi_path : str
        The file path of the input MIDI file to be quantized.
    output_midi_path : str
        The file path where the quantized MIDI file will be saved.
    quantization_level : float, optional
        The time grid resolution for quantization

    Returns
    -------
    None
        The function saves the quantized MIDI file to the output_midi_path.
    """
    midi_data = pretty_midi.PrettyMIDI(input_midi_path)
    
    # Process each instrument in the MIDI file
    for instrument in midi_data.instruments:
        # Process each note in the instrument
        for note in instrument.notes:
            original_start = note.start
            original_end = note.end
            # Quantize the start and end times to the nearest time grid
            quantized_start = round(original_start / quantization_level) * quantization_level
            quantized_end = round(original_end / quantization_level) * quantization_level
            # Make sure the note duration is not too short
            min_length = quantization_level / 2
            note.start = quantized_start
            note.end = max(quantized_start + min_length, quantized_end)

    # Save
    midi_data.write(output_midi_path)
    print(f"Quantization complete!")
    
def is_quantized(midi_path, quantization_level=1/16, tolerance=1e-6):
    """
    Test if the MIDI file is quantized successfully and output the information of unaligned notes.
    
    Parameters
    ----------
    midi_path : str
        The file path of the MIDI file to be tested.
    quantization_level : float, optional
        The time grid resolution for quantization
    tolerance : float, optional
        The tolerance for floating-point comparison
    """
    midi_data = pretty_midi.PrettyMIDI(midi_path)

    total_notes = 0
    unaligned_notes = 0

    print(f"test file: {midi_path}")
    print(f"quantization level: 1/{int(1/quantization_level)}")

    for instrument in midi_data.instruments:
        for note in instrument.notes:
            total_notes += 1
            # test if the start and end times of the note are aligned to the time grid
            start_aligned = abs(note.start / quantization_level - round(note.start / quantization_level)) < tolerance
            end_aligned = abs(note.end / quantization_level - round(note.end / quantization_level)) < tolerance

            if not start_aligned or not end_aligned:
                unaligned_notes += 1
                start_diff = note.start / quantization_level - round(note.start / quantization_level)
                end_diff = note.end / quantization_level - round(note.end / quantization_level)
                print(f"unaligned note - start time: {note.start:.6f}, end time: {note.end:.6f}")
                print(f" start time error: {start_diff:.6f}, end time error: {end_diff:.6f}")

    # calculate the ratio of unaligned notes
    unaligned_ratio = unaligned_notes / total_notes if total_notes > 0 else 0.0
    is_successful = unaligned_notes == 0

    if total_notes > 0:
        print(f"total notes: {total_notes}, unaligned notes: {unaligned_notes}, unaligned ratio: {unaligned_ratio:.2%}")
    else:
        print("unrecognized notes!")

    return is_successful, unaligned_ratio

# Test the quantize_midi function
if __name__ == "__main__":
    # Quantize the input MIDI file
    input_file = "test/test_quantization.mid"
    output_file = input_file.replace(".mid", "_output.mid")
    quantization_level=1/32
    quantize_midi(input_file, output_file, quantization_level=quantization_level)

    # test if the quantization is successful
    success, unaligned_ratio = is_quantized(output_file, quantization_level=quantization_level)
    if success:
        print("Quantization test passed! All notes are successfully aligned to the time grid.")
    else:
        print(f"Quantization test failed! The ratio of unaligned notes: {unaligned_ratio:.2%}")
import csv
import ast
input_file = 'output_2.csv'
output_file = 'updated_pop.csv'
def denormalize(norm_val, min_norm, max_norm, min_pitch, max_pitch):
    if max_norm == min_norm:
        return (min_pitch + max_pitch) / 2.0
    return ((norm_val - min_norm) / (max_norm - min_norm)) * (max_pitch - min_pitch) + min_pitch
with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        pitch_sequence = ast.literal_eval(row['pitch_sequence'])
        normalized_pitch_sequence = ast.literal_eval(row['normalized_pitch_sequence'])
        min_pitch, max_pitch = min(pitch_sequence), max(pitch_sequence)
        min_norm, max_norm = min(normalized_pitch_sequence), max(normalized_pitch_sequence)
        if 'input_pitch' in row and row['input_pitch'].strip():
            input_norm_list = ast.literal_eval(row['input_pitch'])
            input_pitch_list = [round(denormalize(val, min_norm, max_norm, min_pitch, max_pitch))
                                for val in input_norm_list]
            row['input_pitch'] = str(input_pitch_list)
        for opt_col in ['option_1','option_2','option_3','option_4','option_5','option_6','option_7','option_8','option_9','option_10']:
            if row[opt_col].strip():
                opt_norm_list = ast.literal_eval(row[opt_col])
                opt_pitch_list = [round(denormalize(val, min_norm, max_norm, min_pitch, max_pitch))
                                  for val in opt_norm_list]
                row[opt_col] = str(opt_pitch_list)
        writer.writerow(row)
print("Conversion complete. Output written to:", output_file)

import csv
import ast
def pad_input_pitch(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            input_pitch = ast.literal_eval(row['input_pitch'])
            if len(input_pitch) < 32:
                first_note = input_pitch[0]
                padding = [first_note] * (32 - len(input_pitch))
                input_pitch = padding + input_pitch
            row['input_pitch'] = str(input_pitch)
            writer.writerow(row)
input_csv = 'updated_pop.csv'  
output_csv = 'updated_pop_ext.csv'  
pad_input_pitch(input_csv, output_csv)
print(f"Processing complete. Updated file saved to {output_csv}.")

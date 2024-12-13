import csv
import ast
def parse_float_sequence(seq_str):
    return ast.literal_eval(seq_str.strip())
def main(output_csv="output.csv"):
    with open(output_csv, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            melody = row["melody"]
            norm_seq = parse_float_sequence(row["normalized_pitch_sequence"])
            option_1_seq = parse_float_sequence(row["option_1"])
            last_eight = norm_seq[-8:] if len(norm_seq) >= 8 else norm_seq
            if option_1_seq == last_eight:
                print(f"Melody {melody}: option_1 matches the last eight notes of the normalized_pitch_sequence.")
            else:
                print(f"Melody {melody}: option_1 does NOT match.\n"
                      f"  Expected: {last_eight}\n"
                      f"  Got:      {option_1_seq}")
if __name__ == "__main__":
    main()

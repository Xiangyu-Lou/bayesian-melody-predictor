import csv
import ast
import random
def parse_float_sequence(seq_str):
    return ast.literal_eval(seq_str.strip())
def build_constraints(all_sequences, context_size):
    """
    Build constraints for a given context_size.
    context_size = N means we use (N-1) previous notes as the context.
    """
    constraints = {}
    order = context_size - 1
    for seq in all_sequences:
        for i in range(len(seq) - order):
            context = tuple(seq[i:i+order])
            next_note = seq[i+order]
            if context not in constraints:
                constraints[context] = set()
            constraints[context].add(next_note)
    return constraints
def generate_with_context(constraints, start_seq, length=8, context_size=4):
    """
    Attempt to generate up to `length` notes using the given constraints and context_size.
    Returns the list of generated notes (could be shorter if stuck).
    """
    order = context_size - 1
    if len(start_seq) < order:
        return []
    current_context = tuple(start_seq[-order:])
    generated = []
    for _ in range(length):
        if current_context in constraints and constraints[current_context]:
            possible_next = list(constraints[current_context])
            next_note = random.choice(possible_next)
            generated.append(next_note)
            if order > 0:
                current_context = tuple(list(current_context[1:]) + [next_note])
            else:
                current_context = (next_note,)
        else:
            break
    return generated
def generate_sequence_with_fallback(constraints_4, constraints_3, constraints_2, start_seq, length=8, fallback_notes=None):
    """
    Generate a sequence of length=8 using:
    1) context_size=4 constraints
    2) if can't reach length 8, use context_size=3
    3) if still can't reach length 8, use context_size=2
    4) if still can't reach length 8, fill with random notes
    """
    partial = generate_with_context(constraints_4, start_seq, length=length, context_size=4)
    if len(partial) == length:
        return partial
    needed = length - len(partial)
    seq_so_far = start_seq + partial
    partial2 = generate_with_context(constraints_3, seq_so_far, length=needed, context_size=3)
    partial += partial2
    if len(partial) == length:
        return partial
    needed = length - len(partial)
    seq_so_far = start_seq + partial
    partial3 = generate_with_context(constraints_2, seq_so_far, length=needed, context_size=2)
    partial += partial3
    if len(partial) == length:
        return partial
    needed = length - len(partial)
    if fallback_notes and len(fallback_notes) > 0:
        for _ in range(needed):
            partial.append(random.choice(fallback_notes))
    return partial
def main(input_csv="input.csv", output_csv="output.csv"):
    with open(input_csv, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    option_columns = [col for col in (fieldnames or []) if col.startswith("option_")]
    if not option_columns:
        option_columns = [f"option_{i}" for i in range(1, 11)]
        for oc in option_columns:
            if oc not in fieldnames:
                fieldnames.append(oc)
    all_norm_seqs = []
    for row in rows:
        norm_seq = parse_float_sequence(row["normalized_pitch_sequence"])
        all_norm_seqs.append(norm_seq)
    constraints_4 = build_constraints(all_norm_seqs, context_size=4)
    constraints_3 = build_constraints(all_norm_seqs, context_size=3)
    constraints_2 = build_constraints(all_norm_seqs, context_size=2)
    all_notes = [note for seq in all_norm_seqs for note in seq]
    for i, row in enumerate(rows):
        input_seq = parse_float_sequence(row["input_pitch"])
        for oc in option_columns:
            if oc == "option_1" and oc in row and row[oc].strip() != "":
                continue
            generated_ending = generate_sequence_with_fallback(
                constraints_4, constraints_3, constraints_2, input_seq,
                length=8, fallback_notes=all_notes
            )
            row[oc] = str(generated_ending)
            if oc == "option_1":
                print(f"Wrote option_1 for row {i}: {generated_ending}")
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
if __name__ == "__main__":
    main()

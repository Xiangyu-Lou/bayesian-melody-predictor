INPUT_FILE = "volpiano_entries.txt"
OUTPUT_FILE = "volpiano_entries_unique.txt"
try:
    with open(INPUT_FILE, "r", encoding="utf-8") as input_file:
        volpiano_entries = input_file.readlines()
except FileNotFoundError:
    print(f"Error: {INPUT_FILE} not found.")
    exit(1)
cleaned_entries = [entry.strip() for entry in volpiano_entries if entry.strip()]
unique_entries = list(set(cleaned_entries))
with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
    for entry in unique_entries:
        output_file.write(entry + "\n")
total_original = len(volpiano_entries)
total_cleaned = len(cleaned_entries)
total_unique = len(unique_entries)
duplicates_removed = total_cleaned - total_unique
print(f"Total entries in original file: {total_original}")
print(f"Total non-empty entries: {total_cleaned}")
print(f"Total unique entries: {total_unique}")
print(f"Duplicates removed: {duplicates_removed}")
print(f"Unique volpiano entries saved to {OUTPUT_FILE}.")

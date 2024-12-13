import os
import csv
CSV_DIR = "nonemptyCSVs"
OUTPUT_FILE = "volpiano_entries.txt"
total_melodies = 0
with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
    for filename in os.listdir(CSV_DIR):
        if filename.endswith(".csv"):
            csv_path = os.path.join(CSV_DIR, filename)
            print(f"Processing {csv_path}...")
            try:
                with open(csv_path, "r", encoding="utf-8") as csv_file:
                    reader = csv.DictReader(csv_file)
                    if "volpiano" in reader.fieldnames:
                        for row in reader:
                            volpiano = row.get("volpiano", "").strip()
                            if volpiano.startswith("1"):
                                output_file.write(volpiano + "\n")
                                total_melodies += 1
                                print(f"Added volpiano entry: {volpiano}")
            except Exception as e:
                print(f"Error processing {csv_path}: {e}")
print(f"Total volpiano melodies starting with '1': {total_melodies}")
print(f"Volpiano entries saved to {OUTPUT_FILE}.")

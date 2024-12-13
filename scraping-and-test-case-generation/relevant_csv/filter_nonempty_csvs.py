import os
import csv
import shutil
VALID_CSV_DIR = "validCSVs"
NONEMPTY_CSV_DIR = "nonemptyCSVs"
os.makedirs(NONEMPTY_CSV_DIR, exist_ok=True)
def has_nonempty_volpiano(csv_path):
    try:
        with open(csv_path, "r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            if "volpiano" not in reader.fieldnames:
                return False  
            for row in reader:
                if row.get("volpiano"):  
                    return True
        return False  
    except Exception as e:
        print(f"Error processing {csv_path}: {e}")
        return False
for filename in os.listdir(VALID_CSV_DIR):
    if filename.endswith(".csv"):
        csv_path = os.path.join(VALID_CSV_DIR, filename)
        print(f"Checking {csv_path} for non-empty volpiano column...")
        if has_nonempty_volpiano(csv_path):
            shutil.copy(csv_path, os.path.join(NONEMPTY_CSV_DIR, filename))
            print(f"Copied {filename} to {NONEMPTY_CSV_DIR}.")
        else:
            print(f"Skipped {filename} (empty volpiano column).")
print("Processing complete. Non-empty CSVs saved in the 'nonemptyCSVs' directory.")

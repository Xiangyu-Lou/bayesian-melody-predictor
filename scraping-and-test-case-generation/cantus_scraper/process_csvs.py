import requests
import os
import csv
CSV_DIR = "validCSVs"
os.makedirs(CSV_DIR, exist_ok=True)
def check_volpiano_column(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            reader = csv.reader(content.splitlines())
            headers = next(reader)  
            if 'volpiano' in headers:
                return True
        return False
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return False
with open("valid_sources.txt", "r") as f:
    numbers = [line.split(":")[0].strip() for line in f]  
for number in numbers:
    csv_url = f"https://cantusdatabase.org/source/{number}/csv/"
    print(f"Checking CSV for source {number} at {csv_url}...")
    response = requests.get(csv_url)
    if response.status_code == 200:
        print(f"CSV exists for source {number}. Checking for volpiano column...")
        if check_volpiano_column(csv_url):
            print(f"volpiano column found for source {number}. Downloading CSV...")
            file_path = os.path.join(CSV_DIR, f"{number}.csv")
            with open(file_path, "wb") as csv_file:
                csv_file.write(response.content)
            print(f"CSV for source {number} saved to {file_path}.")
        else:
            print(f"No volpiano column found in source {number}. Skipping...")
    else:
        print(f"No valid CSV file for source {number}.")
print("Processing complete. Valid CSVs are saved in the 'validCSVs' directory.")

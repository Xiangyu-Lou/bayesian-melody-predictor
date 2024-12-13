INPUT_FILE = "volpiano_entries_unique.txt"
try:
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()
except FileNotFoundError:
    print(f"Error: {INPUT_FILE} not found.")
    exit(1)
old_line_count = len(lines)
cleaned_lines = [line for line in lines if line.strip()]
new_line_count = len(cleaned_lines)
with open(INPUT_FILE, "w", encoding="utf-8") as file:
    file.writelines(cleaned_lines)
print(f"Old line count: {old_line_count}")
print(f"New line count: {new_line_count}")
print(f"Empty lines removed: {old_line_count - new_line_count}")

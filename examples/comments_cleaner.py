import os

def clean_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    clean_lines = []
    for line in lines:
        # Skip lines that start with our tutorial marker (ignoring leading whitespace)
        stripped = line.strip()
        if stripped.startswith("##"):
            continue
        clean_lines.append(line)
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(clean_lines)
    print(f"Cleaned: {output_path}")

# Example usage: Strip tutorials from a folder and save to a 'clean' folder
os.makedirs("clean_code", exist_ok=True)
clean_file("importing/import_stl.py", "clean_code/import_stl.py")
import json

def read_json_data(file_path):
    """Read JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def compare_values(files_keys, target_key):
    """Extract values for a specific key from multiple files and write them in a formatted way to a new file."""
    # Read data from all files
    all_data = {fk['display']: read_json_data(fk['file']) for fk in files_keys}
    
    # Determine all distortion types from all files
    distortions = set()
    for data in all_data.values():
        distortions.update(data.keys())

    # Open a file to write the comparisons
    with open('comparison_output.txt', 'w') as file:
        for distortion in sorted(distortions):
            file.write(f"Distortion: {distortion}\n")

            # Collect arrays for comparison
            arrays = []
            for fk in files_keys:
                key = fk['key']
                display_name = fk['display']
                data = all_data[display_name].get(distortion, {}).get(key, {}).get(target_key, [])
                arrays.append(data)

            # Labels for each row
            labels = ["TP", "FP", "TN", "FN"]

            # Formatting to align headers correctly
            # Calculate the maximum width needed for any value or header, then add a padding
            max_len = max(len(str(x)) for array in arrays for x in array) if arrays else 0
            max_len = max(max_len, max(len(fk['display']) for fk in files_keys))
            column_width = max_len + 10  # Adding extra space for padding

            # Write the specific key and align the headers
            file.write(f"Key: {target_key}\n")
            header = "".join(f"{fk['display']:^{column_width}}" for fk in files_keys)
            file.write(f"      {header}\n")
            
            for label in labels:
                row = f"{label:<5} "
                for array in arrays:
                    if len(array) > labels.index(label):
                        row += f"{array[labels.index(label)]:^{column_width}}"
                    else:
                        row += " " * column_width
                file.write(f"{row}\n")
            file.write("\n")

# Example usage
files_keys = [
    {'file': 'assets/results/Phash-Dhash-Vit 50K/roc_curve.json', 'key': 'Phash', 'display': 'Phash'},
    {'file': 'assets/results/Phash-Dhash-Vit 50K/roc_curve.json', 'key': 'Phash_Vit', 'display': 'Phash_Vit'},
    {'file': 'assets/results/Phash-Dhash-Vit 50K/roc_curve.json', 'key': 'Phash_Dhash', 'display': 'Phash_Dhash'}
    # Add more files, keys, and display names as needed
]

target_key = '0.96875'
compare_values(files_keys, target_key)

import json

def read_json_data(file_path):
    """Read JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_accuracy(TP, FP, TN, FN):
    """Calculate the accuracy score."""
    total = TP + FP + TN + FN
    return (TP + TN) / total if total > 0 else 0

def combine_data(file_paths, method_preferences):
    """Combine data from multiple JSON files based on method preferences."""
    combined_data = {}
    method_sources = {}  # Tracks the source file for each method
    for path in file_paths:
        data = read_json_data(path)
        for distortion, hash_methods in data.items():
            if distortion not in combined_data:
                combined_data[distortion] = {}
            for method, results in hash_methods.items():
                if method not in combined_data[distortion] or path == method_preferences.get(method):
                    combined_data[distortion][method] = results
                    method_sources[method] = path
    return combined_data

def format_matrix(file_paths, method_preferences):
    """Read data, compute metrics, and format them into a matrix-like file."""
    combined_data = combine_data(file_paths, method_preferences)
    with open('matrix_results.txt', 'w') as file:
        for distortion, hash_methods in combined_data.items():
            file.write(f"Distortion: {distortion}\n")
            hash_method_names = list(hash_methods.keys())
            # Header row
            headers = ' ' * 15 + ' '.join(f"{name:^30}" for name in hash_method_names) + '\n'
            file.write(headers)

            # Initialize data storage for matrix rows with fixed label width
            label_width = 15
            threshold_row = [f"{'Threshold:':<{label_width}}"]
            accuracy_row = [f"{'Accuracy:':<{label_width}}"]
            tp_row = [f"{'TP:':<{label_width}}"]
            fp_row = [f"{'FP:':<{label_width}}"]
            tn_row = [f"{'TN:':<{label_width}}"]
            fn_row = [f"{'FN:':<{label_width}}"]

            # Find the best threshold for each hash method and collect data
            for hash_method in hash_method_names:
                thresholds = hash_methods[hash_method]
                best_accuracy = -1
                best_info = None

                for threshold, values in thresholds.items():
                    TP, FP, TN, FN = values
                    accuracy = calculate_accuracy(TP, FP, TN, FN)
                    if accuracy > best_accuracy:
                        best_accuracy = accuracy
                        best_info = (threshold, accuracy, TP, FP, TN, FN)

                if best_info:
                    threshold, accuracy, TP, FP, TN, FN = best_info
                    threshold_row.append(f"{threshold:^30}")
                    accuracy_row.append(f"{accuracy:^30.4f}")
                    tp_row.append(f"{TP:^30d}")
                    fp_row.append(f"{FP:^30d}")
                    tn_row.append(f"{TN:^30d}")
                    fn_row.append(f"{FN:^30d}")

            # Write each row
            file.write(' '.join(threshold_row) + '\n')
            file.write(' '.join(accuracy_row) + '\n')
            file.write(' '.join(tp_row) + '\n')
            file.write(' '.join(fp_row) + '\n')
            file.write(' '.join(tn_row) + '\n')
            file.write(' '.join(fn_row) + '\n')
            file.write('\n')

# Example usage
file_paths = [
    'assets/results/50K Phash-Dhash-Phash_Dhash_Vit\optimal_thresholds_values.json', 
    'assets/results/50K Phash_Vit\optimal_thresholds_values.json',
    'assets/results/10_05_2024 - 03_29_37\optimal_thresholds_values.json',
    'assets/results/10_05_2024 - 19_14_37\optimal_thresholds_values.json'
]
# Define which file's method to prioritize in case of overlap
method_preferences = {
    'Phash_Vit': 'assets/results/50K Phash_Vit\optimal_thresholds_values.json',

    # Add more methods and their preferred source file as needed
}

format_matrix(file_paths, method_preferences)
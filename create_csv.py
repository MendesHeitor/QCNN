import re
import pandas as pd
from collections import defaultdict
import numpy as np

# Path to your input .txt file
input_path = "results_final.txt"  # Change to your actual file path
output_path = "gate_encoding_accuracy.csv"

# Read the file content
with open(input_path, "r") as file:
    text = file.read()

# Regular expression pattern to match: Accuracy for [gate] [encoding] : [value]
pattern = r"Accuracy\s+for\s+(\S+)\s+(\S+)\s*:\s*([0-9.]+)"

# Extract matches
matches = re.findall(pattern, text)

# Store results in nested dictionary
results = defaultdict(lambda: defaultdict(list))

for gate, encoding, value in matches:
    results[gate][encoding].append(float(value))

# Average multiple values per gate/encoding combination
averaged_results = {
    gate: {enc: np.mean(vals) for enc, vals in enc_dict.items()}
    for gate, enc_dict in results.items()
}

# Convert to DataFrame
df = pd.DataFrame(averaged_results).T  # Rows = gates, columns = encodings

# Ensure the specified order for rows (gates) and columns (encodings)
gate_order = ['U_TTN', 'U_9', 'U_15', 'U_13', 'U_14', 'U_SO4', 'U_5', 'U_6', 'U_SU4']
encoding_order = ['resize256', 'pca8', 'autoencoder8', 'pca16-compact', 'autoencoder16-compact', 'pca32-1', 'autoencoder32-1', 'pca30-1', 'autoencoder30-1']

# Reindex the DataFrame to match the specified order
df = df.reindex(index=gate_order, columns=encoding_order)

# Save to CSV
df.to_csv(output_path)
print(f"Saved table to {output_path}")

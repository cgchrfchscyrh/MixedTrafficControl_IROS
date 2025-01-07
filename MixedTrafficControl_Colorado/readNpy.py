import numpy as np
import os
import matplotlib.pyplot as plt
from collections import defaultdict
import re  # For regular expression to extract Junc ID

# Define data path
base_directory = "histograms"

# Initialize data storage
all_histograms = defaultdict(lambda: {"counts": [], "bins": None})

# Load data
total_files = 0
unique_junc_ids = set()  # To track unique Junc IDs
for episode_dir in os.listdir(base_directory):
    episode_path = os.path.join(base_directory, episode_dir)
    if os.path.isdir(episode_path):
        print(f"Processing folder: {episode_path}")
        for npy_file in os.listdir(episode_path):
            if npy_file.endswith(".npy"):
                file_path = os.path.join(episode_path, npy_file)
                total_files += 1
                try:
                    # Updated regex to extract Junc ID up to "_episode"
                    match = re.search(r'junction_([^_]+(?:_[^_]+)*)_episode', npy_file)
                    if match:
                        junc_id = match.group(1)  # Extract the matched Junc ID
                        unique_junc_ids.add(junc_id)
                    else:
                        print(f"Could not extract Junc ID from file: {npy_file}")
                        continue

                    # Load npy file content
                    data = np.load(file_path, allow_pickle=True).item()

                    # Store bin and count data
                    if all_histograms[junc_id]["bins"] is None:
                        all_histograms[junc_id]["bins"] = data["bins"]
                        print(f"Found {npy_file} for junction {junc_id}")
                    all_histograms[junc_id]["counts"].append(data["counts"])

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

# Verify the number of unique Junc IDs
if len(unique_junc_ids) > 18:
    print(f"Warning: Detected more than 18 unique Junc IDs: {unique_junc_ids}")

# Compute average histogram for each junction and plot
output_directory = "aggregated_histograms"
os.makedirs(output_directory, exist_ok=True)

for junc_id, data in all_histograms.items():
    if len(data["counts"]) > 0:
        # Compute average values across all workers
        avg_counts = np.mean(data["counts"], axis=0)
        bins = data["bins"]
        
        # Plot average histogram
        plt.figure(figsize=(10, 6))
        plt.bar(bins[:-1], avg_counts, width=(bins[1] - bins[0]), align="edge", alpha=0.7, color="blue")
        plt.title(f"Ours: Average Waiting Time Histogram at Junction {junc_id}")
        plt.xlabel("Waiting Time (s)")
        plt.ylabel("Vehicle Count")
        plt.grid(True)
        
        # Save the plot
        output_file = os.path.join(output_directory, f"average_histogram_{junc_id}.jpg")
        plt.savefig(output_file, format="jpg")
        print(f"Saved average histogram for Junction {junc_id} to {output_file}, with {len(data['counts'])} data points.")
        plt.close()
    else:
        print(f"No data available for Junction {junc_id}.")

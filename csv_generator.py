import os
import csv

# Define your directories and group names here
directories = {
    "./data/mvtec_visdiff_large/set_a": "good bottle from top view",
    "./data/mvtec_visdiff_large/set_b": "broken bottle from top view with crack"
}

# Define the CSV file name
csv_file_name = "Mvtec_visdiff_large.csv"

# Create or overwrite the CSV file with sorted file names
with open(csv_file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header again
    writer.writerow(["group_name", "path"])
    
    # Loop through each directory and its corresponding group name, with sorting
    for directory, group_name in directories.items():
        # Check if directory exists
        if os.path.exists(directory):
            # List all files in the directory, filter .png files, and sort them by the numeric part of the file name
            sorted_files = sorted(
                [f for f in os.listdir(directory) if f.endswith(".png")],
                key=lambda x: int(os.path.splitext(x)[0])
            )
            # Write the sorted files to the CSV
            for filename in sorted_files:
                file_path = os.path.join(directory, filename)
                writer.writerow([group_name, file_path])

print(f"CSV file '{csv_file_name}' has been created with sorted paths.")


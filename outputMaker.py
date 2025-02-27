import os
import subprocess

# Define input and output directories
input_dir = "../all_inputs/inputs"
output_dir = "all_outputs"
script_name = "TentTree.py"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Iterate over all input files in the input directory
for input_file in os.listdir(input_dir):
    if input_file.endswith(".txt"):  # Process only .txt files
        input_path = os.path.join(input_dir, input_file)
        output_path = os.path.join(output_dir, input_file)  # Output file has the same name
        
        # Run TreeTent.py with input and output file as arguments
        subprocess.run(["python3", script_name, input_path, output_path])
        
        print(f"Processed: {input_file} -> {output_path}")


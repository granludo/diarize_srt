#!/bin/bash
## 
# Check if the directory arguments are provided
echo "$0 diarizes speakers in .wav files in a directory to txt files"

if [ -z "$1" ]; then
    echo "Usage: $0 <source directory> <destination directory>"
    echo "missing <source directory>"
    exit 1
fi

if [ -z "$2" ]; then
    echo "Usage: $0 <source directory> <destination directory>"
    echo "missing <destination directory>"
    exit 1
fi

# Assign the first and second arguments to variables
source_dir=$1
destination_dir=$2

# Loop through .srt files in the specified source directory
for file in "$source_dir"/*.wav; do
    echo "Processing $file"

    # Extract filename without extension
    filename=$(basename -- "$file")
    filename="${filename%.*}"

    # Construct the destination file path
    destination_file="$destination_dir/$filename.txt"

    # Execute the Python script
    python diarize.py "$file" "$destination_file"
done


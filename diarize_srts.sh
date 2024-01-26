
#!/bin/bash
## 
# Check if the directory arguments are provided
echo "$0 merges diarizations in .txt files in a directory with srt files in another directory and outputs like a boss"

if [ -z "$1" ]; then
    echo "Usage: $0 <source txt directory> <sorce srt directory> <destination directory> Speaker_to_keep"
    echo "missing <source txt directory>"
    exit 1
fi

if [ -z "$2" ]; then
    echo "Usage: $0 <source txt directory> <sorce srt directory> <destination directory> Speaker_to_keep"
    echo "missing <source srt directory>"
    exit 1
fi

if [ -z "$3" ]; then
    echo "Usage: $0 <source txt directory> <sorce srt directory> <destination directory> Speaker_to_keep"
    echo "missing <destination directory>"
    exit 1
fi



# Assign the first and second arguments to variables
source_txt_dir=$1
source_srt_dir=$2
destination_dir=$3

# Loop through .srt files in the specified source directory
for file in "$source_dir"/*.txt; do
    echo "Processing $file"
    # Extract filename without extension
    filename=$(basename -- "$file")
    filename="${filename%.*}"
    srt_file="$source_srt_dir/$filename.srt"
    # Construct the destination file path
    destination_file="$destination_dir/$filename.srt"
    # Check if the .srt file exists
    if [ -f "$srt_file" ]; then
        echo "Found corresponding .srt file: $srt_file"
        # Add processing logic here for when the .srt file exists
        python3 remove_speaker.py "$file" "$srt_file" "$destination_file" $4
    else
        echo "No corresponding .srt file found for $file"
        # Add processing logic here for when the .srt file does not exist
    fi
    
done

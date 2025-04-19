#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <source_file>"
    exit 1
fi

SOURCE_FILE=$1
BYTECODE_FILE="${SOURCE_FILE%.*}.bytecode"

# Generate bytecode
python3 bytecode_generator.py "$SOURCE_FILE" "$BYTECODE_FILE"

if [ $? -eq 0 ]; then
    echo "Running bytecode..."
    ./bytecode_interpreter "$BYTECODE_FILE"
else
    echo "Error generating bytecode"
    exit 1
fi
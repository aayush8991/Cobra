#!/bin/bash

# Build the C bytecode interpreter
gcc -Wall -O2 bytecode_interpreter.c -o bytecode_interpreter

if [ $? -eq 0 ]; then
    echo "Bytecode interpreter built successfully"
else
    echo "Error building bytecode interpreter"
    exit 1
fi
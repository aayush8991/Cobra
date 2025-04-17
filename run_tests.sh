# #!/bin/bash

# # Define the root directory for tests
# TESTS_DIR="tests"

# # Clear previous coverage data
# coverage erase

# # Function to run a single test with coverage
# run_test() {
#     local test_folder="$1"
#     local code_file="$test_folder/code.txt"
#     local expected_file="$test_folder/expected.txt"

#     # Run the test with a 5-second timeout, tracking coverage
#     timeout 5s coverage run --append helper.py "$code_file" > "$test_folder/actual.txt" 2>&1

#     # Check if the command timed out
#     if [ $? -eq 124 ]; then
#         echo -e "\e[31m$test_folder (Timeout)\e[0m" # Red for timeout
#         return
#     fi

#     # Compare actual output with expected output
#     diff -q "$test_folder/actual.txt" "$expected_file" > /dev/null
#     if [ $? -eq 0 ]; then
#         echo -e "\e[32m$test_folder (Passed)\e[0m" # Green for passed
#     else
#         echo -e "\e[31m$test_folder (Failed)\e[0m" # Red for failed
#     fi
# }

# # Run all tests
# for test_folder in "$TESTS_DIR"/*; do
#     if [ -d "$test_folder" ]; then
#         run_test "$test_folder"
#     fi
# done

# # Generate coverage report
# coverage report -m  # Show coverage in the terminal
# coverage html        # Generate an HTML report

# echo "Coverage report generated. Open 'htmlcov/index.html' to view."


#!/bin/bash

# Define the root directory for tests
TESTS_DIR="tests"

# Clear previous coverage data
coverage erase

# Function to run a single test with coverage
run_test() {
    local test_folder="$1"
    local code_file="$test_folder/code.txt"
    local expected_file="$test_folder/expected.txt"

    # Run the test with a 5-second timeout, tracking coverage
    timeout 5s coverage run --append helper.py "$code_file" > "$test_folder/actual.txt" 2>&1

    # Check if the command timed out
    if [ $? -eq 124 ]; then
        echo -e "\e[31m$test_folder (Timeout)\e[0m" # Red for timeout
        return
    fi

    # Compare actual output with expected output
    diff -q "$test_folder/actual.txt" "$expected_file" > /dev/null
    if [ $? -eq 0 ]; then
        echo -e "\e[32m$test_folder (Passed)\e[0m" # Green for passed
    else
        echo -e "\e[31m$test_folder (Failed)\e[0m" # Red for failed
    fi
}

# Run all tests
for test_folder in "$TESTS_DIR"/*; do
    if [ -d "$test_folder" ]; then
        run_test "$test_folder"
    fi
done

# Generate coverage report ONLY for selected files
coverage report -m lexer.py parser.py eval.py tree.py
coverage html --include=lexer.py,parser.py,eval.py,tree.py

echo "Coverage report generated. Open 'htmlcov/index.html' to view."

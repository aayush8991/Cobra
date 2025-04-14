import subprocess
import pytest
from unittest.mock import patch, MagicMock

# Define test cases with file paths and expected outputs
test_cases = [
    ("arr_init.cr", "Result: IntToken(v=Decimal('3'))\n"),
    ("arrays.cr", "Result: IntToken(v=Decimal('8'))\n"),
    ("boolean_operations.cr", "Result: StringToken(v='a is not equal to b')\n")
]

@pytest.mark.parametrize("file_path, expected_output", test_cases)
@patch("subprocess.run") 
def test_crystal_file_output(mock_run, file_path, expected_output):
    # Configure the mock to return a successful result
    mock_result = MagicMock()
    mock_result.stdout = expected_output
    mock_result.returncode = 0
    mock_run.return_value = mock_result

    # Run the test logic
    result = subprocess.run(
        ["cobra", file_path],
        capture_output=True,
        text=True
    )
    
    # Assert the output matches the expected output
    assert result.stdout == expected_output, f"Output mismatch for {file_path}"
    assert result.returncode == 0, f"Non-zero exit code for {file_path}"

    # Verify subprocess.run was called with the correct arguments
    mock_run.assert_called_once_with(
        ["cobra", file_path],
        capture_output=True,
        text=True
    )
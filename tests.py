from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

import os

def test_get_file_content():
    """Test suite for get_file_content function"""
    working_directory = "/home/andrew/boot-agent/calculator"
    
    print("=== Testing get_file_content function ===\n")
    
    # Test 2: Valid File Test
    print("Test 2: Valid File Test (main.py)")
    result = get_file_content(working_directory, "main.py")
    print(result)
    print()
    
    # Test 3: Nested Valid File Test
    print("Test 3: Nested Valid File Test (pkg/calculator.py)")
    result = get_file_content(working_directory, "pkg/calculator.py")
    print(result)
    print()
    
    # Test 4: Permission/System File Test
    print("Test 4: Binary File Test (/bin/cat)")
    result = get_file_content(working_directory, "/bin/cat")
    print(result)
    print()
    
    # Test 5: Non-Existent File Test
    print("Test 5: Non-Existent File Test (pkg/does_not_exist.py)")
    result = get_file_content(working_directory, "pkg/does_not_exist.py")
    print(result)
    print()
    
    print("=== Test suite completed ===")

def test_write_file():
    """Test suite for write_file function"""
    working_directory = "/home/andrew/boot-agent/calculator"
    
    print(write_file(working_directory, "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file(working_directory, "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file(working_directory, "/tmp/temp.txt", "this should not be allowed"))

def test_run_python_file():
    working_directory = "/home/andrew/boot-agent/calculator"
    print(run_python_file(working_directory, "main.py"))
    print(run_python_file(working_directory, "main.py", ["3 + 5"]))
    print(run_python_file(working_directory, "tests.py"))
    print(run_python_file(working_directory, "../main.py"))
    print(run_python_file(working_directory, "nonexistent.py"))
    print(run_python_file(working_directory, "lorem.txt"))

if __name__ == "__main__":
    test_run_python_file()

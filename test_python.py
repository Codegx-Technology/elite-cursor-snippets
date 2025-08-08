import sys
import os
from pathlib import Path

print("Python test script running!")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")

# Try to create a test file
try:
    with open('test_output.txt', 'w') as f:
        f.write("Test file created successfully!")
    print("Successfully created test_output.txt")
except Exception as e:
    print(f"Error creating test file: {e}")

print("Test script completed!")

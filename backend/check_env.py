# check_env.py
import sys
import transformers

print("--- Python Executable ---")
print(sys.executable)
print("\n--- Transformers Library Info ---")
print(f"Version: {transformers.__version__}")
print(f"Path: {transformers.__file__}")
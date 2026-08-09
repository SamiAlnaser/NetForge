import sys
from pathlib import Path

print("NetForge environment check")
print(f"Python version: {sys.version.split()[0]}")
print(f"Python executable: {sys.executable}")
print(f"Working directory: {Path.cwd()}")

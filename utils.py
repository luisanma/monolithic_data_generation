import json
import os


def load_json(file_path):
    """Loads a JSON file and returns its content."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "r") as file:
        return json.load(file)

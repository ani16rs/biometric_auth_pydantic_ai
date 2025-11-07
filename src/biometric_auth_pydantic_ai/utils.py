"""
    File name: utils.py

    Purpose:
        Utility functions.
"""

import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

def clean_up_result(result_output):
    clean_output = result_output.strip()
    if clean_output.startswith("```"):
        # Remove leading and trailing triple backticks with optional "json"
        clean_output = re.sub(r"^```[a-zA-Z]*\n?", "", clean_output)
        clean_output = re.sub(r"\n?```$", "", clean_output)

    return clean_output

def get_test_case(test_case: str):
    input_path, template_path = None, None

    if test_case == "positive1":
        print("\nSame person. FPs from CS266 project. One normal, other with a dash.")
        input_path = ROOT_DIR / "images" / "img1-0.jpg"       # fp image from CS266 project
        template_path = ROOT_DIR / "images" / "img1-1.jpg"    # fp image from CS266 project with a dash drawn in it
    elif test_case == "positive2":
        print("\nSame person. FPs from nbis test_data. Different captures.")
        input_path = ROOT_DIR / "images" / "img2-0.png"        # fp image from nbis-rs test_data
        template_path = ROOT_DIR / "images" / "img2-1.png"     # fp image from nbis-rs test_data
    elif test_case == "negative1":
        input_path = ROOT_DIR / "images" / "img1-0.jpg"       # fp image from CS266 project
        template_path = ROOT_DIR / "images" / "img2-0.png"    # fp image from nbis-rs test_data
        print("\nDiff persons. FPs from nbis test_data.")
    
    return input_path, template_path
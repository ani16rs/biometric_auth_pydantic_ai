import re

def clean_up_result(result_output):
    clean_output = result_output.strip()
    if clean_output.startswith("```"):
        # Remove leading and trailing triple backticks with optional "json"
        clean_output = re.sub(r"^```[a-zA-Z]*\n?", "", clean_output)
        clean_output = re.sub(r"\n?```$", "", clean_output)

    return clean_output
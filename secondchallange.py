import json
import re
from datetime import datetime

# Helper function to transform RFC3339 to Unix Epoch
def rfc3339_to_unix_epoch(date_str):
    try:
        return int(datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").timestamp())
    except ValueError:
        return None

# Helper function to clean string values
def clean_string(s):
    return s.strip()

# Helper function to transform a numeric string into an actual number
def transform_number(n):
    try:
        n_cleaned = clean_string(n).lstrip('0') or '0'
        return float(n_cleaned) if '.' in n_cleaned else int(n_cleaned)
    except ValueError:
        return None

# Helper function to transform boolean values
def transform_bool(b):
    truthy_values = {'1', 't', 'T', 'TRUE', 'true', 'True'}
    falsy_values = {'0', 'f', 'F', 'FALSE', 'false', 'False'}
    b_cleaned = clean_string(b)
    if b_cleaned in truthy_values:
        return True
    elif b_cleaned in falsy_values:
        return False
    return None

# Helper function to handle null values
def transform_null(value):
    if clean_string(value) in {'1', 't', 'T', 'TRUE', 'true', 'True'}:
        return None
    elif clean_string(value) in {'0', 'f', 'F', 'FALSE', 'false', 'False'}:
        return "omit"
    return "omit"

# Recursive function to transform the input JSON structure
def transform(data):
    result = {}
    for key, value in data.items():
        if key.strip() == "":  # Omit empty keys
            continue

        if isinstance(value, dict):
            if "S" in value:
                cleaned_string = clean_string(value["S"])
                if cleaned_string == "":
                    continue  # Omit empty strings
                if re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", cleaned_string):
                    result[key] = rfc3339_to_unix_epoch(cleaned_string)
                else:
                    result[key] = cleaned_string
            elif "N" in value:
                transformed_number = transform_number(value["N"])
                if transformed_number is not None:
                    result[key] = transformed_number
            elif "BOOL" in value:
                transformed_bool = transform_bool(value["BOOL"])
                if transformed_bool is not None:
                    result[key] = transformed_bool
            elif "NULL" in value:
                transformed_null_value = transform_null(value["NULL"])
                if transformed_null_value != "omit":
                    result[key] = None
            elif "M" in value:
                transformed_map = transform(value["M"])
                if transformed_map:
                    result[key] = transformed_map
            elif "L" in value and isinstance(value["L"], list):
                transformed_list = []
                for item in value["L"]:
                    if "S" in item and clean_string(item["S"]) != "":
                        continue  # Omit empty strings in lists
                    if "N" in item:
                        transformed_number = transform_number(item["N"])
                        if transformed_number is not None:
                            transformed_list.append(transformed_number)
                    elif "BOOL" in item:
                        transformed_bool = transform_bool(item["BOOL"])
                        if transformed_bool is not None:
                            transformed_list.append(transformed_bool)
                if transformed_list:
                    result[key] = transformed_list

    return result

# Main function to process the input JSON and print the transformed output
def main():
    input_json = {
        "number_1": {
            "N": "1.50"
        },
        "string_1": {
            "S": "784498 "
        },
        "string_2": {
            "S": "2014-07-16T20:55:46Z"
        },
        "map_1": {
            "M": {
                "bool_1": {
                    "BOOL": "truthy"
                },
                "null_1": {
                    "NULL ": "true"
                },
                "list_1": {
                    "L": [
                        {
                            "S": ""
                        },
                        {
                            "N": "011"
                        },
                        {
                            "N": "5215s"
                        },
                        {
                            "BOOL": "f"
                        },
                        {
                            "NULL": "0"
                        }
                    ]
                }
            }
        },
        "list_2": {
            "L": "noop"
        },
        "list_3": {
            "L": [
                "noop"
            ]
        },
        "": {
            "S": "noop"
        }
    }

    # Transform the input data
    transformed_data = transform(input_json)

    # Wrap the transformed data into a list as required by the output format
    output = [transformed_data]

    # Print the output JSON to stdout
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()

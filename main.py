import hashlib
import json
import os
import sys
import pandas as pd


# Get the csv file
args = sys.argv[1:]  # get command line *args
assert args, "No file/dir was provided"  # raise error is no arg is passed
csv_file = args[0]


def content_list(csv_file):
    '''
    -Takes a filename
    -Reads the file in the current working directory
    -Returns the contents of the file as a list
    '''
    with open(csv_file, 'r') as f:
        contents = f.readlines()
        for i, content in enumerate(contents):
            contents[i] = content.rstrip()
        return contents


def sha256_hex(filepath):
    '''
    -takes a filepath
    -Reads the file in the current working directory
    -Returns the sha256 hex_value of the file
    '''
    with open(filepath, 'rb') as f:
        content = f.read()
        sha256 = hashlib.sha256()
        sha256.update(content)
        hex_value = sha256.hexdigest()
        return hex_value


def json_gen(content_list):
    '''
    -Takes a list
    -Creates a dictionary for each item in the list
    -Creates a json file for each item
    -calls the sha256_hex function for each item
    -returns a modified list containing the hex value of each item
    '''
    df = pd.read_csv(csv_file)
    content_list[0] = content_list[0] + ',Hash'
    for index, row in df.iterrows():
        # values_of_content_columns = content.split(',')
        info = {
            "format": "CHIP-0007",
            "name": df.at[index, 'Filename'],
            "description": df.at[index, 'Description'],
            "minting_tool": "SuperMinter/2.5.2",
            "sensitive_content": False,
            "series_number": int(df.at[index, 'Series Number']),
            "series_total": 420,
            "attributes": [
                {
                    "trait_type": "Gender",
                    "value": df.at[index, 'Gender'],
                },
                {
                    "trait_type": "Description",
                    "value": df.at[index, 'Attributes'],
                }

            ],
            "collection": {
                "name": "Zuri NFT Collection",
                "id": df.at[index, 'UUID'],
            },
        }

        # Serializing json
        json_object = json.dumps(info, indent=4)

        json_filename = f"nft{df.at[index, 'Filename']}.json"
        json_filepath = os.path.join(os.getcwd(), "json_data", json_filename)

        with open(json_filepath, 'w') as outfile:
            outfile.write(json_object)

        hex_value = sha256_hex(json_filepath)

        new_content = content_list[index+1] + \
            f",{df.at[index, 'Filename']}.{hex_value}.csv"
        content_list[index+1] = new_content
    return content_list


# Make a list of the file contents
contents = content_list(csv_file)

# Generate and hash jason files. Amend contents
contents = json_gen(contents)

# write result to new csv file
with open(f'new_{csv_file}', 'w') as f:
    for content in contents:
        f.write(f'{content}\n')

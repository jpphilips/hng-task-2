import hashlib
import json
import os
import sys
import pandas as pd


# Get the csv file
args = sys.argv[1:]  # get command line *args
assert args, "No file/dir was provided"  # raise error is no arg is passed
csv_file = args[0]


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


df = pd.read_csv(csv_file)

for index, row in df.iterrows():
    #get attributes column
    attributes = df.at[index, 'attributes']
    attributes_list = attributes.split(';')

    #clean data
    if attributes_list[-1] == '' or attributes_list[-1] == ' ':
        attributes_list.pop()

    attributes_dict_list = []

    #create list of attributes
    for attribute in attributes_list:
        traits = attribute.split(':')
        trait_type = traits[0]
        trait_value = traits[1]
        trait_dict = {
            'trait_type': trait_type.strip(),
            'value': trait_value.strip(),
        }

        attributes_dict_list.append(trait_dict)

    #maintain team names
    team_name = df.at[index, 'TEAM NAMES']
    if str(team_name) != 'nan':
        new_team_name = team_name

    info = {
        "format": "CHIP-0007",
        "name": df.at[index, 'Filename'],
        "description": df.at[index, 'Description'],
        "minting_tool": new_team_name if str(team_name) == 'nan' else team_name,
        "sensitive_content": False,
        "series_number": int(df.at[index, 'Series Number']),
        "series_total": 420,
        "attributes": [
            {
                "trait_type": "Gender",
                "value": df.at[index, 'Gender'],
            },
        ] + attributes_dict_list,
        "collection": {
            "name": "Zuri NFT Collection for Free Lunch",
            "id": "b774f676-c1d5-422e-beed-00ef5510c64d",
        },
    }

    # Serializing json
    json_object = json.dumps(info, indent=4)

    #create json file
    json_filename = f"nft{df.at[index, 'Filename']}.json"
    json_filepath = os.path.join(os.getcwd(), "json_data", json_filename)

    with open(json_filepath, 'w') as outfile:
        outfile.write(json_object)

    #get hash of json file and add to hash column
    hex_value = sha256_hex(json_filepath)
    df['Hash'] = f"{df.at[index, 'Filename']}.{hex_value}.csv"

#create output csv
df.to_csv(f'new_{csv_file}', index=False)

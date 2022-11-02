import hashlib
import json


def content_list(csv_file):
    '''
    -Takes a filename
    -Reads the file in the current working directory
    -Returns the contents of the file as a list
    '''
    with open(csv_file, 'r') as f:
        contents = f.readlines()
        for content in contents:
            content = content.strip(r'\n')
        return contents


def sha256_hex(filename):
    '''
    -takes a filename
    -Reads the file in the current working directory
    -Returns the sha256 hex_value of the file
    '''
    with open(filename, 'r') as f:
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
    for content in contents_list[1:]:
        values_of_content_columns = content.split(',')
        info = {
            "format": "CHIP-0007",
            "name": values_of_content_columns[1],
            "description": values_of_content_columns[2],
            "minting_tool": "SuperMinter/2.5.2",
            "sensitive_content": false,
            "series_number": values_of_content_columns[0],
            "series_total": 400,
            "attributes": [
                {
                    "trait_type": "Gender",
                    "value": values_of_content_columns[4],
                },

            ],
            "collection": {
                "name": "HNG NFT Collection",
                "id": values_of_content_columns[3],
            }
        }

        # Serializing json
        json_object = json.dumps(info, indent=4)

        json_filename = f'nft{values_of_content_columns[1]}.json'

        with open(json_filename, 'w') as outfile:
            outfile.write(json_object)

        hex_value = sha256_hex(json_filename)

        content = content + f',{values_of_content_columns[1]}.{hex_value}.csv'

    return content_list


# Get the csv file
csv_file = 'file path'

# Make a list of the file contents
contents = content_list(csv_file)

# Generate and hash jason files. Amend contents
contents = json_gen(contents)

# write result to new csv file
with open('HNG_NFT_DATA.csv', 'w') as f:
    for content in contents:
        f.write(f'{content}\\n')

# Hng-task-2

 A script tat uses CSV provided by the teams, generates a CHIP-0007 compatible json, calculates the sha256 of the json file and append it to each line in the csv (as a filename.output.csv)

## Setup instructions
```
python -r requirements.txt
```
- call the script and pass the name or names of the csv file without spaces
```
python main.py HNGi9.csv
```
## Output

-will create Json files of each row of the csv in the 'json_data' folder
-will create a new csv 'new_filename' with the udated data

## Author
[JPPhilips](https://www.github.com/jpphilips)


## Disclaimers, if any

if not installed, need to:
- python.exe

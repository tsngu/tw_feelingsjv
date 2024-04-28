import csv
import json
import argparse

def csv_to_json(csv_file_path, json_file_path):
    # Open the CSV file for reading
    with open(csv_file_path, 'r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t')
        data = []
        for row in csv_reader:
            data.append(row)
    
    # Write the data to a JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

parser = argparse.ArgumentParser(description="convert csv file to json file")
#parser.add_argument("json_string", type=str, help="JSON string to write to the file")
parser.add_argument("input_path", type=str, help="Path to the input file (csv)")
parser.add_argument("output_path", type=str, help="Path to the output file (json)")
args = parser.parse_args()

csv_to_json(args.input_path, args.output_path)

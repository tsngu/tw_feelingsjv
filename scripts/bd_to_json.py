import sqlite3
import json
import argparse

def convert_to_json(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM Jeux")
    columns = [description[0] for description in cur.description]
    results = []
    for row in cur.fetchall():
        result = dict(zip(columns, row))
        results.append(result)
    conn.close()
    return json.dumps(results, indent=4)

parser = argparse.ArgumentParser(description="Write JSON string to a file")
#parser.add_argument("json_string", type=str, help="JSON string to write to the file")
parser.add_argument("input_path", type=str, help="Path to the input file")
parser.add_argument("output_path", type=str, help="Path to the output file")

args = parser.parse_args()

json_data = convert_to_json(args.input_path)
print(json_data)

# Write the JSON string to the file
with open(args.output_path, 'w') as json_file:
    json_file.write(json_data)

print(f"JSON string has been written to {args.output_path}.")
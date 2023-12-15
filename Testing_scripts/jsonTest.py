import re
import json

def counter_generator():
    count = 0
    while True:
        yield count
        count += 1

# Create an instance of the counter generator
counter = counter_generator()

# Sample log text (shortened for demonstration)
log_text = '''
2023-10-03 10:50:03,768 - vb_manager.mm - info - PFT.9f779.1 - ActionPoint(id: 'GTW01') started.
2023-10-03 11:00:17,057 - vb_manager.am - info - PFT.9f779.1 - Action completed.
2023-10-03 11:00:17,288 - vb_manager.mm - info - PFT.9f779.2 - ActionPoint(id: 'C0309') started.
... # Rest of the log text
'''

# Initialize an empty dictionary to store parsed log entries
log_entries = {}

# Define a regex pattern to extract information from log lines
pattern = re.compile(r"(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2},\d{3}) - (\S+) - (\S+) - (\S+\.\S+) - (.*)")

# Split the log text into individual log lines and parse them
for index, line in enumerate(log_text.strip().split('\n')):
    match = pattern.match(line)
    if match:
        log_entry = {
            "timestamp": match.group(1),
            "component": match.group(2),
            "level": match.group(3),
            "identifier": match.group(4),
            "message": match.group(5)
        }
        # Use timestamp as the key to store log entries in the dictionary
        log_entries[f"line{index}"] = log_entry

# Output the dictionary containing log entries
#print(json.dumps(log_entries, indent=2))


original_json = json.dumps(log_entries, indent=2)
data = json.loads(original_json)

# Group items by identifier into a new dictionary

grouped_data = {'values': []}
dict_data = {}
for index, (key, value) in enumerate(sorted(data.items()), start=1):
    identifier = value["identifier"]
    print(value)
    if identifier not in grouped_data["values"]:
        grouped_data["values"].append(identifier)
        num = next(counter)
        grouped_data[f"AP{num}"] = {f"L{index}": value}
    
####### Recursive search algorithm: ######
def find_value(dictionary, value):
    # Iterate through each key-value pair in the dictionary
    for k, v in dictionary.items():
        # Check if the value matches the desired value
        if v == value:
            return k, v  # Return the key and value if found

        # If the current value is another dictionary, recursively search it
        if isinstance(v, dict):
            result = find_value(v, value)
            if result:
                return (k,) + result  # Prepend the current key to the result

    return None  # Return None if the value is not found in the dictionary


# Convert the grouped data back to JSON
grouped_json = json.dumps(grouped_data, indent=2)

print(grouped_json)
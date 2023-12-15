import re

def filter_for_extracting_column_name(column):
    column_content = []
    column_name = ""

    # Using regex to match column name and content within brackets
    match = re.match(r'(\w+)\(([^)]*)\)', column)

    if match:
        column_name = match.group(1)  # Extracting column name
        content = match.group(2)  # Extracting content within brackets

        # Split the content by commas to create a list
        column_content = [item.strip() for item in content.split(',')]
        
    return column_content, column_name


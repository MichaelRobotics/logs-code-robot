import pandas as pd
import re

# Sample raw data
data = {
    'Column_1 (ID)': [1, 2, 3],
    'Column_2 (Name)': ['Alice', 'Bob', 'Charlie'],
    'Column_3 (Age)': [25, 30, 28]
}

# Create a DataFrame
raw_data = pd.DataFrame(data)

# List of columns to search
column_search_list = ['ID', 'Age']

# Code snippet
for col in raw_data.columns:
    # Remove the string within brackets including brackets
    cleaned_col_name = re.sub(r'\(.*\)', '', col).strip()

    # Check if the cleaned column name is in column_search_list
    if cleaned_col_name in column_search_list:
        print(f"{cleaned_col_name} is in column_search_list")
    else:
        print(f"{cleaned_col_name} is not in column_search_list")

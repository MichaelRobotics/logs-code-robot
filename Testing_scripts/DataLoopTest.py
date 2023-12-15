import pandas as pd

class Example:
    def __init__(self):
        # Assume self.raw_ap_dataframe is a DataFrame
        self.raw_ap_dataframe = pd.DataFrame({
            'Column1': [1, 2, 3],
            'Column2': ['A', 'B', 'C'],
            'Column3': [4.5, 5.5, 6.5]
        })

    def print_dataframe_format(self):
        row_data_list = []  # List to store row data as dictionaries
        for index, row in self.raw_ap_dataframe.iterrows():
            ap = {}  # Dictionary to store column names and values for the current row
            for column, value in row.items():
                ap[column] = value  # Store column name and its corresponding value in ap  # Append the dictionary for the current row to the list
            row_data_list.append(ap)
            break

        # Convert the list of dictionaries to a DataFrame and print it
        row_data_df = pd.DataFrame(row_data_list)
        print(row_data_df)

# Create an instance of the class
example_obj = Example()

# Call the method to print row data in DataFrame-like format
example_obj.print_dataframe_format()

import pandas as pd

# Creating sample dataframes
data1 = {'A': [1, 2, 3],
         'B': ['a', 'b', 'c']}
data2 = {'A': [4, 5, 6],
         'B': ['d', 'e', 'f']}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

table =[]

if table:
    print("Table is not empty")
# Concatenating rows using concat(
merged_df = pd.concat([df1, df2], axis=0)
print(merged_df)

# Or using append() method
merged_df = df1.append(df2, ignore_index=True)
print(merged_df)
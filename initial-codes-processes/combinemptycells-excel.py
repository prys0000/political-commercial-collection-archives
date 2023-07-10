import pandas as pd

# Read the Excel file into a data frame
df = pd.read_excel(r'D:\GITHUB\GITHUB\combined2.xlsx')

# Specify the source column and target column
source_column = 'OFFICE'
target_column = 'OFF'

# Copy text from source column to target column if target column is empty
df[target_column] = df.apply(lambda row: row[source_column] if pd.isnull(row[target_column]) else row[target_column], axis=1)

# Save the modified data frame as a new Excel file
output_file = 'modified_file.xlsx'
df.to_excel(output_file, index=False)

print(f"Modified Excel file saved to {output_file}")

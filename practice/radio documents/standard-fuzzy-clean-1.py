import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Read the input Excel file
input_file = 'path/to/your/input_file.xlsx'
df = pd.read_excel(input_file)

# Columns to compare and standardize
column_to_standardize = 'Column1'
reference_column = 'ReferenceColumn'

# Function to find the best match from the reference column
def find_best_match(value, reference_column_values):
    return process.extractOne(value, reference_column_values)[0]

# Get unique values from the reference column
reference_values = df[reference_column].unique()

# Iterate through the column to standardize
standardized_names = []
for name in df[column_to_standardize]:
    best_match = find_best_match(name, reference_values)
    standardized_names.append(best_match)

# Add the standardized names to a new column in the DataFrame
df['Standardized Names'] = standardized_names

# Save the updated DataFrame to a new Excel file
output_file = 'path/to/your/output_file.xlsx'
df.to_excel(output_file, index=False)

print(f"Standardized names saved to {output_file}")

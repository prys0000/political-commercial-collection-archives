import pandas as pd

# Read the input Excel file
input_file = 'path/to/your/input_file.xlsx'
df = pd.read_excel(input_file)

# Combine columns
# Assuming you want to combine columns A, B, and C into a new column named "Combined"
df['Combined'] = df['A'].astype(str) + df['B'].astype(str) + df['C'].astype(str)

# Save the updated DataFrame to a new Excel file
output_file = 'path/to/your/output_file.xlsx'
df.to_excel(output_file, index=False)

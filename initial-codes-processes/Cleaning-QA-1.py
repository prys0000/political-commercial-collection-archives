import pandas as pd
import string
from language_tool_python import LanguageTool

# Read the worksheet
file_path = r"D:\GITHUB\practice tv - qa.csv"
df = pd.read_csv(file_path)

# Rename the columns to column letters
column_letters = list(string.ascii_uppercase) + [f"A{letter}" for letter in string.ascii_uppercase]
df.columns = column_letters[:len(df.columns)]

# Check for spelling, grammar, and acronym errors
tool = LanguageTool('en-US')
errors = []

for column in df.columns:
    for cell in df[column]:
        matches = tool.check(cell)
        errors.extend(matches)

# Sort columns and rows by Election year, State, Last_Name, and First_Name
df.sort_values(by=['E', 'N', 'J', 'K'], inplace=True)

# Display or save the cleaned and sorted DataFrame
print(df)
# Or save it to a new CSV file
df.to_csv("cleaned_and_sorted_worksheet.csv", index=False)

import os
import pandas as pd

# Folder path containing the Excel files
folder_path = r"D:\GITHUB\GITHUB\TV_Candidates"

# Create an empty list to store the data frames
dfs = []

# Iterate through the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx"):
        # Generate the full path of the Excel file
        file_path = os.path.join(folder_path, filename)

        # Read the Excel file into a data frame
        df = pd.read_excel(file_path)

        # Append the data frame to the list
        dfs.append(df)

# Concatenate the data frames into a single data frame
combined_df = pd.concat(dfs)

# Save the combined data frame as a new Excel file
output_file = os.path.join(folder_path, "combined.xlsx")
combined_df.to_excel(output_file, index=False)

print(f"Combined Excel file saved to {output_file}")

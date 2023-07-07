import pandas as pd
from fuzzywuzzy import fuzz

# Read the Hsall_members.csv file into a DataFrame
hs_members_df = pd.read_csv(r'D:\GITHUB\HSall_members.csv')

# Read the compiled_list.csv file into a DataFrame
compiled_list_df = pd.read_csv(r'D:\GITHUB\compiled_list.csv', encoding='latin-1', dtype=str, low_memory=False)

# Function to perform fuzzy matching between two strings
def fuzzy_match(string1, string2):
    return fuzz.token_set_ratio(string1.lower(), string2.lower())

# List to store the matched records
matched_records = []

# Iterate through each row in the compiled_list DataFrame
for index, compiled_row in compiled_list_df.iterrows():
    best_match_ratio = 0
    best_match_index = -1

    # Iterate through each row in the hs_members DataFrame
    for hs_index, hs_row in hs_members_df.iterrows():
        match_ratio = fuzzy_match(compiled_row['lastname_firstname'], hs_row['bioname'])

        # Update the best match if a higher ratio is found
        if match_ratio > best_match_ratio:
            best_match_ratio = match_ratio
            best_match_index = hs_index

    # Add the matched record to the list
    if best_match_ratio > 80:  # Adjust the threshold as needed
        matched_records.append(hs_members_df.loc[best_match_index])

# Create a new DataFrame with the matched records
matched_records_df = pd.DataFrame(matched_records)

# Write the matched records to an Excel file
matched_records_df.to_excel('matched_records.xlsx', index=False)

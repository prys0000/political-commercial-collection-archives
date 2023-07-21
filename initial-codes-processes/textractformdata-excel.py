import os
import PyPDF2
import pandas as pd

# Path to the directory containing the form files
forms_directory = r"D:\GITHUB\Practice\tv files"

# List to store extracted form data
form_data = []

# Iterate over the form files in the directory
for filename in os.listdir(forms_directory):
    if filename.endswith(".pdf"):
        # Extract text from the form file
        file_path = os.path.join(forms_directory, filename)
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            extracted_text = ""
            for page in pdf_reader.pages:
                extracted_text += page.extract_text()

        # Process the extracted text and extract relevant information
        # You can use techniques like regular expressions or string manipulation
        # to extract specific fields from the text

        # Extracted field values
        field1 = extract_field1(text, TAPE_ID)
        field2 = extract_field2(text, OFFICE_SOUGHT)
        field3 = extract_field3(text, FORMAT)
        field4 = extract_field4(text, DATE_RECEIVED)
        field5 = extract_field5(text, STATE)
        field6 = extract_field6(text, ELECTION_YEAR)
        field7 = extract_field7(text, DISTRICT)
        field8 = extract_field8(text, PARTY_AFFILIATION)
        field9 = extract_field9(text, CANDIDATE_NAME)
        field10 = extract_field10(text, INCUMBENT)
        field11 = extract_field11(text, FORMAT)
        field12 = extract_field12(text, TAPE_SHELF_ID)
        field13 = extract_field13(text, ELECTION_TYPE)
        field14 = extract_field14(text, RESULTS)
        field15 = extract_field15(text, AD_PRODUCTION_AGENCY)
        field16 = extract_field16(text, RECEIVED_FROM)
        field17 = extract_field17(text, TAPE_DESCR_DIMENSIONS)
        field18 = extract_field18(text, TIMER_NUMBER)
        field19 = extract_field19(text, SLATE_ID_NUMBER)
        field20 = extract_field20(text, DATE)
        field21 = extract_field21(text, COMMERCIAL_TITLE)
        field22 = extract_field22(text, COMMERCIAL_DESCRIPTION)

        # Add the extracted form data to the list
        form_data.append({
            'File Name': filename,
            'Field1': TAPE_ID
            'Field2': OFFICE_SOUGHT
            'Field3': FORMAT
            'Field4': DATE_RECEIVED
            'Field5': STATE
            'Field6': ELECTION_YEAR
            'Field7': DISTRICT
            'Field8': PARTY_AFFILIATION
            'Field9': CANDIDATE_NAME
            'Field10': INCUMBENT
            'Field11': FORMAT
            'Field12': TAPE_SHELF_ID
            'Field13': ELECTION_TYPE
            'Field14': RESULTS
            'Field15': AD_PRODUCTION_AGENCY
            'Field16': RECEIVED_FROM
            'Field17': TAPE_DESCR_DIMENSIONS
            'Field18': TIMER_NUMBER
            'Field19': SLATE_ID_NUMBER
            'Field20': DATE
            'Field21': COMMERCIAL_TITLE
            'Field22': COMMERCIAL_DESCRIPTION
        })

# Create a DataFrame from the form data
df = pd.DataFrame(form_data)

# Save the DataFrame to an Excel file
output_file = r"D:\GITHUB\form_data.xlsx"
df.to_excel(output_file, index=False)
print(f"Form data extracted and saved to {output_file}")

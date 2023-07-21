import openpyxl

def clean_text_in_excel(file_path, sheet_name):
    # Load the workbook
    workbook = openpyxl.load_workbook(file_path)

    # Select the sheet
    sheet = workbook[sheet_name]

    # Iterate over the rows in the sheet
    for row in sheet.iter_rows():
        # Iterate over the cells in each row
        for cell in row:
            # Check if the cell contains text
            if cell.data_type == 's':
                # Clean the text by removing leading and trailing spaces and converting to lowercase
                cleaned_text = cell.value.strip().lower()
                # Update the cell value with the cleaned text
                cell.value = cleaned_text

    # Save the updated workbook
    workbook.save(file_path)

# Example usage
file_path = r'D:\GITHUB\Practice\tv files\extracted_text.xlsx'
sheet_name = '1978'
clean_text_in_excel(file_path, sheet_name)

import pandas as pd
from docx import Document
from docx.shared import RGBColor
import os

def docx_to_excel(filename):
    doc = Document(filename)

    rows = []
    current_row = []

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if 'received' in run.text.lower() and run.bold and run.font.color.rgb == RGBColor(255, 0, 0):
                if current_row:  # If current_row is not empty, add it to rows
                    rows.append(current_row)
                current_row = [run.text]  # Start a new row with 'received'
            else:
                current_row.append(run.text)

    # Don't forget to add the last row
    if current_row:
        rows.append(current_row)

    # Create a DataFrame and save it to an Excel file
    df = pd.DataFrame(rows)
    df.to_excel('output.xlsx', index=False)

docx_to_excel(r'D:\GITHUB\date_formatted_formatted_standardized_cleaned_file.docx')

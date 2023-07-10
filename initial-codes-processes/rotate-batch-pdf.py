import os
from PyPDF2 import PdfReader, PdfWriter

# Directory path containing the PDF files
directory = r'D:\GITHUB\GITHUB\Binder Scans - Candidates'

# Rotation angle in degrees (90 for clockwise rotation, 270 for counterclockwise rotation)
rotation_angle = 90

# Iterate over each PDF file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.pdf'):
        # Open the PDF file
        input_path = os.path.join(directory, filename)
        pdf = PdfReader(input_path)

        # Create a new PDF writer
        output_pdf = PdfWriter()

        # Iterate over each page in the PDF
        for page_num in range(len(pdf.pages)):
            # Rotate the page
            page = pdf.pages[page_num]
            page.rotate = (page.rotate + rotation_angle) % 360

            # Add the rotated page to the output PDF
            output_pdf.add_page(page)

        # Save the rotated PDF to a new file
        output_path = os.path.join(directory, 'rotated_' + filename)
        with open(output_path, 'wb') as output_file:
            output_pdf.write(output_file)

        print(f'{filename} has been rotated and saved as {output_path}')

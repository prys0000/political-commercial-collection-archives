from PyPDF2 import PdfFileMerger, PdfReader, PdfWriter
import os

pdf_folder = r"C:\Users\user\Desktop\NEH ACSC\Process-1-NEH-Test\Pdf-Owen"
watermark_path = r"C:\Users\user\Desktop\NEH ACSC\Process-1-NEH-Test\CAC.pdf"
output_folder = r"C:\Users\user\Desktop\NEH ACSC\Process-1-NEH-Test\Reduced_watermarked-Owen"

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the watermark PDF
watermark_pdf = PdfReader(watermark_path)
watermark_page = watermark_pdf.pages[0]

# Process all PDF files in the input folder
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        merged_path = os.path.join(output_folder, filename)

        with open(pdf_path, "rb") as input_file:
            input_pdf = PdfReader(input_file)

            output = PdfWriter()

            for i in range(len(input_pdf.pages)):
                pdf_page = input_pdf.pages[i]
                pdf_page.merge_page(watermark_page)
                pdf_page.compress_content_streams()
                output.add_page(pdf_page)

            with open(merged_path, "wb") as merged_file:
                output.write(merged_file)

print("Processing complete.")

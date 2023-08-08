import os
import fitz  # PyMuPDF

input_folder = r"C:\Users\user\Desktop\NEH ACSC\Process-1-NEH-Test\Pdf-Owen"
output_folder = r"C:\Users\user\Desktop\NEH ACSC\Process-1-NEH-Test\Searchable-PDFs"
watermark_image_path = r"C:\Users\user\Desktop\NEH ACSC\Process-1-NEH-Test\CAC.png"  # Update this path to your watermark.png

# Ensure the output directory exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# First, make the PDFs searchable with invisible annotations
for filename in os.listdir(input_folder):
    if filename.endswith(".pdf"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        pdf_document = fitz.open(input_path)

        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text = page.get_text("text")

            # Just create a generic rectangle anywhere on the page since the text is invisible.
            rect = fitz.Rect(0, 0, 100, 100)
            text_annotation = page.add_freetext_annot(rect, text, fontname="helv", fontsize=12)
            text_annotation.set_opacity(0.0)  # Set annotation to invisible
            text_annotation.update()

        pdf_document.save(output_path)
        pdf_document.close()

# Now, watermark the output PDFs
for filename in os.listdir(output_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(output_folder, filename)
        pdf_document = fitz.open(pdf_path)

        for page in pdf_document:
            # Overlay the watermark onto the page
            image_rect = fitz.Rect(page.rect.width * 0.05, page.rect.height * 0.9, page.rect.width * 0.95, page.rect.height)
            page.insert_image(image_rect, filename=watermark_image_path, overlay=True)

        new_pdf_path = os.path.join(output_folder, "temp_" + filename)
        pdf_document.save(new_pdf_path)
        pdf_document.close()  # Close the file to release its lock

        # Make sure the file is really closed before we proceed
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        os.rename(new_pdf_path, pdf_path)

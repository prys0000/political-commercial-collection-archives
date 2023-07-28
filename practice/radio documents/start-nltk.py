import spacy
import pandas as pd
import os

# Load the trained spaCy NER model
model_path = r"D:\GITHUB\Practice\tv files\TRAINING DATASETS\en_core_political_science_model"
nlp = spacy.load(model_path)

def extract_text_from_pdf(pdf_file_path):
    # Code to read and extract text from the PDF file goes here
    # You can use libraries like PyPDF2, pdfminer.six, or pdfplumber to read PDFs

    # For example, using pdfplumber:
    import pdfplumber

    text = ""
    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    return text

def extract_named_entities(pdf_file_path):
    text = extract_text_from_pdf(pdf_file_path)
    doc = nlp(text)
    named_entities = [(ent.text, ent.label_) for ent in doc.ents]
    return named_entities

def save_to_excel(pdf_file_path, output_folder):
    named_entities = extract_named_entities(pdf_file_path)

    # Convert the named entities to a pandas DataFrame
    df = pd.DataFrame(named_entities, columns=["Entity", "Type"])

    # Create the output Excel file path
    output_file_path = os.path.join(output_folder, r"D:\GITHUB\Practice\tv files\TRAINING DATASETS\named_entities_output.xlsx")

    # Write the DataFrame to Excel
    df.to_excel(output_file_path, index=False)

    print("Named entities saved to Excel file.")

if __name__ == "__main__":
    pdf_file_path = r"D:\GITHUB\Practice\tv files\TRAINING DATASETS\tv-sample-orig-scanned.pdf"
    output_folder = r"D:\GITHUB\Practice\tv files\TRAINING DATASETS"

    save_to_excel(pdf_file_path, output_folder)

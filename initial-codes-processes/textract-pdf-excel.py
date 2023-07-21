import boto3
import botocore.config
import os
import PyPDF2
import docx2txt
from PIL import Image
import pytesseract
import pandas as pd
import tempfile

# Create a session using your AWS credentials
session = boto3.Session(
    aws_access_key_id='AKIA5FPWHKQOXTCJNL5T',
    aws_secret_access_key='gKVaerOuSNyiHVycSFIw2RkOdgPhJ631HGdriInF',
    region_name='us-east-1'
)

# Set the S3 bucket name
s3_bucket_name = "pccgithub"
aws_region = 'us-east-1'

# Initialize the DataFrame to store the extracted text
df = pd.DataFrame(columns=["File Name", "Page", "Extracted Text"])

# Initialize Tesseract OCR for handwritten text extraction
pytesseract.pytesseract.tesseract_cmd = r'Path_to_tesseract_executable'

# Initialize AWS Textract client
textract_client = session.client('textract', region_name=aws_region)

# Configure the maximum timeout for S3 client
s3_client = session.client('s3', region_name=aws_region, config=botocore.config.Config(connect_timeout=5, read_timeout=5))

# Retrieve the list of objects in the S3 bucket
response = s3_client.list_objects(Bucket=s3_bucket_name)

# Iterate over the objects in the bucket
for obj in response.get('Contents', []):
    # Get the object key
    object_key = obj['Key']

    # Get the file extension
    file_extension = os.path.splitext(object_key)[1].lower()

    if file_extension == ".pdf":
        # Extract text from PDF
        pdf_file_path = os.path.join(tempfile.gettempdir(), object_key)
        s3_client.download_file(s3_bucket_name, object_key, pdf_file_path)
        with open(pdf_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages, start=1):
                extracted_text = page.extract_text()
                df = pd.concat([df, pd.DataFrame({"File Name": [object_key], "Page": [page_num], "Extracted Text": [extracted_text]})],
                               ignore_index=True)

    elif file_extension == ".docx":
        # Extract text from DOCX
        docx_file_path = os.path.join(tempfile.gettempdir(), object_key)
        s3_client.download_file(s3_bucket_name, object_key, docx_file_path)
        extracted_text = docx2txt.process(docx_file_path)
        df = pd.concat([df, pd.DataFrame({"File Name": [object_key], "Page": [1], "Extracted Text": [extracted_text]})],
                       ignore_index=True)

    elif file_extension in [".jpg", ".jpeg", ".png", ".tiff"]:
        # Extract text from image using OCR
        image_file_path = os.path.join(tempfile.gettempdir(), object_key)
        s3_client.download_file(s3_bucket_name, object_key, image_file_path)
        image = Image.open(image_file_path)

        # Check if the image contains handwritten text using Tesseract OCR
        extracted_text = pytesseract.image_to_string(image)

        # If Tesseract OCR does not detect handwritten text, use AWS Textract for typewritten text extraction
        if not extracted_text:
            with open(image_file_path, 'rb') as file:
                response = textract_client.detect_document_text(Document={'Bytes': file.read()})
            text = [item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE']
            extracted_text = ' '.join(text)

        df = pd.concat([df, pd.DataFrame({"File Name": [object_key], "Page": [1], "Extracted Text": [extracted_text]})],
                       ignore_index=True)

    elif file_extension == ".txt":
        # Extract text from TXT
        txt_file_path = os.path.join(tempfile.gettempdir(), object_key)
        s3_client.download_file(s3_bucket_name, object_key, txt_file_path)
        with open(txt_file_path, 'r') as file:
            extracted_text = file.read()
        df = pd.concat([df, pd.DataFrame({"File Name": [object_key], "Page": [1], "Extracted Text": [extracted_text]})],
                       ignore_index=True)

# Save the DataFrame to an Excel file
output_file = r"D:\extracted_text.xlsx"
df.to_excel(output_file, index=False)
print(f"Extraction completed. Results saved to {output_file}")

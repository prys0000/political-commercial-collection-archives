import pandas as pd
import spacy

# Load the English language model for spaCy
nlp = spacy.load("en_core_web_sm")

# Load the Excel data into a pandas DataFrame
df = pd.read_excel(r'D:\GITHUB\Practice\audio-recog-output1.xlsx')  # Replace with your Excel file path

# Check if 'Text' column exists in the DataFrame
if 'Text' in df.columns:
    # Function to extract proper nouns from a text
    def extract_proper_nouns(text):
        doc = nlp(text)
        return [ent.text for ent in doc.ents if ent.label_ in ['PERSON', 'ORG', 'GPE', 'LOC', 'NORP']]

    # Apply the function to the 'Text' column
    df['Text_proper_nouns'] = df['Text'].apply(extract_proper_nouns)

    # Write the DataFrame back to Excel
    df.to_excel('data_with_proper_nouns.xlsx', index=False)
else:
    print("Column 'Text' does not exist in the DataFrame.")

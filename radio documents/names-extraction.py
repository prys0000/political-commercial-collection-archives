import pandas as pd
import spacy

# Load the English language model for spaCy
nlp = spacy.load("en_core_web_sm")

# Load the Excel data into a pandas DataFrame
df = pd.read_excel('data.xlsx')  # Replace with your Excel file path

# Function to extract proper nouns from a text
def extract_proper_nouns(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ in ['PERSON', 'ORG', 'GPE', 'LOC', 'NORP']]

# Apply the function to each cell in the DataFrame
for column in df.columns:
    df[f'{column}_proper_nouns'] = df[column].apply(extract_proper_nouns)

# Write the DataFrame back to Excel
df.to_excel('data_with_proper_nouns.xlsx', index=False)

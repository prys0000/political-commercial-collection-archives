import os
import pandas as pd
import spacy
import pdfplumber
from sklearn.model_selection import train_test_split
from spacy.training.example import Example
import random  # Add the import statement for the 'random' module

def train_model(nlp, train_examples):
    # Create an optimizer
    optimizer = nlp.begin_training()

    # Training loop
    for epoch in range(10):
        random.shuffle(train_examples)
        losses = {}
        # Batch examples and iterate over them
        for batch in spacy.util.minibatch(train_examples, size=8):
            nlp.update(batch, drop=0.5, sgd=optimizer, losses=losses)
        print("Epoch:", epoch, "Losses:", losses)

    return nlp


# Load the annotated data from the CSV file
data = pd.read_csv(r"D:\GITHUB\Practice\tv files\TRAINING DATASETS\ner_training_politicalscience.csv", encoding='latin-1')

# Split the data into training and evaluation sets
train_data, eval_data = train_test_split(data, test_size=0.2, random_state=42)

# Train the Named Entity Recognition (NER) model using the training data
nlp = spacy.blank("en")  # Create a blank spaCy model
ner = nlp.add_pipe("ner", name="my_ner")

# Add custom labels to the NER component
custom_labels = ['LOCATION_STATE', 'ORGANIZATION_AGENCY', 'POLITICAL_PARTY']

for label in custom_labels:
    ner.add_label(label)

# Convert the labels to the BILOU format
def to_bilou(annotations):
    bilou_annotations = []
    for label in annotations:
        if label in custom_labels:
            bilou_annotations.append(label)
        else:
            bilou_annotations.append('O')
    return bilou_annotations

# Convert the training data to spaCy format
train_examples = []
for _, annotations in train_data.iterrows():
    bilou_annotations = to_bilou(annotations['label'])
    entities = []
    start = 0
    for i, label in enumerate(bilou_annotations):
        if label != 'O':
            if i == 0 or bilou_annotations[i - 1] != label:
                start = i
            if i == len(bilou_annotations) - 1 or bilou_annotations[i + 1] != label:
                entities.append((start, i + 1, label))

    train_examples.append(Example.from_dict(nlp.make_doc(annotations['text']), {"entities": entities}))

# Initialize the model with the tok2vec component
nlp.initialize(lambda: train_examples)

# Define the optimizer and loss function
optimizer = nlp.begin_training()
losses = {}

# Train the NER model
nlp = train_model(nlp, train_examples)

# Save the trained model to a specific location
output_folder = r"D:\GITHUB\Practice\tv files\TRAINING DATASETS"
output_model_path = os.path.join(output_folder, "en_core_political_science_model")
nlp.to_disk(output_model_path)

# Load the trained model
nlp = spacy.load(output_model_path)

def extract_text_from_pdf(pdf_file_path):
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

def save_to_txt(pdf_file_path, output_folder):
    named_entities = extract_named_entities(pdf_file_path)

    # Create the output .txt file path
    output_file_path = os.path.join(output_folder, "named_entities_output.txt")

    # Write the named entities to the .txt file
    with open(output_file_path, "w", encoding="utf-8") as txt_file:
        for entity, label in named_entities:
            txt_file.write(f"Entity: {entity}, Type: {label}\n")

if __name__ == "__main__":
    pdf_file_path = r"D:\GITHUB\Practice\tv files\TRAINING DATASETS\tv-sample-orig-scanned.pdf"
    output_folder = r"D:\GITHUB\Practice\tv files\TRAINING DATASETS"

    save_to_txt(pdf_file_path, output_folder)

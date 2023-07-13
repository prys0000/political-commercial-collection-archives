import os
import speech_recognition as sr
import pandas as pd

# Folder path containing audio files
folder_path = r'D:\GITHUB\Practice\radio files'

# List to store the extracted text and file names
data = []

# Initialize a speech recognizer object
recognizer = sr.Recognizer()

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is an audio file (you can customize the check based on your file types)
    if filename.endswith('.wav') or filename.endswith('.mp3') or filename.endswith('.flac'):
        try:
            # Construct the full file path
            file_path = os.path.join(folder_path, filename)

            # Load the audio file
            with sr.AudioFile(file_path) as source:
                # Read the audio data
                audio = recognizer.record(source)

                # Perform speech recognition
                text = recognizer.recognize_google(audio)

                # Append the extracted text and file name to the data list
                data.append({'File Name': filename, 'Text': text})
        except Exception as e:
            # Handle any errors that occur during the process
            print(f"Error processing {filename}: {e}")

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Output file path for the Excel file
output_path = r'D:\GITHUB\Practice\radiooutput.xlsx'

# Write the DataFrame to an Excel file
df.to_excel(output_path, index=False)

print(f"Text extraction completed. Results saved in {output_path}.")

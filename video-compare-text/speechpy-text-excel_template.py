import os
import speech_recognition as sr
from moviepy.editor import AudioFileClip
from moviepy.editor import VideoFileClip
import pandas as pd

# Initialize the recognizer
r = sr.Recognizer()

# Folder path containing the video files
folder_path = "ADD YOUR FILEPATH"

# Create an empty list to store the results
results = []

# Create a directory to store the TXT files
output_dir = os.path.join(folder_path, "transcriptions")
os.makedirs(output_dir, exist_ok=True)

# Iterate through the files in the folder
for filename in os.listdir(folder_path):
    try:
        # Generate the full path of the video file
        video_file = os.path.join(folder_path, filename)

        # Load the video file using moviepy
        video = VideoFileClip(video_file)

        # Extract the audio from the video
        audio: AudioFileClip = video.audio

        # Save the extracted audio as a temporary file
        audio_file = "temp_audio.wav"
        audio.write_audiofile(audio_file)

        # Open the audio file for speech recognition
        with sr.AudioFile(audio_file) as source:
            # Load the audio to memory
            audio_data = r.record(source)

            # Use Google Speech Recognition to transcribe the audio
            transcript = r.recognize_google(audio_data)

            # Append the filename and transcript to the results list
            results.append((filename, transcript))

            # Create a TXT file for each transcript
            output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")
            with open(output_file, "w") as f:
                f.write(transcript)

            # Print the transcript
            print(f"Transcript for {filename}: {transcript}")

    except sr.UnknownValueError:
        print(f"Could not transcribe {filename}")
    except sr.RequestError as e:
        print(f"Error occurred during transcription for {filename}: {e}")
    finally:
        # Delete the temporary audio file
        if audio:
            audio.close()

# Check if the lengths of the two arrays are the same
if len(os.listdir(folder_path)) == len(results):
    # Create a pandas DataFrame with the results
    df = pd.DataFrame(results, columns=['Filename', 'Transcript'])

    # Add a column for the file names
    df['File Name'] = [os.path.splitext(filename)[0] + ".txt" for filename in df['Filename']]

    # Save the DataFrame as an Excel file
    output_file = os.path.join(output_dir, "transcripts.xlsx")
    try:
        df.to_excel(output_file, index=False)
        print(f"Transcripts saved to {output_file}")
    except Exception as e:
        print(f"Error occurred while saving transcripts: {e}")
else:
    print("Error: Length mismatch between filenames and transcripts.")

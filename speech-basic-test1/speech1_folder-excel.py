import os
import speech_recognition as sr
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip
import pandas as pd

# Initialize the recognizer
r = sr.Recognizer()

# Folder path containing the video files
folder_path = r"E:\Speechpy\mp4access"

# Create an empty list to store the results
results = []

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

    # Save the DataFrame as an Excel file
    output_file = 'transcripts.xlsx'
    try:
        df.to_excel(output_file, index=False)
        print(f"Transcripts saved to {output_file}")
    except Exception as e:
        print(f"Error occurred while saving transcripts: {e}")
else:
    print("Error: Length mismatch between filenames and transcripts.")

# common workflows - transcriptions

This appendix provides basic scripts for transcribing audio and video files. Each script can be utilized as a template to build customizable options. The results of the following scripts are extremely accurate though there could be errors based on the quality of the digital files. ***note***: processing batch files of a tested **500 audio files** is 00:27:00 hh:mm:ss and **500 video files** is 01:32:00 hh:mm:ss on an average Dell PC. 

## audio transcription workflow

1. Make sure you have the required libraries installed in your virtual environment. If not, you can install them using the following command:
   
```bash
pip install SpeechRecognition moviepy

```
2. Edit the script to set the folder_path variable to the path of the directory containing your audio files and save the script as 'audio_transcription.py'

```python
import os
import speech_recognition as sr
from moviepy.editor import AudioFileClip
from moviepy.editor import VideoFileClip
import pandas as pd

# Initialize the recognizer
r = sr.Recognizer()

# Folder path containing the video files
folder_path = r'Z:\Reagan' #ENTER YOUR PATH TO FILES HERE

# Create an empty list to store the results
results = []

# Create a directory to store the TXT files
output_dir = r'E:\Reagan\transcriptions' #ENTER YOUR PATH TO WHERE YOU WANT TRANSCRIPTIONS HERE
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

```

3. Run the script using the following command:

```bash
python audio_transcription.py
```
4. The script will **transcribe each audio file in the specified directory and save the transcripts to TXT and EXCEL files**.


## video transcription workflow

1. Make sure you have the required libraries installed in your virtual environment. If not, you can install them using the following command:
   
```bash
pip install SpeechRecognition moviepy PyQt5 pandas

```
2. Edit the script to set the folder_path variable to the path of the directory containing your audio files and save the script as 'video_transcription_app.py'

```python
import os
import speech_recognition as sr
from moviepy.editor import AudioFileClip
from moviepy.editor import VideoFileClip
import pandas as pd

# Initialize the recognizer
r = sr.Recognizer()

# Folder path containing the video files
folder_path = r'Z:\Reagan' #ENTER YOUR PATH TO FILES HERE

# Create an empty list to store the results
results = []

# Create a directory to store the TXT files
output_dir = r'E:\Reagan\transcriptions' #ENTER YOUR PATH TO WHERE YOU WANT TRANSCRIPTIONS HERE
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

```


3. Run the script using the following command:

```bash
python video_transcription_app.py

```

4. The script will **transcribe each video file in the specified directory and save the transcripts to TXT and EXCEL files**.

## notes

* Feel free to ***explore and modify the scripts*** to suit your specific needs. These basic workflows provide a ***starting point for audio and video transcription*** tasks using speech recognition.

* Make sure to ***replace audio_transcription.py and video_transcription_app.py with the actual names of your script files***.

#


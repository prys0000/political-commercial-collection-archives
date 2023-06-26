import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip

# Initialize the recognizer
r = sr.Recognizer()

# Folder path containing the video files
folder_path = r"C:/Users/ADMIN/OneDrive - University of Oklahoma/Desktop/SpeechReg/MP4_AccessCopies"

# Iterate through the files in the folder
for filename in os.listdir(folder_path):
    video_file = os.path.join(folder_path, filename)
    try:
        # Load the video file using moviepy
        video = VideoFileClip(video_file)

        # Extract the audio from the video
        audio = video.audio

        # Save the extracted audio as a temporary file
        audio_file = "temp_audio.wav"
        audio.write_audiofile(audio_file)

        # Open the audio file for speech recognition
        with sr.AudioFile(audio_file) as source:
            # Load the audio to memory
            audio_data = r.record(source)

            # Use Google Speech Recognition to transcribe the audio
            transcript = r.recognize_google(audio_data)

            # Print the transcript
            print(f"Transcript for {filename}: {transcript}")

            # Extract individual words from the transcript
            words = transcript.split()

            # Print the extracted words
            print(f"Words extracted from {filename}: {words}")

            # Save the transcript to a text file
            output_file = f"{filename}_transcript.txt"
            with open(output_file, "w") as f:
                f.write(transcript)

            print(f"Transcript saved to {output_file}")

    except sr.UnknownValueError:
        print(f"Could not transcribe {filename}")
    except sr.RequestError as e:
        print(f"Error occurred during transcription for {filename}: {e}")
    finally:
        # Delete the temporary audio file
        if audio:
            audio.close()

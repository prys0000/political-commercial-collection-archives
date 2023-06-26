import time

# Start the timer
start_time = time.time()

import speech_recognition as sr
from moviepy.editor import VideoFileClip

# Initialize the recognizer
r = sr.Recognizer()

# List of video file names
video_files = ["P-1463-71759.mp4", "P-1522-75384.m4v", "P-1841-104282.mp4", "P-720-119861.m4v"]

# Iterate through the video files
for video_file in video_files:
    try:
        # Load the video file using moviepy
        video = VideoFileClip(video_file)

        # Extract the audio from the video
        audio = video.audio

        # Save the extracted audio as a temporary file
        audio_file = f"temp_audio.wav"
        audio.write_audiofile(audio_file)

        # Open the audio file for speech recognition
        with sr.AudioFile(audio_file) as source:
            # Load the audio to memory
            audio_data = r.record(source)

            # Use Google Speech Recognition to transcribe the audio
            transcript = r.recognize_google(audio_data)

            # Print the transcript
            print(f"Transcript for {video_file}: {transcript}")

            # Extract individual words from the transcript
            words = transcript.split()

            # Print the extracted words
            print(f"Words extracted from {video_file}: {words}")

            # Save the transcript to a text file
            output_file = f"{video_file}_transcript.txt"
            with open(output_file, "w") as f:
                f.write(transcript)

            print(f"Transcript saved to {output_file}")

    except sr.UnknownValueError:
        print(f"Could not transcribe {video_file}")
    except sr.RequestError as e:
        print(f"Error occurred during transcription for {video_file}: {e}")
    finally:
        # Delete the temporary audio file
        if audio:
            audio.close()
            audio.close()
# End the timer
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"Elapsed time: {elapsed_time} seconds")
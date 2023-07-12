import os
import speech_recognition as sr
from pydub import AudioSegment
import pandas as pd


def transcribe_audio(folder_path):
    recognizer = sr.Recognizer()

    filenames = []
    transcripts = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3'):
            file_path = os.path.join(folder_path, filename)

            # Convert mp3 file to wav
            audio = AudioSegment.from_mp3(file_path)
            audio.export("temp.wav", format="wav")

            # Transcribe audio file
            with sr.AudioFile("temp.wav") as source:
                audio = recognizer.record(source)
                transcript = recognizer.recognize_sphinx(audio)

            filenames.append(filename)
            transcripts.append(transcript)

    # Delete temporary .wav file
    if os.path.exists("temp.wav"):
        os.remove("temp.wav")

    df = pd.DataFrame({
        'Filename': filenames,
        'Transcript': transcripts
    })
    df.to_excel('transcripts.xlsx', index=False)


transcribe_audio(r'D:\GITHUB\Practice\radio files')

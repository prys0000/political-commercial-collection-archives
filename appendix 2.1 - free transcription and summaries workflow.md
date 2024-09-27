
# creating transcriptions and summaries (free)

Using Gensim, you can implement **free and fast summarization** for your transcripts without the need for [**paid APIs like OpenAI**](https://github.com/openai/whisper) using [**NLTK** (Natural Language Toolkit) and **Gensim**](https://www.nltk.org/howto/gensim.html) libraries in Python. Gensim provides a simple summarization method that can extract key points from a text.

<br>

## **workflow transcription and summarization:**


```python
import os
import speech_recognition as sr
from moviepy.editor import AudioFileClip, VideoFileClip
from pydub import AudioSegment, silence
import pandas as pd
import tempfile
from gensim.summarization import summarize  # Gensim for free summarization

# Initialize recognizer
r = sr.Recognizer()

# Folder paths
folder_path = r'PATH_TO_VIDEO_FILES'
output_dir = r'PATH_TO_SAVE_TRANSCRIPTIONS'
os.makedirs(output_dir, exist_ok=True)

results = []

# Function to detect silence times
def detect_silence_times(audio_file):
    """Detects the start and stop times of speech segments in an audio file."""
    audio_segment = AudioSegment.from_wav(audio_file)
    silent_intervals = silence.detect_silence(
        audio_segment, 
        min_silence_len=500, 
        silence_thresh=audio_segment.dBFS - 16
    )
    speech_intervals = [(silent_intervals[i][1], silent_intervals[i+1][0]) for i in range(len(silent_intervals) - 1)]
    return speech_intervals

# Function to generate summary using Gensim
def generate_summary(transcript):
    """Generate a summary of the transcript using Gensim's summarize."""
    try:
        if len(transcript.split()) > 50:  # Ensure transcript is long enough
            summary = summarize(transcript, word_count=150)
            return summary
        else:
            return "Transcript too short for meaningful summary."
    except ValueError as e:
        print(f"Error summarizing transcript: {e}")
        return "Summary generation failed."

# Iterate through video files
for filename in os.listdir(folder_path):
    try:
        file_path = os.path.join(folder_path, filename)
        video = VideoFileClip(file_path)
        audio = video.audio

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
            audio_file = tmp_audio.name
            audio.write_audiofile(audio_file)

        # Detect speech start/stop times
        speech_intervals = detect_silence_times(audio_file)

        # Transcribe audio using SpeechRecognition
        with sr.AudioFile(audio_file) as source:
            audio_data = r.record(source)
            transcript = r.recognize_google(audio_data)

        # Generate summary using Gensim
        summary = generate_summary(transcript)

        results.append({
            "Filename": filename, 
            "Transcript": transcript, 
            "Summary": summary, 
            "Speech Intervals": speech_intervals
        })

        # Save the transcript
        output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")
        with open(output_file, "w") as f:
            f.write(transcript)

    except Exception as e:
        print(f"Error with {filename}: {e}")
    finally:
        # Clean up temporary files
        if os.path.exists(audio_file):
            os.remove(audio_file)
```

<br>



## potential limitations of [gensim](https://www.nltk.org/howto/gensim.html):
- **Gensim’s summarization** works best for larger texts and might not provide meaningful summaries for very short transcripts.
- It **extracts sentences** rather than generating a human-like abstract, which may differ from OpenAI’s more creative output.

<br>



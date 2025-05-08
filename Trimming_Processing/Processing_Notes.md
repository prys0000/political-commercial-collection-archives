# Political Advertisement Analysis Pipeline: Technical Documentation

## Overview

This script [fast_house_pipeline.py](https://github.com/prys0000/political-commercial-collection-archives/blob/c97381ea544ab1032515425bdd86b11b357e34b3/scripts/summarizeAI.py) implements a comprehensive end-to-end pipeline for analyzing political campaign advertisements. The system processes video files through multiple stages of analysis to extract transcripts, key visual frames, AI-generated descriptions, and concise summaries. This multimodal approach combines audio transcription, computer vision, and natural language processing to create a rich dataset for political advertisement research.

## Pipeline Workflow

The script executes four main processing stages in sequence:

1. **Speech Transcription** - Using Whisper-v3 to convert spoken content to text
2. **Frame Extraction** - Capturing key visual frames through two methods:
   - Speech-centered keyframes (aligned with detected speech)
   - Regular-interval frames (at consistent time points)
3. **Visual Content Analysis** - Using GPT-4-Vision to describe visual frames
4. **Video Summarization** - Generating concise 50-word ad summaries

## System Requirements

### Dependencies

- **Core Python Libraries**: pandas, numpy, tqdm, pathlib, concurrent.futures
- **Machine Learning Models**: 
  - OpenAI API (GPT-4o, GPT-4-turbo)
  - Whisper-v3 via faster_whisper
- **Multimedia Processing**: 
  - FFmpeg/FFprobe for video manipulation
  - PIL (Python Imaging Library) for image handling
- **Data Handling**: json, base64, csv

### Hardware Requirements

- CUDA-compatible GPU (for Whisper transcription)
- Sufficient disk space for storing extracted frames
- Internet connection for API calls

## Configuration Parameters

The script uses the following key configuration settings:

| Parameter | Description |
|-----------|-------------|
| ROOT | Base directory for all processing |
| VIDEO_DIR | Source directory for MP4 files |
| METADATA_F | CSV file with video metadata |
| TRANSCRIPT_* | Directories for transcript outputs (JSON/TSV/TXT) |
| FRAME_* | Directories for extracted frames |
| DESC_* | Directories for frame descriptions |
| SUMMARY_DIR | Directory for final video summaries |
| N_FFMPEG_PROC | Number of concurrent FFmpeg processes |
| N_GPT_FRAMES | Concurrent GPT frame description jobs |
| N_GPT_SUMMARIES | Concurrent GPT summary jobs |

## Detailed Process Flow

### 1. Speech Transcription

The script uses Whisper-v3, a state-of-the-art speech recognition model, to transcribe the audio from each video file:

```python
segments, _ = WHISPER_MODEL.transcribe(
    str(mp4), beam_size=5,
    temperature=[0.0, 0.2, 0.4],
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=500),
    word_timestamps=False
)
```

**Key Features**:
- Uses beam search with size 5 for improved accuracy
- Applies temperature sampling for varied outputs
- Employs Voice Activity Detection (VAD) to filter non-speech
- Outputs in three formats:
  - Plain text (full transcript)
  - JSON (with detailed segment metadata)
  - TSV (tab-separated with start/end timestamps)

### 2. Frame Extraction

The pipeline extracts two sets of frames from each video:

#### A. Speech-Centered Frames
Extracts frames at the midpoint of each spoken segment:

```python
mid = (seg['start'] + seg['end']) / 2
```

This approach captures visuals that align with speech content, ensuring frames are relevant to the verbal messaging.

#### B. Regular-Interval Frames
Extracts frames at consistent time intervals (every 3 seconds):

```python
max_ms = min(180_000, max(3000, int(dur*1000)))
steps = max(1, max_ms // 3000)
```

Key features:
- Adaptive interval based on video duration
- Maximum of 60 frames (for 3-minute videos)
- Minimum of 1 frame for very short videos
- Intelligent handling of video boundaries

Both methods use FFmpeg to extract high-quality JPEG frames with careful parameter settings to ensure proper encoding and dimension handling:

```python
cmd = [
    FFMPEG, '-hide_banner', '-loglevel', 'error', '-y',
    '-ss', f"{ts:.3f}", '-i', str(path),
    '-vframes', '1', '-q:v', '2', str(out_jpg)
]
```

### 3. Visual Content Analysis

The script uses GPT-4o (Vision) to analyze each extracted frame, generating concise descriptions focused on visual content:

```python
resp = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
            ]
        }
    ],
    max_tokens=100
)
```

**Key Features**:
- Base64 encoding of images for API submission
- Carefully crafted prompt that includes:
  - Election year context
  - Party affiliation
  - Candidate information
  - Full transcript for additional context
- Prompt guidelines for 15-word objective descriptions
- Special handling for "anti-candidate" ads
- Rate limiting protection with exponential backoff

The prompt instructs the model to focus on objective visual features while avoiding inference about identities or intent, ensuring descriptions are fact-based rather than interpretive.

### 4. Video Summarization

The final stage synthesizes all collected data into concise 50-word summaries of each advertisement:

```python
resp = openai_client.chat.completions.create(
    model="gpt-4-turbo",
    temperature=0.0,
    top_p=1.0,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1000
)
```

**Key Features**:
- Uses GPT-4-turbo for optimal language generation
- Zero temperature setting for deterministic outputs
- Incorporates multi-modal information:
  - Full transcript text
  - Chronologically ordered frame descriptions
  - Metadata about candidate, party, election year
- Specific 50-word length target for standardized outputs
- Special handling for attack ads vs. promotional ads

## Error Handling and Resilience

The script implements comprehensive error handling throughout:

1. **Transcript Fallbacks**: Uses placeholder text if transcript files are missing
2. **Rate Limit Handling**: Implements exponential backoff for API rate limits
3. **IO Error Protection**: Handles file read/write errors with appropriate logging
4. **Metadata Fallbacks**: Creates default metadata if CSV can't be loaded
5. **Process Monitoring**: Detailed logging to file and console output

Example of retry logic with exponential backoff:
```python
wait_time = 5  # Start with 5 seconds
for attempt in range(3):  # Try 3 times
    log.warning(f"Rate limited, waiting {wait_time}s before retry ({attempt+1}/3)")
    time.sleep(wait_time)
    wait_time *= 2  # Exponential backoff
    # Retry API call...
```

## Concurrency and Optimization

The script uses multiple concurrency approaches for optimal performance:

1. **Sequential Core Pipeline**: Main processing stages run in sequence
2. **Parallel Frame Extraction**: Uses process pool for CPU-intensive frame extraction
3. **Threaded API Calls**: Uses thread pools for network-bound API operations
4. **Batched Processing**: Processes smaller batches to manage API rate limits
5. **Inter-batch Delays**: Adds delays between batches to prevent rate limiting

## Directory Structure and Output Organization

The pipeline creates and organizes outputs in a structured hierarchy:

```
ROOT/
├── pres_ad_whisptranscripts_json/  # JSON transcripts with metadata
├── pres_ad_whisptranscripts_tsv/   # Tab-separated transcripts with timestamps
├── pres_ad_whisptranscripts_txt/   # Plain text transcripts
├── keyframes_speechcentered/       # Frames extracted at speech midpoints
├── keyframes_regintervals/         # Frames at regular time intervals
├── GPT_frame_descriptions_speechcentered/ # Descriptions of speech frames
├── GPT_frame_descriptions_regintervals/   # Descriptions of interval frames
└── GPT_video_summaries/            # Final 50-word ad summaries
```

Each directory contains files named consistently to allow easy cross-referencing. For example, a video `P-1234-5678.mp4` would generate outputs like:
- `P-1234-5678.txt` (transcript)
- `P-1234-5678_1500.jpg` (frame at 1.5 seconds)
- `P-1234-5678_1500.txt` (description of that frame)
- `P-1234-5678.txt` (in the summaries directory - final summary)

## Setup and Usage Instructions

1. **Environment Setup**:
   - Install required Python packages: `pandas`, `numpy`, `tqdm`, `openai`, `faster_whisper`, `Pillow`
   - Ensure FFmpeg and FFprobe are installed and in your system PATH
   - Have a CUDA-compatible GPU for Whisper transcription

2. **Directory Configuration**:
   - Update the `ROOT` path to your desired working directory
   - Ensure the `VIDEO_DIR` points to where your MP4 files are located
   - Set `METADATA_F` to point to your CSV metadata file

3. **API Configuration**:
   - Set your OpenAI API key in the `OPENAI_KEY` variable or via environment variables

4. **Performance Tuning**:
   - Adjust `N_FFMPEG_PROC`, `N_GPT_FRAMES`, and `N_GPT_SUMMARIES` based on your system capabilities and API quota
   - For large batches, consider reducing concurrency to avoid rate limits

5. **Execution**:
   - Run the script: `python fast_house_pipeline.py`
   - Monitor the console output for progress indicators
   - Check the log file (`video_pipeline.log`) for detailed operation records

## Metadata CSV Format

The script expects a CSV file with at least the following columns:
- `FILENAME`: MP4 filename (e.g., "P-1234-5678.mp4")
- `ELECTION`: Election year (e.g., "2020")
- `PARTY`: Political party (e.g., "Republican", "Democratic")
- `FIRST_NAME`: Candidate's first name
- `LAST_NAME`: Candidate's last name

Additional columns will be ignored but can be present in the file.

## Best Practices for Use

1. **Video Preparation**:
   - Ensure videos are in MP4 format
   - Use consistent naming conventions matching your metadata
   - Verify audio quality for better transcription results

2. **Resource Management**:
   - Monitor disk space - frame extraction can use significant storage
   - Watch API usage costs - GPT-4o Vision API calls can be expensive
   - Consider running in batches for large collections

3. **Error Recovery**:
   - The script will skip already-processed items
   - If interrupted, you can safely restart to continue from where it stopped
   - Check the log file to identify and address any persistent errors

4. **Output Validation**:
   - Review sampled transcripts for accuracy
   - Check frame descriptions for relevance and accuracy
   - Ensure summaries capture the essential messaging of the ads

## Limitations and Considerations

1. **API Dependency**: Relies on OpenAI's APIs, which may change pricing or availability
2. **Resource Intensive**: Requires significant disk space and GPU resources
3. **Batch Size Trade-offs**: Smaller batches are safer but slower; larger batches risk rate limits
4. **Language Limitations**: Best performance on English-language advertisements
5. **Context Windows**: Limited by API context windows for very long advertisements

## Customization Options

The script can be modified in several ways to adapt to specific research needs:

1. **Frame Extraction Frequency**: Adjust `max_ms // 3000` to change frame intervals
2. **Description Prompting**: Modify the GPT-4o Vision prompt to extract different visual aspects
3. **Summary Length**: Change `response_wordcount` for longer or shorter summaries
4. **Custom Metadata**: Add additional fields to the metadata CSV for more context
5. **Output Formats**: Add exporters for other formats (XML, SQL, etc.)

## Conclusion

This pipeline provides a comprehensive solution for analyzing political advertisements through multi-modal AI techniques. By combining audio transcription, visual frame analysis, and natural language processing, it generates structured data that can support various research applications in political communication, campaign analysis, and media studies.

The modular design allows for step-by-step processing with appropriate error handling and optimization, making it suitable for processing large collections of advertisements while maintaining detailed records of the analysis process.

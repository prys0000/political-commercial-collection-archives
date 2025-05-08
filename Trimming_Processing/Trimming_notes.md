# Video Processing Script with Tone Detection: Technical Documentation

## Overview

This Python script (`1trim_nowm.py`) is an enhanced video processing pipeline designed to automatically detect content boundaries in videos and trim them with appropriate padding. The script uses a combination of visual person detection and audio speech recognition, with special filtering to distinguish between actual speech and pure tones or beeps, which can cause incorrect trimming points.

## Key Features

1. **Multi-Modal Content Detection**
   - Visual detection of people using YOLO object detection
   - Audio detection of speech using Whisper speech recognition
   - Spectral analysis for tone vs. speech differentiation

2. **Intelligent Trimming Logic**
   - Uses the earliest detected content for start point
   - Uses the latest detected content for end point
   - Applies configurable padding to both ends
   - Enforces duration constraints and validation

3. **Diagnostic Capabilities**
   - Generates detailed JSON reports of detection process
   - Visual person detection analysis
   - Audio spectral analysis with tone probability scores
   - Final trim decision documentation

4. **Robust Error Handling**
   - Comprehensive try/except blocks
   - Fallback mechanisms when detection fails
   - Detailed logging of all operations

## Technical Architecture

### Dependencies

- **Computer Vision**: OpenCV, YOLOv3
- **Audio Processing**: librosa, soundfile, faster_whisper
- **Core Processing**: NumPy, subprocess (for FFmpeg/FFprobe)
- **I/O and Formatting**: json, tempfile, Path

### Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| INPUT_DIR | (path) | Source directory for videos |
| OUTPUT_DIR | (path) | Destination for trimmed videos |
| REPORT_DIR | (path) | Location for diagnostic reports |
| PAD_SEC | 2.5 | Seconds of padding to add at start and end |
| DEFAULT_START | 5.0 | Default start time if no content detected |
| STRIDE_FRAMES | 5 | Check every Nth frame for person detection |
| TONE_THRESHOLD | 0.8 | Threshold for tone detection (higher = stricter) |
| DIAGNOSTIC | True | Enable/disable detailed reporting |

## Processing Pipeline

### 1. Initialization
- Set up logging
- Load YOLO model for person detection
- Load Whisper model for speech recognition
- Create output and report directories

### 2. Video Processing Flow
For each video in the input directory:
   1. Convert to MP4 format if needed
   2. Determine output path
   3. Check for existing output and handle based on FORCE_PROCESS setting
   4. Execute the trim operation
   5. Verify output and log results

### 3. Content Detection
The script employs two parallel detection methods:

#### Visual Person Detection
- Uses YOLOv3 to detect people in video frames
- Samples frames at regular intervals (STRIDE_FRAMES)
- Records first and last timestamps where people appear
- Generates detailed person detection reports

#### Audio Speech Detection with Tone Filtering
1. **Speech Detection**
   - Uses Whisper model to transcribe and timestamp speech segments
   - Applies Voice Activity Detection (VAD) to identify speech boundaries

2. **Tone Filtering**
   - Extracts audio for spectral analysis
   - Analyzes each segment for tone-like characteristics:
     - Spectral flatness (pure tones have flat spectra)
     - Spectral bandwidth (tones have narrow bandwidth)
     - Zero-crossing regularity (tones have regular patterns)
     - Crest factor (amplitude consistency)
   - Calculates a "tone probability" score
   - Filters out segments exceeding TONE_THRESHOLD

3. **Audio Analysis Metrics**
   - **Spectral Flatness**: Measures how tone-like the spectrum is (higher = more tone-like)
   - **Spectral Bandwidth**: Measures frequency spread (lower = more tone-like)
   - **Zero-Crossing Rate**: Measures frequency regularity (regular = more tone-like)
   - **Crest Factor**: Measures amplitude consistency (higher = more tone-like)

### 4. Trim Decision Logic
- Determines content start time:
  - Uses earliest of person/speech detection if both available
  - Falls back to available detection method if only one works
  - Uses DEFAULT_START if no content detected

- Determines content end time:
  - Uses latest of person/speech detection if both available
  - Falls back to available detection method if only one works
  - Calculates reasonable end time if no content detected

- Applies padding:
  - Adds PAD_SEC seconds before content start (if possible)
  - Adds PAD_SEC seconds after content end (if possible)
  - Ensures padding stays within video boundaries

### 5. FFmpeg Execution
- Uses seeking BEFORE input flag for accurate trimming
- Specifies duration instead of end point
- Includes timestamp handling flags
- Preserves video and audio quality

### 6. Diagnostic Reporting
Generates three types of JSON reports for each video:

1. **Person Detection Report**:
   - Frame-by-frame person detection results
   - Confidence scores for each detection
   - First and last person timestamps

2. **Audio Analysis Report**:
   - Valid speech segments after tone filtering
   - Filtered tone segments with probabilities
   - Detailed spectral metrics for each segment

3. **Trim Report**:
   - Original content detection boundaries
   - Final trim decisions with reasoning
   - Actual padding applied

## Technical Implementation Notes

### JSON Serialization
- Custom NumpyEncoder class handles NumPy data types
- Explicit type casting for consistent serialization
- Proper handling of None values and boolean types

### Audio Analysis
- Uses librosa for advanced spectral analysis
- Combines multiple audio features with weighted scoring
- Normalizes features for consistent comparison

### Error Handling
- Robust exception handling throughout
- Detailed error logging with context
- Graceful fallbacks when components fail

## Usage Instructions

1. **Installation**:
   - Install required Python packages: `opencv-python`, `numpy`, `faster_whisper`, `librosa`, `soundfile`
   - Ensure FFmpeg and FFprobe are installed and in system PATH

2. **Configuration**:
   - Set INPUT_DIR to folder containing source videos
   - Set OUTPUT_DIR for trimmed videos
   - Set REPORT_DIR for diagnostic reports
   - Adjust PAD_SEC for desired padding amount
   - Modify TONE_THRESHOLD to control tone filtering sensitivity

3. **Execution**:
   - Run the script: `python newtrim_nowm.py`
   - Monitor log output for processing status
   - Check report directory for detailed analysis

4. **Results**:
   - Trimmed videos will be saved to OUTPUT_DIR
   - Each video will have "_clip" appended to filename
   - Diagnostic reports provide detailed insight into processing decisions

## Troubleshooting

- If videos are incorrectly trimmed due to tones, lower TONE_THRESHOLD
- If speech is being incorrectly filtered as tones, increase TONE_THRESHOLD
- Check diagnostic reports to understand trim decisions
- Enable DEBUG mode for more detailed logging

## Conclusion

This script provides an intelligent solution for automatically trimming videos based on meaningful content, with special handling for distinguishing between speech and tones. The comprehensive diagnostic reporting helps identify and resolve any issues with specific videos, making it suitable for processing large batches of content with minimal manual intervention.

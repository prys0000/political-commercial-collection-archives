#!/usr/bin/env python3
# newtrim_nowm.py – Enhanced video processing with tone detection

import os
import glob
import subprocess
import logging
import datetime as dt
import tempfile
import json
import math
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional, Tuple, List, Dict

import cv2
import numpy as np
from faster_whisper import WhisperModel
import librosa
import soundfile as sf

# ───────────────────────── CONFIG ───────────────────────── #
INPUT_DIR     = ""
OUTPUT_DIR    = ""
REPORT_DIR    = ""
YOLO_CFG      = "yolov3.cfg"
YOLO_WEIGHTS  = "yolov3.weights"
COCO_NAMES    = "coco.names"
PAD_SEC       = 2.5         # Seconds of padding to add at start and end
DEFAULT_START = 5.0         # Default start time if no content detected
STRIDE_FRAMES = 5           # Check every Nth frame for person detection
FFMPEG        = "ffmpeg"    # FFmpeg executable 
FFPROBE       = "ffprobe"   # FFprobe executable
DEBUG         = True        # Enable detailed logging
FORCE_PROCESS = True        # Force reprocessing of existing files
DIAGNOSTIC    = True        # Generate diagnostic reports
MIN_SPEECH_CONFIDENCE = 0.6 # Minimum confidence for speech detection
TONE_THRESHOLD = 0.8        # Tone detection threshold (higher = stricter)
LIBROSA_SAMPLE_RATE = 16000 # Sample rate for audio analysis

# ─────────────────────── Set Up Logger ─────────────────────── #
log = logging.getLogger("VideoTrim")
log.setLevel(logging.INFO)
fh = RotatingFileHandler("video_trim.log", maxBytes=5_000_000, backupCount=3, encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
log.addHandler(fh)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
log.addHandler(ch)

# ─────────────────────── Initialize Detectors ─────────────────────── #
# Load YOLO model for person detection
try:
    net = cv2.dnn.readNet(YOLO_WEIGHTS, YOLO_CFG)
    with open(COCO_NAMES, 'r') as f:
        classes = [line.strip() for line in f]
    
    layer_names = net.getLayerNames()
    try:
        # Handle different OpenCV versions
        if isinstance(net.getUnconnectedOutLayers(), np.ndarray):
            output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        else:
            output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    except:
        # Final fallback
        output_layers = []
        for i in net.getUnconnectedOutLayers():
            if isinstance(i, np.ndarray):
                output_layers.append(layer_names[i[0] - 1])
            else:
                output_layers.append(layer_names[i - 1])
                
    log.info("Loaded YOLO detector")
    HAVE_YOLO = True
except Exception as e:
    log.error(f"Failed to load YOLO: {e}")
    HAVE_YOLO = False

# Load Whisper model for speech detection
try:
    whisper = WhisperModel('tiny.en', device='cpu', compute_type='int8')
    log.info("Loaded Whisper model")
    HAVE_WHISPER = True
except Exception as e:
    log.error(f"Failed to load Whisper: {e}")
    HAVE_WHISPER = False

# ─────────────────────── Helper Functions ─────────────────────── #

def get_duration(video_path):
    """Get video duration using ffprobe"""
    try:
        cmd = [
            FFPROBE, '-v', 'error', 
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(result.stdout.strip())
    except Exception as e:
        log.warning(f"FFprobe failed: {e}, falling back to OpenCV")
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            cap.release()
            return frames / fps
        except Exception as e2:
            log.error(f"OpenCV fallback failed: {e2}")
            return 0

def convert_to_mp4(input_path):
    """Convert MPG to MP4 if needed"""
    if not input_path.lower().endswith('.mpg'):
        return input_path
        
    output_path = os.path.splitext(input_path)[0] + '.mp4'
    if os.path.exists(output_path):
        log.info(f"Using existing MP4: {Path(output_path).name}")
        return output_path
        
    log.info(f"Converting {Path(input_path).name} to MP4")
    try:
        cmd = [
            FFMPEG, '-y', '-i', input_path,
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-c:a', 'aac', '-b:a', '128k',
            output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log.info(f"Converted to {Path(output_path).name}")
        return output_path
    except Exception as e:
        log.error(f"Conversion failed: {e}")
        return input_path  # Return original if conversion fails

def extract_audio(video_path, output_path=None):
    """Extract audio from video for analysis"""
    if output_path is None:
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, f"{Path(video_path).stem}_audio.wav")
    
    try:
        cmd = [
            FFMPEG, '-y', '-i', video_path,
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # PCM 16-bit
            '-ar', str(LIBROSA_SAMPLE_RATE),  # Sample rate
            '-ac', '1',  # Mono
            output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_path
    except Exception as e:
        log.error(f"Audio extraction failed: {e}")
        return None

# Custom JSON encoder for NumPy and complex types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (bool, np.bool_)):
            return bool(obj)  # Fix for boolean types
        return super(NumpyEncoder, self).default(obj)

def analyze_audio_segment(audio, sr, start_time, end_time, diagnosis=None):
    """Analyze audio segment for tone detection.
    Returns probability of being a tone (0-1), higher means more likely a tone."""
    start_sample = int(start_time * sr)
    end_sample = min(int(end_time * sr), len(audio))
    
    if end_sample <= start_sample:
        return 0.0
    
    segment = audio[start_sample:end_sample]
    
    # Skip if segment is too short
    if len(segment) < sr * 0.2:  # Less than 0.2 seconds
        return 0.0
    
    # Calculate spectral features
    spec_centroid = librosa.feature.spectral_centroid(y=segment, sr=sr).mean()
    spec_bandwidth = librosa.feature.spectral_bandwidth(y=segment, sr=sr).mean()
    spec_flatness = librosa.feature.spectral_flatness(y=segment).mean()
    zero_crossing_rate = librosa.feature.zero_crossing_rate(segment).mean()
    
    # Calculate amplitude statistics
    rms = np.sqrt(np.mean(segment**2))
    crest_factor = np.max(np.abs(segment)) / rms if rms > 0 else 0
    
    # Tone indicators:
    # 1. High spectral flatness (flat spectrum = tone-like)
    # 2. Low spectral bandwidth (narrow = tone-like)
    # 3. Stable centroid (steady tone)
    # 4. High zero-crossing regularity (pure tones have regular zero crossings)
    # 5. High crest factor (steady amplitude for tones)
    
    # Normalize features
    norm_flatness = min(spec_flatness * 10, 1.0)  # Higher is more tone-like
    norm_bandwidth = max(0, 1.0 - (spec_bandwidth / 2000))  # Lower bandwidth is more tone-like
    norm_zcr_regularity = min(1.0, abs(zero_crossing_rate * 1000))  # Regular ZCR is tone-like
    norm_crest = min(crest_factor / 5, 1.0)  # Higher crest factor for pure tones
    
    # Combine metrics (weighted average)
    tone_probability = (
        norm_flatness * 0.4 +
        norm_bandwidth * 0.3 +
        norm_zcr_regularity * 0.2 +
        norm_crest * 0.1
    )
    
    # Save diagnostic info if requested
    if diagnosis is not None:
        diagnosis["segments"].append({
            "start": float(start_time),
            "end": float(end_time),
            "duration": float(end_time - start_time),
            "spectral_flatness": float(spec_flatness),
            "spectral_bandwidth": float(spec_bandwidth),
            "spectral_centroid": float(spec_centroid),
            "zero_crossing_rate": float(zero_crossing_rate),
            "rms_amplitude": float(rms),
            "crest_factor": float(crest_factor),
            "norm_flatness": float(norm_flatness),
            "norm_bandwidth": float(norm_bandwidth),
            "norm_zcr": float(norm_zcr_regularity),
            "norm_crest": float(norm_crest),
            "tone_probability": float(tone_probability),
            "is_likely_tone": bool(tone_probability > TONE_THRESHOLD)  # Explicitly cast to bool
        })
    
    return tone_probability

def detect_people(video_path):
    """Find timestamps of first and last person appearance"""
    if not HAVE_YOLO:
        log.warning("YOLO not available, skipping person detection")
        return None, None
        
    try:
        log.info("Detecting people in video...")
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            log.error(f"Could not open video: {video_path}")
            return None, None
            
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        
        first_person = None
        last_person = None
        person_count = 0
        person_frames = []
        
        # Check frames at regular intervals
        for frame_idx in range(0, total_frames, STRIDE_FRAMES):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if not ret:
                break
                
            # Run person detection
            height, width = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), swapRB=True, crop=False)
            net.setInput(blob)
            
            try:
                outs = net.forward(output_layers)
                found_person = False
                max_confidence = 0
                
                for out in outs:
                    for detection in out:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        
                        if confidence > 0.5 and classes[class_id] == "person":
                            found_person = True
                            person_count += 1
                            timestamp = frame_idx / fps
                            max_confidence = max(max_confidence, confidence)
                            
                            person_frames.append((timestamp, max_confidence))
                            
                            if first_person is None:
                                first_person = timestamp
                            last_person = timestamp
                            break
                    if found_person:
                        break
            except Exception as e:
                log.error(f"Detection error at frame {frame_idx}: {e}")
                continue
                
        cap.release()
        
        # Generate person detection report if in diagnostic mode
        if DIAGNOSTIC and person_frames:
            video_name = Path(video_path).stem
            os.makedirs(REPORT_DIR, exist_ok=True)
            report_path = os.path.join(REPORT_DIR, f"{video_name}_person_detection.json")
            
            with open(report_path, 'w') as f:
                json.dump({
                    "video": video_path,
                    "total_frames": total_frames,
                    "fps": fps,
                    "person_detections": [
                        {"time": float(t), "confidence": float(c)} 
                        for t, c in person_frames
                    ],
                    "first_person": float(first_person) if first_person is not None else None,
                    "last_person": float(last_person) if last_person is not None else None
                }, f, indent=2, cls=NumpyEncoder)  # Use custom encoder
            
            log.info(f"Saved person detection report to {report_path}")
        
        if first_person is not None:
            log.info(f"Found {person_count} person instances: first at {first_person:.2f}s, last at {last_person:.2f}s")
        else:
            log.warning("No people detected in video")
            
        return first_person, last_person
    except Exception as e:
        log.error(f"Person detection failed: {e}")
        return None, None

def detect_speech_with_tone_filtering(video_path):
    """Find timestamps of first and last speech, filtering out tones"""
    if not HAVE_WHISPER:
        log.warning("Whisper not available, skipping speech detection")
        return None, None
        
    try:
        log.info("Detecting speech in video...")
        # First get all segments from Whisper
        segments, _ = whisper.transcribe(
            video_path, beam_size=1, language='en',
            vad_filter=True, 
            vad_parameters={'min_silence_duration_ms': 800, 'threshold': 0.4}
        )
        segments = list(segments)
        
        if not segments:
            log.warning("No speech detected by Whisper")
            return None, None
            
        # Extract audio for tone analysis
        audio_path = extract_audio(video_path)
        if not audio_path or not os.path.exists(audio_path):
            log.error("Failed to extract audio for tone analysis")
            # Fall back to basic filtering
            valid_segments = [s for s in segments if len(s.text.strip()) > 5 and any(c.isalpha() for c in s.text)]
            if valid_segments:
                return valid_segments[0].start, valid_segments[-1].end
            return None, None
        
        # Load audio for analysis
        audio, sr = librosa.load(audio_path, sr=LIBROSA_SAMPLE_RATE, mono=True)
        
        # Prepare diagnosis report if in diagnostic mode
        diagnosis = {"segments": []} if DIAGNOSTIC else None
        
        # Filter segments by checking for tones
        valid_segments = []
        tone_segments = []
        
        for seg in segments:
            text = seg.text.strip()
            
            # Basic text validation (requires alphanumeric content)
            if not any(c.isalpha() for c in text):
                continue
                
            # Check if this segment looks like a tone
            tone_prob = analyze_audio_segment(audio, sr, seg.start, seg.end, diagnosis)
            
            if tone_prob < TONE_THRESHOLD:
                # Not a tone, likely actual speech
                valid_segments.append({
                    "start": float(seg.start),
                    "end": float(seg.end),
                    "text": text,
                    "confidence": float(getattr(seg, 'confidence', 0.0)),
                    "tone_probability": float(tone_prob)
                })
            else:
                # This segment is likely a tone
                tone_segments.append({
                    "start": float(seg.start),
                    "end": float(seg.end), 
                    "text": text,
                    "tone_probability": float(tone_prob)
                })
                log.info(f"Filtered out likely tone at {seg.start:.2f}s-{seg.end:.2f}s: '{text}'")
        
        # Save diagnostic report if requested
        if DIAGNOSTIC:
            video_name = Path(video_path).stem
            os.makedirs(REPORT_DIR, exist_ok=True)
            report_path = os.path.join(REPORT_DIR, f"{video_name}_audio_analysis.json")
            
            with open(report_path, 'w') as f:
                json.dump({
                    "video": video_path,
                    "valid_segments": valid_segments,
                    "tone_segments": tone_segments,
                    "audio_analysis": diagnosis
                }, f, indent=2, cls=NumpyEncoder)  # Use custom encoder
            
            log.info(f"Saved audio analysis report to {report_path}")
        
        # Clean up temporary audio file
        try:
            os.remove(audio_path)
        except:
            pass
        
        if not valid_segments:
            log.warning("No valid speech segments after tone filtering")
            return None, None
            
        # Sort by time to ensure correct order
        valid_segments.sort(key=lambda x: x["start"])
        
        first_speech = valid_segments[0]["start"]
        last_speech = valid_segments[-1]["end"]
        
        log.info(f"Found {len(valid_segments)} valid speech segments (filtered out {len(tone_segments)} tones)")
        log.info(f"Speech boundaries: {first_speech:.2f}s - {last_speech:.2f}s")
        
        return first_speech, last_speech
    except Exception as e:
        log.error(f"Speech detection with tone filtering failed: {e}")
        return None, None

def trim_video(input_path, output_path):
    """Trim video with padding based on content detection with tone filtering"""
    duration = get_duration(input_path)
    if duration <= 0:
        log.error(f"Invalid duration: {duration}")
        return False
    log.info(f"Video duration: {duration:.2f}s")
    
    # Detect content bounds with tone filtering
    speech_start, speech_end = detect_speech_with_tone_filtering(input_path)
    person_start, person_end = detect_people(input_path)
    
    # Determine actual content boundaries
    content_start = None
    content_end = None
    
    # Find the earliest start time
    if person_start is not None and speech_start is not None:
        content_start = min(person_start, speech_start)
        log.info(f"Using earliest detection for start: {content_start:.2f}s")
    elif person_start is not None:
        content_start = person_start
        log.info(f"Using person detection for start: {content_start:.2f}s")
    elif speech_start is not None:
        content_start = speech_start
        log.info(f"Using speech detection for start: {content_start:.2f}s")
    else:
        content_start = min(DEFAULT_START, duration * 0.1)
        log.warning(f"No content detected, using default start: {content_start:.2f}s")
    
    # Find the latest end time
    if person_end is not None and speech_end is not None:
        content_end = max(person_end, speech_end)
        log.info(f"Using latest detection for end: {content_end:.2f}s")
    elif person_end is not None:
        content_end = person_end
        log.info(f"Using person detection for end: {content_end:.2f}s")
    elif speech_end is not None:
        content_end = speech_end
        log.info(f"Using speech detection for end: {content_end:.2f}s")
    else:
        content_end = max(content_start + 30, duration * 0.9)
        log.warning(f"No content end detected, using calculated end: {content_end:.2f}s")
    
    # Validate content window
    if content_end <= content_start:
        log.error(f"Invalid content window: {content_start:.2f}s - {content_end:.2f}s")
        return False
    
    # Apply padding
    padded_start = max(0, content_start - PAD_SEC)
    padded_end = min(duration, content_end + PAD_SEC)
    
    # Calculate actual padding applied
    start_padding = content_start - padded_start
    end_padding = padded_end - content_end
    
    log.info(f"Content bounds: {content_start:.2f}s - {content_end:.2f}s")
    log.info(f"Padded bounds: {padded_start:.2f}s - {padded_end:.2f}s")
    log.info(f"Applied padding: start={start_padding:.2f}s, end={end_padding:.2f}s")
    
    # Save trim report if in diagnostic mode
    if DIAGNOSTIC:
        video_name = Path(input_path).stem
        os.makedirs(REPORT_DIR, exist_ok=True)
        report_path = os.path.join(REPORT_DIR, f"{video_name}_trim_report.json")
        
        with open(report_path, 'w') as f:
            # Convert all values to float to ensure JSON serialization
            json.dump({
                "video": input_path,
                "duration": float(duration),
                "content_detection": {
                    "speech_start": float(speech_start) if speech_start is not None else None,
                    "speech_end": float(speech_end) if speech_end is not None else None,
                    "person_start": float(person_start) if person_start is not None else None,
                    "person_end": float(person_end) if person_end is not None else None
                },
                "content_bounds": {
                    "start": float(content_start),
                    "end": float(content_end)
                },
                "padded_bounds": {
                    "start": float(padded_start),
                    "end": float(padded_end),
                    "start_padding": float(start_padding),
                    "end_padding": float(end_padding)
                }
            }, f, indent=2, cls=NumpyEncoder)  # Use custom encoder
        
        log.info(f"Saved trim report to {report_path}")
    
    # Perform the trim operation
    try:
        # Use seeking BEFORE input for more accurate trimming
        cmd = [
            FFMPEG, '-y',
            '-ss', f'{padded_start:.3f}',  # Start time
            '-i', input_path,              # Input file
            '-t', f'{padded_end - padded_start:.3f}',  # Duration
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-c:a', 'aac',
            '-avoid_negative_ts', '1',     # Prevent timestamp issues
            output_path
        ]
        
        log.info(f"Executing FFmpeg trim: {Path(input_path).name} -> {Path(output_path).name}")
        result = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            log.error(f"FFmpeg error: {result.stderr}")
            return False
            
        # Verify the output file exists and has a reasonable duration
        if not os.path.exists(output_path):
            log.error("Output file was not created")
            return False
            
        out_duration = get_duration(output_path)
        expected_duration = padded_end - padded_start
        
        log.info(f"Output duration: {out_duration:.2f}s (expected {expected_duration:.2f}s)")
        
        # Accept if within reasonable tolerance
        if abs(out_duration - expected_duration) > min(1.0, expected_duration * 0.1):
            log.warning(f"Duration mismatch: {abs(out_duration - expected_duration):.2f}s difference")
            # Still consider it successful if the file exists
        
        return True
    except Exception as e:
        log.error(f"Trimming failed: {e}")
        return False

def process_videos():
    """Process all videos in the input directory with tone filtering"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if DIAGNOSTIC:
        os.makedirs(REPORT_DIR, exist_ok=True)
        
    video_files = sorted(glob.glob(os.path.join(INPUT_DIR, '*.mpg')) + 
                         glob.glob(os.path.join(INPUT_DIR, '*.mp4')))
    
    if not video_files:
        log.warning(f"No video files found in {INPUT_DIR}")
        return
    
    log.info(f"Starting batch processing: {len(video_files)} files, pad={PAD_SEC}s")
    success = 0
    failure = 0
    
    for i, video_file in enumerate(video_files):
        log.info(f"Processing file {i+1}/{len(video_files)}: {Path(video_file).name}")
        
        try:
            # Convert to MP4 if needed
            mp4_file = convert_to_mp4(video_file)
            
            # Determine output path
            output_file = os.path.join(OUTPUT_DIR, Path(mp4_file).stem + '_clip.mp4')
            
            # Check if output already exists
            if os.path.exists(output_file) and not FORCE_PROCESS:
                log.info(f"Output already exists: {Path(output_file).name}")
                success += 1
                continue
                
            # Remove existing file if forcing reprocessing
            if os.path.exists(output_file) and FORCE_PROCESS:
                os.remove(output_file)
                log.info(f"Removed existing file for reprocessing: {Path(output_file).name}")
            
            # Process the video with tone filtering
            if trim_video(mp4_file, output_file):
                log.info(f"Successfully processed: {Path(video_file).name}")
                success += 1
            else:
                log.error(f"Failed to process: {Path(video_file).name}")
                failure += 1
                
        except Exception as e:
            log.error(f"Error processing {Path(video_file).name}: {e}")
            failure += 1
    
    log.info(f"Batch complete: {success} succeeded, {failure} failed")

if __name__ == "__main__":
    start_time = dt.datetime.now()
    log.info(f"Starting enhanced video processing with tone detection at {start_time}")
    
    try:
        process_videos()
    except Exception as e:
        log.error(f"Pipeline failed: {e}")
    
    end_time = dt.datetime.now()
    duration = (end_time - start_time).total_seconds()
    log.info(f"Processing completed at {end_time} (took {duration:.1f}s)")

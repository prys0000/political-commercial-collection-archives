#!/usr/bin/env python3
# fast_house_pipeline.py – end-to-end batch for House-ad MP4s (Vision-Enhanced)
# ---------------------------------------------------------------------------
"""
Steps
1. Whisper-v3 transcription   → pres_ad_whisptranscripts_{json|tsv|txt}
2a. Speech-centred key-frames → keyframes_speechcentered
2b. Regular-interval frames   → keyframes_regintervals
3. GPT-4-Vision frame descriptions → GPT_frame_descriptions_*   (20–30 words)
4. 50-word video summaries    → GPT_video_summaries
"""

import base64
import time
import json
import logging
import subprocess
import datetime as dt
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Tuple, List

import pandas as pd
from tqdm import tqdm
from openai import OpenAI
from faster_whisper import WhisperModel
from PIL import Image
import numpy as np

# ───────── CONFIG ───────── #
ROOT             = Path("")
VIDEO_DIR        = ROOT
METADATA_F       = Path("")

TRANSCRIPT_JSON  = ROOT / "pres_ad_whisptranscripts_json"
TRANSCRIPT_TSV   = ROOT / "pres_ad_whisptranscripts_tsv"
TRANSCRIPT_TXT   = ROOT / "pres_ad_whisptranscripts_txt"
FRAME_SPEECH     = ROOT / "keyframes_speechcentered"
FRAME_INTERVAL   = ROOT / "keyframes_regintervals"
DESC_SPEECH      = ROOT / "GPT_frame_descriptions_speechcentered"
DESC_INTERVAL    = ROOT / "GPT_frame_descriptions_regintervals"
SUMMARY_DIR      = ROOT / "GPT_video_summaries"

FFMPEG, FFPROBE   = "ffmpeg", "ffprobe"
OPENAI_KEY       = ""  # ← set your OpenAI API key here or via env var
N_FFMPEG_PROC    = 12
N_GPT_FRAMES     = 16
N_GPT_SUMMARIES  = 8

# ───────── logging ───────── #
log = logging.getLogger("HousePipeline")
log.setLevel(logging.INFO)
fh = logging.FileHandler("video_pipeline.log", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
log.addHandler(fh)

# create output directories
for p in [TRANSCRIPT_JSON, TRANSCRIPT_TSV, TRANSCRIPT_TXT,
          FRAME_SPEECH, FRAME_INTERVAL, DESC_SPEECH, DESC_INTERVAL,
          SUMMARY_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# ───────── Initialize models ───────── #
log.info("Loading Whisper large-v3 …")
WHISPER_MODEL = WhisperModel(
    "large-v3", device="cuda", compute_type="float16"
)
openai_client = OpenAI(api_key=OPENAI_KEY)

# ───────── HELPERS ───────── #
def ffprobe_duration(path: Path) -> float:
    """Return video duration in seconds"""
    try:
        out = subprocess.check_output([
            FFPROBE, "-v", "error", "-select_streams", "v:0",
            "-show_entries", "format=duration",
            "-of", "default=nw=1:nk=1", str(path)
        ], text=True)
        return float(out.strip())
    except Exception as e:
        log.error(f"Error getting duration for {path}: {str(e)}")
        print(f"Error getting duration for {path}: {str(e)}")
        # Return a default duration of 60 seconds if we can't get the actual duration
        return 60.0


# Helper function for base64 encoding
def encode_image_to_base64(image_path):
    """Convert an image to base64 data URI format for API submission"""
    with open(image_path, "rb") as image_file:
        base64_bytes = base64.b64encode(image_file.read()).decode('utf-8')
        # Return properly formatted data URI
        return f"data:image/jpeg;base64,{base64_bytes}"

# ───── 1. Whisper transcription ───── #
def transcribe_one(mp4: Path) -> str:
    vid = mp4.stem
    out_txt = TRANSCRIPT_TXT / f"{vid}.txt"
    if out_txt.exists():
        return f"[skip] {vid}"

    try:
        segments, _ = WHISPER_MODEL.transcribe(
            str(mp4), beam_size=5,
            temperature=[0.0, 0.2, 0.4],
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
            word_timestamps=False
        )
        segments = list(segments)
        full_text = " ".join(s.text.strip() for s in segments)

        # write TXT
        out_txt.write_text(full_text, encoding="utf-8")
        # write JSON
        (TRANSCRIPT_JSON / f"{vid}.json").write_text(
            json.dumps({"segments":[s._asdict() for s in segments], "text":full_text},
                       ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        # write TSV
        with (TRANSCRIPT_TSV / f"{vid}.tsv").open("w", encoding="utf-8") as tsv:
            tsv.write("start\tend\ttext\n")
            for s in segments:
                tsv.write(f"{s.start}\t{s.end}\t{s.text.replace(chr(9),' ')}\n")

        return f"[done] {vid}"

    except Exception as e:
        log.error(f"Whisper error {vid}: {e}")
        return f"[err ] {vid}"

# ───── 2A. Speech-centered keyframes ───── #
def extract_speech_frames(mp4: Path) -> str:
    vid      = mp4.stem
    seg_file = TRANSCRIPT_JSON / f"{vid}.json"
    if not seg_file.exists():
        return f"{vid}: no transcript"

    # ←— make sure this is here
    segs = json.loads(seg_file.read_text(encoding="utf-8"))["segments"]

    saved = 0
    for seg in segs:
        mid     = (seg['start'] + seg['end']) / 2
        out_jpg = FRAME_SPEECH / f"{vid}_{int(mid*1000):07d}.jpg"
        if out_jpg.exists():
            continue

        subprocess.run([
            FFMPEG, '-hide_banner', '-loglevel', 'error', '-y',
            '-ss', f"{mid:.3f}", '-i', str(mp4),

            # ensure even dimensions
            '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
            # force MJPEG encoder + JPEG‐friendly pix_fmt
            '-c:v', 'mjpeg',
            '-pix_fmt', 'yuvj420p',

            '-frames:v', '1',
            '-q:v', '2',
            str(out_jpg)
        ], check=True)

        saved += 1

    return f"{vid}: {saved} speech-frames"

# ───── 2B. Regular-interval keyframes ───── #
def extract_interval_frames(task: Tuple[str,str,float]) -> str:
    path_str, vid, dur = task
    path = Path(path_str)
    
    # Verify the path exists
    if not path.exists():
        return f"{vid}: ERROR - file not found: {path_str}"
    
    saved = failed = 0
    # Ensure we have at least 1 step even for very short videos
    max_ms = min(180_000, max(3000, int(dur*1000)))
    steps = max(1, max_ms // 3000)
    
    print(f"  Extracting {steps} frames for {vid} (duration: {dur:.2f}s)")
    
    for i in range(int(steps)):
        ts = 3.0*(i+1)
        # Make sure we don't exceed the video duration
        if ts >= dur:
            ts = max(0.5, dur - 0.5)  # Go to near the end but not quite
            
        out_jpg = FRAME_INTERVAL / f"{vid}_{int(ts*1000)}.jpg"
        if out_jpg.exists():
            print(f"  Skipping existing frame: {out_jpg.name}")
            saved += 1  # Count as saved even though we skipped it
            continue
            
        try:
            cmd = [
                FFMPEG, '-hide_banner', '-loglevel', 'error', '-y',
                '-ss', f"{ts:.3f}", '-i', str(path),
                '-vframes', '1', '-q:v', '2', str(out_jpg)
            ]
            print(f"  Running: {' '.join(cmd)}")
            
            res = subprocess.run(cmd, check=False, capture_output=True, text=True)
            
            if res.returncode == 0 and out_jpg.exists():
                print(f"  Successfully extracted: {out_jpg.name}")
                saved += 1
            else:
                error_output = res.stderr or "Unknown error"
                print(f"  Failed to extract frame at {ts:.2f}s: {error_output}")
                log.error(f"FFMPEG error for {vid} at {ts:.2f}s: {error_output}")
                failed += 1
                
        except Exception as e:
            print(f"  Exception extracting frame at {ts:.2f}s: {str(e)}")
            log.error(f"Exception for {vid} at {ts:.2f}s: {str(e)}")
            failed += 1

    return f"{vid}: {saved} saved, {failed} failed"

# ───── 3. GPT-4-Vision frame descriptions ───── #
def gpt_describe_frame(jpg: Path, row, transcript: str, dest: Path) -> str:
    """Generate a description of the frame using GPT-4o Vision"""
    
    if not jpg.exists() or jpg.stat().st_size == 0:
        log.error(f"Image file missing or empty: {jpg}")
        return f"[err ] {jpg.name} - file missing or empty"
        
    # Skip if output already exists
    if dest.exists():
        return f"[skip] {jpg.name}"
        
    # Extract metadata for context
    election_year = row.get('ELECTION', '?')
    party = row.get('PARTY', 'Unknown')
    candidate = f"{row.get('FIRST_NAME','').strip()} {row.get('LAST_NAME','').strip()}".strip() or 'Unknown candidate'
    
    prompt = (
        "You are a political ad analysis assistant. "
        "Describe what is depicted in this video frame in no more than 15 words. "
        "Do not say it’s an old ad or judge image quality. "
        "If the image includes text, then state that it includes text and also include a summary of the text that is shown."
        "Do not infer identities or intent. "
        "Summarize the most salient observable elements—clothing, posture, symbols, colors, setting—in a single flowing phrase. "
        f"Context: still from the {election_year} {party} {candidate} U.S. House campaign ad; "
        f"full transcript:\n{transcript}"
    )

    # Handle anti-candidate ads
    if 'anti' in candidate.lower():
        anti_candidate = candidate.replace('anti-', '').replace('anti ', '')
        prompt = (
            "You are a political ad analysis assistant. "
            "Describe what is depicted in this video frame in no more than 15 words. "
            "Do not say it’s an old ad or judge image quality. "
            "If the image includes text, then state that it includes text and also include a summary of the text that is shown."
            "Do not infer identities or intent. "
            "Summarize the most salient observable elements—clothing, posture, symbols, colors, setting—in a single flowing phrase. "
            f"Context: still from the {election_year} {party} {candidate} U.S. House campaign ad; "
            f"full transcript:\n{transcript}"
        )

    
    # Log the prompt
    print('\n\n', prompt, '\n')
    
    # Read the image file
    try:
        with open(jpg, 'rb') as img_file:
            img_data = img_file.read()
            img_b64 = base64.b64encode(img_data).decode('utf-8')
    except Exception as e:
        log.error(f"Failed to read image {jpg}: {str(e)}")
        return f"[err ] {jpg.name} - failed to read image: {str(e)}"
    
    # Create the API request
    try:
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
        
        # Extract the description
        desc = resp.choices[0].message.content.strip()
        
        # Write to file
        dest.write_text(desc, encoding='utf-8')
        return f"[done] {jpg.name}"
        
    except Exception as e:
        error_msg = str(e)
        log.error(f"Vision GPT error for {jpg.name}: {error_msg}")
        
        # Handle rate limiting with exponential backoff
        if "rate limit" in error_msg.lower() or "too many requests" in error_msg.lower():
            wait_time = 5  # Start with 5 seconds
            for attempt in range(3):  # Try 3 times
                log.warning(f"Rate limited, waiting {wait_time}s before retry ({attempt+1}/3)")
                time.sleep(wait_time)
                wait_time *= 2  # Exponential backoff
                
                try:
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
                    desc = resp.choices[0].message.content.strip()
                    dest.write_text(desc, encoding='utf-8')
                    return f"[done] {jpg.name} (after retry {attempt+1})"
                except Exception as retry_e:
                    log.error(f"Retry {attempt+1} failed for {jpg.name}: {str(retry_e)}")
                    continue
            
        return f"[err ] {jpg.name} - API error: {error_msg}"

# ───── 4. GPT video summaries ───── #
def gpt_summarize_ad(row, transcript, frame_descs, response_wordcount=50):
    # Create empty frame_times array or extract it if available
    # If frame_descs is a list of strings, create dummy timestamps
    frame_times = np.arange(len(frame_descs))
    
    # Sort frame descriptions by their timestamps
    frame_times_argsort = np.argsort(frame_times)
    frame_descs_sorted = np.asarray(frame_descs)[frame_times_argsort]
    
    # Get metadata from row
    election_year = row.get('ELECTION', '?')
    party = row.get('PARTY', '?')
    candidate = f"{row.get('FIRST_NAME', '')} {row.get('LAST_NAME', '')}"
    filename = row.get('FILENAME', '').replace('.mp4', '')
    
    # Create output path
    out = SUMMARY_DIR / f"{filename}.txt"
    if out.exists():
        return "[skip] " + filename
    
    # Create the prompt
    prompt = (
        f"Provide a {response_wordcount} word summary of a political television ad for the academic community. "
        f"Your summary should not exceed {response_wordcount} words. For context, this ad was for the {election_year} "
        f"U.S. House campaign of {party} candidate {candidate}.\n"
        f"The transcript of the entire ad is:\n{transcript}\n\n"
        f"The ad video depicts a set of scenes that can be described as follows:\n\n" + 
        '\n\n'.join([f"{idx+1}: {segment}" for idx, segment in enumerate(frame_descs_sorted)])
    )
    
    # Handle anti-candidate ads
    if 'anti' in candidate.lower():
        anti_candidate = candidate.replace('anti-', '').replace('anti ', '')
        prompt = (
            f"Provide a {response_wordcount} word summary of a political television ad for the academic community. "
            f"Your summary should not exceed {response_wordcount} words. For context, this ad was for the {election_year} "
            f"U.S. House election. This ad is anti-{anti_candidate} and pro-{party}.\n"
            f"The transcript of the entire ad is:\n{transcript}\n\n"
            f"The ad video depicts a set of scenes that can be described as follows:\n\n" + 
            '\n\n'.join([f"{idx+1}: {segment}" for idx, segment in enumerate(frame_descs_sorted)])
        )
    
    # Log the prompt
    print('\n\n\n', prompt, '\n')
    
    try:
        # Create the API request
        resp = openai_client.chat.completions.create(
            model="gpt-4-turbo",
            temperature=0.0,
            top_p=1.0,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        # Extract and save the summary
        summary = resp.choices[0].message.content.strip()
        out.write_text(summary, encoding='utf-8')
        return "[done] " + filename
    except Exception as e:
        error_msg = str(e)
        log.error(f"GPT summary error {filename}: {error_msg}")
        
        # Handle rate limiting with exponential backoff
        if "rate limit" in error_msg.lower() or "too many requests" in error_msg.lower():
            wait_time = 5  # Start with 5 seconds
            for attempt in range(3):  # Try 3 times
                log.warning(f"Rate limited, waiting {wait_time}s before retry ({attempt+1}/3)")
                time.sleep(wait_time)
                wait_time *= 2  # Exponential backoff
                
                try:
                    resp = openai_client.chat.completions.create(
                        model="gpt-4-turbo",
                        temperature=0.0,
                        top_p=1.0,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1000
                    )
                    summary = resp.choices[0].message.content.strip()
                    out.write_text(summary, encoding='utf-8')
                    return f"[done] {filename} (after retry {attempt+1})"
                except Exception as retry_e:
                    log.error(f"Retry {attempt+1} failed for {filename}: {str(retry_e)}")
                    continue
        
        return "[err ] " + filename

# Define the summary worker function
def summary_worker(args):
    row, transcript, frame_descs = args
    return gpt_summarize_ad(row, transcript, frame_descs)

# ───── multiprocessing helper ───── #
def run_interval_pool(tasks: List[Tuple[str,str,float]]) -> None:
    if not tasks:
        log.warning("No interval-frame tasks")
        return
    
    # Instead of using ProcessPoolExecutor which might be causing issues,
    # use a simpler approach with a regular loop
    for task in tqdm(tasks, desc="Interval frames"):
        try:
            res = extract_interval_frames(task)
            log.info(res)
            print(f"  {res}")
        except Exception as e:
            error_msg = str(e)
            log.error(f"Error processing interval frame task: {error_msg}")
            print(f"  Error: {error_msg}")

def main():
    # Check there are actually MP4 files present
    mp4s = sorted(VIDEO_DIR.glob("*.mp4"))
    if not mp4s:
        log.error(f"No MP4 files found in {VIDEO_DIR}")
        print(f"ERROR: No MP4 files found in {VIDEO_DIR}")
        return
        
    # Debug output for file paths
    print(f"Script working directory: {Path.cwd()}")
    print(f"Looking for MP4 files in: {VIDEO_DIR.absolute()}")
    for mp4 in mp4s:
        print(f"  Found video file: {mp4.absolute()}")
        if not mp4.exists():
            print(f"  WARNING: File exists in glob but not when checked directly: {mp4}")
            
    # Verify ffmpeg and ffprobe are accessible
    try:
        ffmpeg_version = subprocess.check_output([FFMPEG, "-version"], text=True, stderr=subprocess.STDOUT)
        ffprobe_version = subprocess.check_output([FFPROBE, "-version"], text=True, stderr=subprocess.STDOUT)
        print(f"ffmpeg version: {ffmpeg_version.splitlines()[0]}")
        print(f"ffprobe version: {ffprobe_version.splitlines()[0]}")
    except Exception as e:
        print(f"ERROR: Cannot access ffmpeg or ffprobe: {str(e)}")
        print("Please ensure ffmpeg is properly installed and in your PATH")
        log.error(f"Cannot access ffmpeg/ffprobe: {str(e)}")
        # We'll continue anyway, in case the paths are different
    
    log.info(f"Found {len(mp4s)} MP4 files to process")
    print(f"Found {len(mp4s)} MP4 files to process")
    
    # 1. Whisper transcription
    print("Step 1: Running Whisper transcription...")
    for m in tqdm(mp4s, desc="Whisper"):
        result = transcribe_one(m)
        log.info(result)
        print(f"  {result}")
    
    # 2A. Speech-centered frames
    print("Step 2A: Extracting speech-centered frames...")
    for m in tqdm(mp4s, desc="Speech frames"):
        result = extract_speech_frames(m)
        log.info(result)
        print(f"  {result}")
    
    # 2B. Interval frames
    print("Step 2B: Extracting regular-interval frames...")
    # Create tasks with proper error handling
    tasks = []
    for mp4 in mp4s:
        try:
            duration = ffprobe_duration(mp4)
            tasks.append((str(mp4), mp4.stem, duration))
            print(f"  Video {mp4.name} has duration: {duration:.2f}s")
        except Exception as e:
            log.error(f"Could not create task for {mp4}: {str(e)}")
            print(f"  Error: Could not process {mp4}: {str(e)}")
    
    if tasks:
        run_interval_pool(tasks)
    else:
        log.warning("No valid tasks for interval frames")
        print("  Warning: No valid tasks created for interval frames")
    
    # Load metadata
    try:
        meta_df = pd.read_csv(METADATA_F, dtype=str)
        log.info(f"Loaded metadata with {len(meta_df)} entries")
        print(f"Loaded metadata with {len(meta_df)} entries")
    except Exception as e:
        log.error(f"Error loading metadata: {str(e)}")
        print(f"Warning: Error loading metadata: {str(e)}")
        # Create a simple metadata DataFrame as fallback
        meta_df = pd.DataFrame([{
            "FILENAME": mp4.name,
            "ELECTION": "?",
            "PARTY": "Unknown",
            "FIRST_NAME": "",
            "LAST_NAME": ""
        } for mp4 in mp4s])
    
    # 3. GPT-4-Vision descriptions
    print("Step 3: Generating GPT-4-Vision frame descriptions...")
    
    # Build jobs list for both frame types
    jobs = []
    for folder, dest_folder in [(FRAME_SPEECH, DESC_SPEECH), (FRAME_INTERVAL, DESC_INTERVAL)]:
        # Make sure destination folder exists
        dest_folder.mkdir(parents=True, exist_ok=True)
        
        # Collect all jpg files
        all_jpgs = list(folder.glob("*.jpg"))
        log.info(f"Found {len(all_jpgs)} frames in {folder}")
        print(f"Found {len(all_jpgs)} frames in {folder}")
        
        for jpg in all_jpgs:
            vid = jpg.stem.split("_")[0]
            match = meta_df["FILENAME"].str.strip().str.lower() == f"{vid}.mp4"
            if match.any():
                row = meta_df.loc[match].iloc[0]
            else:
                log.warning(f"No metadata match for {vid}")
                row = {"ELECTION":"?","PARTY":"Unknown","FIRST_NAME":"","LAST_NAME":""}
            
            # Get transcript - UPDATED WITH ERROR HANDLING
            t_path = TRANSCRIPT_TXT / f"{vid}.txt"
            try:
                transcript = t_path.read_text(encoding="utf-8", errors="replace") if t_path.exists() else "No transcript available."
            except Exception as e:
                log.warning(f"Error reading transcript for {vid}: {str(e)}")
                transcript = "No transcript available."
            
            # Define output path
            dest = dest_folder / f"{jpg.stem}.txt"
            
            # Skip if already processed
            if dest.exists():
                continue
                
            # Add to jobs list
            jobs.append((jpg, row, transcript, dest))
    
    log.info(f"Created {len(jobs)} vision description jobs")
    print(f"Created {len(jobs)} vision description jobs")
    
    # Process in batches to manage rate limits better
    batch_size = 10
    batches = [jobs[i:i+batch_size] for i in range(0, len(jobs), batch_size)]
    print(f"Processing {len(batches)} batches of frame descriptions")
    
    for batch_idx, batch in enumerate(batches):
        print(f"Processing batch {batch_idx+1}/{len(batches)} ({len(batch)} jobs)")
        log.info(f"Processing batch {batch_idx+1}/{len(batches)} ({len(batch)} jobs)")
        
        results = []
        for job in tqdm(batch, desc=f"Batch {batch_idx+1} frames"):
            # Process one at a time to better handle errors
            try:
                results.append(gpt_describe_frame(*job))
            except Exception as e:
                log.error(f"Error processing job: {str(e)}")
                results.append(f"[err ] {job[0].name} - {str(e)}")
            # Small delay between items
            time.sleep(0.5)
            
        for res in results:
            log.info(res)
            print(f"  {res}")
        
        # Add a small delay between batches to avoid rate limits
        if batch_idx < len(batches) - 1:
            delay = 2
            print(f"Waiting {delay}s before next batch...")
            time.sleep(delay)
    
    # 4. Summaries
    print("Step 4: Generating video summaries...")
    summary_jobs = []
    for _, row in meta_df.iterrows():
        vid = Path(row.get('FILENAME', '')).stem
        if not vid:
            continue
            
        try:
            trans_path = TRANSCRIPT_TXT / f"{vid}.txt"
            trans_text = trans_path.read_text(encoding='utf-8', errors='replace') if trans_path.exists() else "No transcript available."
        except Exception as e:
            log.warning(f"Error reading transcript for {vid}: {str(e)}")
            trans_text = "No transcript available."
        
        # Get all descriptions with error handling
        descs = []
        try:
            descs += [p.read_text(encoding='utf-8', errors='replace') for p in DESC_SPEECH.glob(f"{vid}_*.txt")]
        except Exception as e:
            log.warning(f"Error reading speech descriptions for {vid}: {str(e)}")
        
        try:
            descs += [p.read_text(encoding='utf-8', errors='replace') for p in DESC_INTERVAL.glob(f"{vid}_*.txt")]
        except Exception as e:
            log.warning(f"Error reading interval descriptions for {vid}: {str(e)}")
        
        summary_jobs.append((row, trans_text, descs))
    
    log.info(f"Created {len(summary_jobs)} summary jobs")
    print(f"Created {len(summary_jobs)} summary jobs")
    
    with ThreadPoolExecutor(max_workers=N_GPT_SUMMARIES) as pool:
        for res in tqdm(pool.map(summary_worker, summary_jobs), total=len(summary_jobs), desc="GPT summaries"):
            log.info(res)
            print(f"  {res}")

if __name__ == '__main__':
    start = dt.datetime.now()
    print(f"Starting pipeline at {start}")
    main()
    end = dt.datetime.now()
    elapsed = end - start
    log.info(f"Finished in {elapsed}")
    print(f"Pipeline completed in {elapsed}")

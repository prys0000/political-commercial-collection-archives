# appendix 1 - python list of codes

## Install Python and configure PyCharm

* Download and install [**Python**](http://www.python.org/) -- Windows user, we recommend that you install [**Python for Windows**](https://www.python.org/downloads/windows/)

* Configure at least one [**Python interpreter**](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html)

**Each script is a template or starting point for development of your own processes. Each script is followed by basic instructions to get you started!**

#
#
## Instructions for [**audio-recog.py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/audio-recog.py):

Install Required Libraries: Before running the code, ensure that you have installed the required libraries. You can install them using pip as follows:

```python
pip install SpeechRecognition
pip install pandas
```
Import Libraries: At the beginning of your Python script, import the necessary libraries:

```python
import os
import speech_recognition as sr
import pandas as pd
```
* Set Folder Path: Replace PATH TO YOUR FILES with the path to the folder containing the audio files that you want to process. Ensure that the folder contains audio files in the supported formats (wav, mp3, flac).

* Initialize Recognizer: The code initializes a speech recognizer object from the speech_recognition library:

```python
recognizer = sr.Recognizer()
```


* Iterate Over Audio Files: The code iterates over the files in the specified folder and checks if they have the supported audio file extensions. If an audio file is found, it is processed for speech recognition.

* Speech Recognition: The code uses Google's Web Speech API for speech recognition. It reads the audio data from each audio file and performs speech recognition using recognizer.recognize_google(audio).

* Error Handling: The code includes error handling to handle exceptions that may occur during the speech recognition process. If an error occurs, the filename and the corresponding error message will be printed.

* Create DataFrame and Excel File: The extracted text along with the file names is stored in a list called data. The code creates a pandas DataFrame from this list, and the DataFrame is then saved to an Excel file named 'radiooutput.xlsx'.

* Modify Output File Path: Replace YOU PATH_output.xlsx' with the desired output file path and name for the Excel file containing the extracted text.

* Run the Code: After making the necessary modifications, run the Python script. The script will process the audio files in the specified folder, perform speech recognition, and save the extracted text along with the corresponding file names in an Excel file.

***Note: Make sure to have the appropriate permissions to read the audio files and write the Excel file in the specified file paths. The script will automatically create the 'radiooutput.xlsx' file if it does not exist. If you need to process audio files with different extensions, modify the condition in the if statement accordingly.***

#
#

## Instructions for [**excel-format-.py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/excel-format-.py):

Install Required Libraries: Before running the code, ensure that you have installed the required libraries. You can install them using pip as follows:

```python
pip install pandas
pip install python-docx
```
Import Libraries: At the beginning of your Python script, import the necessary libraries:

```python
import pandas as pd
from docx import Document
from docx.shared import RGBColor
import os
```
* Define the docx_to_excel Function: Copy and paste the docx_to_excel function into your script. This function takes the path to a Word document as input and converts it into an Excel file. The function identifies rows in the Word document based on the presence of the word "received" in bold and red text.

* Modify File Path: Replace the file path YOUR PATH FILE_cleaned_file.docx' with the actual path to the Word document that you want to convert. Make sure the file path is correct and points to an existing file.

* Run the Code: After making the necessary modifications, run the Python script. The docx_to_excel function will read the input Word document, process it, and save the contents into an Excel file named "output.xlsx".

* Run the Code: After making the necessary modifications, run the Python script. The function format_received_and_dates will read the input document, process it, and save the formatted document with highlighted dates.

***Note: Make sure to have the appropriate permissions to read the Word document and write the Excel file in the specified file paths. The output Excel file will be saved in the same directory where the Python script is located unless a different path is specified. If you have multiple documents to convert, you can call the docx_to_excel function with different file paths accordingly.***

#
#



## Instructions for [**fuzzy-frames-comp_template.py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/video-compare-text/fuzzy-frames-comp_template.py)

This code demonstrates how to compare the similarity between two videos based on their frame features using OpenCV and numpy. Here are the instructions to use the code:

Install Required Libraries: Before running the code, ensure that you have installed the required libraries. You can install them using pip as follows:

```python
pip install cv2
pip install 
```
Import Libraries: At the beginning of your Python script, import the necessary libraries:

```python
import cv2
import numpy as np
```

Set Video File Paths: Replace 'INSERT FILE PATH' with the paths to your two video files that you want to compare. Make sure to provide the full paths to the video files.

```python
video1_path = 'INSERT FILE PATH'
video2_path = 'INSERT FILE PATH'
```

Set Frame Features: Modify 'ADD FEATURES - YOU CAN ADD MORE DETAILS HERE' to represent the specific features you want to extract from each video frame. You can add more details here based on your feature extraction requirements.

Set Sampling Rate: Adjust the sampling_rate variable to specify the frame sampling rate. For example, if sampling_rate = 10, it means every 10th frame will be processed for feature extraction. Adjust this value based on your specific needs to balance processing time and accuracy.


```python
sampling_rate = 10
```

Implement Feature Extraction: Implement the extract_features function to convert each video frame into a feature representation. This function should take the frame as input and return the corresponding feature representation.

Process Frames and Extract Features: The code reads frames from both videos one by one, extracts features using the extract_features function, and stores the feature representations in frame_features1 and frame_features2 lists.

Convert Frame Features to NumPy Arrays: Convert frame_features1 and frame_features2 lists into NumPy arrays for easier calculations.

```python
frame_features1 = np.array(frame_features1)
frame_features2 = np.array(frame_features2)
```

Calculate Similarity Score: Implement the calculate_similarity function to calculate the similarity score between the two sets of frame features. The function should take frame_features1 and frame_features2 as inputs and return the similarity score.

Output Similarity Score: The script calculates the similarity score using the calculate_similarity function and prints it as the output.

```python
print(f"Similarity score: {similarity_score}")
```

Release Video Captures: After processing the videos, release the video captures to free up resources.

```python
video1.release()
video2.release()
```

Run the Code: After making the necessary modifications and ensuring that you have implemented the extract_features and calculate_similarity functions, run the Python script. The script will process the two videos, extract features, calculate the similarity score, and print the result.

***Note: You need to implement the extract_features and calculate_similarity functions according to your specific requirements for comparing video frames. The features and similarity metric will depend on the type of video analysis you wish to perform. Additionally, ensure that you have provided valid video file paths and have the necessary permissions to read the video files.***
#
#

## Instructions for [**combo-replace-add-class.py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/combo-replace-add-class.py):

Install Required Libraries: Before running the code, ensure that you have installed the required libraries. You can install them using pip as follows:

```python
pip install pandas
```
Import Libraries: At the beginning of your Python script, import the necessary libraries:

```python
import pandas as pd
```
* Define US States and Political Parties: The script defines lists of US states and political parties in lowercase. You can modify or add to these lists if needed.

* Define Short Forms to Long Forms Mapping: The code defines a mapping of short forms to their long forms. You can modify this mapping to suit your specific needs.

* Load the Excel File: Make sure you have an Excel file named 'input.xlsx' containing the data you want to process. Place this file in the same directory as your Python script.

* Define the add_prefix Function: Copy and paste the add_prefix function into your script. This function takes a value as input and checks whether it matches any US state, political party, or short form in the mapping. It then adds the appropriate prefix to the value and returns the updated value.

* Apply the Function to the DataFrame: The code reads the data from 'input.xlsx' into a pandas DataFrame named df. It then applies the add_prefix function to each cell in the DataFrame using the applymap method.

* Write the Result to a New File: The updated DataFrame, df, is saved to a new Excel file named 'output.xlsx'. The file will be created in the same directory as your Python script.

* Run the Code: After making the necessary modifications and ensuring the existence of 'input.xlsx', run the Python script. The output with the prefixed values will be stored in 'output.xlsx'.

***Note: Make sure to have the appropriate permissions to read and write files in the specified file paths. The script will automatically create the 'output.xlsx' file if it does not exist. If you need to process a different Excel file, update the file name accordingly in both the pd.read_excel and df.to_excel functions.***

#
#

## Instructions for [**names-extract.py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/names-extraction.py):

Install Required Libraries: Before running the code, ensure that you have installed the required libraries. You can install them using pip as follows:

```python
pip install pandas
pip install spacy
```
Import Libraries: At the beginning of your Python script, import the necessary libraries:

```python
import pandas as pd
import spacy
```

Load the Language Model: The code loads the English language model for spaCy. Make sure you have installed the model using spacy download en_core_web_sm before running the script.

```python
nlp = spacy.load("en_core_web_sm")
```

Load Excel Data: Replace 'YOUR PATH TO FILE.xlsx' with the path to your Excel file containing the data that you want to process.

```python
df = pd.read_excel('YOUR PATH TO FILE-output1.xlsx')
```

Check Column Existence: The code checks if the 'Text' column exists in the DataFrame. If the column exists, it proceeds with further processing; otherwise, it prints a message.

```python
if 'Text' in df.columns:
```

Define the extract_proper_nouns Function: Copy and paste the extract_proper_nouns function into your script. This function takes a text as input, processes it using spaCy's NLP pipeline, and extracts proper nouns of specific entity types (PERSON, ORG, GPE, LOC, NORP)

Apply the Function to the DataFrame: The code applies the extract_proper_nouns function to the 'Text' column in the DataFrame, creating a new column called 'Text_proper_nouns' to store the extracted proper nouns.

```python
df['Text_proper_nouns'] = df['Text'].apply(extract_proper_nouns)
```

Write the DataFrame to a New Excel File: The updated DataFrame, including the new column 'Text_proper_nouns', is saved to a new Excel file named 'data_with_proper_nouns.xlsx'.

```python
df.to_excel('data_with_proper_nouns.xlsx', index=False)
```

Run the Code: After making the necessary modifications and ensuring the existence of the Excel file, run the Python script. The script will extract proper nouns from the 'Text' column using spaCy and create a new Excel file named 'data_with_proper_nouns.xlsx' with the extracted information.


***Note: Make sure to have the appropriate permissions to read the Excel file and write the new Excel file in the specified file paths. If you need to process a different Excel file, update the file name accordingly in the pd.read_excel and df.to_excel functions.***

#
#

## Instructions for [**pattern-font-structure-date(2i).py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/pattern-font-structure-date(2i).py):

Install Required Libraries: Before running the code, ensure that you have installed the required libraries. You can install them using pip as follows:

```python
pip install python-docx
pip install python-dateutil
```
Import Libraries: At the beginning of your Python script, import the necessary libraries:

```python
from docx import Document
from docx.shared import RGBColor, Pt
from dateutil.parser import parse
import re
import os
```
* Define the is_date Function: Copy and paste the is_date function into your script. This function checks whether a given string can be interpreted as a date.

* Define the format_received_and_dates Function: Copy and paste the format_received_and_dates function into your script. This function takes the path to a Word document as input, processes the document, and highlights the "received" keyword in red and the date that follows in blue.

* Modify File Path: Replace 'place path to document here' with the actual path to the Word document that you want to process. Make sure the file path is correct and points to an existing file.

* Run the Code: After making the necessary modifications, run the Python script. The function format_received_and_dates will read the input document, process it, and save the formatted document with highlighted dates.

***Note: Make sure to have the appropriate permissions to read and write files in the specified file paths. Additionally, ensure that the input Word document has the extension ".docx". If you have multiple documents to process, you can call the format_received_and_dates function with different file paths accordingly.***

#
#

## Instructions for [**speechpy-text-excel_template.py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/video-compare-text/speechpy-text-excel_template.py).
This code performs automatic transcription of audio from video files using the Google Speech Recognition API. Here are the instructions to use the code:

Install Required Libraries: Before running the code, ensure that you have installed the required libraries. You can install them using pip as follows:

```python
pip install SpeechRecognition
pip install moviepy
pip install pandas
```
Import Libraries: At the beginning of your Python script, import the necessary libraries:

```python
import os
import speech_recognition as sr
from moviepy.editor import AudioFileClip, VideoFileClip
import pandas as pd
```

Set Folder Path: Replace "ADD YOUR FILEPATH" with the path to the folder containing the video files that you want to process. Ensure that the folder contains video files in supported formats (e.g., .mp4, .avi, .mkv).

```python
folder_path = "ADD YOUR FILEPATH"
```

Initialize Speech Recognizer: The code initializes a speech recognizer object from the speech_recognition library:


```python
r = sr.Recognizer()
```

Create Output Directory: The code creates an output directory named "transcriptions" inside the video files' folder to store the resulting TXT files.

```python
output_dir = os.path.join(folder_path, "transcriptions")
os.makedirs(output_dir, exist_ok=True)
```

Video and Audio Processing: The code iterates through the video files in the specified folder, extracts the audio from each video, and performs speech recognition on the extracted audio using Google's Web Speech Recognition API.

Transcriptions and TXT Files: The transcriptions for each video are stored in the results list, and corresponding TXT files are created for each transcription in the "transcriptions" folder.

DataFrame and Excel File: The code creates a pandas DataFrame (df) from the transcriptions in the results list. The DataFrame includes columns for filenames and transcriptions. It then saves the DataFrame as an Excel file named "transcripts.xlsx" in the "transcriptions" folder.

Run the Code: After making the necessary modifications and ensuring the existence of video files in the specified folder, run the Python script. The script will process the video files, perform speech recognition on their audio, and save the transcriptions in TXT files. The results will also be stored in an Excel file named "transcripts.xlsx".


***Note: Make sure to have the appropriate permissions to read the video files and write TXT and Excel files in the specified file paths. The script will automatically create the "transcriptions" folder if it does not exist. If you need to process video files with different extensions or formats, modify the condition in the if statement accordingly..***

#
#

## Instructions for [**videohash-1.py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/video-compare-text/videohas-1.py)

This script is for comparing video hashes using the VideoHash library. The script compares the perceptual hashes of different video files to determine their similarity or dissimilarity.

Here are the instructions to use the code:

Install Required Libraries: Before running the code, ensure that you have installed the required libraries. You can install them using pip as follows:

```python
pip install videohash
```
Import the VideoHash class: At the beginning of your Python script, import the necessary class from the videohash library:

```python
from videohash import VideoHash
```

Set Video File Paths: Replace the placeholders 'E:\Speechpy\simcomp-1\P-1463-71759_Trim.mp4', 'E:\Speechpy\simcomp-1\P-1463-71760_Trim.mp4', 'E:\Speechpy\simcomp-2\P-1139-49189.mp4', and 'path/to/video4.mp4' with the full paths to your video files that you want to compare. If FFmpeg is not in the system's PATH, specify the correct path to the ffmpeg_path parameter for each VideoHash object.


```python
path1 = "E:\Speechpy\simcomp-1\P-1463-71759_Trim.mp4"
videohash1 = VideoHash(path=path1, ffmpeg_path="C:\\Users\\user\\Desktop\\ffmpeg-master-latest-win64-gpl-shared\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe")

path2 = "E:\Speechpy\simcomp-1\P-1463-71760_Trim.mp4"
videohash2 = VideoHash(path=path1, ffmpeg_path="C:\\Users\\user\\Desktop\\ffmpeg-master-latest-win64-gpl-shared\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe")

path3 = "E:\Speechpy\simcomp-2\P-1139-49189.mp4"
videohash3 = VideoHash(path=path1, ffmpeg_path="C:\\Users\\user\\Desktop\\ffmpeg-master-latest-win64-gpl-shared\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe")

path4 = "path/to/video4.mp4"
videohash4 = VideoHash(path=path4)
```

Calculate Video Hash Differences: The code calculates the differences between video hashes using the - operator and prints the results.

```python
diff = videohash2 - videohash1
print(diff)

diff = videohash3 - videohash1
print(diff)

diff = videohash3 - videohash2
print(diff)

diff = videohash4 - videohash1
print(diff)

diff = videohash4 - videohash2
print(diff)
```

Check Video Hash Similarity: The code checks the similarity between video hashes using the is_similar() method and prints the results.

```python
similar = videohash2.is_similar(videohash1)
print(similar)

similar = videohash3.is_similar(videohash1)
print(similar)

similar = videohash3.is_similar(videohash2)
print(similar)

equal = videohash4 == videohash1
print(equal)

similar = videohash4.is_similar(videohash2)
print(similar)

similar = videohash4.is_similar(videohash4)
print(similar)

similar = videohash4.is_similar(videohash3)
print(similar)
```

Run the Code: After providing the correct video file paths and making sure FFmpeg is correctly specified (if needed), run the Python script. The script will calculate the differences and check the similarity between video hashes based on the provided video files. The results will be printed to the console.

***Note: Ensure that you have provided valid video file paths and have the necessary permissions to read the video files. If FFmpeg is in the system's PATH, you can omit the ffmpeg_path parameter when creating the VideoHash object. If you encounter any errors, check that FFmpeg is correctly installed and accessible from the specified paths.***

#
#

## Instructions for [**listwords-comp-text.py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/video-compare-text/listwords-comp-text.py)

This script compares two text files and identifies the differing words between them using the difflib library. It then saves the differing words to a new text file called differing_words.txt.

Here are the instructions to use the code:

Install Required Libraries: Before running the code, ensure that you have installed the required libraries. You can install them using pip as follows:

```python
pip install difflib
```
Import the SequenceMatcher class: At the beginning of your Python script, import the necessary class from the difflib library:

```python
from difflib import SequenceMatcher
```

Define the compare_text_files function: This function takes two file paths (file1 and file2) as inputs. It compares the contents of the two text files and identifies the differing words.

Provide the File Paths: Replace the placeholders 'YOUR PATH TO FILE.txt' and 'YOUR PATH TO FILE.txt' in the file1_path and file2_path variables, respectively, with the full paths to your two text files that you want to compare.

```python
file1_path = YOUR PATH TO FILE.txt
file2_path = YOUR PATH TO FILE.txt
```

Call the compare_text_files function: After providing the correct file paths, call the function to compare the text files and identify the differing words.

```python
compare_text_files(file1_path, file2_path)
```

Save the Result: The script will identify the differing words between the two text files and save them to a new text file named differing_words.txt in the same directory as the script. The file will list the differing words, each on a separate line.

Run the Code: Save the script with a .py extension and run it using Python. The script will perform the comparison and save the differing words to the differing_words.txt file.

***Note: Ensure that you have provided valid file paths and have the necessary permissions to read the text files and create/write files in the specified directory. The script is useful for identifying the differences between two text files and can be used for various text comparison tasks.***

#
#

## Instructions for [**Batch convert-ffmpeg.py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/initial-codes-processes/Batch%20convert-ffmpeg.py)

To use FFMpeg as a batch converter to convert videos from MPEG to MP4 format with a watermark, you can use the subprocess module in Python. 

This code loops through the MPEG videos in the input directory, performs the conversion using FFMpeg with the specified watermark, and saves the output MP4 files in the output directory. The overlay filter is used to add the watermark to the videos.

Here are the instructions to use the code:

Install FFMpeg: Before running the code, ensure that you have FFMpeg installed on your system. You can download FFMpeg from the official website (https://www.ffmpeg.org/download.html) and install it according to your operating system.

Set Paths: Replace the placeholder 'path_to_ffmpeg_executable', 'path_to_input_mpeg_videos', 'path_to_output_mp4_videos', and 'path_to_watermark_image' with the appropriate paths for your system.

```python
ffmpeg_path = 'path_to_ffmpeg_executable'
input_directory = 'path_to_input_mpeg_videos'
output_directory = 'path_to_output_mp4_videos'
watermark_file = 'path_to_watermark_image'
```
Loop Through MPEG Videos: The script will loop through all the files in the input_directory and check if they have the .mpeg extension. It will then proceed to convert these MPEG videos to MP4 format with a watermark.

Execute FFMpeg Command: The script constructs an FFMpeg command for each video conversion with a watermark. It uses subprocess.run() to execute the FFMpeg command.

Conversion with Watermark: The script uses the overlay filter to add the watermark to the video. The watermark will be positioned 10 pixels from the right edge (W-w-10) and 10 pixels from the bottom edge (H-h-10) of the video.

Save Output: The converted MP4 videos with the watermark will be saved in the output_directory. The output filenames will have the same name as the input MPEG files, but with the .mp4 extension.

Run the Code: Save the script with a .py extension and run it using Python. The script will convert all the MPEG videos in the specified input directory to MP4 format with the specified watermark and save them in the output directory.

***Note: Ensure that you have provided valid file paths and have the necessary permissions to read the input MPEG videos, write output MP4 videos, and access the watermark image. The script is useful for batch conversion of MPEG videos to MP4 format with a watermark using FFMpeg.***

#
#

## Instructions for [**Clean-QA-1.py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/initial-codes-processes/Cleaning-QA-1.py)

This code performs several data cleaning and sorting operations on a worksheet (CSV file) using the pandas library and the language_tool_python library for language checking.

Here are the instructions to use the code:

Install Required Libraries: Before running the code, make sure you have the necessary libraries installed. 

```python
pip install pandas
pip install language_tool_python
```
Import Libraries: Include the necessary import statements at the beginning of your Python script:

```python
import pandas as pd
import string
from language_tool_python import LanguageTool
```

Read the Worksheet: Update the file_path variable with the path to your CSV file. The code will read the CSV file into a pandas DataFrame.

```python
file_path = r"Path\to\your\worksheet.csv"
df = pd.read_csv(file_path)
```

Rename Columns (Optional): If your worksheet columns are not in the standard letter format (A, B, C, ...), you can rename them using column letters. This is helpful for easier referencing and working with the DataFrame.

```python
column_letters = list(string.ascii_uppercase) + [f"A{letter}" for letter in string.ascii_uppercase]
df.columns = column_letters[:len(df.columns)]
```

Language Checking: The code uses the LanguageTool class from the language_tool_python library to check for spelling, grammar, and acronym errors in each cell of the DataFrame. Detected errors are stored in the errors list.

```python
tool = LanguageTool('en-US')
errors = []

for column in df.columns:
    for cell in df[column]:
        matches = tool.check(cell)
        errors.extend(matches)
```

Sort DataFrame: The code sorts the DataFrame by one or more columns to organize the data in a meaningful order. In this case, the DataFrame is sorted by 'E' (Election year), 'N' (State), 'J' (Last_Name), and 'K' (First_Name).

```python
df.sort_values(by=['E', 'N', 'J', 'K'], inplace=True)
```

Display or Save the Cleaned and Sorted DataFrame: You can either display the cleaned and sorted DataFrame using print(df) or save it to a new CSV file using df.to_csv().

* To display the DataFrame:

```python
print(df)
```

* To save the DataFrame to a new CSV file:

```python
df.to_csv("cleaned_and_sorted_worksheet.csv", index=False)
```

Run the Code: Save the script with a .py extension and run it using Python. Ensure that the CSV file exists and has the correct data format.

***Note: Make sure to replace "Path\to\your\worksheet.csv" with the actual path to your CSV file. Adjust the code as needed for your specific use case. The script is useful for data cleaning, language checking, and sorting operations on CSV files containing tabular data.***

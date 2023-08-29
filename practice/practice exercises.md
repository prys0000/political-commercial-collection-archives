# practice exercises

### radio (audio only) files

#### small batch of audio files with limited available metadata

This document provides instructions for practicing a baseline processing workflow on a small batch of audio files with limited available metadata. The files are from the Julian P. Kanter Political Commercial Collection in the way they were acquired by the Center.

### Step 1: Review Radio Files

1. Access the [radio files folder](https://github.com/prys0000/political-commercial-collection-archives/tree/main/practice/radio%20documents) to review the file contents and how they were ingested, including their respective titles.

### Step 2: Review Scanned Documents

1. Access the radio documents folder and open the [attached PDF-1972-1986 A-Z-Scanned-Radio](https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/1972-1986%20A-Z-Scanned-Radio.pdf). This PDF contains scanned documentation related to the radio files as they were discovered.
2. Consider strategies to manage the information within the sampled pages:
	- Identify discernible patterns to structure information in an organized manner.
	- Identify consistent terminology or headers. (hint: the term *"received"* appears consistent and can be used as a header or section identifier)
	
### Step 3: Create a Structured Word Document 
1. Create a manageable .docx highlighting and structuring consistent or patterned data. We will use the term *"received"* for this example. Use [pattern-structure2i.py](https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/pattern-structure2i.py) script to identify the word "received" in the document and highlight it in red. Additionally, the code looks for dates immediately following the word "received" and highlights them in blue.

	* **results:**


<img src="https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/picture%20-%20pattern-format-example.png" width=40% height=40%>
	
### Step 4: Create Structured Excel

1. Create an Excel file from the resulting .docx file above to provide a structured excel file. Use the [word-excel-1.py](https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/word-excel-1.py) script to generate rows and columns.
2. The resulting Excel file will divide the pdf at every recognition of the term *"received"* easier to merge with transcriptions in the next step.

	* **results:**
	
	
<img src="https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/results-word-excel-1.png" width=40% height=40%>


### Step 5: Analyze Excel and Clear Issues Affecting Data 

1. Issue 1: Inches Representation

	- The inches are represented inconsistently as "ll" and "11", |1, || throughout the file when referring to audio formats. We know audio reels come in various sizes, such as 3", 5", 7", and 10".
	- Resolution: Replace the inconsistent characters "ll" and "11" with the appropriate format sizes (3", 5", 7", 10"). 
	- Add the term "format:" to the text to clarify the audio format.

2. Issue 2: Time Representation

	- Time is represented inconsistently throughout the original documents, using seconds (e.g., :10, :30, :60) and, in some cases, "minutes."
	- The Python script has identified 3" followed by :30 as "JII:JO," which needs to be replaced with the correct terms.

3. Issue 3: Other Identifiable Terminology 

	- Continue to identify additional issues that affect data management. 
	- Record identifiable conditions and elements to build an effective script (states, titles, special characters)

4. Run the [replace-add-format](https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/replace-add-format.py) script to assist in managing the data. 	


### Step 6: Transcribe Audio Files

1. Access the [radio.wav files](https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/README_radio%20files.md).
2. Consider the titles, sizes, length and other notable characteristics of the sample of audio files. (*hint: there may not be any discernable notable elements) 
2. Run the [audio-recog.py](https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/audio-recog.py) script that performs speech recognition on audio files and extracts the speech content from them. It utilizes the SpeechRecognition library (speech_recognition).
2. The script (for this example)will generate an Excel file with the current titles of the audio files in one column and the transcribed text in another column.

* **results:**

<img src="https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/results-audio-recognition.png" width=40% heigh=40%>


### Step 7: Extract Named Entities

1. Run the [names-extract.py](https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/names-extraction.py) script to recognize and extract proper nouns (names of people, places, organizations, etc.).
2. The script will place the extracted named entities into a new column in the Excel file. These results will assist in the next step. 

* **results:**

<img src="https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/results-names-extraction.png" width=40% height=40%>

3. (*Alternate*) Run the [advanced names extraction](https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/1-start-nltk.py) script for training and using a NEW named entity recognition model to extract named entities from excel, pdf, or other file type.  An alternate to this script is available for political science data that we have used for this project [start-nltk.py](https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/start-nltk.py) which was created from an [annotated control list](https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/ner_training_politicalscience.csv) and [ner structured list from annotated](https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/ner_results.csv). 


### Step 8: Data Cleanup

1. Run [standard-fuzzy-clean-1.py](https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/standard-fuzzy-clean-1.py) script to perform fuzzy string matching to standardize values (from controlled vocabulary or other sources) in specific columns of an Excel file based on a reference column containing the standardized values.
2. Run [clean-1.py](https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/clean-1.py) to clean text data by checking cell contents, verifying text, removing leading or trailing spaces, spelling, entity identification, and standardized data from previous steps. 
3. Analyze the data and resolve issues like inconsistent formatting or terminologies.


### Step 9: Compare and Link Data

1. Consider combining both datasets/into one workbook with tabs, although two separate worksheets will work (edit the script to define). There will be one worksheet with filenames of audio files, transcriptions, and collumns of named entities and dates. The second worksheet will be the extracted data from the scanned pages that have been sorted and structured for management. 
2. Run [record-link.py](https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/record-link.py) script to  identify and link records in two different datasets that likely refer to the same entity, despite variations in data formatting or errors. The report will be output to a new excel worksheet. This ouput will identify enough linkage to assign filenamed files with the extracted informmation that describes the audio files. 
	- *Note: The threshold used in the classification step (len(df1.columns) times 0.75) can be adjusted according to the specific needs and characteristics of the datasets being compared. Lowering the threshold may increase the likelihood of finding matches but also increase the chances of false positives. Conversely, raising the threshold may reduce the chances of false positives but may also miss potential matches. The threshold should be fine-tuned based on the data and use case.*


### Step 7: Create a Working Metadata Worksheet

1. Combine and organize the data into a new metadata worksheet.
2. The new worksheet should include identification, transcription data, and legacy data.

### Step 8: Streamline the Workflow

1. Consider combining Steps 1-6 into one or two Python scripts to improve workflow efficiency.
2. The streamlined workflow will serve as a baseline collection management platform for newly acquired, large-scale collections.

### Step 9: Export Worksheet XML to Audio Files

1. Export the metadata worksheet to the audio files.
2. Apply any necessary renaming, convert preservation copies to preservation access copies, and create access copies as per the repository policy.
3. Organize the exported files into folders for migration to the server.

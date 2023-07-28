# practice exercises - https://github.com/prys0000/political-commercial-collection-archives/tree/main/practice

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
	
### Step 3: Create Structured Excel

1. Create an Excel file from the resulting .docx file above to provide a structured excel file. Use the [word-excel-1.py](https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/word-excel-1.py) script to generate rows and columns.
2. The resulting Excel file will divide the pdf at every recognition of the term *"received"* easier to merge with transcriptions in the next step.

	* **reults:**
	
<img src="https://github.com/prys0000/political-commercial-collection-archives/blob/main/practice/radio%20documents/results-word-excel-1.png" width=40% height=40%>

### Step 4: Transcribe Audio Files

1. Run the audio-recog.py script to quickly transcribe the audio files.
2. The script will generate an Excel file with the current titles of the audio files in one column and the transcribed text in another column.

### Step 5: Extract Named Entities

1. Run the names-extract.py script to recognize and extract proper nouns (names of people, places, organizations, etc.).
2. The script will place the extracted named entities into a new column in the Excel file.

### Step 6: Data Comparison and Cleanup

1. Use Python scripts to compare the result files and link document names from steps 2b and 4.
2. Run a Python error check script to clean up or highlight significant errors in the result file from step 5.
3. Analyze the data and resolve issues like inconsistent formatting or terminologies.

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

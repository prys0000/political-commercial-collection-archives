## practice exercises 

### small batch of audio files from born-digital collection with limited metadata

This workflow will provide an ***example*** of a baseline processing workflow. The files are from the Julian P. Kanter Political Commercial Collection in the way they were acquired by the Center.

1.	Access the [**radio files**](https://github.com/prys0000/political-commercial-collection-archives/tree/main/radio%20files) folder and review the file contents, including how they were ingested and their respective titles.
2.	Access the [**radio documents**](https://github.com/prys0000/political-commercial-collection-archives/tree/main/radio%20documents) folder and open the attached pdf, which contains scanned documentation. 

   ***NOTE: normal practice combines several processes into one Python file, but for this exercise, we are dividing it into separate processes.***

   * Consider strategies on managing the text within the pdf document. 
      * Identify discernible patterns that can help in structuring the dataset in a more organized manner. 
        * In this document, the term **"received"** is consistent and can function as a header or section identifier. 
        * Refer to [**python template - pattern-font-structure-date(2i).py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/pattern-font-structure-date(2i).py) and [**example of new document after python**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/date_formatted_formatted_standardized_cleaned_file.pdf)
       * The [**resulting document**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/example-compare.jpg) helps identify a consistent pattern by highlighting information and formatting commonalities, making it easier for the human eye to recognize.
       * Create an excel that structures the document into a working structure by creating rows of “recognized” from ‘b’ by running [**excel-format-.py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/excel-format-.py) which results in an [**easily managed excel file**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/excel-format-output.xlsx) to merge with transcriptions (below in #3)
3.	Quickly analyze the excel sheet and determine what issues would assist in managing the data. This example above has ***clear issues that can be resolved***. 
	- Inches is represented by “ll”, “11” throughout the file when referring to formats of the audio. We know that audio reels come in various sizes (3”, 5”, 7”, 10”). Replace the characters with “and add “format:” to the text.
	- Time is represented throughout the original documents in seconds (:10, :30, :60) and several by ‘minutes’. However, the python script identified 3” followed by :30 as JII:JO. Replace those terms. 
		- By correcting the issues, we now have a ***new way to classify the data*** (time, format)
		- Combine the issues into one python script and run [**example-combo-replace-add-class.py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/combo-replace-add-class.py) – the **results** help to clean data easily and very quickly without much effort [**see the results of this example**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/state-ad-modified.xlsx) 
         
4.	Access the [**radio files**](https://github.com/prys0000/political-commercial-collection-archives/tree/main/radio%20files) folder and run the [**audio-recog.py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/audio-recog.py) script to quickly transcribe the audio files and create an excel file with current titles of the audio files in one column and the transcribed text in another column. 
	* results: [**results of transcription example**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/excel-format-output.xlsx)

5.	Run the [**names-extract.py**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/names-extraction.py) script to recognize and extract proper nouns (names of people, places, organizations, etc.) and place them into a new column.
	* results: [**results of NER example**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/names-states-mod.xlsx) 

	- ***note: The results from 4 and 5 can now be applied to step 3 and create useful columns to run the comparisons and sync both worksheets:***

6. Run a [Python script] to compare the result files and link document names from steps 2b and 4. a. Run a [Python error check script] to clean up or highlight significant errors in the result file from step 5
	-	[**results: transcription, NER, fuzzy sort**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/results-steps%204-5-3_1.jpg)

	-	[**results: worksheet from pdf scans, NER, fuzzy sort, count format**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/results-steps%204-5-3_mod_2.png)

	-	[**results: pages matching results from both worksheets**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/results-scans-matching-4-5-3_3.png)

6.	Run a [Python script] to create a working metadata worksheet. This will combine and place data in new columns to help manage the items.

	- [**results: new worksheet with identification, transcription data, and legacy data**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/new-worksheet-ids.png)

7.	Steps 1-6 can be streamlined into one or two python scripts to improve workflow efficieny. The results allow for a baseline collection management platform to develop as newly acquired, large-scale collections are received.

8. Export worksheet XML to the audio files. *Depending on the repository policy, apply renaming of files, convert preservation copies to preservation access copies, create access copies and export to folders for migration to the server.*



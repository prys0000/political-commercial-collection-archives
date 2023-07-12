## practice exercises

### small batch of audio files from born-digital collection with limited metadata

This workflow will provide an overview of the baseline processing workflow. The files have been converted to .mp3 for ease of accessibility, storage, and optional listening.

1.	Access the [**radio files**](https://github.com/prys0000/political-commercial-collection-archives/tree/main/radio%20files) folder and review the file contents, including how they were ingested and their respective titles.
2.	Access the [**radio documents**](https://github.com/prys0000/political-commercial-collection-archives/tree/main/radio%20documents) folder and open the attached pdf, which contains scanned documentation. 
    * Consider strategies on managing the text within the pdf document. 
    * Identify discernible patterns that can help in structuring the dataset in a more organized manner. In this document, the term "received" is consistent and can function as a header or section identifier. 
    * Refer to [python template - pattern-font-structure-date(2i).py](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/pattern-font-structure-date(2i).py) and [example of new document after python](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/date_formatted_formatted_standardized_cleaned_file.pdf)
    * The resulting document helps identify a consistent pattern by highlighting information and formatting commonalities, making it easier for the human eye to recognize.

    >  

       <img src="https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/picture%20-%20pattern-format-example.png" width="75%" height="75%"/>
   >
    


3.	Access the [**radio files**](https://github.com/prys0000/political-commercial-collection-archives/tree/main/radio%20files) folder and run the [audio-recog.py] script to quickly transcribe the audio files and create an excel file with current titles of the .mp3 files in one column and the transcribed text in another column. (Typically, we would combine several processes into one Python file, but for this exercise, we are dividing it into separate processes.)
4.	Run the [names-extract.py] script to recognize and extract proper nouns (names of people, places, organizations, etc.) and place them into a new column.
5.	Run a [Python script] to compare the result files and link document names from steps 2b and 4. a. Run a [Python error check script] to clean up or highlight significant errors in the result file from step 5.
6.	Run a [Python script] to create a working metadata worksheet.
7.	Depending on the repository policy, apply renaming of files, convert preservation copies to preservation access copies, create access copies and export to folders for migration to the server.



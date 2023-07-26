**Sample Student Access ‘Groups A-B’ Processes:**

1. Sort sheet by LAST NAME – FIRST NAME (workflow specific) 
2. Implement [**controlled standardization script**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radio%20documents/combo-replace-add-class.py) to standardize irregularities  (must be 87% confidence to edit)
    * &ensp; Names and nicknames vary for the candidate
   
    * &ensp; ICPSR numbers may vary for the candidate
   
    * &ensp; States may vary for the candidate
   
    * &ensp; Parties may vary for the candidate
   
4. Review terms or strings corrected and add extracted text to ‘control sheet-text’.
5. Implement [**controlled abbreviations script**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radiodocuments/combo-replace-add-class.py) to standardize all acronyms, short-hand, jargon. Add extracted/corrected text to ‘control sheet-tab abbr.)
6. Implement [**error-A_B-1 script**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radiodocuments/combo-replace-add-class.py) - this will export a report with highlighted ‘suggestions, alerts’ for human review.
7. Clear duplicates from master lists and amend (add parties, states, ICPSR numbers, etc…)
8. Backup files  

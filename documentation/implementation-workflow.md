## **implementation of controls**

In this phase of the (re)processing, the primary objective was to implement control mechanisms for data cohesion. Intern students were provided with the integrated data. Assigned workflow included identifying irregularities, common grammatical elements, and standardizing various aspects such as topics, subjects, offices, names, and other relevant data elements.

**cleaning and standardizing data**

The pandemic posed significant challenges in developing and implementing efficient workflows. Processing and cleansing data became more complex due to limitations like students accessing files from international locations, limited technology availability, and restricted access to students for training or skill development.
To address confusion and accessibility issues, a workflow was designed to streamline applications, condense Python scripts, and incorporate other automation methods. The objective was to improve overall efficiency and effectiveness despite the pandemic-induced constraints.

The workflow was organized based on academic semesters (Fall, Spring, Summer) and allocated to internship students. These students were divided into three groups: Group A, B, and C. Each student was given specific 'chunks' of data, which were obtained by dividing the master worksheet. They also received a metadata master sheet containing their assigned lines, a folder with original scans from the aggregated information, and another folder with available videos.

Automated delivery points were set up for each folder, triggering updates and reports. Once the work was completed, it was deposited into a Quality Assurance (QA) folder, which automatically assigned it to the groups responsible for quality checking. After undergoing two QA checks, the work was automatically sent to the collection archivist for finalization and preparation for the second phase[^1].

#
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

#
**Sample Student Access ‘Groups C’ Processes:**

1. Sort sheet by LAST NAME – FIRST NAME (workflow specific) 
2. Run [**fuzzy-comp-1 script**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/initial-codes-processes/names-abbrv-fuzzycomp-C.py) to verify NAMES and ABBREVIATIONS and make sure they are in the CONTROL-SHEET-TAB-TEXT and CONTROL-SHEET-TAB-ABBRV.
3. Run [**error-C-1 script**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radiodocuments/combo-replace-add-class.py) for report of ‘suggested’ alerts, spell checker
4. Implement [**controlled abbreviations script**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/radiodocuments/combo-replace-add-class.py) to standardize all acronyms, short-hand, jargon. Add extracted/corrected text to ‘control sheet-tab abbr.)
5. Sort sheet LAST NAME – FIRST NAME/OFFICE/ELECTION YEAR
6. Backup files

#
**Sample Student Access ‘Groups QA-Rover-1' Processes:**

1. Files will be automatically added to the assigned QA/R folder
2. Perform data validation and standardization based on the controlled vocabulary with [**QA-1 script**](https://github.com/prys0000/political-commercial-collection-archives/blob/main/initial-codes-processes/QA-1.py). This script will identify and handle any errors or inconsistencies in the data. This will generate a report highlighting the issues found and suggest possible corrections.
3. Review report and address issues (save report and notes/changes/alterations made).
4. Backup files

#
 **Sample Student Access ‘Groups QA-Rover-2' Processes:**

1. Open new metadata worksheet and sort by ‘Component ID’
2. Open ‘KanterVideos’ folder, CTRL+A, right click SHIFT, copy as path
3. Paste in new tab in metadata worksheet ‘files’ (CTRL+A, CTRL+H, replace the path leaving the P-#-#. 
4. In metadata sheet copy the Component ID column into the ‘files’ tab next to the just pasted video files.
5. Select both columns and in excel in the ‘Home’  ‘Conditional Formatting’  ‘Highlight Cell Rules’  ‘Duplicate Values’
6. Review the files that are in both videos and excel by sorting the columns by cell color, clear the cells leaving only the non-duplicates
   
<br/>

### --this will begin a new phase of the project--


<br/>

### footnotes:
[^1]: Pryse, JA. Archival Education and Research Institute AERI (June 19-23, 2023) - Julian P. Kanter Collection: Chaos and Order. Louisiana State University.

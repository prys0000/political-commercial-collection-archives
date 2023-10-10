## follow-up documentation (updated October 10, 2023)

### Physical Inspection

During the re-processing of our physical collections, we encountered various complexities, which we have documented on this page along with their corresponding solutions. 
***This comprehensive documentation process ensures the accuracy and usability of our digital and physical collections.***

**Assumptions**
1. In the large cold room storage area, we identified two separate groups of boxes. Each box had a label with a large-font number, and additional numbers were listed below:
    * Section one consisted of 15 rows of 5 shelves with white plastic archival storage containers, numbered from 1 to 928 with additional numbers below.
    * Section two contained 15 rows of 5 shelves with a mix of box types (plastic and standard archival storage boxes), numbered from 1 to 1108 with additional numbers below.
2. We assumed that section one housed film and older audio/video formats (such as 16mm, 8mm, 1" videotape, 2" videotape, and magnetic tape), while section two contained migrated copies (3/4" videotape, Beta SP, VHS, and other iterations, including cassettes, etc.).

**Problems**
1. Boxes in both sections did not align, meaning that "box 1" in section one did not correspond to "box 1" in section two.
2. Contents inside the boxes often did not match the labels, causing discrepancies. For instance, "box 1" with items 32556-32564 did not contain the items listed in our documentation.
3. Each box contained items that may or may not have been documented elsewhere.
4. Items not found in our documentation were cross-referenced visually by matching numbers, election years, dates, candidates, formats, and titles.
5. Some items matched multiple elements of our documentation (e.g., title, election year, candidate) but lacked unique identifiers or contained misidentified information.

### Physical and Digital Inspection

As we inspected the items within the boxes, we identified comments such as "possible duplicate," "similar to ---," and "VC number does not match but is the same as --." These observations prompted us to develop new methods for cross-referencing current records against newly discovered physical items.

**Methodology**
1. We consolidated all office metadata worksheets containing digital videos and performed quality checks on the metadata.
2. We combined the "working" physical inspection notes/list to create a new "Master List."
3. The [**AV_Transcription-app.py**](https://github.com/prys0000/congressional-portal-project/blob/main/scripts-notes/AV_Transcript-app.py) script was used to generate transcriptions for the digital records listed on the Master List:
    * We utilized the .mp4 access copies for transcription, excluding preservation master, preservation access, and migration formats as well as watermarked .mp4 files.
4. We applied the ***=INDEX($E$1:$E$, MATCH(A1, $D$1:$D$, 0))*** formula to match the UNIQUE ID column with its corresponding transcript.
   
5. Transcripts were sorted:
    * (1) Exact matches in strings.
    * (2) Matching all exact text to each UNIQUE ID.
    * (3) We created 'NOTES' in the 'NOTES' column to document all matching files and preserved legacy notes, shifting them to a sub-column.
    * (4) Due to programming limitations and the extensive collection, data processing was carried out systematically by office.

</br>
 
<img src="https://github.com/prys0000/political-commercial-collection-archives/blob/1ccaf7507930d7260cf98df3649176d24da516af/images/trans-fuzzy.png">
    

6. We used the [**FuzzyTrans.py**] script with varying thresholds to identify "similar" files and documented them:
    * For instance, we looked for minor alterations or additional content at the end of advertisements.
    * This is essential for research and usability purposes, as it enables a more accurate description of videos, preventing information overload.
      

<img src="https://github.com/prys0000/political-commercial-collection-archives/blob/16acef311a78b95739d5266e1a387381620d2bb0/images/fuzzytrans.png">


7. We were able to create chunks of video files organized by similarity or duplication and applied [**fuzzy-frames-1.py**](https://github.com/prys0000/political-commercial-collection-archives/blob/16acef311a78b95739d5266e1a387381620d2bb0/video-compare-text/fuzzy-frames-1-template.py) to compare the similarity between 'duplicate' or 'semi-duplicate' videos based on a combination of frame features as well as SSIM and MSE scoring. 

8. New documentation was added to the Master List, along with notes from the physical investigation of items. 
    * Additional notes for exact matches or similar items included identifying the analog format. 

9. With the new list of duplicates we were able to 'trace' the history of each file to determine archival reasoning for duplication, various identification numbers, and titles. Documentation was compiled from a number of records, notes, and indexes.

</br>

<img src="https://github.com/prys0000/political-commercial-collection-archives/blob/995c749e5cb07447603822a739a93b7d14709ee0/images/1988-Dukakis-Failed.png">

</br>

*** These notes help determine the "original" or "most complete" copy of the ad, which can be handled accordingly and protect the integrity of the Collections' history.***
      

  ## follow-up documentation (9/27/2023)

  ### Physical Inspection

  When re-processing the physcial collections many layers of complexities were discovered. This page documents the problems and solutions. 

**Assumptions**
  1. In the large cold room storage area were two seperate groups of boxes which were numbered with labels, written/typed including a large font number and below were additional numbers.
      * Section one included 15 rows of 5 shelves with white plactic archival storage containers with labels on each ranging from 1-928 with additional numbers included below.
      * Section two included 15 rows of 5 shelves , mix box types (plastic and standard archival storage boxes) with labels ranging 1-1108 with additional numbers included below.
  2. The assumption was section one included film and older audio/video formats (16mm, 8mm, 1' videotape, 2" videotape, magnetic tape (sound)) and section two included the migrated copies (3/4" videotape, Beta SP, VHS, other iterations to include casseettes, etc...)

**Problems**
1. The boxes in both sections did not link/match [box 1 in section one did not coincide with box 1 in section 2]
2. The items inside of the boxes did not match the labels in most occassions, insie of the boxes [box 1 with items 32556-32564 were not the items in the boxes on the documentation that we have]
3. Each box contained items that may or may not have a record of their existence on the documentation that we have compiled and readily available.
4. Items without representation in the documentation were checked by visually matching any numbers on the item to the master worksheet, matching election years or dates, candidates, formats, titles.
5. Some items twere matched to multiple elements of the worksheet [i.e. title, election year, candidate] but missing unique identifiers or containing misidentified identification were noted

### Physical and Digital Inspection

Inspecting the items in the boxes there are several noted comments concerning "possible duplicate", "similar to ---", "VC number does not match but is the same as --"
Concerned about exact duplications or similarities of ads in files instigated new methods to check the current records against newly didcovered physical items.

**Methodology**

1. Combined all office metadata worksheets that had digital videos accounted for and quality checked/metadata.
2. Added the 'working' physical inspection notes/list to develop a new 'Master List'
3. Utilized the [**AV_Transcription-app.py**](https://github.com/prys0000/congressional-portal-project/blob/main/scripts-notes/AV_Transcript-app.py) script to create transcriptions for the digital records contained on the Master list
    * Digital files utilized were the .mp4 access copies created
    * Preservation master, preservation access, and migration formats were not used
    * Watermarked .mp4 files not used
4. Used =INDEX($E$1:$E$, MATCH(A1, $D$1:$D$, 0)) to match UNIQUE ID column to corresponding transcript
5. Sorted the transcripts
    * (1) exact matches in strings
    * (2) matched all exact txt to each UNIQUE ID
    * (3) created 'NOTES' in 'NOTES' column documenting all matching files - did not remove legacy notes, shifted to sub column
    * (4) Due to programming timing out and the vast collection, chunks of data were processed systematically by office
6. Next, we use [**FuzzyTrans.py**] with varied threshhold to identify 'similar' files to document
    * i.e. at the end of an ad there is a campaign statement, endorsement, or minor alteration that needs to be noted (for ***research and usability purposes***)
       * Research and usability means that more accurate descrtipion of the videos to include minor alterations helps the user filter information rather than overloading
7. New documentation was added to the Master List and physical investigation of items notes
    * Other notes to matching exacts or similars involved identityfiing the aalog format (1" videotape P-1859-255669 vs. 3/4" videotape P-582-19665 vs. VHS videotape P-185-2085)
         * If the transcripts are exact matches the analog format notes help determne the 'original' or 'most complete' copy of the ad and iterations can be handled accordingly
         * For example: 1" was created in 1956; 3/4" created in 1971; VHS created 1976 = 1" is the possible original format (pre-video examination)


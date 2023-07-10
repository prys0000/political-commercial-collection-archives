## issues with system infrastructure and normalization

System infrastructure is a key factor in facilitating the processing, integration, validation, and accuracy of textual and data content within an archival repository. The efficiency of the structural processes involved in migrating archival information greatly influences the normalization of the collection content, ensuring its longevity.

A fundamental objective in managing large and intricate collections is to establish a functional strategy that supports the seamless interconnection of components from data ingestion to dissemination. This strategy encompasses the entire lifecycle of the collection and aims to optimize the management and accessibility of the content.

Throughout the duration of this project, a multitude of processes have been created to effectively handle legacy collection records and facilitate their transition into a modern archival structure. These processes have continually evolved and adapted to incorporate new information, overcome obstacles, and tackle emerging data management challenges.

### normalization

In the context of this project, text normalization refers to the process of transforming text data into a standardized and consistent format. The [goal of text normalization](https://github.com/prys0000/political-commercial-collection-archives/blob/main/images/controlled-1.jpg) is to ensure uniformity and improve the cohesiveness of the data for long-term preservation, discoverability, and interoperability . This process involves removing or replacing certain elements in text to achieve a standard representation. By normalizing text, it becomes easier to manage and analyze data, ensuring its compatibility with various systems and facilitating its accessibility and understanding in the future.

The consolidation and analysis of the collection's legacy data and amalgamated inventories posed a significant challenge in establishing consistent file identification and managing administrative and descriptive metadata elements. The process of removing redundancies, correcting metadata errors, [resolving conflicting entries](https://github.com/prys0000/political-commercial-collection-archives/blob/main/images/Name-index.jpg) , and standardizing terminology, substantial improvements were made in data governance and the overall representation of the collection. An additional example of code to use at this phase of the project is [videohash.py](https://pypi.org/project/videohash/). This endeavor also led to the discovery of previously unidentified outliers, contributing to a deeper comprehension of the data corpus .

### component identification (P_COPY-OID)

With multiple decades separating many of the acquired materials and entirely different personnel responsible for development of the Collection, information utilized to record collection data has proven to be highly inconsistent. Identifying the most used categorization that signified a sense of order was recognized as a priority when standardizing and formatting the collection. Compiled data analysis helped uncover relationships and associations between the identification numbers and other data elements. This enabled a deeper understanding of how each identification number was utilized and interconnected within the records.
During the process of integrating the collection data and formatting the available records, a closer examination revealed the need for a primary and secondary identification number . It became apparent that the P_COPY identification number served as a top-level grouping container, encompassing various item-level components referred to as OID numbers. This insight provided a deeper understanding of the hierarchical structure within the dataset and facilitated more granular analysis and organization.

[P_COPY-1](https://github.com/prys0000/political-commercial-collection-archives/blob/main/images/P_COPY-1.jpg)

### redundancy – 2

The amalgamation of the P_COPY and OID numbers resulted in the creation of the Unique ID, which serves as a categorical identifier for individual ads in the collection. In order to ensure data accuracy and avoid redundancy, additional redundancy checks were implemented after integrating the collection data. It is common for files in the collection to have multiple iterations, including both digital and analog items that have not been digitized yet.

[P_COPY combination-explanation](https://github.com/prys0000/political-commercial-collection-archives/blob/main/images/P_COPY-combine.jpg) 

By normalizing the corpus of information in the archival collection, it becomes possible to conduct data quality checking processes to identify contradictory, inaccurate, or new instances of redundancy. This normalization process helps filter and narrow down the volume of data, enabling the application of [content mitigation analysis – example-1](https://github.com/prys0000/political-commercial-collection-archives/blob/main/video-compare-text/speechpy-text-excel_template.py) [*notes*](https://github.com/prys0000/political-commercial-collection-archives/blob/main/video-compare-text/speechpy-text-excel_notes.txt), [content mitigation analysis – example-2](https://github.com/prys0000/political-commercial-collection-archives/blob/main/video-compare-text/fuzzy-frames-comp_template.py) [*notes*](https://github.com/prys0000/political-commercial-collection-archives/blob/main/video-compare-text/fuzzy-frames-comp_notes.txt) techniques. As a result, inconsistencies and redundancies can be more effectively detected and addressed, improving the overall reliability and usability of the archival data.

As an example, during text analysis, two files, P-1139-49189 and P-1935-130892, showed a high similarity score. However, further analysis through video examination revealed that these files were distinct and not similar. This process helped to clarify and differentiate between the files, ensuring accurate categorization and avoiding duplication.

[P-1139-P-1935-1](https://github.com/prys0000/political-commercial-collection-archives/blob/main/images/P-1139-P-1935-1.jpg)

[P-1139-P-1935-2](https://github.com/prys0000/political-commercial-collection-archives/blob/main/images/P-1139-P-1935-2.jpg)



___________________________________________
### footnotes:
1. The example snippets have been simplified and cleaned up to provide a baseline for public editing. Multiple iterations of the examples and combinations of different code segments have been used during the course of the project.
2. Ruochen Liu’s research concerning video similarity with object detection has proven to be a highly useful tool when developing workflow and scripting for mitigating redundancy within the collection (http://www.cs.columbia.edu/~jrk/NSFgrants/videoaffinity/Interim/21y_Nick.pdf). 
3. Combining collection inventories, notes, and other historical documents identified various identifications which have been mentioned in previous sections. Other identification numbers included: NID, PCA_ID, and various legacy identification items. 


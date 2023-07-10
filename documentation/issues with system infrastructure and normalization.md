## issues with system infrastructure and normalization

System infrastructure is a key factor in facilitating the processing, integration, validation, and accuracy of textual and data content within an archival repository. The efficiency of the structural processes involved in migrating archival information greatly influences the normalization of the collection content, ensuring its longevity.

A fundamental objective in managing large and intricate collections is to establish a functional strategy that supports the seamless interconnection of components from data ingestion to dissemination. This strategy encompasses the entire lifecycle of the collection and aims to optimize the management and accessibility of the content.

Throughout the duration of this project, a multitude of processes have been created to effectively handle legacy collection records and facilitate their transition into a modern archival structure. These processes have continually evolved and adapted to incorporate new information, overcome obstacles, and tackle emerging data management challenges.

### normalization

In the context of this project, text normalization refers to the process of transforming text data into a standardized and consistent format. The [goal of text normalization](https://github.com/prys0000/political-commercial-collection-archives/blob/main/images/controlled-1.jpg)[^1] is to ensure uniformity and improve the cohesiveness of the data for long-term preservation, discoverability, and interoperability . This process involves removing or replacing certain elements in text to achieve a standard representation. By normalizing text, it becomes easier to manage and analyze data, ensuring its compatibility with various systems and facilitating its accessibility and understanding in the future.

The consolidation and analysis of the collection's legacy data and amalgamated inventories posed a significant challenge in establishing consistent file identification and managing administrative and descriptive metadata elements. The process of removing redundancies, correcting metadata errors, [resolving conflicting entries](https://github.com/prys0000/political-commercial-collection-archives/blob/main/images/Name-index.jpg) , and standardizing terminology, substantial improvements were made in data governance and the overall representation of the collection . An additional example of code to use at this phase of the project is [videohash.py](https://pypi.org/project/videohash/)[^2]. This endeavor also led to the discovery of previously unidentified outliers, contributing to a deeper comprehension of the data corpus.

### component identification (P_COPY-OID)

With multiple decades separating many of the acquired materials and entirely different personnel responsible for development of the Collection, information utilized to record collection data has proven to be highly inconsistent. Identifying the most used categorization that signified a sense of order was recognized as a priority when standardizing and formatting the collection. Compiled data analysis helped uncover relationships and associations between the identification numbers and other data elements. This enabled a deeper understanding of how each identification number was utilized and interconnected within the records.
During the process of integrating the collection data and formatting the available records, a closer examination revealed the need for a primary and secondary identification number. It became apparent that the P_COPY identification number served as a top-level grouping container, encompassing various item-level components referred to as OID numbers. This insight provided a deeper understanding of the hierarchical structure within the dataset and facilitated more granular analysis and organization.

[P_COPY-1](https://github.com/prys0000/political-commercial-collection-archives/blob/main/images/P_COPY-1.jpg)[^3] 

### redundancy – 2

The amalgamation of the P_COPY and OID numbers resulted in the creation of the Unique ID, which serves as a categorical identifier for individual ads in the collection. In order to ensure data accuracy and avoid redundancy, additional redundancy checks were implemented after integrating the collection data. It is common for files in the collection to have multiple iterations, including both digital and analog items that have not been digitized yet.

[P_COPY combination-explanation](https://github.com/prys0000/political-commercial-collection-archives/blob/main/images/P_COPY-combine.jpg)[^4] 

By normalizing the corpus of information in the archival collection, it becomes possible to conduct data quality checking processes to identify contradictory, inaccurate, or new instances of redundancy. This normalization process helps filter and narrow down the volume of data, enabling the application of [content mitigation analysis – example-1](https://github.com/prys0000/political-commercial-collection-archives/blob/main/video-compare-text/speechpy-text-excel_template.py) [notes](https://github.com/prys0000/political-commercial-collection-archives/blob/main/video-compare-text/speechpy-text-excel_notes.txt), [content mitigation analysis – example-2](https://github.com/prys0000/political-commercial-collection-archives/blob/main/video-compare-text/fuzzy-frames-comp_template.py) [notes](https://github.com/prys0000/political-commercial-collection-archives/blob/main/video-compare-text/fuzzy-frames-comp_notes.txt) techniques. As a result, inconsistencies and redundancies can be more effectively detected and addressed, improving the overall reliability and usability of the archival data.

  >**example-1:** As an example, during text analysis, two files, P-1139-49189 and P-1935-130892, showed a high similarity score. However, further analysis through video examination revealed that these files were &nbsp; distinct and not similar. This process helped to clarify and differentiate between the files, ensuring accurate categorization and avoiding duplication.

  - [P-1139-P-1935-1](https://github.com/prys0000/political-commercial-collection-archives/blob/main/images/P-1139-P-1935-1.jpg)
  - [P-1139-P-1935-2](https://github.com/prys0000/political-commercial-collection-archives/blob/main/images/P-1139-P-1935-2.jpg)

>**example-2:** Another common barrier to data cohesion and content mitigation was actual video production discrepencies including slight variations in music, text overlays, objects within video frames, and other visual aspects. These differences create unique collection items and require accurate analysis and categorization of the ads.

Political campaign-focused marketing strategies frequently require making minor adjustments and edits to the ads, leading to the creation of new 'unique' items customized for specific regional locations, marketing analyses, and other factors. These modifications encompass a range of changes, such as subtle alterations in depicted objects, variations in background materials, adjustments to the colors of buildings, cars, and people, and even slight modifications to the theme song or background music. 

[similarity in ads P-1463-71760 and P-1463-71759](https://github.com/prys0000/political-commercial-collection-archives/blob/main/images/similar-diff-1%20copy.jpg)

[![Watch](https://i.ytimg.com/an_webp/nx6MqTxNS_U/mqdefault_6s.webp?du=3000&sqp=CJaUsaUG&rs=AOn4CLDp5oMifZH4PsrgfKABmR5F_WaDVA)](https://youtu.be/nx6MqTxNS_U)


The image exhibits a common issue within the collection. In comparison of two files, P-1463-71759 and P-1463-71760, both digital files appear to be possible duplicates with same digital file size and length of video. The metadata representing the files included exact title, creator, extent, and dates, however, when analyzing video data, the videos were not duplicate ads. 

[P-1463–comp-sim-py](https://github.com/prys0000/political-commercial-collection-archives/blob/main/images/P-1463-comp-sim.jpg)

Additionally initial analysis of the collection indicated inconsistencies with candidate names, parties, or other descriptive attributes. Some variations may be more challenging to detect, such as non-standard frame heights or widths, which are sometimes employed to adhere to network limitations or address copyright concerns during later stages of ad design.

In order to identify and analyze the collection in greater detail, extract additional pattern of errors or variation requires the use of comparison algorithms and collection specific methodologies. By developing fundamental platforms of analysis, the level of similarity or differences between files can be measured more accurately to depict uniqueness. This approach contributes to the effective organization of the collection and ensures that each item is accurately classified based on its specific characteristics .


___________________________________________
### footnotes:
[^1]: The image provided illustrates the implementation of a controlled vocabulary/thesaurus in this project, customized to cover various aspects such as content, creators, candidates, and other campaign-related information.By employing controlled vocabulary, the processing of information by students and staff becomes more efficient and accurate, as it helps narrow down criteria and ensure consistency.
[^2]: The archival collection faced significant challenges due to variations in candidate names, states, parties, and other elements, resulting in problematic and inconsistent information. The provided image showcases an index of candidates, which includes ICPSR data for enrolled individuals. Extensive documentation of the variations in names, states, and parties has been carried out for the legacy data, and for this project, a standardized and controlled approach has been implemented to ensure consistency and usability.
[^3]: Compiled legacy data includes multiple identifications assigned to items within the collection (see [case-study]( https://github.com/prys0000/political-commercial-collection-archives/blob/main/documentation/case-study.md) for more information. 
[^4]: By implementing a standardized unique identifier, we established a clear and consistent means of ensuring long-term continuity. In the process, we removed any additional identifiers during (re)processing, and the newly created identifier, known as the P_COPY+OID number (P-####-#####), took precedence. This decision was driven by the need to advance with the latest iteration of the indexed inventory and maintain a streamlined and efficient approach.



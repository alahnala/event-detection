
# *PhraseNet* Replication Study

***Introduction.*** This codebase features a demo from my replication study of "Event Detection and Summarization using Phrase Network" (Melvin et al., 2017) for Advanced Data Mining (EECS 576), Fall 2019.
The original work proposed a model they call *PhraseNet*, an unsupervised event detection model for Twitter using textual features.

***Motivation.*** The *PhraseNet* paper was published in ***ECML PKDD 2017*** and had not gained much attention. However, I was curious about its implementation because I am interested in graph applications for language, and it seems interesting that the entire event detection in this method was mainly based on textual features.

***Method summary.*** *PhraseNet* can be broken down into the following steps:
1. Extract high frequency phrases from set of tweets
2. Graphically represent relationships between these phrases in terms of tweet co-occurrence in a timestep.
3. Apply a community detection algorithm over this graph to establish initial event candidates by phrase communities. 
4. For each event candidate, determine peaks in terms of relative frequency of its phrases across the timestep distribution. 
5. Determine an event candidate is an event by analyzing the number of peaks across timesteps, the peak height intensities, and the standard deviation of peak heights across timesteps.
6. Evaluate the performance based on precision and recall on a set of manually determined target events.
7.  Consider the phrases of the event's phrase clusters to be the event summary, and compare these summaries to baseline Twevent (Li et al., 2012). 
   
***References.*** 

Sara Melvin, Wenchao Yu, Peng Ju, Sean Young, and Wei Wang. 2017. Event Detection and Summarization Using Phrase Network. In Machine Learning and Knowledge Discovery in Databases.

Chenliang Li, Aixin Sun, and Anwitaman Datta. 2012. Twevent: segment-based eventdetection from tweets. InProceedings of the 21st ACM international conference onInformation and knowledge management. ACM, 155–164.

## Replication Study Report

To read the full report of the study, see [ReplicationReport.pdf](./ReplicationReport.pdf).

# Demo

***Data:***

I provided a small, preprocessed sample of tweets from November 10-12, 2019 in [sample_dataset/](./sample_dataset/).

***Parameters:***

I've chosen a parameter set that results in events being detected in this small dataset. The parameters used in the big data setting are in the paper. The parameters are set in lines 53-69 in demo.sh, in case you would like to experiment :)  

***To Run:***

```bash
./demo.sh [number of cpu threads (default is 2)]
```

***Output:***

This demo execution is quite verbose. The output of interest is a latex-formatted table showing the events detected. You can also view this in [Report.md](./Report.md).

***Program Execution:***

The command above will execute the following:

1. [count_tweets.py](./src/count_tweets.py): Runs at the beginning of the program to count the number of tweets in the given dataset.
   ```bash
    python src/count_tweets.py [folder of tweet files]
    ```
2. [divide_folder.py](./src/divide_folder.py): Divides [folder of tweet files] into [number of threads] subfolders for parallel processing.
3. [parallel_topmine.py](./src/parallel_topmine.py): Runs the TopMine algorithm (El-Kishky). 
    
    Input: file of tweet text separated by lines 
    
    Output: frequent phrases for a unit of time
    ```bash
    python src/parallel_topmine.py [folder of tweet files]/[thread]/ [minimum support] [num topics] [phrase size] [alpha] [output folder name] [(optional) stopwords file idx]
    ```
    1. Reference: El-Kishky, Ahmed, et al. "Scalable topical phrase mining from text corpora." Proceedings of the VLDB Endowment 8.3 (2014): 305-316. 
    2. Added parallel processing to implementation built off of https://github.com/anirudyd/topmine.
4. [parallel_fp_growth.py](./src/parallel_fp_growth.py): Efficient method for identifying the most frequent co-occurring phrase pairs. Creates files representing graphs by edges. Prints the number of edges.

    ```bash
    python src/parallel_fp_growth.py [folder of tweet files]/[thread]/ [minimum support]
    ```
    1. Uses [pyfpgrowth_mod.py](./src/pyfpgrowth_mod.py) this is a modification of https://pypi.org/project/pyfpgrowth/.
    2. Calls [phrase_weights.py](./src/phrase_weights.py)
5. [sub_counter.py](./src/sub_counter.py): Counts the number of frequent phrases / edges across all threads.
    ```
    python src/sub_counter.py [file with frequent phrases count for each thread separated by lines]
    ```
6. [join_folders.py](./src/join_folders.py): Rejoins subfolders
7. [event_candidates.py](./src/event_candidates.py): Selects candidates for events.
    ```bash
    python src/event_candidates.py sample_dataset/
    ```
    1. calls [phrase_clustering.py](./src/phrase_clustering.py)
    2. calls [event_similarity.py](./src/event_similarity.py)
8. [params_table.py](./src/params_table.py): Outputs a latex-formatted table to log the parameters used in the experiment.
9. [peak_detection_2.py](./src/peak_detection_2.py): Detects peaks to determine the events. Outputs a latex-formatted table to show the events.
    ```bash
    python src/peak_detection_2.py sample_dataset/ 12 n/a 1 0 10 .0005 .005
    ```
    1. Calls [sliding_window.py](./src/sliding_window.py)


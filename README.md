
# Example

```bash
./experiment_pipeline.sh sample_dataset/ 5 5 1 12 1 0.001 .0005 .005 24hr n/a 0 1 24hr 10 2 exp5_sw1 0 logs/demo_report.log 5
```

# Demo Program

After running ```./demo.sh [number of threads]```, the following will execute:

1. [count_tweets.py](./src/count_tweets.py): Runs at the beginning of the program to count the number of tweets in the given dataset.
   ```bash
    python src/count_tweets.py [folder of tweet files]
    ```
2. [divide_folder.py](./src/divide_folder.py): Divides [folder of tweet files] into [number of threads] subfolders for parallel processing.
3. [parallel_topmine.py](./src/parallel_topmine.py): Runs the TopMine algorithm. 
    
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
    1. Uses [pyfpgrowth_mod.py](./src/pyfpgrowth_mod.py) this is a modification of https://pypi.org/project/pyfpgrowth/
    2. Calls [phrase_weights.py](./src/phrase_weights.py)
5. [sub_counter.py](./src/sub_counter.py): Counts the number of frequent phrases / edges across all threads.
    ```
    python src/sub_counter.py [file with frequent phrases count for each thread separated by lines]
    ```
6. [join_folders.py](./src/join_folders.py):
5. [event_candidates.py](./src/event_candidates.py): Selects candidates for events.
    ```bash
    python src/event_candidates.py sample_dataset/
    ```
    1. calls [phrase_clustering.py](./src/phrase_clustering.py)
    2. calls [event_similarity.py](./src/event_similarity.py)
6. [params_table.py](./src/params_table.py)
7. [peak_detection_2.py](./src/peak_detection_2.py)
    ```bash
    python src/peak_detection_2.py sample_dataset/ 12 n/a 1 0 10 .0005 .005
    ```
    1. Calls [sliding_window.py](./src/sliding_window.py)




[](./src/latex_table.py)
[](./src/parallel_fp_growth.py)


[](./src/phrase_clustering.py)



[](./src/utilities.py)

# Utilities

[](./src/utilities.py)
1. **cprint**: print function that adds terminal text color and outputs to log files

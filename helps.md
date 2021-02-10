# 576replication


## demo instructions

 Hi - I think I messed up the makefile in the code submission that I uploaded (I just noticed this request when I opened up the assignment tonight to submit so I was trying to make it in a rush, so so sorry....) and I am past the deadline for my late day balance. 
 
 What the makefile should have done is run demo.sh in the demo directory, followed by some number that you want to specify for CPU threads. 
 I put a very small dataset so 1 or 2 should not be too bad but it will run really fast if you put a higher number.
  You can cd into demo/ and just do ./demo.sh 5 for example. 
  
  With a dataset as small as the one I submitted this does not detect events with the parameters I used for a dataset that was a little larger. 
  
  I think demo.sh is fairly readable, the parameters are set starting in line 55, so you can play around the parameters if you're curious! 
  
  But if you just want to see some even detection output it looks like making ToPMineMinSupport="5", ToPMinePhraseSize="5", and topminealpha="2" will give a handful of meaningful results on this dataset. I've attached a demo.sh with these modified parameters for you here if you like. Again I am so sorry about the makefile and the parameters not being set to output an event result! 


#### extract high frequency phrases from tweets

#### create phrase network
in phrase_network.py

ToPMine algorithm

#### Preprocessing data

data_prep/preprocess_tweets.py [unprocessed tweet directory] [directory for preprocessed output] [method = allie, author, or scalability]

allie: does data cleansing based on source
author: follows the instructions from the PhraseNet paper
scalability: processes any tweet that is in valid format (14 attributes and non empty text), does not eliminate non-english tweets.

Note that some preprocessings steps are done in ToPMine. Originally I had removed those steps from the ToPMine program and put them here. But some preprocessing steps are useful to experiment with whereas others would stay constant across all experiments. The constant preprocessing steps are done here, and the preprocessing steps I experiment with (stopword removal) are done in ToPMine.


#### fp_growth.py

Set your own values:
phrase_folder="topmine-master/output_w_sw/" #this should be the output file of topmine
intermediate_folder="topmine-master/intermediate_output_w_sw/"
graph_folder="graphs/test_tweets/"

#### requires
python-louvain
networkx
contractions
regex
emoji

#### great lakes
sbatch slurm.big
squeue -A mihalcea
scancel jobid


#### data_validation/sources.txt
Lists the sources from the tweet data. This is used to qualitatively determine which sources to eliminate if they are ads/bots/automatically generated tweets.


#### Experiments

Performance (F1 score) experiments are in experiments_scripts/. 
Scalability experiments are in scalability_experiments/.


#### True events

true_events/timeanddate.txt collected observance, federal holidays, religious holidays, seasonal
https://www.timeanddate.com/holidays/us/2015

#### Other:

I don't use pipeline scripts but I'm keeping them in case they would be useful to refer to.
experimentOneParsable="results/allie_parseable.txt";
timestamp() {
  date +"%X"
}

log_progress () {
  echo -e "$1" >> $2;
  echo -e "$1";
}

#preprocess
scalingTmpDir=sample_dataset/;
# mkdir -p "${scalingTmpDir}";
totalTweets="$(python count_tweets.py sample_dataset/)"; # count total tweets

resultsFolder=demo_results/;
mkdir -p "${resultsFolder}";

logFolder=logs/;
mkdir -p "${logFolder}";
logfile="${logFolder}demo.log";
scaleReportLog="${logFolder}demo_report.log";

run_proportion () {
	resultsFile="${resultsFolder}$1"; #make results file
	numThreads=$2;

	log_progress "\e[1mTotal tweets:\e[0m $totalTweets" $scaleReportLog; # log

	log_progress "\e[95m$(timestamp) $1% start\e[0m" $logfile; # log start time
	SECONDS=0;
	./experiment_pipeline.sh sample_dataset/ $ToPMineMinSupport $ToPMinePhraseSize $FPGrowthMinSupport $slidingWindowTimesteps $Theta $Omega $Beta $Chi $Tau $dampeningCoefficient $StartingTimeStep $ToPMinenumTopics $TimestepsInTau $Alpha $topminealpha $resultsFile $stopwordsFile $scaleReportLog $numThreads; # run
	log_progress "\e[95m$(timestamp) $1% end\e[0m" $logfile;
	log_progress "\e[1mCompleted in $SECONDS seconds\e[0m" $scaleReportLog;
	echo "$SECONDS" >> $experimentOneParsable; # log
	echo "" >> $experimentOneParsable; # log
	echo "" >> $experimentOneParsable; # log

}

numThreads=$1;


# Report Header
time=$(date);
STR="\e[1;4;44;97mDemo reports for experiments started $time\e[0m";
log_progress "$STR" $scaleReportLog;
STR=$'\n\n';
log_progress "$STR" $scaleReportLog;

ToPMineMinSupport="5"; # paper = 40
ToPMinePhraseSize="5"; # paper = 5
FPGrowthMinSupport="1"; # paper = 8
slidingWindowTimesteps="12"; # paper = unknown
# if slidingWindowTimesteps="6" theta = 2, 12->3
Theta="1"; # paper = 3, minimum threshold.
Omega="0.001"; # paper = 0.1. this is the dampening coefficient.
Beta=".0005"; # paper = .05 this is minumum threshold
Chi=".005"; # paper = .5 minimum threshold.
Tau="24hr";
dampeningCoefficient="n/a"; #todo remove
StartingTimeStep="0"; 
ToPMinenumTopics="1"; 
TimestepsInTau="24hr"; 
Alpha="10"; #paper = 10, high alpha threshold in peak detection 
topminealpha="2"; #not sure what to put here
stopwordsFile="0"; # 2 is the nltk stopwords. 0 is all, 1 is topmine.

# Experiment Header
STR=$'\e[1;107;95mExperiment 5: Easy constraints (low FP growth, low thresholds except theta)\e[0m';
log_progress "$STR" $scaleReportLog;
run_proportion exp5_sw1 $numThreads;

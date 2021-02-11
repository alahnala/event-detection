mkdir -p logs;
mkdir -p results;
timestamp() {
  date +"%X"
}


# Log and print progress function
logfile="logs/demo.log";

log_progress () {
  echo -e "$1" >> "$2";
  echo -e "$1";
}

# set data location, include slash at end
tweetFolder="$1"; 
datalocation="$tweetFolder";


allResults=${17};
log_progress "logging results in" $allResults;
log_results () {
  echo "$1" >> ${allResults};
  echo "$1";
}



#set paper specified parameters
ToPMineMinSupport="$2";
ToPMinePhraseSize="$3";
FPGrowthMinSupport="$4";
slidingWindowTimesteps="$5";
Theta="$6";
Omega="$7";
Beta="$8"
Chi="$9";
Tau="${10}";
dampeningCoefficient="${11}"
StartingTimeStep="${12}"
Alpha="${15}"


#set other parameters
ToPMinenumTopics="${13}";
TimestepsInTau="${14}";
TopMineAlpha="${16}";
StopWords="${18}";
ScaleReportLog="${19}"


mkdir -p "src/topmine/${tweetFolder}" 
mkdir -p "src/topmine/${tweetFolder}output/"
mkdir -p "src/topmine/${tweetFolder}intermediate_output/"
if grep -Fxq "src/topmine/${tweetFolder}" .gitignore
then
	# don't need to add it to .gitignore
	:
else
	#add the prepared folder to gitignore so we don't accidentally add or overwrite the folder
	echo "src/topmine/${tweetFolder}" >> .gitignore 
fi




# mkdir -p "graphs/${tweetFolder}";

rm -f results/frequent_phrases.count; # remove if it already exists so we can get a clean count
frequentPhrases="results/frequent_phrases.count";
rm -f results/num_edges.count; # remove if it already exists so we can get a clean count
numEdges="results/num_edges.count";

function process_subfolder () {
	data=$1
	log_progress "$(timestamp): python src/parallel_topmine.py $data $ToPMineMinSupport $ToPMinenumTopics $ToPMinePhraseSize $TopMineAlpha $tweetFolder $StopWords" ${logfile}
	FREQ_PHRASES="$(python src/parallel_topmine.py $data $ToPMineMinSupport $ToPMinenumTopics $ToPMinePhraseSize $TopMineAlpha $tweetFolder $StopWords)" #run topmine
	# echo "done topmine $data"
	echo "${FREQ_PHRASES}" >> $frequentPhrases
	# echo "starting fpgrowth $data"

	
	log_progress "$(timestamp): python src/parallel_fp_growth.py $data $FPGrowthMinSupport" $logfile 
	NUM_EDGES="$(python src/parallel_fp_growth.py $data $FPGrowthMinSupport)" #run fp_growth to find high co-occurring phrases and generate graph files
	echo "${NUM_EDGES}" >> $numEdges
	mkdir -p src/topmine/${tweetFolder}output/
	mv src/topmine/$2/output/* src/topmine/${tweetFolder}output/
	mkdir -p src/topmine/${tweetFolder}intermediate_output/
	mv src/topmine/$2/intermediate_output/* src/topmine/${tweetFolder}intermediate_output/
	rm -r src/topmine/$2/
	mkdir -p src/graphs/$tweetFolder
	mv src/graphs/$2/* src/graphs/$tweetFolder
	rm -r src/graphs/$2/
}

numThreads="${20}";
log_progress "$(timestamp): python src/divide_folder.py $datalocation $numThreads" $logfile
OUTPUT="$(python src/divide_folder.py $datalocation $numThreads)";
COUNTER=0
while [  $COUNTER -lt $numThreads ]; do
	subFolder="$datalocation$COUNTER/"
	# echo running topmine and fpgrowth on $subFolder

	# Step 1: Run and log topmine

	process_subfolder $subFolder $COUNTER &
	pids[${COUNTER}]=$!
	let COUNTER=COUNTER+1 
done


# wait for all pids
for pid in ${pids[*]}; do
    wait $pid
done
#I want to get the total
TOTAL_FREQ_PHRASES="$(python src/sub_counter.py $frequentPhrases)";
echo -e "ToPMine frequent phrases: ${TOTAL_FREQ_PHRASES}" >> $ScaleReportLog;
echo -e "ToPMine frequent phrases: ${TOTAL_FREQ_PHRASES}";
TOTAL_EDGES="$(python src/sub_counter.py $numEdges)";
echo -e "FPGrowth graph edges: ${TOTAL_EDGES}" >> $ScaleReportLog;
echo -e "FPGrowth graph edges: ${TOTAL_EDGES}";
log_progress "$(timestamp) Topmine and FPGrowth complete" $logfile; 
log_progress "" $logfile; 
log_progress "" $logfile; 

OUTPUT="$(python src/join_folders.py $datalocation)";


if [ -d "src/event_candidates/${tweetFolder}" ]
then
    rm -r "src/event_candidates/${tweetFolder}"
else
	:
fi



# Run and log initial event candidates from phrase network
log_progress "Event candidates. Determines initial candidates with Louvain Community Detection." $logfile;
log_progress "$(timestamp): python src/event_candidates.py $tweetFolder" $logfile;
OUTPUT="$(python src/event_candidates.py ${tweetFolder})";
time=$(date)
echo -e "Louvain and merge phrase clusters: ${OUTPUT}" >> $ScaleReportLog;
# echo "${OUTPUT}," >> $experimentOneParsable;
log_progress "    Total phrase clusters: ${OUTPUT}" $logfile;
log_progress "$(timestamp) Event candidates complete" $logfile; 
log_progress "" $logfile; 


# ["ToPMine minsupport", "ToPMine n-gram",  "FPgrowth minsupport", "$\\theta$", "$\omega$", "$\\alpha$", "$\\beta$", "$\chi$", "$\\tau"]
# ["ToPMine \#topics", "$t \in \\tau$"]
#Log parameters
PARAMETERS="$(python src/params_table.py $ToPMineMinSupport $ToPMinePhraseSize  $FPGrowthMinSupport $Theta $Omega $Alpha $Beta $Chi $Tau $ToPMinenumTopics $TopMineAlpha $StopWords)";


# Run and log peak detection and event detection
log_progress "Peak detection. Finds peaks and determines final events by analyzing peaks." $logfile;
log_progress "$(timestamp): python src/peak_detection_2.py ${tweetFolder} ${slidingWindowTimesteps} ${dampeningCoefficient} ${Theta} ${StartingTimeStep} ${Alpha} ${Beta} ${Chi}" $logfile; 
OUTPUT="$(python src/peak_detection_2.py ${tweetFolder} ${slidingWindowTimesteps} ${dampeningCoefficient} ${Theta} ${StartingTimeStep} ${Alpha} ${Beta} ${Chi})";
log_progress "$(timestamp) Event detection complete." $logfile;

numEvents="${OUTPUT##*$'\n'}";
echo -e "Final events: $numEvents" >> $ScaleReportLog;
echo "Parameters:" >> $ScaleReportLog;
echo "$PARAMETERS" >> $ScaleReportLog;
echo "Events:" >> $ScaleReportLog;
echo "$OUTPUT" >> $ScaleReportLog;

log_results "Parameters:";
log_results "$PARAMETERS";
log_results "";
log_results "Events:";
log_results "${OUTPUT}";



./clean.sh
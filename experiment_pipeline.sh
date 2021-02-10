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


mkdir -p "topmine-master/${tweetFolder}" 
mkdir -p "topmine-master/${tweetFolder}output/"
mkdir -p "topmine-master/${tweetFolder}intermediate_output/"
if grep -Fxq "topmine-master/${tweetFolder}" .gitignore
then
	# don't need to add it to .gitignore
	:
else
	#add the prepared folder to gitignore so we don't accidentally add or overwrite the folder
	echo "topmine-master/${tweetFolder}" >> .gitignore 
fi




mkdir -p "graphs/${tweetFolder}";

rm -f demo_results/frequent_phrases.count; # remove if it already exists so we can get a clean count
frequentPhrases="demo_results/frequent_phrases.count";
rm -f demo_results/num_edges.count; # remove if it already exists so we can get a clean count
numEdges="demo_results/num_edges.count";

function process_subfolder () {
	data=$1
	log_progress "\e[104m$(timestamp): python parallel_topmine.py $data $ToPMineMinSupport $ToPMinenumTopics $ToPMinePhraseSize $TopMineAlpha $tweetFolder $StopWords\e[0m" ${logfile}
	FREQ_PHRASES="$(python parallel_topmine.py $data $ToPMineMinSupport $ToPMinenumTopics $ToPMinePhraseSize $TopMineAlpha $tweetFolder $StopWords)" #run topmine
	echo "done topmine $data"
	echo "${FREQ_PHRASES}" >> $frequentPhrases
	echo "starting fpgrowth $data"

	
	log_progress "\e[104m$(timestamp): python parallel_fp_growth.py $data $FPGrowthMinSupport\e[0m" $logfile 
	NUM_EDGES="$(python parallel_fp_growth.py $data $FPGrowthMinSupport)" #run fp_growth to find high co-occurring phrases and generate graph files
	echo "${NUM_EDGES}" >> $numEdges
	echo "mv topmine-master/$2/output/* topmine-master/${tweetFolder}output/"
	mv topmine-master/$2/output/* topmine-master/${tweetFolder}output/
	echo "mv topmine-master/$2/intermediate_output/* topmine-master/${tweetFolder}intermediate_output/"
	mv topmine-master/$2/intermediate_output/* topmine-master/${tweetFolder}intermediate_output/
	echo "rm -r topmine-master/$2/"
	rm -r topmine-master/$2/
	echo "mv graphs/$2/* graphs/$tweetFolder"
	mv graphs/$2/* graphs/$tweetFolder
	echo "rm -r graphs/$2/"
	rm -r graphs/$2/
}

numThreads="${20}";
log_progress "\e[104m$(timestamp): python divide_folder.py $datalocation $numThreads\e[0m" $logfile
OUTPUT="$(python divide_folder.py $datalocation $numThreads)";
COUNTER=0
while [  $COUNTER -lt $numThreads ]; do
	subFolder="$datalocation$COUNTER/"
	echo running topmine and fpgrowth on $subFolder

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
TOTAL_FREQ_PHRASES="$(python sub_counter.py $frequentPhrases)";
echo -e "\e[1mToPMine frequent phrases:\e[0m ${TOTAL_FREQ_PHRASES}" >> $ScaleReportLog;
echo -e "\e[1mToPMine frequent phrases:\e[0m ${TOTAL_FREQ_PHRASES}";
TOTAL_EDGES="$(python sub_counter.py $numEdges)";
echo -e "\e[1mFPGrowth graph edges:\e[0m ${TOTAL_EDGES}" >> $ScaleReportLog;
echo -e "\e[1mFPGrowth graph edges:\e[0m ${TOTAL_EDGES}";
log_progress "\e[92m$(timestamp) Topmine and FPGrowth complete\e[0m" $logfile; 
log_progress "" $logfile; 
log_progress "" $logfile; 

OUTPUT="$(python join_folders.py $datalocation)";
# OUTPUT="$(python parallel_gl_scripts/join_topmine_folders.py $datalocation topmine-src/$tweetFolder/)";


if [ -d "event_candidates/${tweetFolder}" ]
then
	echo "Clearing out event_candidates/${tweetFolder}"
    rm -r "event_candidates/${tweetFolder}"
else
	:
fi
# create location for event candidates output (graphs for this corpus)
mkdir -p "event_candidates/${tweetFolder}"; 
if grep -Fxq "event_candidates/${tweetFolder}" .gitignore;
then
	# don't need to add it to .gitignore
	:
else
	#add the prepared folder to gitignore so we don't accidentally add or overwrite the folder
	echo "event_candidates/${tweetFolder}" >> .gitignore 
fi


# Run and log initial event candidates from phrase network
log_progress "Event candidates. Determines initial candidates with Louvain Community Detection." $logfile;
log_progress "\e[104m$(timestamp): python event_candidates.py $tweetFolder\e[0m" $logfile;
OUTPUT="$(python event_candidates.py ${tweetFolder})";
time=$(date)
echo -e "\e[1mLouvain and merge phrase clusters:\e[0m ${OUTPUT}" >> $ScaleReportLog;
# echo "${OUTPUT}," >> $experimentOneParsable;
log_progress "    Total phrase clusters: ${OUTPUT}" $logfile;
log_progress "\e[92m$(timestamp) Event candidates complete\e[0m" $logfile; 
log_progress "" $logfile; 


# ["ToPMine minsupport", "ToPMine n-gram",  "FPgrowth minsupport", "$\\theta$", "$\omega$", "$\\alpha$", "$\\beta$", "$\chi$", "$\\tau"]
# ["ToPMine \#topics", "$t \in \\tau$"]
#Log parameters
PARAMETERS="$(python params_table.py $ToPMineMinSupport $ToPMinePhraseSize  $FPGrowthMinSupport $Theta $Omega $Alpha $Beta $Chi $Tau $ToPMinenumTopics $TopMineAlpha $StopWords)";


# Run and log peak detection and event detection
log_progress "Peak detection. Finds peaks and determines final events by analyzing peaks." $logfile;
log_progress "\e[104m$(timestamp): python peak_detection_2.py ${tweetFolder} ${slidingWindowTimesteps} ${dampeningCoefficient} ${Theta} ${StartingTimeStep} ${Alpha} ${Beta} ${Chi}\e[0m" $logfile; 
OUTPUT="$(python peak_detection_2.py ${tweetFolder} ${slidingWindowTimesteps} ${dampeningCoefficient} ${Theta} ${StartingTimeStep} ${Alpha} ${Beta} ${Chi})";
log_progress "\e[92m$(timestamp) Event detection complete.\e[0m" $logfile;

numEvents="${OUTPUT##*$'\n'}";
echo -e "\e[1mFinal events:\e[0m $numEvents" >> $ScaleReportLog;
log_results "Parameters:";
log_results "$PARAMETERS";
log_results "";
log_results "Events:";
log_results "${OUTPUT}";


echo "removing graphs" $logfile;
rm -r graphs/$tweetFolder;


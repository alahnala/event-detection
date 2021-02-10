""" Implements the algorithm provided in the following research paper:

El-Kishky, Ahmed, et al. "Scalable topical phrase mining from text corpora." Proceedings of the VLDB Endowment 8.3 (2014): 305-316.

Credit goes to https://github.com/anirudyd/topmine
"""
import subprocess, shlex, glob, sys, os
from utilities import cprint
import time
from tqdm import tqdm
from traceback import print_exc, format_exc
from pprint import pprint

def get_output_of(command):
	args = shlex.split(command)
	return subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]


def ToPMine_algorithm(file_name, folder_name, min_support=40, ngram_limit=5, num_topics=4, alpha=2):
	'''
	input: file of tweet text only, separated by lines.
	paper specifications:
		uses the minimum support of 40
		phrases were given a limit to search no more than 5-gram.

	code available here: https://github.com/anirudyd/topmine. This code has the most stars and watches.
	El-Kishky et al., 2014: "Scalable topical phrase mining from text corpora."

	output: frequent phrases (for a unit of time?? What granularity of time?)

	I could do this for each file so i have time of 4 hour windows? The paper says "the ToPMine algorithm [6]was used to identify the frequent phrases for a certain unit of time," so I'll just do this per file. I actually think they did this for 24 hour windows.
	'''
	phrase_mining_cmd = "python3 topmine-master/topmine_src/run_phrase_mining.py {} {} {} {} {}".format(file_name, ngram_limit, min_support, folder_name, alpha)
	# print("running", phrase_mining_cmd)
	# print(get_output_of(phrase_mining_cmd))
	get_output_of(phrase_mining_cmd)

	#Update, we only need the most frequent phrases which is found in the first program.
	# phrase_lda_cmd = "python3 topmine-master/topmine_src/run_phrase_lda.py {} {} {}".format(num_topics, file_name, folder_name)
	# print(get_output_of(phrase_lda_cmd))
	return get_output_of(phrase_mining_cmd)

def ToPMine_algorithm_2(file_name, folder_name, min_support=40, ngram_limit=5, num_topics=4, alpha=2, stopword_file="topmine-master/topmine_src/stopwords.txt"):

	phrase_mining_cmd = "python3 topmine-master/topmine_src/run_phrase_mining.py {} {} {} {} {} {}".format(file_name, ngram_limit, min_support, folder_name, alpha, stopword_file)
	# print("running", phrase_mining_cmd)
	# print(get_output_of(phrase_mining_cmd))
	get_output_of(phrase_mining_cmd)

	# prints the number of frequent phrases
	return get_output_of(phrase_mining_cmd)


def main():
	'''
	Prints total number of frequent phrases
	'''
	data_location=sys.argv[1]
	min_support=int(sys.argv[2])
	tweet_files = glob.glob(data_location + "*") #files separated by date time they were collected
	num_topics=int(sys.argv[3]) #in paper they don't say
	phrase_size=int(sys.argv[4]) #per phrasenet paper, the phrase size was set to 5-gram
	# min_support=40 #per phrasenet paper, the min support is 40
	alpha=float(sys.argv[5])
	folder_name = sys.argv[6]

	# print("data_location", data_location.split('/'))
	folder_name = data_location.split('/')[-2] + '/'
	# print("folder_name", folder_name)
	os.makedirs("topmine-master/"+folder_name + "intermediate_output/", exist_ok=True)
	os.makedirs("topmine-master/"+folder_name + "output/", exist_ok=True)
	# quit()

	total_freq_phrases = 0
	if len(sys.argv) > 7:
		stopwords_file = int(sys.argv[7])
		for file_name in tqdm(sorted(tweet_files)):
			start = time.time()
			# cprint("Starting ToPMine for {}".format(file_name), logname="topmine", p2c=False)
			num_freq_phrases = ToPMine_algorithm_2(file_name, folder_name, min_support=min_support, ngram_limit=phrase_size, num_topics=num_topics, alpha=alpha, stopword_file=stopwords_file)	
			end = time.time()
			# cprint("ToPMine took {} seconds for {}".format(end - start, file_name), logname="topmine", p2c=False)		
			total_freq_phrases += int(num_freq_phrases)

	else:
		for file_name in tqdm(sorted(tweet_files)):
			start = time.time()
			# cprint("Starting ToPMine for {}".format(file_name), logname="topmine", p2c=False)
			num_freq_phrases = ToPMine_algorithm(file_name, folder_name, min_support=min_support, ngram_limit=phrase_size, num_topics=num_topics, alpha=alpha)
			end = time.time()
			# cprint("ToPMine took {} seconds for {}".format(end - start, file_name), logname="topmine", p2c=False)
			total_freq_phrases += int(num_freq_phrases)

	print(total_freq_phrases)

if __name__ == "__main__":
	main()
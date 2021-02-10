'''
I am filling in some blanks here about things that were not explicitly stated in the paper.

The purpose of this is to identify the most frequent co-occurring phrase pairs efficiently, ie they mean identify co-occurring phrase pairs that happen 8 times
'''
from pyfpgrowth_mod import FPTree
import pyfpgrowth_mod
import os
import glob
import itertools
import networkx as nx
import sys
from tqdm import tqdm
from traceback import print_exc
import phrase_weights
from collections import OrderedDict


'''
if i get maximum depth exceeded:
import sys
sys.setrecursionlimit(some_value)
'''

def match_tweets_topmine():
	'''
	function given the input folders for topmine output and tweets, 
	'''
	topmine_files = glob.glob(folder_name + "*.txt") #files separated by date time they were collected

	return

def define_transactions(topmine, tweets):
	'''
	Input: Need the output of topmine
	the transactions input should be a list of lists of phrases in tweets that were picked out from the top-mine algorithm.
	'''
	return


def jaccard_coefficient_mod(frequent_items, patterns, confidence_threshold):
	"""
	modified pattern rules from pyfpgrowth
	
	Given a set of frequent itemsets, return a dict
	of association rules in the form
	{(left): ((right), confidence)}
	"""
	rules = {}
	for itemset in patterns.keys():
		p1_and_p2 = patterns[itemset] #frequency of phrase 1 AND phrase 2

		#i'm not sure why this is so complicated
		for i in range(1, len(itemset)):
			for antecedent in itertools.combinations(itemset, i):
				antecedent = tuple(sorted(antecedent))
				consequent = tuple(sorted(set(itemset) - set(antecedent)))

				if antecedent in patterns:
					consequent = consequent[0]
					p2 = frequent_items[consequent]
					p1 = patterns[antecedent] #frequency of phrase 1
					jaccard = float(p1_and_p2) / (p1 + p2)
					rules[itemset] = jaccard

	return rules

def jaccard_coefficient_old(frequent_items, patterns, confidence_threshold):
	"""
	Credit to pyfpgrowth
	
	Given a set of frequent itemsets, return a dict
	of association rules in the form
	{(left): ((right), confidence)}
	"""
	jaccards = {}
	for itemset in patterns.keys():
		if len(itemset) > 2:
			for antecedent in itertools.combinations(itemset, 2):
				p1_and_p2 = patterns[antecedent]
				p1 = frequent_items[antecedent[0]]
				p2 = frequent_items[antecedent[1]]
		elif len(itemset) == 2:
			p1_and_p2 = patterns[itemset]
			p1 = frequent_items[itemset[0]]
			p2 = frequent_items[itemset[1]]
		else:
			continue
		jaccard = float(p1_and_p2) / (p1 + p2)
		jaccards[itemset] = jaccard

	return jaccards

def jaccard_coefficients(patterns, phrase_file):
	counts = phrase_weights.parse_topmine_counts(phrase_file)
	jaccards = {}
	for itemset in patterns.keys():
		if len(itemset) > 2:
			for antecedent in itertools.combinations(itemset, 2):
				if antecedent in patterns:
					p1_and_p2 = patterns[antecedent]
					p1 = counts[antecedent[0]]
					p2 = counts[antecedent[1]]
					jaccard = float(p1_and_p2) / (p1 + p2)
					jaccards[antecedent] = jaccard

		elif len(itemset) == 2:
			p1_and_p2 = patterns[itemset]
			p1 = counts[itemset[0]]
			p2 = counts[itemset[1]]
			jaccard = float(p1_and_p2) / (p1 + p2)
			jaccards[itemset] = jaccard
		else:
			continue
	return jaccards


def convert_code_to_tweet(tweet, key_to_word):
	tweet_phrases = tweet.split(",")
	real_phrases = []
	for phrase in tweet_phrases:
		real_phrase = []
		words = phrase.split()
		for word in words:
			real_phrase.append(key_to_word[int(word.strip())])
		real_phrases.append(' '.join(real_phrase))
	
	return real_phrases

def parse_topmine(tweet_file, vocab_file, phrase_file):
	'''
	returns the transaction object for the fp-growth algorithm
	'''

	#read in the vocab to a list
	with open(vocab_file) as f:
		lines = f.readlines()
		vocab = {word.strip():i for i, word in enumerate(lines)}
		key_to_word = {i:word.strip() for i, word in enumerate(lines)}
	#read in the tweet_file to a list and convert to words so everything is easier
	with open(tweet_file) as f:
		codes = f.readlines()
	tweets = []
	for code in codes:
		tweets.append(convert_code_to_tweet(code, key_to_word))
	#read in the phrases to a list
	with open(phrase_file) as f:
		frequent_phrases = {item.split("'")[1]:1 for item in f.readlines()}
	#first, find the phrases in the vocab. what number are they?
	#make a dictionary of the number sequences of phrases


	#iterate over all tweets, saving the ones where at least one of the phrase sequences appear.
	
	saved_tweets = []
	for tweet in tweets:
		tweet_phrases = []
		for phrase in tweet:
			if phrase in frequent_phrases:
				tweet_phrases.append(phrase)
		tweet_phrases = list(OrderedDict.fromkeys(tweet_phrases)) 
		if len(tweet_phrases) > 1:
			saved_tweets.append(tweet_phrases)
	return saved_tweets, vocab, key_to_word

def parse_topmine_2(tweet_file, vocab_file, phrase_file):
	'''
	returns the transaction object for the fp-growth algorithm
	'''
	#read in the tweet_file to a list
	with open(tweet_file) as f:
		tweets = f.readlines()
	#read in the vocab to a list
	with open(vocab_file) as f:
		lines = f.readlines()
		vocab = {word.strip():i for i, word in enumerate(lines)}
		key_to_word = {i:word.strip() for i, word in enumerate(lines)}
	#read in the phrases to a list
	with open(phrase_file) as f:
		phrases = f.readlines()
	#first, find the phrases in the vocab. what number are they?
		#make a dictionary of the number sequences of phrases
	phrase_code_seqs = [] #sequences of phrases in terms of numbers
	for item in phrases:
		phrase_words = item.split("'")[1].split()
		phrase_codes = []
		for w in phrase_words:
			phrase_codes.append(str(vocab[w]))

		#adding the sequence with a comma, and a newline, so we don't misattribute phrase subsets as co-occurring (e.g., "i love you" and "i love")
		phrase_code_seqs.append(' '.join(phrase_codes)) 
		# phrase_code_seqs.append(' '.join(phrase_codes) + ',') 
		# phrase_code_seqs.append(' '.join(phrase_codes) + '\n')
	#iterate over all tweets, saving the ones where at least one of the phrase sequences appear.
	saved_tweets = []
	for tweet in tweets:
		tweet_phrases = []
		for phrase in phrase_code_seqs:
			if phrase in tweet:
				tweet_phrases.append(phrase)
		tweet_phrases = list(OrderedDict.fromkeys(tweet_phrases)) 
		if len(tweet_phrases) > 0:
			saved_tweets.append(tweet_phrases)

	return saved_tweets, vocab, key_to_word

def get_set_words(codes, key_to_word):
	'''
	returns the words from a set a phrases
	'''
	word_set = []
	for item in codes:
		words = []
		for code in item.split():
			word = key_to_word[int(code)]
			words.append(word)
		word_set.append(' '.join(words))

	return word_set

def find_frequent_patterns(transactions, support_threshold):
	"""
	Given a set of transactions, find the patterns in it
	over the specified support threshold.
	"""
	tree = FPTree(transactions, support_threshold, None, None)
	frequent_items = tree.frequent
	return tree.mine_patterns(support_threshold), frequent_items

def main():
	'''
	prints number of graph edges.
	'''
	data_location = sys.argv[1]
	# folder = data_location.split('/')[-1] + '/'
	folder = data_location.split('/')[-2] + '/'
	minsupport = int(sys.argv[2])
	if len(sys.argv) > 3:
		author = sys.argv[3]
	phrase_folder="topmine-master/{}output/".format(folder) #this should be the output file of topmine
	intermediate_folder="topmine-master/{}intermediate_output/".format(folder)
	graph_folder="graphs/{}".format(folder)
	os.makedirs(graph_folder, exist_ok=True)
	

	phrase_files = sorted(glob.glob(phrase_folder + "*.txt")) #files separated by date time they were collected
	intermediate_files = {filename.split('.')[0]:intermediate_folder+filename.split('.')[0] for filename in os.listdir(intermediate_folder) if "txt" in filename} #beginning of file name as key, full filename as value

	edges = 0

	for phrase_file in tqdm(phrase_files):
		phrase_file=phrase_file
		tweet_file=intermediate_files[phrase_file.split('/')[-1].split('.')[0]] + ".partitioneddocs.txt"
		vocab_file=intermediate_files[phrase_file.split('/')[-1].split('.')[0]] + ".vocab.txt"
		transcation_object, vocab, key_to_word = parse_topmine(tweet_file, vocab_file, phrase_file)

		#second parameter is minimum support. Minimum support threshold define in paper is 8. 

		patterns, frequent_items = find_frequent_patterns(transcation_object, minsupport)
		rules = jaccard_coefficients(patterns, phrase_file)



		if len(rules) > 0:
			edges += len(rules)
		with open(graph_folder + phrase_file.split('/')[-1].split('.')[0], 'w+') as graph:
			for phrase_set in rules:
				graph.write("{}\t{}\t{}\r\n".format(phrase_set[0], phrase_set[1], rules[phrase_set]))
	
	print(edges)
	return

if __name__ == "__main__":
	main()
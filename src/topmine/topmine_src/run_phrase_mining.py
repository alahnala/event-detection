import phrase_mining
import og_phrase_mining
import sys
import utils
from utilities import cprint
import cProfile
import re

arguments = sys.argv
# cprint('Running Phrase Mining...', logname="topmine")

file_name = arguments[1]

# length of the maximum phrase size
phrase_size = int(arguments[2])
max_phrase_size=phrase_size

# represents the minimum number of occurences you want each phrase to have.
min_support = int(arguments[3])
folder = arguments[4]

# represents the threshold for merging two words into a phrase. A lower value
# alpha leads to higher recall and lower precision,
alpha = float(arguments[5])

stop_word_files = ["src/topmine/topmine_src/stopwords/allie.txt", "src/topmine/topmine_src/stopwords/tm_stopwords.txt", "src/topmine/topmine_src/stopwords/nltk_sw.txt"]
if len(arguments) > 6:
	stopwords_file=stop_word_files[int(arguments[6])]
	phrase_miner = og_phrase_mining.PhraseMining(file_name, min_support, max_phrase_size, alpha, stopwords_file)
else:
	phrase_miner = og_phrase_mining.PhraseMining(file_name, min_support, max_phrase_size, alpha);
# phrase_miner = og_phrase_mining.PhraseMining(file_name, min_support, max_phrase_size, alpha);
partitioned_docs, index_vocab = phrase_miner.mine()
# print(partitioned_docs)
frequent_phrases = phrase_miner.get_frequent_phrases(min_support)
# print(frequent_phrases)
utils.store_partitioned_docs(partitioned_docs, path="src/topmine/{}/intermediate_output/{}.partitioneddocs.txt".format(folder, file_name.split('/')[-1]))
utils.store_vocab(index_vocab, path="src/topmine/{}/intermediate_output/{}.vocab.txt".format(folder, file_name.split('/')[-1]))
utils.store_frequent_phrases(frequent_phrases, path='src/topmine/{}/output/{}.frequent_phrases.txt'.format(folder, file_name.split('/')[-1]))

print(len(frequent_phrases))
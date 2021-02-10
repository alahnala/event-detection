import phrase_lda
import sys
import utils
from utilities import cprint

arguments = sys.argv

num_topics = int(arguments[1])
file_name = arguments[2]
folder = arguments[3]
iteration = 1100
optimization_burnin = 100
alpha = 4
optimization_iterations = 50
beta = 0.01

cprint('Running PhraseLDA...', logname="topmine")

#TODO: update the path where these are stored so that it is written to a file for a particular file
partitioned_docs = utils.load_partitioned_docs(path="topmine-master/{}/intermediate_output/{}.partitioneddocs.txt".format(folder, file_name.split('/')[-1]))
#TODO: update the path where these are stored so that it is written to a file for a particular file
vocab_file = utils.load_vocab(path="topmine-master/{}/intermediate_output/{}.vocab.txt".format(folder, file_name.split('/')[-1]))

plda = phrase_lda.PhraseLDA( partitioned_docs, vocab_file, num_topics , alpha, beta, iteration, optimization_iterations, optimization_burnin);

document_phrase_topics, most_frequent_topics = plda.run()
#TODO: update the path where these are stored so that it is written to a file for a particular file
utils.store_phrase_topics(document_phrase_topics, path="topmine-master/{}/intermediate_output/{}.phrase_topics.txt".format(folder, file_name.split('/')[-1]))
utils.store_most_frequent_topics(most_frequent_topics, prefix_path="topmine-master/{}/output/{}.topic".format(folder, file_name.split('/')[-1]))
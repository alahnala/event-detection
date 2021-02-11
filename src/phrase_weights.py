from collections import defaultdict



def s_weights(t1, t2, input="counts"):
	'''
	"input" indicates if you pass in a file or you already did the counts
	if input == file: t1 and t2 should be file paths to the topmine file output for the timestep
	elif input == counts: t1 and t2 should be phrase count dictionaries
	Computes phrase weights in the space of s, the space of all phrases across t1 and t2
	'''
	if input == "file":
		#get phrase counts for both time step
		ctr1 = parse_topmine_counts(t1)
		ctr2 = parse_topmine_counts(t2)

		#merge ctr1 and ctr2
		sCtr = defaultdict(lambda:0)
		for c in ctr1:
			sCtr[c] += ctr1[c]
		for c in ctr2:
			sCtr[c] += ctr2[c]
		s_phrase_weights = weight_phrases(sCtr)
	elif input == "counts":
		#merge t1 and t2
		sCtr = defaultdict(lambda:0)
		for c in t1:
			sCtr[c] += t1[c]
		for c in t2:
			sCtr[c] += t2[c]
		s_phrase_weights = weight_phrases(sCtr)
	return s_phrase_weights


def parse_topmine_counts(phrase_file):
		#read in the phrases to a list
	phrase_count = defaultdict(lambda:0)
	with open(phrase_file) as f:
		phrases = f.readlines()
	# print(phrases)
	for item in phrases:
		phrase = item.split("'")[1]
		count = float(item.split()[-1][:-1]) #last item, but remove parathesis
		phrase_count[phrase] = count
	return phrase_count

def weight_phrases(phrase_count):
	'''
	Input: dictionary of phrases and their count
	'''
	phrase_weights = {}
	denominator = sum(phrase_count.values())
	for phrase in phrase_count:
		weight = phrase_count[phrase] / denominator
		phrase_weights[phrase] = weight
	return phrase_weights

def get_phrase_weights(phrase_file):
	phrase_counts = parse_topmine_counts(phrase_file)
	phrase_weights = weight_phrases(phrase_counts)
	return phrase_weights

def main():
	folder = sys.argv[1]
	phrase_folder="topmine/{}output/".format(folder) #this should be the output file of topmine
	phrase_weight_folder ="phrase_weights/{}".format(folder)
	phrase_files = glob.glob(phrase_folder + "*.txt") #files separated by date time they were collected
	#beginning of file name as key, full filename as value

	for phrase_file in phrase_files:
		phrase_weights = get_phrase_weights(phrase_counts)


if __name__ == "__main__":
	main()
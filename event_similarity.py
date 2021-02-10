import phrase_clustering
import sys
import phrase_weights
from collections import defaultdict
from termcolor import colored
from utilities import cprint
'''

Big P is set of phrases. Each phrase p_m has a weight w_m associated with it that will be normalized by the total number of phrases in the time interval t, denoted as n in the equation below.

F(p_m) = frequency of phase p_m.
w_m = F(p_m) / sum([F(p_i) for i in range(1, n)])
	similarity = max(sum([w_s for  p_s in intersection(P_{i, t}, P_{i,t+1}) w_s]) / sum([w_r for  p_r in intersection(P_{i, t}, P_{i,t+1}) w_s]), sum([w_s for  p_s in intersection(P_{i, t}, P_{i,t+1}) w_s]) / sum([w_j for  p_j in intersection(P_{i, t}, P_{i,t+1}) w_s]))
'''

def intersecting_phrases(t1_event, t2_event):
	'''
	Event candidates have a set of phrases.
	'''
	
	return set(t1_event).intersection(set(t2_event))



def similarities(t1, t2):

	# get phrase weights for the phrases at each time step
	phrase_file1 = "topmine-master/"+t1.split('/')[-2] +'/output/'+ t1.split('/')[-1] + ".frequent_phrases.txt"
	t1_phrase_weights = phrase_weights.get_phrase_weights(phrase_file1)
	phrase_file2 = "topmine-master/"+t2.split('/')[-2] +'/output/'+ t2.split('/')[-1] + ".frequent_phrases.txt"
	t2_phrase_weights = phrase_weights.get_phrase_weights(phrase_file2)

	# get intersection weights
	s_phrase_weights = phrase_weights.s_weights(phrase_file1, phrase_file2)

	# get event candidates
	t1_candidates = event_candidates.get_event_candidates(t1)
	t2_candidates = event_candidates.get_event_candidates(t2)


	merge = []
	# check event similarities for all event candidates of t1 and t2
	for t1_event in t1_candidates:
		for t2_event in t2_candidates:
			inter_phrases = intersecting_phrases(t1_candidates[t1_event], t2_candidates[t2_event])
			# if the event candidates have an intersection of phrases
			if inter_phrases:
				# Calculate the similarity of the events
				numerator = sum([s_phrase_weights[phrase] for phrase in inter_phrases])
				left_denom = sum([t1_phrase_weights[phrase] for phrase in t1_candidates[t1_event]])
				right_denom = sum([t2_phrase_weights[phrase] for phrase in t2_candidates[t2_event]])
				sim = max(numerator/left_denom, numerator/right_denom)
				if sim > 0.5:
					#this is the threshold set in the paper indicating that we should merge these events.
					# not sure what I'm supposed to do in this case, so I'll just put in s_phrase_weights[phrase] in timestep t?
					# Later, we will remove t1_event from t1_candidates, t2_event from t2_candidates, and use the numerator as the phrase weight, and keep the inter_phrase. I could also try union?
					merge.append((t1_event, t2_event, inter_phrases)) 
					print("add to merge", (t1_event, t2_event, inter_phrases))
	final_t1_candidates = {} #maps an event to candidate event phrase clusters and a list of the phrase weights for the associated phrase cluster
	final_t2_candidates = {} 
	# first remove the similar events and add the intersection to the t1_final candidates
	for item in merge:
		del t1_candidates[item[0]]
		del t2_candidates[item[1]]
		final_t1_candidates[item[0]] = (item[2], [s_phrase_weights[phrase] for phrase in item[2]])
	for e in t1_candidates:
		final_t1_candidates[e] = (t1_candidates[e], [t1_phrase_weights[phrase] for phrase in t1_candidates[e]])
	for e in t2_candidates:
		final_t2_candidates[e] = (t2_candidates[e], [t2_phrase_weights[phrase] for phrase in t2_candidates[e]])
				
	return final_t1_candidates, final_t2_candidates

def merge_events(t1_items, t2_items, s_phrase_weights):
	'''
	input:
	t1_items = (t1_phrase_weights, t1_candidates)
	t2_items = (t2_phrase_weights, t2_candidates)
	s_phrase_weights = the phrase weights in the space of t1 and t2

	returns:
	final_t1_candidates[e] = {phrase:, [t1_phrase_weights[phrase] for phrase in t1_candidates[e]]}
	final_t2_candidates[e] = (t2_candidates[e], [t2_phrase_weights[phrase] for phrase in t2_candidates[e]])
	'''
	t1_phrase_weights, t1_candidates = t1_items
	t2_phrase_weights, t2_candidates = t2_items

	merge = []
	# check event similarities for all event candidates of t1 and t2
	for t1_event in t1_candidates:
		for t2_event in t2_candidates:
			inter_phrases = intersecting_phrases(t1_candidates[t1_event], t2_candidates[t2_event])

			# if the event candidates have an intersection of phrases
			if inter_phrases:
				
				# Calculate the similarity of the events
				numerator = sum([s_phrase_weights[phrase] for phrase in inter_phrases])
				try:
					left_denom = sum([t1_phrase_weights[phrase] for phrase in t1_candidates[t1_event]])
				except:
					print("error")
					# print(t1_phrase_weights)
				right_denom = sum([t2_phrase_weights[phrase] for phrase in t2_candidates[t2_event]])
				sim = max(numerator/left_denom, numerator/right_denom)
				cprint("inter_phrases: {}; similarity: {}".format(inter_phrases, sim), logname="interphrases", p2c=False)
				if sim > 0.5:
					#this is the threshold set in the paper indicating that we should merge these events.
						# not sure what I'm supposed to do in this case, so I'll just put in s_phrase_weights[phrase] in timestep t?
					# Later, we will remove t1_event from t1_candidates, t2_event from t2_candidates, and use the numerator as the phrase weight, and keep the inter_phrase. I could also try union?
					merge.append((t1_event, t2_event, inter_phrases)) 

	final_t1_candidates = {} #maps an event to candidate event phrase clusters and a list of the phrase weights for the associated phrase cluster
	final_t2_candidates = {} 
	# first remove the similar events and add the intersection to the t1_final candidates
	for item in merge:

		if item[0] in t1_candidates: #because it could have been deleted earlier in this for loop
			del t1_candidates[item[0]]
		if item[1] in t2_candidates:
			del t2_candidates[item[1]]
		final_t1_candidates[item[0]] = {}
		for phrase in item[2]:
			final_t1_candidates[item[0]][phrase] = s_phrase_weights[phrase]
	for e in t1_candidates:
		final_t1_candidates[e] = {}
		for phrase in t1_candidates[e]:
			final_t1_candidates[e][phrase] = t1_phrase_weights[phrase]

	for e in t2_candidates:
		final_t2_candidates[e] = {}
		for phrase in t2_candidates[e]:
			final_t2_candidates[e][phrase] = t2_phrase_weights[phrase]	

	return final_t1_candidates, final_t2_candidates


def main():
	t1 = sys.argv[1] #for now just try between two test time steps
	t2 = sys.argv[2]
	t1_candidates, t2_candidates = similarities(t1, t2)





if __name__ == "__main__":
	main()
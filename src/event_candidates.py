import phrase_weights
import phrase_clustering
import event_similarity
import sys
import glob
import pickle
import os
from pprint import pprint
from tqdm import tqdm

def weighted_cluster_frequency():
	return

def candidate_weights(candidates, weights):
	'''
	returns a candidate map
	'''
	candidate_map = {}
	for e in candidates:
		candidate_map[e] = {}
		for phrase in candidates[e]:
			candidate_map[e][phrase] = weights[phrase]

	return candidate_map

def main():
	folder = sys.argv[1] #tweetFolder
	phrase_folder = "src/topmine/"+folder +'output/'
	graph_folder = "src/graphs/"+folder
	os.makedirs("src/event_candidates/" + folder, exist_ok=True)
	phrase_files = sorted(glob.glob(phrase_folder + "*frequent_phrases.txt")) #files separated by date time they were collected
	graph_files = sorted(glob.glob(graph_folder + "*")) #files separated by date time they were collected

	#not all tweet files has a graph file.
	# datetime_to_timestep = {}
	timestep_to_datetime = {}
	timestep_to_phrase_file = {}
	for t, f in enumerate(phrase_files):
		timestep = t
		datetime = f.split('/')[-1][:19] #get datetime
		timestep_to_datetime[timestep] = datetime
		timestep_to_phrase_file[timestep] = f
	timesteps = {}

	# at the end of this for loop, we have the finalized event candidates after merging events.
	for t in tqdm(range(0, len(timestep_to_datetime))):
		if t+1 == len(timestep_to_datetime):
			# print("quitting", t+1, len(timestep_to_datetime))
			#because I can't do len() - 1 bc we need to make sure we read the last timestep if it was not read as a t+1 case
			break
		datetime = timestep_to_datetime[t]
		if t in timesteps:
			# print("if t in timesteps:")
			#this is the case where we already added i+1 when we merged events
			t1_weights = t2_weights
			t1_phrases = t2_phrases
			t1_candidates = final_t2_candidates
		elif graph_folder + datetime in graph_files:
			# print("elif graph_folder + datetime in graph_files:")
		# get the phrase weights and original event candidates for t1
			t1_weights = phrase_weights.get_phrase_weights(timestep_to_phrase_file[t])
			t1_phrases = phrase_clustering.get_event_candidates(graph_folder + datetime)
			t1_candidates = candidate_weights(t1_phrases, t1_weights)
		else:
			# print("else 1:")
			continue
		next_time = timestep_to_datetime[t+1]
		if graph_folder + next_time in graph_files:
			# print("if graph_folder + next_time in graph_files:")
			# get the phrase weights and original event candidates for t2
			t2_weights = phrase_weights.get_phrase_weights(timestep_to_phrase_file[t+1])
			t2_phrases = phrase_clustering.get_event_candidates(graph_folder + next_time)

			t2_candidates = candidate_weights(t2_phrases, t2_weights)
			# get the phrase weights in the space of t and t+1
			s_phrase_weights = phrase_weights.s_weights(timestep_to_phrase_file[t], timestep_to_phrase_file[t+1], input="file")

			final_t1_candidates, final_t2_candidates = event_similarity.merge_events((t1_weights, t1_phrases), (t2_weights, t2_phrases), s_phrase_weights)
			timesteps[t] = final_t1_candidates
			timesteps[t+1] = final_t2_candidates
		else:
			# print("else 2:")
			timesteps[t] = candidate_weights(t1_phrases, t1_weights)
	
	for t2 in range(len(phrase_files)):
		if t2 not in timesteps:
			timesteps[t2] = {}
	
	clusters = []
	cluster_candidates = 0
	for t in timesteps:

		cluster_candidates += len(timesteps[t])
		for ec in timesteps[t]:
			clusters.append(sorted(timesteps[t][ec].keys()))

	pickle_out = open("src/event_candidates/" + folder + "timesteps.pickle","wb")
	pickle.dump(timesteps, pickle_out)
	pickle_out.close()
	pickle_out = open("src/event_candidates/" + folder + "timestep_to_datetime.pickle","wb")
	pickle.dump(timestep_to_datetime, pickle_out)
	pickle_out.close()

	print(cluster_candidates)
	return


if __name__ == "__main__":
	main()
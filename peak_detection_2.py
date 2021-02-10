import sliding_window
import sys
import pickle
import operator
from pprint import pprint
import latex_table
from scipy import stats
import numpy as np
from collections import defaultdict
from tqdm import tqdm
from copy import deepcopy
import calendar
from termcolor import colored
from utilities import cprint


def phrase_cluster_z_score(phrase_weights, t, theta, timesteps, T, dampening_weight=0.1):
	'''
	input: t = current timestep
	'''
	cluster_weight = sum([phrase_weights[phrase] for phrase in phrase_weights])
	sliding_window_mean = sliding_window.sliding_window_mean_weighted_damp(phrase_weights, timesteps, T, t, dampening_weight)
	# print("sliding_window_mean", sliding_window_mean)
	sliding_window_std = sliding_window.sliding_window_std(phrase_weights, timesteps, T, t, sliding_window_mean, dampening_weight)
	# print("Calculatation: (cluster_weight - sliding_window_mean) / sliding_window_std\n ({} - {})/{}".format(cluster_weight, sliding_window_mean, sliding_window_std))

	#This is the z-score
	z_score = (cluster_weight - sliding_window_mean) / sliding_window_std
	return round(z_score, 2), round(cluster_weight, 2), round(sliding_window_mean, 2), round(sliding_window_std, 2)

def compute_z_score(cluster_weight, sliding_window_mean, sliding_window_std, dampening_weight=0.1):
	'''
	T = sliding window size.
	input: t = current timestep
	'''
	#note that the inner sum is complete. The list being passed in is the list of inner numbers for each timestep t.

	#for z-score dampened, we go over each value
	z_score_dampened = 0

	#This is the z-score
	z_score = (cluster_weight - sliding_window_mean) / sliding_window_std
	if cluster_weight > 0:
		cprint(colored("{} = ({} - {}) / {}".format(z_score, cluster_weight, sliding_window_mean, sliding_window_std), color="magenta"), logname="z-scores", p2c=False)
	return z_score

def sliding_window(phrase_distribution, T, total_timesteps):
	'''
	T = sliding window size.
	phrase_distribution is a list of phrase weights for a particular phrase at each timestep
	simple z-score
	'''
	sliding_windows = []
	i = 0
	while i <= len(phrase_distribution) - T:
		sw_mean = np.mean(phrase_distribution[i:i+T])
		sw_std = np.std(phrase_distribution[i:i+T])
		z_scores = [compute_z_score(cw, sw_mean, sw_std) for cw in phrase_distribution[i:i+T]]
		sliding_windows.append(z_scores)
		i += T
	return sliding_windows



def print_z_score_table(event_candidates, n, reverse=True):
	'''
	prints top n event candidates by z-score
	'''
	top_list = sorted(event_candidates, key=operator.itemgetter(0), reverse=reverse)[:n]

	# #find what the max number of phrases is for this list
	# pkl_max = max([len(l[1]) for l in sorted(top_list)])
	# print(pkl_max)

	#print latex table for the event candidates
	top_n_list = [] 
	for value, phrase_keys in top_list:
		l = list(phrase_keys)
		top_n_list.append([value] + [', '.join(l)])
	header = ["z_score", "event phrases"]
	latex_table.print_latex_table(top_n_list, header=header, alignment="rl")

def print_z_score_calculation_table(calc_info, n, reverse=True):
	'''
	prints top n event candidates by z-score
	'''
	top_list = sorted(calc_info, key=operator.itemgetter(1), reverse=True)[:n]

	#print latex table for the event candidates
	header = ["event phrases", "z_score", "cluster_weight", "$\\mu_{T}$", "$\\sigma_{T}$"]
	latex_table.print_latex_table(top_list, header=header, alignment="lrrrr")

def determine_peaks(sliding_windows, threshold):

	peaks = [score > threshold for w in sliding_windows for score in w]
	return peaks

def filter_non_peaks(phrase_distribution, peaks):
	diff = len(phrase_distribution) - len(peaks)
	pad = [False for i in range(diff)]
	peaks += pad

	event_candidates = [weight  if peak else 0 for weight, peak in zip(phrase_distribution, peaks)]

	return event_candidates

def sort_by_num_peaks(phrase_clusters):
	'''
	(αi > αj where i 6= j)
	'''

	num_peaks = {p:sum(i > 0 for i in phrase_clusters[p]) for p in phrase_clusters}
	return sorted(num_peaks.items(), key=operator.itemgetter(1))


def sort_by_std_peak_height(phrase_clusters):
	'''
	 (βi < βj where i 6= j)
	'''
	stds = {p:np.std(np.array(phrase_clusters[p])) for p in phrase_clusters}
	return sorted(stds.items(), key=operator.itemgetter(1), reverse=True)

def sort_by_peak_intensity(phrase_clusters):
	'''
	intensity = height = cluster weight = normalized frequency 
	(χi < χj where i 6= j). The last feature (χ) is used to merely sort
	between the most popular phrase groups to aid in identifying the most urgent
	events.
	'''
	intensities = {p:max(phrase_clusters[p]) for p in phrase_clusters}
	return sorted(intensities.items(), key=operator.itemgetter(1), reverse=True)

def sort_by_peak_z_score(phrase_clusters):
	'''
	intensity = height = cluster weight = normalized frequency 
	(χi < χj where i 6= j). The last feature (χ) is used to merely sort
	between the most popular phrase groups to aid in identifying the most urgent
	events.
	'''
	intensities = {p:max(phrase_clusters[p]) for p in phrase_clusters}
	return sorted(intensities.items(), key=operator.itemgetter(1), reverse=True)
	 
def determine_events(phrase_clusters, parameters):
	'''
	sorted_lists = (sorted_by_peaks, sorted_by_std, sorted_by_intensity) 
	parameters = (alpha=10, beta=0.05, chi=0.5)
	'''
	clusters = {key:None for key in phrase_clusters}
	# for p in phrase_clusters:
	# 	print(p)

	intensities = {p:max(phrase_clusters[p]) for p in phrase_clusters}
	intensity_timesteps = {p:phrase_clusters[p].index(max(phrase_clusters[p])) for p in phrase_clusters}
	num_peaks = {p:sum(i > 0 for i in phrase_clusters[p]) for p in phrase_clusters}
	num_peaks = {p:sum(i > 0 for i in phrase_clusters[p]) for p in phrase_clusters}
	stds = {p:np.std(np.array(phrase_clusters[p])) for p in phrase_clusters}

	sorted_by_peaks = sorted(num_peaks.items(), key=operator.itemgetter(1))
	sorted_by_std = sorted(stds.items(), key=operator.itemgetter(1), reverse=True) 
	sorted_by_intensity = sorted(intensities.items(), key=operator.itemgetter(1), reverse=True)
	alpha, beta, chi = parameters

	final_events = {}
	fails = {}
	# least number of peaks
	for phrase, phrase_peaks in sorted_by_peaks:
		if alpha <= phrase_peaks: #this is a max threshold
			# final_events[phrase] = clusters[phrase]
			fails[phrase] = 1
		# if alpha > phrase_peaks:
		# 	if phrase in clusters:
		# 		del clusters[phrase]
		# 	break
	for phrase, std in sorted_by_std:
		if beta >= std: #this is a min threshold
			fails[phrase] = 1
			# final_events[phrase] = clusters[phrase]
			# if phrase in clusters:
			# 	del clusters[phrase]
			# break
	for phrase, intensity in sorted_by_intensity:
		if chi >= intensity: # this is a min threshold
			# final_events[phrase] = clusters[phrase]
			fails[phrase] = 1
			# if phrase in clusters:
			# 	del clusters[phrase]
			# break

	for phrase in clusters:
		# print(phrase)
		if phrase not in fails:
			final_events[phrase] = {"alpha":num_peaks[phrase],"beta":stds[phrase],"chi":intensities[phrase],"timestep":intensity_timesteps[phrase]}

	return final_events

def graph_n_best(timestep_measure_event, n, headers):
	data = []
	# just so I save all the results:
	# n = len(toplist)
	if n > len(toplist):
		n=len(toplist)
	for t,e,v in toplist[:n]:
		data.append([timestep_to_datetime[event], str(round(val, 2)),str(event)])
	if len(data) > 0:
		latex_table.print_latex_table(data, header=headers, alignment="llr")
	return

def full_analysis(clusters, timestep_to_datetime, n):
	'''
	clusters[phrase] = {"alpha":num_peaks[phrase],"beta":stds[phrase],"chi":intensities[phrase]}
	'''
	if n > len(clusters):
		n=len(clusters)
	# #graph by smallest number of peaks
	# alphas = {event:clusters[event]["alpha"] for event in clusters}
	# sorted_alphas = sorted(alphas.items(), key=operator.itemgetter(1))
	# timestep_measure_event = []
	# for e,v in sorted_alphas[:n]:
	# 	timestep_measure_event.append([timestep_to_datetime[clusters[e]["timestep"]], "{}".format(v), "{:.3f}".format(clusters[e]["beta"]), "{:.3f}".format(clusters[e]["chi"]), e]) 
	
	# latex_table.print_latex_table(data=timestep_measure_event, header=["timestep", "$\\alpha$","$\\beta$", "$\chi$", "event"], alignment="llllp{12.0cm}", caption="$\\alpha$, the number of peak heights", color="green")

	# betas = {event:clusters[event]["beta"] for event in clusters}
	# sorted_betas = sorted(betas.items(), key=operator.itemgetter(1), reverse=True)
	# timestep_measure_event = []
	# for e,v in sorted_betas[:n]:
	# 	timestep_measure_event.append([timestep_to_datetime[clusters[e]["timestep"]], "{:.3f}".format(v),"{:.3f}".format(clusters[e]["chi"]),"{:.3f}".format(clusters[e]["alpha"]), e]) 
	# latex_table.print_latex_table(data=timestep_measure_event, header=["timestep", "$\\beta$","$\chi$","$\\alpha$", "event"], alignment="llllp{12.0cm}", caption="$\\beta$, the std of peak heights", color="green")

	chis = {event:clusters[event]["chi"] for event in clusters}
	sorted_chis = sorted(chis.items(), key=operator.itemgetter(1), reverse=True)
	timestep_measure_event = []
	for e,v in sorted_chis[:n]:
		timestep_measure_event.append([timestep_to_datetime[clusters[e]["timestep"]], "{:.3f}".format(v),"{:.3f}".format(clusters[e]["alpha"]),"{:.3f}".format(clusters[e]["beta"]), e]) 
	latex_table.print_latex_table(data=timestep_measure_event, header=["timestep", "$\chi$","$\\alpha$","$\\beta$", "event"], alignment="llllp{12.0cm}", caption="$\chi$, highest peak intensity", color="green")

	return


def convert_timestamp_nice(timestamp):
	# 2015_02_23-00_00_01
	year = timestamp[0:4]
	m = timestamp[5:7]
	day = timestamp[8:10]
	month = calendar.month_abbr[int(m)]
	return "{} {}, {}".format(month, day, year)


def main():
	'''
	the event key feature thresholds are the following α = 10, β = .05, and χ = .5.
	'''
	#${tweetFolder} ${slidingWindowTimesteps} ${dampeningCoefficient} ${Theta} ${StartingTimeStep}

	folder = sys.argv[1]
	# okay so we have the timesteps. let's do the peak detection.
	T = int(sys.argv[2]) # amount of timesteps in the sliding window per the paper from midnight to midnight
	dampening_coefficient = sys.argv[3]
	theta = float(sys.argv[4]) # standard deviations above sliding window mean
	starting_timestep = int(sys.argv[5])
	alpha = float(sys.argv[6])
	beta = float(sys.argv[7])
	chi = float(sys.argv[8])

	#load the event candidates
	pickle_in = open("event_candidates/" + folder + "timesteps.pickle","rb")
	timesteps = pickle.load(pickle_in)
	pickle_in.close()
	pickle_in = open("event_candidates/" + folder + "timestep_to_datetime.pickle","rb")
	ob = pickle.load(pickle_in)
	timestep_to_datetime = {}
	for time in ob:
		timestep_to_datetime[time] = convert_timestamp_nice(ob[time]) 
	pickle_in.close()

	# print(timesteps)

	# for each timestep, we want to calculate the peak equations for each phrase cluster
	'''
	Timesteps example: 
	{0: {0: {'happy intldatacenterday': 0.0024154589371980675,
         'user vertiv recognize day': 0.0024154589371980675},
     	1: {'9 wind speed 0': 0.0024154589371980675,
         'direction ssw rain midnight': 0.0024154589371980675,
         'wthd weather 08 00': 0.0024154589371980675},
	'''
	#now we update the event candidates by requiring them to meet a threshold for z-score.
	timestep_clusters = {} #maps timestep t to all the phrase clusters appear in that timestep. Just the text, each phrase in the cluster separated by a comma, mapping to the sum of the phrase weights.
	all_phrase_clusters = {} #just a dictionary of all the phrase clusters
	for t in range(starting_timestep, len(timesteps)):
		timestep_clusters[t] = {}
		for ec in timesteps[t]:
			cluster_phrases = list(timesteps[t][ec].keys())
			cluster_phrases = sorted(cluster_phrases) #sort alphabetically
			cluster_phrases = ', '.join(cluster_phrases)
			cluster_weight = sum(timesteps[t][ec].values())
			timestep_clusters[t][cluster_phrases] = cluster_weight
			all_phrase_clusters[cluster_phrases] = 1

	phrase_cluster_distributions = defaultdict(lambda:[])
	filtered_distributions = defaultdict(lambda:[])
	for phrase_cluster in tqdm(all_phrase_clusters):
		cprint(phrase_cluster, logname="z-scores", p2c=False)
		for t in timestep_clusters: 
			if phrase_cluster in timestep_clusters[t]:
				phrase_cluster_distributions[phrase_cluster].append(timestep_clusters[t][phrase_cluster])
			else:
				phrase_cluster_distributions[phrase_cluster].append(0)
		#then do the sliding window stuff here.
		sliding_window_list = sliding_window(phrase_cluster_distributions[phrase_cluster], T, len(timesteps))
		
		# O(|number of timesteps|)
		peaks = determine_peaks(sliding_window_list, theta)
		
		filtered = filter_non_peaks(phrase_cluster_distributions[phrase_cluster], peaks)
		if any(val > 0 for val in filtered):
			filtered_distributions[phrase_cluster] = filtered
		# Finally, to focus on event candidate peaks, all time steps where the phrase community did not show a peak, their phrase community frequency (weight) is lowered to zero, however, all peak identified time steps maintain the phrase community requency, Pkm=1 F(p(t)m ). This filtering is shown in Figure 1.

	events = determine_events(deepcopy(filtered_distributions), (alpha, beta, chi))
	# print(events)
	full_analysis(events, timestep_to_datetime, 520)
	pickle_in = open("event_candidates/" + folder + "final_events.pickle","wb")
	timesteps = pickle.dump(events, pickle_in)
	pickle_in.close()
	eliminated = set(all_phrase_clusters.keys()) - set(events.keys())
	# print("Eliminated", eliminated)
	pickle_in = open("event_candidates/" + folder + "eliminated.pickle","wb")
	timesteps = pickle.dump(eliminated, pickle_in)
	pickle_in.close()
	'''
	the event key feature thresholds are the following α = 10, β = .05, and χ = .5.
	'''
	'''
	prints the number of events
	'''
	print(len(events))
	return

if __name__ == "__main__":
	main()
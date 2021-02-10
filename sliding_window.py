import phrase_weights



def sliding_window_mean(T):
	'''
	t = curr timestep
	Sliding window W
	T total t timesteps
	u_W = (1/T)sum([sum([F(p_{(t), m}) for m=1 in k])  for t=1 in X])
	'''
	# for each phrase m at timestep t, add the frequency of the phrase
	# timesteps = dictionary {timesteps: event phrases: phrase counts}
	outer_sum = 0
	for t in T:
		inner_sum = sum([timesteps[t][phrase] for phrase in timesteps[t]])
		outer_sum += inner_sum
	mean = (1/T)*outer_sum

	return mean

def sliding_window_mean_weighted(T):
	'''
	t = curr timestep
	Sliding window W
	T total t timesteps
	u_W = (1/T)sum([sum([F(p_{(t), m}) for m=1 in k])  for t=1 in X])
	'''
	# for each phrase m at timestep t, add the frequency of the phrase
	# timesteps = dictionary {timesteps: event phrases: phrase counts}
	outer_sum = 0
	for t in T:
		inner_sum = sum([timesteps[t][phrase] for phrase in timesteps[t]])
		outer_sum += inner_sum
	mean = (1/T)*outer_sum

	return mean

def sliding_window_mean_weighted_damp(phrase_cluster, timesteps, T, t, dampening_weight=0.1):
	'''
	input: t = current timestep. T = sliding window size. timesteps = dictionary of events per timestep. dampening_weight = parameter
	t = curr timestep
	Sliding window W
	T total t timesteps
	u_W = (1/T)sum([sum([F(p_{(t), m}) for m=1 in k])  for t=1 in X])
	'''
	# for each phrase m at timestep t, add the frequency of the phrase
	# timesteps = dictionary {timesteps: event phrases: phrase counts}
	outer_sum = 0
	currenttimestep = t
	# print(len(timesteps[t]))
	# print("currenttimestep", currenttimestep)
	for t in range(currenttimestep, currenttimestep+T): #out sum
		# print("currenttimestep", t)
		if t == len(timesteps):
			#not sure what to do in the case that we don't have more timesteps
			break

		# it would be hard to read in a list comprehension
		# we need to add up the phrase weights at each timestep
		# the phrases are saved in timesteps by which cluster they are in, thats why we iterate for each ec in timesteps[t]
		inner_sum = 0
		for ec in timesteps[t]:
			for phrase in phrase_cluster:
				if phrase in timesteps[t][ec]:
					inner_sum += timesteps[t][ec][phrase]
			

		# # calculate the inner sum for each phrase in the timestep
		# inner_sum = sum([timesteps[t][phrase] if phrase in timesteps[t][ec] else 0 for ec in timesteps[t] for phrase in timesteps[t][ec]])
		outer_sum += dampening_weight * inner_sum
	mean = (1/T)*outer_sum

	return mean
def sliding_window_std(phrase_cluster, timesteps, T, t, sliding_window_mean, dampening_weight=0.1):
	'''
	input: t = current timestep. T = sliding window size. timesteps = dictionary of events per timestep. dampening_weight = parameter
	t = curr timestep
	Sliding window W
	T total t timesteps
	u_W = (1/T)sum([sum([F(p_{(t), m}) for m=1 in k])  for t=1 in X])
	'''
	# for each phrase m at timestep t, add the frequency of the phrase
	# timesteps = dictionary {timesteps: event phrases: phrase counts}
	outer_sum = 0
	currenttimestep = t
	for t in range(currenttimestep, currenttimestep+T): #out sum
		if t == len(timesteps):
			#not sure what to do in the case that we don't have more timesteps
			break

		# it would be hard to read in a list comprehension
		# we need to add up the phrase weights at each timestep
		# the phrases are saved in timesteps by which cluster they are in, thats why we iterate for each ec in timesteps[t]
		inner_sum = 0
		for ec in timesteps[t]:
			for phrase in phrase_cluster:
				if phrase in timesteps[t][ec]:
					current_step = timesteps[t][ec][phrase] - sliding_window_mean
					inner_sum += current_step

		# # calculate the inner sum for each phrase in the timestep
		# inner_sum = sum([timesteps[t][phrase] if phrase in timesteps[t][ec] else 0 for ec in timesteps[t] for phrase in timesteps[t][ec]])
		outer_sum += inner_sum*inner_sum
	std = (1/T)*outer_sum
	return std

def sliding_window_standard_deviation(timesteps, T):
	outer_sum = 0
	for t in T:
		inner_sum = sum([timesteps[t][phrase] - sliding_window_mean(W) for phrase in timesteps[t]])
		inner_part = inner_sum * inner_sum
		outer_sum += inner_sum
	mean = (1/T)*outer_sum

def build_timesteps(phrase_files):
	timesteps = {}
	for t, file in enumerate(phrase_files):
		timesteps[t] = phrase_weights.parse_topmine_counts(file)
	return timesteps
		


def sliding_window(sliding_window=24):
	'''
	Sliding window T consists of X timesteps t.

	Sliding window T = 24 hr per paper.

	As sliding window moves along, a 
	u_T = sliding window mean
	o_T = sliding window standard deviation
	F(p_{(t), m}) = frequency of phrase p_m at time step t in the sliding window T.

	u_T = (1/X)sum([sum([F(p_{(t), m}) for m=1 in k])  for t=1 in X])
	'''
	return

def main():
	return

if __name__ == "__main__":
	main()
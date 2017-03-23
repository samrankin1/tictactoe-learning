import math

def upper_bound_confidence_interval(sample_proportion, sample_size, z_star = 1.96):
	'''Calculate the lower bound of the population's proportion with a default confidence level (z-star) of 95%'''
	lower_bound = sample_proportion + (z_star * math.sqrt((sample_proportion * (1 - sample_proportion)) / (sample_size)))
	return min(lower_bound, 1) # return, at maximum, 1

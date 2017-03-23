import math

# Future:
# assign each result a point value (i.e. win = 1 point, draw = 0 points, loss = -1 points)
# instead of using win percentage, which treats a loss and draw the same way,
# calculate an average "points per game" for each move based on previous outcomes
# then compute an expected values using a mean-based confidence interval instead of one for proportions
# and use these values as weights instead of upper-bound expected win proportion

def upper_bound_confidence_interval(sample_proportion, sample_size, z_star = 1.96):
	'''Calculate the lower bound of the population's proportion with a default confidence level (z-star) of 95%'''
	lower_bound = sample_proportion + (z_star * math.sqrt((sample_proportion * (1 - sample_proportion)) / (sample_size)))
	return min(lower_bound, 1) # return, at maximum, 1

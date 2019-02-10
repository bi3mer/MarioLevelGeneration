def rewards(level_map):
	'''
	Given a map we want to find how often we can find a reward. We expect 
	there to be at most 3 rewards per a column. So the score of 1 will be
	received if the map has 3 rewards on every column. Anything less will
	be rewards_found / (number_of_columns * 3)
	'''
	rewards_found = 0
	for column in level_map:
		# coins
		rewards_found += column.count('c')

		# mushrooms
		rewards_found += column.count('m')

		# star
		rewards_found += column.count('s')

		# red coin
		rewards_found += column.count('R')

	return rewards_found / float(len(level_map) * 3)
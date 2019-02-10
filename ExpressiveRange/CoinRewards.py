def coin_rewards(level_map):
	'''
	Given a map we want to find how often we can find a coin. We expect 
	there to be at most 3 coins per a column. So the score of 1 will be
	received if the map has 3 coins on every column. Anything less will
	be coins_found / (number_of_columns * 3)
	'''
	coins_found = 0
	for column in level_map:
		coins_found += column.count('c')

	return coins_found / float(len(level_map) * 3)
def linearity(level_map):
	'''
	Given a level map this determines the linearity of the level, 
	where a score of 1 means the player would never have to jump
	to complete the level. This isn't exhaustive; the case of:

	...
	#..
	...
	...
	...
	...
	#.#

	will not be perfectly handled because the player could simply 
	walk forward and they would technically make it across the 
	hole without jumping. Regardless, a score of 1 will be rewarded
	to a level where a jump required is not found. 

	1 - (jumps_found / number_of_columns)
	'''
	jumps_found = 0

	for column in level_map:
		col = column.split(',')

		if col[0] == '|':
			if col[1] != ':':
				jumps_found += 1
		else:
			jumps_found += 1

	return 1.0 - (jumps_found / float(len(level_map)))
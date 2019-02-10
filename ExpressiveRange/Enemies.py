def enemies(level_map):
	'''
	Given a map we want to find how often an enemy appears. We count
	enemy appearances per a column where the max score will be that 
	there is an enemy in ever column. enemies_found/column_count
	'''
	enemies_found = 0
	for column in level_map:
		# count goombas
		enemies_found += column.count('g')

		# count koopa troopa
		enemies_found += column.count('k')

		# count red flying koopa troopa
		enemies_found += column.count('K')

		# count hammer bro
		enemies_found += column.count('h')

		# count lakitu
		enemies_found += column.count('L')

		# count buzzy beatle 
		enemies_found += column.count('b')

		# count Cheep Cheep 
		enemies_found += column.count('C')

	return enemies_found / float(len(level_map))
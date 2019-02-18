from map_generation.generate_image import pre_process_map
from collections import deque
from tqdm import tqdm

import queue
import os

def build_grammars_and_mappings(max_grammar_length=4):
	LEVELS_DIR = 'levels/csv_cleaned_maps'

	index_to_column = {}
	column_to_index = {}

	grammars = [{} for i in range(max_grammar_length)]
	queues = [deque(maxlen=i + 1) for i in range(max_grammar_length)]
	index = 0

	print(f'Building grammars on levels found in {LEVELS_DIR}')
	files = os.listdir(LEVELS_DIR)
	for file in files:
		f = open(os.path.join(LEVELS_DIR, file))
		lines = f.readlines()
		f.close()

		# Before we can create any mapping we need to go through the entire map
		# and remove the lines and pre process it for the image and so the grammar
		# understandstand the difference between a pipe on the left and on the
		# right
		for i in range(len(lines)):
			lines[i] = lines[i].strip()
		pre_process_map(lines)

		# With the maps not processed, we can create the grammars. First we set up
		# our mapping for unseen columns and then we update the grammars count
		for column in lines:
			# for every line we first check to see if that column has been found
			# and if not we added to our dictionaries for mapping
			column = ','.join(column)
			if column not in column_to_index:
				index_to_column[str(index)] = column
				column_to_index[column] = str(index)

				index += 1

			# Build out grammar up until this point
			column_index = column_to_index[column]
			for i in range(max_grammar_length):
				grammar_context_queue = queues[i]
				if len(grammar_context_queue) == grammar_context_queue.maxlen:
					grammar_context = ','.join([str(j) for j in grammar_context_queue])

					if grammar_context not in grammars[i]:
						grammars[i][grammar_context] = {}

					if column_index not in grammars[i][grammar_context]:
						grammars[i][grammar_context][column_index] = 1
					else:
						grammars[i][grammar_context][column_index] += 1
				else:
					break

			# Update mapping of columns
			for i in range(max_grammar_length):
				queues[i].append(column_index)

	return grammars, index_to_column, column_to_index


def update_grammar_with_map(grammar, size, m, column_to_index):
	queue = deque(maxlen=size)

	for col in m:
		col_index = column_to_index[col]
		if len(queue) == queue.maxlen:
			grammar_context = ','.join([str(i) for i in queue])
			grammar[grammar_context][col_index] += 1

		queue.append(col_index)

	return grammar

def convert_counted_grammar_to_percentages(grammar, size, verbose=True):
	if verbose:
		print(f'Converting counted grammar {size} to percent weighted version')
		
	new_grammar = {}

	for input_column in grammar:
		total_amount = 0
		for output_index in grammar[input_column]:
			total_amount += grammar[input_column][output_index]

		total_amount = float(total_amount)
		new_grammar[input_column] = {}
		for output_index in grammar[input_column]:
			new_grammar[input_column][output_index] = grammar[input_column][output_index] / total_amount
		
	return new_grammar
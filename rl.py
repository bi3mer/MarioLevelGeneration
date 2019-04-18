from datetime import datetime
from tqdm import tqdm

import random
import json
import sys
import os

from map_generation import generate_image

import ExpressiveRange
import GenerateMap
import generator
import Grammar
import config

def rl(targets):
	grammar_size = config.rl.grammar_size
	grammars, index_to_column, column_to_index, weighted_grammars = generator.build_grammar_info(
		grammar_size,
		grammar_size)

	start_index, flag_index, end_index = generator.define_map_key_indexes(column_to_index)
	grammar = grammars[grammar_size - 1]

	print('Running RL to best match specified targets.')
	for iteration in tqdm(range(config.rl.max_iterations), ascii=True):
		# initialize grammar targets with 0 for every heuristic used
		average_evaluations = {}
		for key in targets:
			average_evaluations[key] = 0

		# Assess how the grammar we have is doing right now
		weighted_grammar = Grammar.convert_counted_grammar_to_percentages(grammar, grammar_size, verbose=False)

		for i in range(config.rl.assessment_iterations):
			map_grammar = GenerateMap.generate_map(weighted_grammar, config.rl.seed, 50, False, start_index, flag_index, end_index)
			map_text = GenerateMap.convert_grammar_array_to_map(map_grammar, index_to_column)
			m = map_text.strip().split('\n')

			for heuristic_type in targets:
				average_evaluations[heuristic_type] += heuristic_type.evaluate(m)

		min_eval_distance = {}
		for key in average_evaluations:
			# compute average for the given heuristic
			average_evaluations[key] /= config.rl.assessment_iterations

			# convert the average to min distance from target for a map 
			# to be utilized in updating the grammars count
			min_eval_distance[key] = abs(targets[key] - average_evaluations[key])


		# Now that we have an estimate of how the grammar is performing, we need to find several
		# maps that perform closer to our desired metrics. 
		maps = []
		index = -1
		broken = False
		while len(maps) < config.rl.minimum_maps:
			index += 1
			if index > 10000:
				print('\n\n\n')
				print('Generating maps no longer creates closer maps. Calling off and ending grammar')
				broken = True
				break

			# generate map
			map_grammar = GenerateMap.generate_map(
				weighted_grammar, random.random(), 50, False, start_index, flag_index, end_index,
				random_selection_chance=0.15)
			map_text = GenerateMap.convert_grammar_array_to_map(map_grammar, index_to_column)
			m = map_text.strip().split('\n')

			# generate a map and check if it meets our requirements to converge towards
			# our ideal structure
			acceptable_map = True
			for eval_type in targets:
				evaluation = eval_type.evaluate(m)

				if abs(targets[eval_type] - evaluation) >= min_eval_distance[eval_type]:
					acceptable_map = False
					break

				maps.append(m)

		# break out of loop when map generation no longer creates valid maps that can be used
		if broken:
			break

		# Since we have several maps that are closer to our desired metrics, we can now update
		# the counting of our current grammar
		for m in maps:
			grammar = Grammar.update_grammar_with_map(grammar, grammar_size, m, column_to_index)

	print('saving grammar')
	grammar_info = {}
	grammar_info['size'] = grammar_size
	grammar_info['grammar'] = grammar
	grammar_info['index_to_column'] = index_to_column
	grammar_info['column_to_index'] = column_to_index

	path = os.path.join('grammars', config.rl.grammar_name)
	f = open(path, 'w')
	f.write(json.dumps(grammar_info))
	f.close()
	
	# helpful text
	cmd = f'python generator.py --grammar-file {path} --display-images'
	print('Run the following to see results:')
	print(cmd)

def set_target(expressive_type, val, targets):
	if val == None:
		return

	targets[expressive_type] = val

if __name__ == '__main__':
	targets = {}
	set_target(ExpressiveRange.Type.CoinReward, config.rl.target_coin_reward, targets)
	set_target(ExpressiveRange.Type.Enemies, config.rl.target_enemies, targets)
	set_target(ExpressiveRange.Type.Linearity, config.rl.target_linearity, targets)
	set_target(ExpressiveRange.Type.Rewards, config.rl.target_rewards, targets)

	rl(targets)


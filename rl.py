from tqdm import tqdm, trange

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import random
import json
import sys
import os

import ExpressiveRange
import GenerateMap
import generator
import Grammar
import config

random.seed(config.rl.seed)

def animate_plot(figure, axis):
	pass

def rl(targets):
	# style.use('fivethirtyeight')
	# fig = plt.figure()
	# axis = fig.add_subplot(1,1,1)

	grammar_size = config.rl.grammar_size
	grammars, index_to_column, column_to_index, weighted_grammars = generator.build_grammar_info(
		grammar_size,
		grammar_size)

	start_index, flag_index, end_index = generator.define_map_key_indexes(column_to_index)
	grammar = grammars[grammar_size - 1]

	results_path = os.path.join('rl_results', f'eval_{config.rl.grammar_name}.csv')
	results_file = open(results_path, 'w')
	results_file.write(','.join([str(heuristic_type).split('.')[1] for heuristic_type in targets]) + '\n')

	print('Running RL to best match specified targets.')
	for iteration in trange(config.rl.max_iterations, ascii=True):
		# initialize grammar targets with 0 for every heuristic used
		average_evaluations = {}
		for key in targets:
			average_evaluations[key] = 0

		# Assess how the grammar we have is doing right now
		weighted_grammar = Grammar.convert_counted_grammar_to_percentages(grammar, grammar_size, verbose=False)

		for i in range(config.rl.assessment_iterations):
			map_grammar = GenerateMap.generate_map(
				weighted_grammar, config.rl.min_map_length, config.rl.max_map_length, 
				False, False, start_index, flag_index, end_index,
				random_selection_chance=config.rl.random_selection_chance)

			map_text = GenerateMap.convert_grammar_array_to_map(map_grammar, index_to_column)
			m = map_text.strip().split('\n')

			for heuristic_type in targets:
				average_evaluations[heuristic_type] += heuristic_type.evaluate(m)


		# compute average for the given heuristic
		for key in average_evaluations:
			average_evaluations[key] /= config.rl.assessment_iterations

		results_file.write(','.join([str(average_evaluations[t]) for t in average_evaluations]) + '\n')

		# Now that we have an estimate of how the grammar is performing, we need to find several
		# maps that perform closer to our desired metrics. 
		maps = []
		index = -1
		broken = False
		while len(maps) < config.rl.minimum_maps:
			index += 1
			if index > 10000:
				print('\n\n\n\n\n')
				print('Generating maps no longer creates closer maps. Calling off and ending grammar')
				broken = True
				break

			# generate map
			map_grammar = GenerateMap.generate_map(
				weighted_grammar, config.rl.min_map_length, config.rl.max_map_length,
				False, False, start_index, flag_index, end_index,
				random_selection_chance=config.rl.random_selection_chance)
				
			map_text = GenerateMap.convert_grammar_array_to_map(map_grammar, index_to_column)
			m = map_text.strip().split('\n')

			# generate a map and check if it meets our requirements to converge towards
			# our ideal structure
			acceptable_map = True
			for eval_type in targets:
				evaluation = eval_type.evaluate(m)

				if abs(targets[eval_type] - evaluation) > abs(targets[eval_type] - average_evaluations[eval_type]):
					acceptable_map = False
					break

			if acceptable_map:
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
	results_file.close()
	
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
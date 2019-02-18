from map_generation import generate_image
from datetime import datetime
from tqdm import tqdm

import ExpressiveRange
import GenerateMap
import generator
import argparse
import Grammar
import random
import json
import sys
import os

MIN_MAPS_FOUND = 10

def build_arg_parser():
	parser = argparse.ArgumentParser(description="Mario NGram Generation")

	parser.add_argument('--grammar-size', type=int, help='REQUIRED: size of grammar being used', required=True)

	parser.add_argument('--grammar-name', type=str, help='name of grammar to be stored')
	parser.add_argument('--max-iterations', type=int, help='maximum number of iterations for rl process')
	parser.add_argument('--seed', type=int, help='seed for rng')

	help_text = '''
		Number of iterations to be run when assessing the current status of the grammar that
		the process is improving. I would recommend somewhere between 50 and a 100.
		'''
	parser.add_argument('--assessment-iterations', type=int, help=help_text)

	parser.add_argument('--coin-rewards', type=float, help='target coin reward score for generated map, between 0 and 1')
	parser.add_argument('--enemies', type=float, help='target enemy score for generated map, between 0 and 1')
	parser.add_argument('--linearity', type=float, help='target linearity score for generated map, between 0 and 1')
	parser.add_argument('--rewards', type=float, help='target rewards scroe for generated map, between 0 and 1')

	return parser.parse_args()

def validate_float_argument(expressive_type, val, targets):
	if val == None:
		return

	if val < 0 or val > 1:
		print(f'{expressive_type.name} must be between 0 and 1')
		sys.exit(0)

	targets[expressive_type] = val

def rl(target_file_name, max_iterations, grammar_size, targets, assessment_iterations, seed):
	grammars, index_to_column, column_to_index, weighted_grammars = generator.build_grammar_info(
		grammar_size,
		grammar_size)

	start_index, flag_index, end_index = generator.define_map_key_indexes(column_to_index)
	grammar = grammars[grammar_size - 1]

	print('Running RL to best match specified targets.')
	for iteration in tqdm(range(max_iterations), ascii=True):
		# initialize grammar targets with 0 for every heuristic used
		average_evaluations = {}
		for key in targets:
			average_evaluations[key] = 0

		# Assess how the grammar we have is doing right now
		weighted_grammar = Grammar.convert_counted_grammar_to_percentages(grammar, grammar_size, verbose=False)

		for i in range(assessment_iterations):
			map_grammar = GenerateMap.generate_map(weighted_grammar, seed, 50, False, start_index, flag_index, end_index)
			map_text = GenerateMap.convert_grammar_array_to_map(map_grammar, index_to_column)
			m = map_text.strip().split('\n')

			for heuristic_type in targets:
				average_evaluations[heuristic_type] += heuristic_type.evaluate(m)

		min_eval_distance = {}
		for key in average_evaluations:
			# compute average for the given heuristic
			average_evaluations[key] /= assessment_iterations

			# convert the average to min distance from target for a map 
			# to be utilized in updating the grammars count
			min_eval_distance[key] = abs(targets[key] - average_evaluations[key])


		# Now that we have an estimate of how the grammar is performing, we need to find several
		# maps that perform closer to our desired metrics. 
		maps = []
		index = -1
		broken = False
		while len(maps) < MIN_MAPS_FOUND:
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

	path = os.path.join('grammars', target_file_name)
	f = open(path, 'w')
	f.write(json.dumps(grammar_info))
	f.close()
	print('completed. Run the following to see the results:')
	print(f'python generator.py --grammar-file {path} --display-images')

if __name__ == '__main__':
	args = build_arg_parser()

	targets = {}
	validate_float_argument(ExpressiveRange.Type.CoinReward, args.coin_rewards, targets)
	validate_float_argument(ExpressiveRange.Type.Enemies, args.enemies, targets)
	validate_float_argument(ExpressiveRange.Type.Linearity, args.linearity, targets)
	validate_float_argument(ExpressiveRange.Type.Rewards, args.rewards, targets)

	max_iterations = args.max_iterations
	if max_iterations == None:
		print('max iterations was not set. Defaulting value to 5000.')
		max_iterations = 5000
	elif max_iterations <= 0:
		print('--max-iterations must be an integer greater than 0')
		sys.exit(0)

	target_file_name = args.grammar_name
	if target_file_name == None:
		target_file_name = datetime.now().strftime("%Y_%m_%d_%H_%M.json")
		print(f'--grammar-name not set. Defaulting to "{target_file_name}".')
	elif target_file_name.endswith('.json') == False:
		print('--grammar-name must specify file name ending with ".json"')
		sys.exit(0)

	grammar_size = args.grammar_size
	if grammar_size == None:
		print('-grammar size not set. Defaulting to 5')
		grammar_size = 5
	elif grammar_size <= 0 or grammar_size >= 10:
		print('--grammar-size must be greater than 0 and less than 10')
		sys.exit(0)

	assessment_iterations = args.assessment_iterations
	if assessment_iterations == None:
		print('--assessment-iterations not set. Defaulting to 25')
		assessment_iterations = 25
	elif assessment_iterations <= 0 or assessment_iterations >= 1000:
		print('--assessment-iterations must be greater than 0 and less than 1000')
		sys.exit(0)

	seed = args.seed
	if seed == None:
		seed = datetime.now()
	rl(target_file_name, max_iterations, grammar_size, targets, assessment_iterations, seed)


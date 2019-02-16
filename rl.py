from map_generation import generate_image
from datetime import datetime
from tqdm import tqdm

import ExpressiveRange
import GenerateMap
import generator
import argparse
import Grammar
import sys

def build_arg_parser():
	parser = argparse.ArgumentParser(description="Mario NGram Generation")

	parser.add_argument('--grammar-size', type=int, help='REQUIRED: size of grammar being used', required=True)

	parser.add_argument('--grammar-name', type=str, help='name of grammar to be stored')
	parser.add_argument('--max-iterations', type=int, help='maximum number of iterations for rl process')

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

def rl(target_file_name, max_iterations, grammar_size, targets):
	print(target_file_name)
	print(max_iterations)
	print(targets)

	grammars, index_to_column, column_to_index, weighted_grammars = generator.build_grammar_info(
		grammar_size,
		grammar_size)

	grammar = grammars[grammar_size - 1]
	print(grammar)

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
	if grammar_size <= 0 or grammar_size >= 10:
		print('--grammar-size must be greater than 0 and less than 10')
		sys.exit(0)

	rl(target_file_name, max_iterations, grammar_size, targets)


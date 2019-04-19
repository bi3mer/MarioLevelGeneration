from map_generation import generate_image
from datetime import datetime
from tqdm import tqdm

import ExpressiveRange
import GenerateMap
import argparse
import Grammar
import json
import sys
import os

def define_map_key_indexes(column_to_index):
	# depending on parsing order, these indexes may change but the hardcoded
	# strings will not unless the entire dataset is change to support VGLC
	start_index = column_to_index['|,:,:,:,:,:,:,:,:,:,:,:']
	flag_index = column_to_index['|,:,:,:,:,:,:,:,:,:,flag,:']
	end_index = column_to_index['|,=,f,f,f,f,f,f,f,f,f,flag_pole_top']

	return start_index, flag_index, end_index

def build_maps(
	weighted_grammars, index_to_column, column_to_index, seed, min_map_length, max_map_length,
	use_random_selection, store_maps, display_png, display_ascii, display_heuristics=False):

	start_index, flag_index, end_index = define_map_key_indexes(column_to_index)

	print('generating maps')
	for i in tqdm(range(len(weighted_grammars)), ascii=True):
		grammar = weighted_grammars[i]
		map_grammar = GenerateMap.generate_map(
			grammar, seed, min_map_length, max_map_length, use_random_selection, 
			start_index, flag_index, end_index)
		map_text = GenerateMap.convert_grammar_array_to_map(map_grammar, index_to_column)

		save_path = None
		if store_maps:
			if use_random_selection:
				save_path = f'screenshots/random_grammar_{i+1}.png'
			else:
				save_path = f'screenshots/weighted_grammar_{i+1}.png'

		generate_image.convert_map(map_text, display_png=display_png, save_path=save_path)

		if display_ascii:
			print(f'Grammar Size: {i}')
			print(map_text)

		if display_heuristics:
			m = map_text.strip().split('\n')
			print()
			print('Expressive Range Heuristics')
			print(f'Coin Rewards: {ExpressiveRange.coin_rewards(m)}')
			print(f'Linearity:    {ExpressiveRange.linearity(m)}')
			print(f'Enemies:      {ExpressiveRange.enemies(m)}')
			print(f'Rewards:      {ExpressiveRange.rewards(m)}')

def build_arg_parser():
	parser = argparse.ArgumentParser(description="Mario NGram Level Generation")

	parser.add_argument(
		'--generate-weighted-maps', 
		action='store_true', 
		help='flag to generate weighted grammar maps')

	parser.add_argument(
		'--generate-random-maps', 
		action='store_true', 
		help='flag to generate generate random maps')

	parser.add_argument('--min-map-length', type=int, help='minimum length of maps generated')
	parser.add_argument('--max-map-length', type=int, help='maximum length of maps generated')
	parser.add_argument('--seed', type=int, help='define seed for generation for consistent results')
	parser.add_argument('--max-grammar-length', type=int, help='define max grammar length used in generated maps')
	parser.add_argument('--save', action='store_true', help='flag to save images in screenshots directory')
	parser.add_argument('--display-images', action='store_true', help='flag to view images after generation')
	parser.add_argument('--display-ascii', action='store_true', help='flag to view ascii version of images after generation')
	parser.add_argument('--grammar-file', type=str, help='file path to grammar built from rl.py')

	return parser.parse_args()

def define_configuration(parser):
	min_map_length = 200
	if parser.min_map_length:
		min_map_length = parser.min_map_length

	max_map_length = 200
	if parser.max_map_length:
		max_map_length = parser.max_map_length

	if max_map_length < min_map_length:
		raise Exception('max-map-length cannot be smaller than min-map-length')

	seed = datetime.now()
	if parser.seed:
		seed = parser.seed

	grammar_count = 4
	if parser.max_grammar_length:
		grammar_count = parser.max_grammar_length

	return min_map_length, max_map_length, seed, grammar_count

def build_grammar_info(min_grammar_size, max_grammar_size):
	grammars, index_to_column, column_to_index = Grammar.build_grammars_and_mappings(max_grammar_length=max_grammar_size)
	
	weighted_grammars = []
	for i in range(min_grammar_size, max_grammar_size):
		weighted_grammars.append(Grammar.convert_counted_grammar_to_percentages(grammars[i], i))

	return grammars, index_to_column, column_to_index, weighted_grammars

if __name__ == '__main__':
	parser = build_arg_parser()

	if not parser.generate_weighted_maps and not parser.generate_random_maps and not parser.grammar_file:
		print('run "python generator.py --help" for options')
		sys.exit(0)

	min_map_length, max_map_length, seed, grammar_count = define_configuration(parser)
	grammars, index_to_column, column_to_index, weighted_grammars = build_grammar_info(0, grammar_count)

	if parser.generate_weighted_maps:
		build_maps(
			weighted_grammars, index_to_column, column_to_index, seed, min_map_length, max_map_length,
			False, parser.save, parser.display_images, parser.display_ascii)

	if parser.generate_random_maps:
		build_maps(
			weighted_grammars, index_to_column, column_to_index, seed, min_map_length, max_map_length,
			True, parser.save, parser.display_images, parser.display_ascii)

	if parser.grammar_file:
		if os.path.isfile(parser.grammar_file) == False:
			print(f'{parser.grammar_file} does not point to an existing file')
			sys.exit(0)

		if parser.grammar_file.endswith('.json') == False:
			print(f'{parser.grammar_file} must end with the ".json" extension')
			sys.exit(0)

		f = open(parser.grammar_file, 'r')
		ngram_information = json.loads(f.read())
		f.close()

		grammar = ngram_information['grammar']
		grammar_size = ngram_information['size']
		index_to_column = ngram_information['index_to_column']
		column_to_index = ngram_information['column_to_index']

		weighted_grammars = [Grammar.convert_counted_grammar_to_percentages(grammar, grammar_size)]
		build_maps(
			weighted_grammars, index_to_column, column_to_index, seed, min_map_length, max_map_length,
			False, parser.save, parser.display_images, parser.display_ascii, display_heuristics=True)





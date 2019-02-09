from map_generation import generate_image
from datetime import datetime
from tqdm import tqdm

import GenerateMap
import argparse
import Grammar
import sys

def build_maps(
	weighted_grammars, index_to_column, seed, min_map_length, use_random_selection, 
	start_index, flag_index, end_index, store_maps, display_png, display_ascii):

	print('generating maps')
	for i in tqdm(range(len(weighted_grammars)), ascii=True):
		grammar = weighted_grammars[i]
		map_grammar = GenerateMap.generate_map(
			grammar, seed, min_map_length, use_random_selection, 
			start_index=start_index, flag_index=flag_index, end_index=end_index)
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

def build_arg_parser():
	parser = argparse.ArgumentParser(description="BGC ApiGateway Helper")

	parser.add_argument(
		'--generate-weighted-maps', 
		action='store_true', 
		help='flag to generate weighted grammar maps')

	parser.add_argument(
		'--generate-random-maps', 
		action='store_true', 
		help='flag to generate generate random maps')

	parser.add_argument('--min-map-length', type=int, help='minimum length of maps generated')
	parser.add_argument('--seed', type=int, help='define seed for generation for consistent results')
	parser.add_argument('--max-grammar-length', type=int, help='define max grammar length used in generated maps')
	parser.add_argument('--save', action='store_true', help='flag to save images in screenshots directory')
	parser.add_argument('--display-images', action='store_true', help='flag to view images after generation')
	parser.add_argument('--display-ascii', action='store_true', help='flag to view ascii version of images after generation')

	return parser.parse_args()

def define_configuration(parser):
	min_map_length = 200
	if parser.min_map_length:
		min_map_length = parser.min_map_length

	seed = datetime.now()
	if parser.seed:
		seed = parser.seed

	grammar_count = 4
	if parser.max_grammar_length:
		grammar_count = parser.max_grammar_length

	return min_map_length, seed, grammar_count

if __name__ == '__main__':
	parser = build_arg_parser()

	if not parser.generate_weighted_maps and not parser.generate_random_maps:
		print('run "python generator.py --help" for options')
		sys.exit(0)

	min_map_length, seed, grammar_count = define_configuration(parser)
	grammars, index_to_column, column_to_index = Grammar.build_grammars_and_mappings(max_grammar_length=grammar_count)
	weighted_grammars = [Grammar.convert_counted_grammar_to_percentages(grammars[i], i) for i in range(grammar_count)]

	# depending on parsing order, these indexes may change but the hardcoded
	# strings will not unless the entire dataset is change to support VGLC
	start_index = column_to_index['|,:,:,:,:,:,:,:,:,:,:,:']
	flag_index = column_to_index['|,:,:,:,:,:,:,:,:,:,flag,:']
	end_index = column_to_index['|,=,f,f,f,f,f,f,f,f,f,flag_pole_top']

	if parser.generate_weighted_maps:
		build_maps(
			weighted_grammars, index_to_column, seed, min_map_length, False, 
			start_index, flag_index, end_index, parser.save, parser.display_images,
			parser.display_ascii)

	if parser.generate_random_maps:
		build_maps(
			weighted_grammars, index_to_column, seed, min_map_length, True, 
			start_index, flag_index, end_index, parser.save, parser.display_images,
			parser.display_ascii)



	
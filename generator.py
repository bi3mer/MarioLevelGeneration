import argparse

def build_arg_parser():
	parser = argparse.ArgumentParser(description="BGC ApiGateway Helper")

	parser.add_argument(
		'--generate-weighted-maps', 
		action='store_true', 
		help='flag to generate weighted grammar maps')

	parser.add_argument(
		'--generated-unweighted-maps', 
		action='store_true', 
		help='flag to generate generated-unweighted-maps')

	return parser.parse_args()

if __name__ == '__main__':
	parser = build_arg_parser()

	if parser.generate_weighted_maps:
		print('build weighted maps')

	if parser.generated_unweighted_maps:
		print('build unweighted maps')

	if not parser.generate_weighted_maps and not parser.generated_unweighted_maps:
		print('run "python generator.py --help" for options')
from PIL import Image, ImageDraw
import json

STEP_SIZE = 16

def build_json():
	'''
	read in the json file for the tile info and return the src portion
	as the info section is only useful for people trying to learn how 
	this code base will work	
	'''
	f = open('tile_info.json')
	data = json.load(f)
	f.close()

	return data['src']

def empty_default_image(im):
	'''
	Set every pixel in the image to have an alpha of zero
	'''
	w,h = im.size

	pixels = []
	for x in xrange(w):
		for y in xrange(h):
			pixels.append((0,0,0,0))

	im.putdata(pixels)

def draw_ground_bottom(image, env_tile_set, x0, y0, xt, yt):
	'''
	Loop through top half of ground and put it at the very bottom
	of the iamge to handle special case of extra 8 pixels at the 
	bottom of every mario map
	'''
	step_size = STEP_SIZE / 2

	# we aren't modifying the pixels after the tiles x coordinates
	y0 += STEP_SIZE

	for y in xrange(step_size):
		for x in xrange(STEP_SIZE):
			pixel = env_tile_set.getpixel((xt + x, yt + y))
			image.putpixel((x0+x, y0+y), pixel)

def parse_json_for_tile_info(data, tile):
	tile_data = None
	tile_length = len(tile)

	if tile_length == 3:
		tile_name = tile[0]
		top_or_bottom = 'bottom' if tile[1] == 'b' else 'top'
		left_or_right = 'left' if tile[2] == 'l' else 'right'
		tile_data = data[tile_name][top_or_bottom][left_or_right]
	elif tile_length == 1 and tile in data:
		tile_data = data[tile]

	return tile_data

def draw_from_sprite_sheet(tile_sets, image, x0, y0, data, tile):
	# ignore air
	if tile == ':':
		return

	data = parse_json_for_tile_info(data, tile)
	if data == None:
		print 'Could not parse data for: ', tile
		return

	tile_set = tile_sets[data['type']]

	# tile set x and y positions
	xt = data['x0']
	yt = data['y0']

	# adjust coodrinates to image space
	x0 *= STEP_SIZE
	y0 *= STEP_SIZE

	# put pixels into image
	for y in xrange(STEP_SIZE):
		for x in xrange(STEP_SIZE):
			pixel = tile_set.getpixel((xt + x, yt + y))
			image.putpixel((x0+x, y0+y), pixel)

	# handle special cases like the 8 pixels at the bottom of the ground
	if tile == '|': draw_ground_bottom(image, tile_set, x0, y0, xt, yt)

def pre_process_map(matrix):
	'''
	Take a map and convert it into something that can easily be converted
	into an image. This mainly contains special cases like the hammer 
	spring which takes up two tile spaces instead of 1. The map has two 
	s characters and this will replace it the bottom with sb and the top
	with st. draw_from_sprite_sheet will use the json which already has
	the defined behavior for these special characters to properly fill 
	out the image
	'''
	for i in xrange(len(matrix)):
		column = list(matrix[i])

		for j in xrange(len(column)):
			tile = column[j]

			if tile == 'p':
				left_column = matrix[i-1]
				if column[j + 1] == 'p':
					if left_column[j] == 'pbl':
						column[j] = 'pbr'
					else:
						column[j] = 'pbl'
				else:
					if left_column[j] == 'ptl':
						column[j] = 'ptr'
					else:
						column[j] = 'ptl'
			elif tile == 'f':
				print 'flag is not yet handled'
			elif tile == 'S':
				print 'spring is not yet handled'

		matrix[i] = column

	print matrix

def create_tilesets(): 
	'''
	open all tilesets from their source png and return them as an array
	that links up with the tileinfo json file for the types where:
		1 = enemy
		2 = environment
		3 = items
	'''
	env_sprite_sheet   = Image.open('../assets/env_tileset.png')
	enemy_sprite_sheet = Image.open('../assets/enemy_tileset.png')
	items_sprite_sheet = Image.open('../assets/items_objects_tileset.png')

	return [enemy_sprite_sheet, env_sprite_sheet, items_sprite_sheet]

def convert_map(map_str, display=True, save_path=None):
	'''
	convert a string of a mario map into an image. 

	- Set save_path to a string for this function to save the image. 
	- Set Display to Falseto not display the map on conversion completion
	'''
	tile_sets = create_tilesets()

	data = build_json()
	lvl_map = map_str.strip().split('\n')
	pre_process_map(lvl_map)

	len_column = len(lvl_map)
	len_row = len(lvl_map[0])

	# there are always 8 extra pixels in a mario level
	height = len_row * STEP_SIZE + 8 
	width = len_column * STEP_SIZE

	im = Image.new('RGBA', (width, height))
	empty_default_image(im)

	for x in xrange(len_column):
		for y in xrange(len_row):
			tile = lvl_map[x][y]
			draw_from_sprite_sheet(tile_sets, im, x, len_row - y - 1, data, tile)

	if display:
		im.show()

	if save_path != None and save_path != "":
		im.save(save_path)

if __name__ == '__main__':
	f = open('../levels/cleaned_maps/1-1.map', 'r')
	map_text = f.read()
	f.close()

	convert_map(map_text)
	# convert_map(map_text, display=False, save_path='../screenshots/sample_incomplete_map_generation_form_1_1.png')
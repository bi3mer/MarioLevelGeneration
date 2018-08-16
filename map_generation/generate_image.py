'''
@note: I'm not attempting to make this code clean or good, just functional
       beacuse this will never be used extensively or have to be re-written.
'''

from PIL import Image, ImageDraw
import json

STEP_SIZE = 16

flag_x = 0
flag_y = 0

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

def draw_from_sprite_sheet(tile_sets, image, x0, y0, data, tile):
	global flag_x
	global flag_y

	# ignore air
	if tile == ':':
		return

	if tile not in data: 
		print 'Could not parse data for (%i, %i): %s' % (x0, y0, tile)
		return

	tile_data = data[tile]
	tile_set = tile_sets[tile_data['type']]

	# tile set x and y positions
	xt = tile_data['x0']
	yt = tile_data['y0']

	# render the flag last
	if tile == 'flag' and flag_x == 0 and flag_y == 0:
		flag_x = x0
		flag_y = y0
		return

	# adjust coodrinates to image space
	x0 *= STEP_SIZE
	y0 *= STEP_SIZE

	# adjust x0 for flag
	if tile == 'flag':
		x0 += 8

	# put pixels into image
	y_step_size = STEP_SIZE
	x_step_size = STEP_SIZE
	if 'extra' in tile_data:
		y_step_size += tile_data['extra']
		y0 -= tile_data['extra']

	if 'reduce_x_right' in tile_data:
		x = tile_data['reduce_x_right']
		x0 += x
		x_step_size -= x
	elif 'reduce_x_left' in tile_data:
		x = tile_data['reduce_x_left']
		xt += x
		x_step_size -=x

	for y in xrange(y_step_size):
		for x in xrange(x_step_size):
			pixel = tile_set.getpixel((xt+x, yt+y))
			image.putpixel((x0+x, y0+y), pixel)

	# handle special cases like the 8 pixels at the bottom of the ground
	if tile == '|':
		draw_ground_bottom(image, tile_set, x0, y0, xt, yt)
	elif tile == 'TM':
		data = data['P']
		draw_ground_bottom(image, tile_set, x0, y0, data['x0'], data['y0'])

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
				if column[j - 1] == '|':
					column[j] = '='
				elif j == len(column) - 2:
					column[j] = 'flag_pole_top'
				elif i + 2 == len(matrix):
					column[j] = 'flag'
			elif tile == 'T': 
				left_column = matrix[i-1]
				right_column = matrix[i+1]

				if 'T' not in left_column[j]:
					column[j] = 'TL'
				elif left_column[j] == 'TL' or right_column[j] == 'T':
					column[j] = 'TM'
				else:
					column[j] = 'TR'
			elif tile == 'e':
				if left_column[j] == 'el':
					column[j] = 'er'
				else:
					column[j] = 'el'
			elif tile == 'S':
				if 's' in column[j-1]:
					column[j] = 'st'
				else:
					column[j] = 'sb'

		matrix[i] = column

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

	# the flag has to be rendered last else there will be ordering issues
	draw_from_sprite_sheet(tile_sets, im, flag_x, flag_y, data, 'flag')

	if display:
		im.show()

	if save_path != None and save_path != "":
		im.save(save_path)

if __name__ == '__main__':
	f = open('../levels/cleaned_maps/4-1.map', 'r')
	map_text = f.read()
	f.close()

	convert_map(map_text)
	# convert_map(map_text, display=False, save_path='../screenshots/sample_complete_map_generation_form_1_1.png')
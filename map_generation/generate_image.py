'''
@note: I'm not attempting to make this code clean or good, just functional
       beacuse this will never be used extensively or have to be re-written.
'''

from PIL import Image, ImageDraw
import json

STEP_SIZE = 16

flag_x = 0

def build_json():
	'''
	read in the json file for the tile info and return the src portion
	as the info section is only useful for people trying to learn how 
	this code base will work	
	'''
	f = None

	if __name__ == '__main__':
		f = open('tile_info.json')
	else:
		f = open('map_generation/tile_info.json')
	data = json.load(f)
	f.close()

	return data['src']

def empty_default_image(im):
	'''
	Set every pixel in the image to have an alpha of zero
	'''
	w,h = im.size

	pixels = []
	for x in range(w):
		for y in range(h):
			pixels.append((0,0,0,0))

	im.putdata(pixels)

def draw_ground_bottom(image, env_tile_set, x0, y0, xt, yt):
	'''
	Loop through top half of ground and put it at the very bottom
	of the iamge to handle special case of extra 8 pixels at the 
	bottom of every mario map
	'''
	step_size = int(STEP_SIZE / 2)

	# we aren't modifying the pixels after the tiles x coordinates
	y0 += STEP_SIZE

	for y in range(step_size):
		for x in range(STEP_SIZE):
			pixel = env_tile_set.getpixel((xt + x, yt + y))
			image.putpixel((x0+x, y0+y), pixel)

def draw_from_sprite_sheet(tile_sets, image, x0, y0, data, tile, is_bottom):
	global flag_x

	# ignore air
	if tile == ':':
		return

	if tile not in data: 
		print('Could not parse data for (%i, %i): %s' % (x0, y0, tile))
		return

	tile_data = data[tile]
	tile_set = tile_sets[tile_data['type']]

	# tile set x and y positions
	xt = tile_data['x0']
	yt = tile_data['y0']

	# render the flag last
	if tile == 'flag' and flag_x == 0:
		flag_x = x0
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

	for y in range(y_step_size):
		if tile == 'flag':
			print(y)

		for x in range(x_step_size):
			if tile == 'flag':
				print(x0 + x)
			pixel = tile_set.getpixel((xt+x, yt+y))
			image.putpixel((x0+x, y0+y), pixel)

	# handle special cases like the 8 pixels at the bottom of the ground
	if is_bottom:
		if tile == '|':
			draw_ground_bottom(image, tile_set, x0, y0, xt, yt)
		elif tile == 'TM' or tile == 'P':
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
	length = len(matrix)
	for i in range(length):
		matrix[i] = matrix[i].split(',')
   
	for i in range(length):
		column = matrix[i]
		for j in range(len(column)):
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
				elif i + 2 == len(matrix):
					column[j] = 'flag'
				elif j == len(column) - 1:
					column[j] = 'flag_pole_top'
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
			elif tile == 'z':
				if tile in column[j-1]:
					column[j] = 'zt'
				elif tile not in column[j+1]:
					column[j] = 'zt'
				else:
					column[j] = 'zb'
			elif tile == 'Z':
				if 'z' not in column[j-1]:
					column[j] = 'zt'
				elif column[j-1] == 'zt':
					column[j] = 'zb'
				else:
					column[j] = 'zt'

		matrix[i] = column

def create_tilesets(): 
	'''
	open all tilesets from their source png and return them as an array
	that links up with the tileinfo json file for the types where:
		1 = enemy
		2 = environment
		3 = items
	'''
	env_sprite_sheet = None
	enemy_sprite_sheet = None
	items_sprite_sheet = None
    
	if __name__ == '__main__':
		env_sprite_sheet   = Image.open('../assets/env_tileset.png')
		enemy_sprite_sheet = Image.open('../assets/enemy_tileset.png')
		items_sprite_sheet = Image.open('../assets/items_objects_tileset.png')
	else: 
		env_sprite_sheet   = Image.open('assets/env_tileset.png')
		enemy_sprite_sheet = Image.open('assets/enemy_tileset.png')
		items_sprite_sheet = Image.open('assets/items_objects_tileset.png')

	return [enemy_sprite_sheet, env_sprite_sheet, items_sprite_sheet]

def convert_map(map_str, display_png=True, save_path=None):
	'''
	convert a string of a mario map into an image. 

	- Set save_path to a string for this function to save the image. 
	- Set Display to Falseto not display the map on conversion completion
	'''
	global flag_x
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

	for x in range(len_column):
		for y in range(len_row):
			tile = lvl_map[x][y]
			draw_from_sprite_sheet(tile_sets, im, x, len_row - y - 1, data, tile, y == 0)

	# the flag has to be rendered last else there will be ordering issues
	# draw_from_sprite_sheet(tile_sets, im, flag_x, 0, data, 'flag', False)
	flag_x = 0

	if display_png:
		im.show()

	if save_path != None and save_path != "":
		im.save(save_path)

if __name__ == '__main__':
	f = open('../levels/test_sample.map', 'r')
	map_text = f.read()
	f.close()

	convert_map(map_text)
	# convert_map(map_text, display=False, save_path='../screenshots/sample_complete_map_generation_form_1_1.png')
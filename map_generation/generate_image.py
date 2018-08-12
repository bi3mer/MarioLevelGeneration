from PIL import Image, ImageDraw
import json

STEP_SIZE = 16

def build_json():
	f = open('tile_info.json')
	data = json.load(f)
	f.close()

	# remove info section which is only useful for newcomers
	return data['src']

def empty_default_image(im):
	w,h = im.size

	pixels = []
	for x in xrange(w):
		for y in xrange(h):
			pixels.append((0,0,0,255))

	im.putdata(pixels)

def draw_from_sprite_sheet(tile_sets, image, x0, y0, data):
	tile_set = tile_sets[data['type']]

	# tile set x and y positions
	xt = data['x0']
	yt = data['y0']

	# adjust coodrinates to image space
	x0 *= STEP_SIZE
	y0 *= STEP_SIZE

	# put pixels into image
	for x in xrange(STEP_SIZE):
		for y in xrange(STEP_SIZE):
			print x0, y0
			print image.size

			pixel = tile_set.getpixel((xt + x, yt + y))
			print pixel
			image.putpixel((x0,y0), pixel)
			y0 += 1
		x0 += 1

def convert_map(map_str, save_path=None):
	env_sprite_sheet = Image.open('../assets/env_tileset.png')
	enemy_sprite_sheet = Image.open('../assets/enemy_tileset.png')
	items_sprite_sheet = Image.open('../assets/items_objects_tileset.png')
	tile_sets = [enemy_sprite_sheet, env_sprite_sheet, items_sprite_sheet]

	data = build_json()
	lvl_map = map_str.strip().split('\n')

	len_column = len(lvl_map)
	len_row = len(lvl_map[0])

	height = len_column * STEP_SIZE
	width = len_row * STEP_SIZE

	im = Image.new('RGB', (height, width))
	empty_default_image(im)

	for y in xrange(len_column):
		for x in xrange(len_row):
			if lvl_map[y][x] == 'g':
				draw_from_sprite_sheet(tile_sets, im, x, y, data['g'])
				
	im.show()

if __name__ == '__main__':
	f = open('../levels/cleaned_maps/1-1.map', 'r')
	map_text = f.read()
	f.close()

	convert_map(map_text)
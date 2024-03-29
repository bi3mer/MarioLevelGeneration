from PIL import Image, ImageDraw
from tqdm import tqdm
import os

step_size = 16

grid_values = {}
index = 48

def convert_square_to_map_character(pixels, w0, h0, w1, h1):
	global index

	grid_value = ""
	for w in xrange(w0, w1):
		for h in xrange(h0, h1):
			grid_value += str(pixels[w,h][0])
		grid_value +='\n'

	if grid_value not in grid_values:
		grid_values[grid_value] = index
		index += 1

	return grid_values[grid_value]

def convert_mario_png_to_map(png_path):
	im = Image.open(png_path).convert("RGB")
	width, height = im.size

	pixels = im.load()
	txt_map = ''

	for w0 in range(0, width, step_size):
		w1 = w0 + step_size - 1
		if w1 > width:
			continue

		txt_str = ''

		# bug here.  the iteration is ending at 16 but should be ending at 8.
		for h0 in range(step_size + 8, height - step_size, step_size):
			h1 = h0 + step_size - 1
			if h1 <= step_size + 8:
				continue

			# convert index to ascii character
			txt_str += chr(convert_square_to_map_character(pixels, w0, h0, w1, h1))

		# append reversed string of text with a new line to string representing the
		# map. We reverse so the ground is at the beginning of the string rather 
		# than the end
		txt_map += txt_str[::-1] + '\n'

	return txt_map

if __name__ == '__main__':
	png_dir = '../levels/png/'
	map_dir = '../levels/map/'

	for png in tqdm(os.listdir(png_dir)):
		result = convert_mario_png_to_map(png_dir + png)

		f = open(map_dir + png.replace('.png', '.map'), 'w')
		f.write(result)
		f.close()

		grid_values = {}
		index = 48
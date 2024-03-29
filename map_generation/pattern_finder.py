from PIL import Image, ImageDraw

sample_map = '../levels/png/1-1.png'
step_size = 16

im = Image.open(sample_map).convert("RGB")
draw = ImageDraw.Draw(im) 

width, height = im.size

for h in range(8, height - step_size, step_size):
	draw.line((0,h, width,h), fill=255)

for w in range(0, width, step_size):
	draw.line((w,0, w,height), fill=255)
	
im.show()
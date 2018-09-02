import os

files = os.listdir()

for file in files:
	# read claned map
	f = open(file, 'r')
	lines = f.readlines()
	f.close()

	# comma seaprate strings
	for i in range(len(lines)):
		# last value will always be a comma that we don't want
		lines[i] = ','.join(lines[i])[:-2] + '\n'

	# write cleaned maps to new location
	f = open('../csv_cleaned_maps/' + file, 'w')
	for line in lines:
		f.write(line)

	f.close()
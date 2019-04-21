import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import style

import time
import sys
import os

if len(sys.argv) != 2:
    raise Exception('Must receive argument for file to watch')

file_path = sys.argv[1]
if not os.path.isfile(file_path):
    raise Exception(f'Received invalid file path "{file_path}"')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.set_xlabel('Training Epoch')
ax1.set_ylabel('Performance')

def animate(i):
    f = open(file_path, 'r')
    lines = f.readlines()
    f.close()
    headers = [line.strip() for line in lines[0].split(',')]
    y_data = [[float(eval_value) for eval_value in line.strip().split(',')]for line in lines[1:]]
    x = [i for i in range(len(y_data))]

    ax1.clear()

    for i in range(len(headers)):
        y = [y_data[column][i] for column in range(len(y_data))]
        ax1.plot(x, y, label=headers[i], linewidth=0.5)

        ax1.legend(loc=4)
        ax1.set_title('Live Training Progress')	
        ax1.set_ylim(bottom=0, top=1)

ani = animation.FuncAnimation(fig, animate, interval=20)
plt.show()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

fig = plt.figure(figsize =(6,4))
ax = fig.add_axes([0.05, 0.1, 0.9, 0.8], projection=None, polar=False,facecolor='white',frame_on=True)


x = np.linspace(0, 3 * np.pi, 500)
y = np.sin(x)

rgba_colors = np.zeros((len(x),4))
x_norm=x/(3 * np.pi)
y_norm=np.abs(y)
rgba_colors[:,0] = x_norm
rgba_colors[:,1] = x_norm
rgba_colors[:,2] = x_norm
rgba_colors[:,3] = y_norm
print(np.shape(rgba_colors))
# Create a set of line segments so that we can color them individually
# This creates the points as a N x 1 x 2 array so that we can stack points
# together easily to get the segments. The segments array for line collection
# needs to be (numlines) x (points per line) x 2 (for x and y)
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

lc = LineCollection(segments,linewidth=2, linestyle='solid', colors=rgba_colors)
line = ax.add_collection(lc)

ax.set_xlim(x.min(), x.max())
ax.set_ylim(-1.1, 1.1)
plt.show()
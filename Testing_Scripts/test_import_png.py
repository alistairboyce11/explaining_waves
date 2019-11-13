

### Importing various python libraries
# numpy is a useful toolkit for scientific computations
import numpy as np
# matplotlib is a plotting toolkit
import matplotlib.pyplot as plt


# import numpy as np
# import matplotlib.pyplot as plt

# Set epicentral distance from Earthquake to Station - use station longitude to increase this 0-180 allowed
epi_dist=20

# depth of earthquake in km
depth_earthquake = 0

radius = 6371                                       # radius of Earth in km


im='../../wavefront_movie_home_screen/Model_graphics_flat.png'
data = plt.imread(im)

fig = plt.figure()
#create axes in the background to show cartesian image
ax0 = fig.add_subplot(121)
ax0.imshow(data)
ax0.axis("off")

# create polar axes in the foreground and remove its background
# to see through
ax = fig.add_subplot(121, polar=True, label="polar")
ax.set_facecolor("None")
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_xticks([])
ax.set_yticks([])

discons = np.array([   0.,2891.5, 5153.5, 6371. ])
ax.set_yticks(radius - discons)
ax.xaxis.set_major_formatter(plt.NullFormatter())
ax.yaxis.set_major_formatter(plt.NullFormatter())



ax1 = plt.subplot(122)

plt.show()

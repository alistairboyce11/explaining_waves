import matplotlib.pyplot as plt


def annotate_axes(fig):
    for i, ax in enumerate(fig.axes):
        ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        ax.tick_params(labelbottom=False, labelleft=False)

#
# fig = plt.figure()
# ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)
# ax2 = plt.subplot2grid((3, 3), (1, 0), colspan=2)
# ax3 = plt.subplot2grid((3, 3), (1, 2), rowspan=2)
# ax4 = plt.subplot2grid((3, 3), (2, 0))
# ax5 = plt.subplot2grid((3, 3), (2, 1))
#
# annotate_axes(fig)
#
# plt.show()



fig = plt.figure(figsize =(10,5))
ax1 = plt.subplot2grid((10, 10), (0, 0), colspan=5, rowspan=10, projection='polar')
ax1.set_theta_zero_location('N')
ax1.set_theta_direction(-1)
ax1.set_xticks([])
ax1.set_yticks([])



ax2 = plt.subplot2grid((10, 10), (1, 6), colspan=5, rowspan=8)
ax2.title.set_size(16)
ax2.title.set_text('Seismograph')
annotate_axes(fig)

plt.show()

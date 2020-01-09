import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def annotate_axes(fig):
    for i, ax in enumerate(fig.axes):
        # ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        ax.tick_params(labelbottom=False, labelleft=False)

fig = plt.figure(figsize =(16,10))
st = fig.suptitle("Inside the Deep Earth", fontsize=20)

ax0 = plt.subplot2grid((10, 16), (1, 1), colspan=2, rowspan=2)
ax0.set_xticks([])
ax0.set_yticks([])

ax1 = plt.subplot2grid((10, 16), (1, 1), colspan=6, rowspan=7, polar=True)
ax1.set_theta_zero_location('N')
ax1.set_theta_direction(-1)
ax1.set_xticks([])
ax1.set_yticks([])

# Axes to add whites space right of plot #1
ax1r = plt.subplot2grid((10, 16), (1, 7), colspan=2, rowspan=10)
ax1r.set_facecolor("red")
# ax1r.axis("off")
ax1r.set_xticks([])
ax1r.set_yticks([])

# Axes to add labels below plot #1
ax1b = plt.subplot2grid((10, 16), (8, 1), colspan=6, rowspan=2)
ax1b.set_facecolor("red")
# ax1b.axis("off")
ax1b.set_xticks([])
ax1b.set_yticks([])

ax2 = plt.subplot2grid((10, 16), (1, 9), colspan=8, rowspan=7)
ax2.title.set_size(16)
ax2.title.set_text('Seismograph')

# Axes to add labels below plot #2
ax2b = plt.subplot2grid((10, 16), (8, 9), colspan=8, rowspan=2)
ax2b.set_facecolor("red")
# ax2b.axis("off")
ax2b.set_xticks([])
ax2b.set_yticks([])

annotate_axes(fig)
plt.tight_layout()
plt.show()

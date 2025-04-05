import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import math


# figure setup
fig = plt.figure(figsize=(8, 8))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, 1)
ax.set_xticks([])
ax.set_ylim(0, 1)
ax.set_yticks([])

# balls setup
balls_pos = np.array([[0.5, 0.5]])
balls_vel = np.array([0.01])
balls_angle = np.array([math.pi / 4])  # int(input())])
balls_size = np.array([128])

# trails
trails_pos = np.array([])

# scatter setup
scat = ax.scatter(
    balls_pos[:, 0],
    balls_pos[:, 1],
    s=balls_size,
)


# MAIN LOOP
def update(frame_number):
    # animate balls
    balls_pos[:, 0] += math.cos(balls_angle) * balls_vel
    balls_pos[:, 1] += math.sin(balls_angle) * balls_vel
    # print(balls_pos[0, :])
    # display balls
    scat.set_offsets(balls_pos)
    scat.set_sizes(balls_size)
    scat.set_facecolors((0, 0, 0, 1))


# build the animation!!
animation = FuncAnimation(fig, update, interval=16)
plt.show()

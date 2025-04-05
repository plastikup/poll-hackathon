import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

tick = 0

# figure setup
fig = plt.figure(figsize=(8, 8))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], frameon=True)
ax.set_xlim(0, 100)
ax.set_xticks([])
ax.set_ylim(0, 100)
ax.set_yticks([])
ax.set_aspect("equal")

# define ball
ball_radius = 1
ball_velocity = 1
ball_angle = math.pi / 2.2
ball = plt.Circle([90, ball_radius], 0, color="black", fill=True, clip_on=False)
ax.add_artist(ball)

# define trails
trails = []
scat = ax.scatter([], [], s=10)


def init():
    ball.set_radius(ball_radius)
    scat.set_facecolors((0, 0, 0, 1))


def animate(_):
    global ball_angle
    global tick

    if tick % 4 == 0:
        trails.append(ball.center)
        scat.set_offsets(trails)

    # cinematics
    ball.center = (
        ball.center[0] + ball_velocity * math.cos(ball_angle),
        ball.center[1] + ball_velocity * math.sin(ball_angle),
    )

    # ball hits borders
    sign = math.cos(ball_angle) * math.sin(ball_angle)
    print(abs(50 - ball.center[0]))
    if abs(50 - ball.center[0]) > 50 - ball_radius:
        # horizontal
        ball.center = (
            100 - ball_radius if ball.center[0] > 50 else ball_radius,
            ball.center[1],
        )
        # reflections
        ball_angle += math.pi / 2 * math.copysign(1, sign)
    if abs(50 - ball.center[1]) > 50 - ball_radius:
        # vertical
        ball.center = (
            ball.center[0],
            100 - ball_radius if ball.center[1] > 50 else ball_radius,
        )
        # reflections
        ball_angle += math.pi / -2 * math.copysign(1, sign)

    tick += 1


ani = animation.FuncAnimation(
    fig, animate, np.arange(0.4, 2, 0.1), init_func=init(), interval=16, blit=False
)
plt.show()

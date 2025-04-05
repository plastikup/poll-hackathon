import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random  # for random ball sizes showcasing our collisions!!

from matplotlib.widgets import Button, Slider

tick = 0
nb_initial_ballz = 10

# figure setup
fig = plt.figure(figsize=(12, 8))
ax = fig.add_axes([0.0, 0.1, 0.8, 0.8], frameon=True)
ax.set_xlim(0, 100)
ax.set_xticks([])
ax.set_ylim(0, 100)
ax.set_yticks([])
ax.set_aspect("equal")

# user interface
nballs_ax = fig.add_axes([0.8, 0.85, 0.15, 0.05])
nballs_slider = Slider(
    nballs_ax, "# of balls", 2, 32, valinit=nb_initial_ballz, valstep=2
)


# define balls yay
class Ball:
    def __init__(self, x, y, r, v, a):
        x = min(max(x, r), 100 - r)
        y = min(max(y, r), 100 - r)

        self.radius = r
        self.velocity = v
        self.angle = a

        self.nx = x
        self.ny = y

        self.b = plt.Circle([x, y], 0, color="black", fill=True, clip_on=False)
        self.b.set_radius(r)
        ax.add_artist(self.b)

    def remove(self):
        self.b.remove()


sack_of_balls = [
    Ball(
        50,
        50,
        random.randrange(4, 12),
        random.randrange(1, 3),
        random.random() * math.pi * 2,
    )
    for _ in range(nb_initial_ballz)
]


# calculate the snap position between two lines while snapping with a given radius
def calc_snap_pos(ball_a, ball_nx, ball_ny, ball_r, wall_a, wall_x, wall_y):
    rc = wall_y - ball_r * math.sqrt(wall_a**2 + 1)
    wm = wall_a - math.tan(ball_a)
    _x = (wall_a * wall_x - math.tan(ball_a) * ball_nx + ball_ny - rc) / (
        wm + (0.0001 if wm == 0 else 0)
    )
    _y = wall_a * (_x - wall_x) + rc
    return _x, _y


# main
def animate(_):
    global tick

    for ball in sack_of_balls:
        # cinematics
        ball.b.center = ball.nx, ball.ny
        ball.nx += ball.velocity * math.cos(ball.angle)
        ball.ny += ball.velocity * math.sin(ball.angle)

        # ball hits balls
        for iball in sack_of_balls:
            if iball == ball:
                continue
            dist = math.sqrt((ball.nx - iball.nx) ** 2 + (ball.ny - iball.ny) ** 2)
            if dist < ball.radius + iball.radius:
                multpl = 1.5

                displacement = (ball.radius + iball.radius) - dist
                angle_to_iball = math.atan2(ball.ny - iball.ny, ball.nx - iball.nx)

                x_displ = displacement / 2 * math.cos(angle_to_iball)
                y_displ = displacement / 2 * math.sin(angle_to_iball)
                ball.nx += x_displ
                ball.ny += y_displ
                ball.angle = math.atan2(
                    math.sin(ball.angle) + y_displ * multpl,
                    math.cos(ball.angle) + x_displ * multpl,
                )

                ix_displ = displacement / -2 * math.cos(angle_to_iball)
                iy_displ = displacement / -2 * math.sin(angle_to_iball)
                iball.nx += ix_displ
                iball.ny += iy_displ
                iball.angle = math.atan2(
                    math.sin(iball.angle) + iy_displ * multpl,
                    math.cos(iball.angle) + ix_displ * multpl,
                )

        # ball hits borders
        if abs(50 - ball.nx) > 50 - ball.radius:
            # horizontal
            if ball.nx > 50:
                ball.nx, ball.ny = calc_snap_pos(
                    ball.angle, ball.nx, ball.ny, -ball.radius, 1000, 100, 0
                )
                ball.nx = min(ball.nx, 99 - ball.radius)
            else:
                ball.nx, ball.ny = calc_snap_pos(
                    ball.angle, ball.nx, ball.ny, ball.radius, 1000, 0, 0
                )
                ball.nx = max(ball.nx, ball.radius + 1)
            # real reflections
            ball.angle = math.pi - ball.angle
        if abs(50 - ball.ny) > 50 - ball.radius:
            # vertical
            if ball.ny > 50:
                ball.nx, ball.ny = calc_snap_pos(
                    ball.angle, ball.nx, ball.ny, ball.radius, 0, 0, 100
                )
                ball.ny = min(ball.ny, 99 - ball.radius)
            else:
                ball.nx, ball.ny = calc_snap_pos(
                    ball.angle, ball.nx, ball.ny, -ball.radius, 0, 0, 0
                )
                ball.ny = max(ball.ny, ball.radius + 1)

            # real reflections
            ball.angle = -ball.angle

    tick += 1


def update(event):
    if nballs_slider.val > len(sack_of_balls):
        sack_of_balls.extend(
            Ball(
                50,
                50,
                random.randrange(4, 12),
                random.randrange(1, 3),
                random.random() * math.pi * 2,
            )
            for _ in range(nballs_slider.val - len(sack_of_balls))
        )
    elif nballs_slider.val < len(sack_of_balls):
        for _ in range(len(sack_of_balls) - nballs_slider.val):
            sack_of_balls.pop().remove()


nballs_slider.on_changed(update)
ani = animation.FuncAnimation(
    fig,
    animate,
    np.arange(0.4, 2, 0.1),
    interval=16,
    blit=False,
)
plt.show()

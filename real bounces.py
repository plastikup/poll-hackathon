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


sack_of_balls = [
    Ball(95, 1, 5, 1, math.pi / 2.2),
    Ball(80, 20, 5, 2, math.pi),
    Ball(40, 1, 5, 2, math.pi / 1.5),
    Ball(0, 0, 10, 1, math.pi / 4),
    Ball(95, 1, 5, 1, math.pi / 2.2),
    Ball(80, 20, 5, 2, math.pi),
    Ball(40, 1, 5, 2, math.pi / 1.5),
    Ball(0, 0, 10, 1, math.pi / 4),
    Ball(95, 1, 5, 1, math.pi / 2.2),
    Ball(80, 20, 5, 2, math.pi),
    Ball(40, 1, 5, 2, math.pi / 1.5),
    Ball(0, 0, 10, 1, math.pi / 4),
    Ball(95, 1, 5, 1, math.pi / 2.2),
    Ball(80, 20, 5, 2, math.pi),
    Ball(40, 1, 5, 2, math.pi / 1.5),
    Ball(0, 0, 10, 1, math.pi / 4),
    Ball(95, 1, 5, 1, math.pi / 2.2),
    Ball(80, 20, 5, 2, math.pi),
    Ball(40, 1, 5, 2, math.pi / 1.5),
    Ball(0, 0, 10, 1, math.pi / 4),
    Ball(95, 1, 5, 1, math.pi / 2.2),
    Ball(80, 20, 5, 2, math.pi),
    Ball(40, 1, 5, 2, math.pi / 1.5),
    Ball(0, 0, 10, 1, math.pi / 4),
    Ball(95, 1, 5, 1, math.pi / 2.2),
    Ball(80, 20, 5, 2, math.pi),
    Ball(40, 1, 5, 2, math.pi / 1.5),
    Ball(0, 0, 10, 1, math.pi / 4),
    Ball(95, 1, 5, 1, math.pi / 2.2),
    Ball(80, 20, 5, 2, math.pi),
    Ball(40, 1, 5, 2, math.pi / 1.5),
    Ball(0, 0, 10, 1, math.pi / 4),
    Ball(95, 1, 5, 1, math.pi / 2.2),
    Ball(80, 20, 5, 2, math.pi),
    Ball(40, 1, 5, 2, math.pi / 1.5),
    Ball(0, 0, 10, 1, math.pi / 4),
    Ball(95, 1, 5, 1, math.pi / 2.2),
    Ball(80, 20, 5, 2, math.pi),
    Ball(40, 1, 5, 2, math.pi / 1.5),
    Ball(0, 0, 10, 1, math.pi / 4),
    Ball(95, 1, 5, 1, math.pi / 2.2),
    Ball(80, 20, 5, 2, math.pi),
    Ball(40, 1, 5, 2, math.pi / 1.5),
    Ball(0, 0, 10, 1, math.pi / 4),
    Ball(95, 1, 5, 1, math.pi / 2.2),
    Ball(80, 20, 5, 2, math.pi),
    Ball(40, 1, 5, 2, math.pi / 1.5),
    Ball(0, 0, 10, 1, math.pi / 4),
]

# define balls trails
trails = []
scat = ax.scatter([], [], s=10)


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
        if tick % 5 == 0:
            trails.append(ball.b.center)
            if len(trails) > 300:
                trails.pop(0)
            scat.set_offsets(trails)

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
                ball.nx = min(ball.nx, 99-ball.radius)
            else:
                ball.nx, ball.ny = calc_snap_pos(
                    ball.angle, ball.nx, ball.ny, ball.radius, 1000, 0, 0
                )
                ball.nx = max(ball.nx, ball.radius+1)
            # real reflections
            ball.angle = math.pi - ball.angle
        if abs(50 - ball.ny) > 50 - ball.radius:
            # vertical
            if ball.ny > 50:
                ball.nx, ball.ny = calc_snap_pos(
                    ball.angle, ball.nx, ball.ny, ball.radius, 0, 0, 100
                )
                ball.ny = min(ball.ny, 99-ball.radius)
            else:
                ball.nx, ball.ny = calc_snap_pos(
                    ball.angle, ball.nx, ball.ny, -ball.radius, 0, 0, 0
                )
                ball.ny = max(ball.ny, ball.radius+1)

            # real reflections
            ball.angle = -ball.angle

    tick += 1


# kickstart our masterpiece!! :D
ani = animation.FuncAnimation(
    fig,
    animate,
    np.arange(0.4, 2, 0.1),
    init_func=(lambda: scat.set_facecolors((0, 0, 0, 1)))(),
    interval=16,
)
plt.show()

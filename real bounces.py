import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.widgets import Button, Slider

tick = 0
DEFAULT_RADIUS = 1
DEFAULT_VEL = 2
DEFAULT_ANGLE = math.pi / 6


# figure setup
fig = plt.figure(figsize=(12, 8))
ax = fig.add_axes([0.0, 0.1, 0.8, 0.8], frameon=True)
ax.set_xlim(0, 100)
ax.set_xticks([])
ax.set_ylim(0, 100)
ax.set_yticks([])
ax.set_aspect("equal")

button_ax = fig.add_axes([0.8, 0.02, 0.15, 0.05])
button = Button(button_ax, "Start", color="0.9" ,hovercolor="0.8")

# nballs_ax = fig.add_axes([0.8, 0.85, 0.15, 0.05])
# nballs_slider = Slider(nballs_ax, "Radius", 1, 10, valinit=1, valstep=1)

radius_ax = fig.add_axes([0.8, 0.85, 0.15, 0.05])
radius_slider = Slider(radius_ax, "Radius", 0.5, 10, valinit=DEFAULT_RADIUS, valstep=0.5)

velocity_ax = fig.add_axes([0.8, 0.75, 0.15, 0.05])
velocity_slider = Slider(velocity_ax, "Velocity", 0.1, 5, valinit=DEFAULT_VEL, valstep=0.1)

angle_ax = fig.add_axes([0.8, 0.65, 0.15, 0.05])
angle_slider = Slider(angle_ax, "Angle (rad)", 0, 2 * math.pi, valinit=DEFAULT_ANGLE)

sack_of_balls = []

# define balls trails
trails = []
scat = ax.scatter([], [], s=10)

ani = None
ball_radius = DEFAULT_RADIUS
ball_velocity = DEFAULT_VEL
ball_angle = DEFAULT_ANGLE


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

# calculate the snap position between two lines while snapping with a given radius
def calc_snap_pos(ball_a, ball_nx, ball_ny, ball_r, wall_a, wall_x, wall_y):
    rc = wall_y - ball_r * math.sqrt(wall_a**2 + 1)
    _x = (wall_a * wall_x - math.tan(ball_a) * ball_nx + ball_ny - rc) / (
        wall_a - math.tan(ball_a)
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

        # ball hits borders
        # sign = math.cos(ball.angle) * math.sin(ball.angle)
        if abs(50 - ball.nx) > 50 - ball.radius:
            # horizontal
            if ball.nx > 50:
                ball.nx, ball.ny = calc_snap_pos(
                    ball.angle, ball.nx, ball.ny, -ball.radius, 1000, 100, 0
                )
            else:
                ball.nx, ball.ny = calc_snap_pos(
                    ball.angle, ball.nx, ball.ny, ball.radius, 1000, 0, 0
                )
            # real reflections
            ball.angle = math.pi - ball.angle
        if abs(50 - ball.ny) > 50 - ball.radius:
            # vertical
            if ball.ny > 50:
                ball.nx, ball.ny = calc_snap_pos(
                    ball.angle, ball.nx, ball.ny, ball.radius, 0, 0, 100
                )
            else:
                ball.nx, ball.ny = calc_snap_pos(
                    ball.angle, ball.nx, ball.ny, -ball.radius, 0, 0, 0
                )
            # real reflections
            ball.angle = -ball.angle

    tick += 1

# kickstart our masterpiece!! :D
def start(event):
    global ani
    global sack_of_balls
    global trails

    for ball in sack_of_balls:
        ball.remove()

    sack_of_balls = [Ball(50, 50, ball_radius, ball_velocity, ball_angle)]
    print(ball_velocity)
    trails = []


    ani = animation.FuncAnimation(
    fig,
    animate,
    np.arange(0.4, 2, 0.1),
    init_func=(lambda: scat.set_facecolors((0, 0, 0, 1)))(),
    interval=16,
    blit=False)

    plt.show()

def update(event):
    global ball_radius
    global ball_velocity
    global ball_angle

    ball_radius = radius_slider.val
    ball_velocity = velocity_slider.val
    ball_angle = angle_slider.val


button.on_clicked(start)
radius_slider.on_changed(update)
velocity_slider.on_changed(update)
angle_slider.on_changed(update)

plt.show()

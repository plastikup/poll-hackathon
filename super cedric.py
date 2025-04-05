import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.widgets import Button, Slider

tick = 0
DEFAULT_RADIUS = 1
DEFAULT_VEL = 2
DEFAULT_ANGLE = math.pi / 6
DEFAULT_XPOS = 50
DEFAULT_YPOS = 50


# figure setup
fig = plt.figure(figsize=(12, 8))
ax = fig.add_axes([0.0, 0.1, 0.8, 0.8], frameon=False)
ax.set_xlim(0, 100)
ax.set_xticks([])
ax.set_ylim(0, 100)
ax.set_yticks([])
ax.set_aspect("equal")


polygon = [[20, 20], [20, 80], [80, 80], [80, 20]]
ax.plot(
    list(map(lambda e: e[0], polygon + [polygon[0]])),
    list(map(lambda e: e[1], polygon + [polygon[0]])),
    "black",
)


button_ax = fig.add_axes([0.775, 0.1, 0.15, 0.05])
button = Button(button_ax, "Start", color="0.9", hovercolor="0.8")

radius_ax = fig.add_axes([0.775, 0.85, 0.15, 0.05])
radius_slider = Slider(
    radius_ax, "Radius", 0.5, 10, valinit=DEFAULT_RADIUS, valstep=0.5
)

velocity_ax = fig.add_axes([0.775, 0.75, 0.15, 0.05])
velocity_slider = Slider(
    velocity_ax, "Velocity", 0.1, 5, valinit=DEFAULT_VEL, valstep=0.1
)

angle_ax = fig.add_axes([0.775, 0.65, 0.15, 0.05])
angle_slider = Slider(angle_ax, "Angle (rad)", 0, 2 * math.pi, valinit=DEFAULT_ANGLE)

xpos_ax = fig.add_axes([0.775, 0.55, 0.15, 0.05])
xpos_slider = Slider(xpos_ax, "X position", 0, 100, valinit=DEFAULT_XPOS)

ypos_ax = fig.add_axes([0.775, 0.45, 0.15, 0.05])
ypos_slider = Slider(ypos_ax, "Y position", 0, 100, valinit=DEFAULT_YPOS)

polygon_ax = fig.add_axes([0.775, 0.35, 0.15, 0.05])
polygon_slider = Slider(polygon_ax, "Polygon", 3, 5, valinit=4, valstep=1)

sack_of_balls = []

# define balls trails
trails = []
scat = ax.scatter([], [], s=10)

ani = None
ball_radius = DEFAULT_RADIUS
ball_velocity = DEFAULT_VEL
ball_angle = DEFAULT_ANGLE
ball_xpos = DEFAULT_XPOS
ball_ypos = DEFAULT_YPOS


# define balls yay
class Ball:
    def __init__(self, x, y, r, v, a, color):
        x = min(max(x, r), 100 - r)
        y = min(max(y, r), 100 - r)

        self.radius = r
        self.velocity = v
        self.angle = a

        self.nx = x
        self.ny = y

        self.b = plt.Circle([x, y], 0, color=color, fill=True, clip_on=False)
        self.b.set_radius(r)
        ax.add_artist(self.b)

        self.delay_log = False

        self.ox = x
        self.oy = y

    def remove(self):
        self.b.remove()


def calc_next_point(corner_list, x_pos, y_pos, angle, v):
    vx = v * math.cos(angle)
    vy = v * math.sin(angle)
    for i in range(len(corner_list)):
        x1, y1 = corner_list[i - 1]
        x2, y2 = corner_list[i]

        # Déterminant de la matrice d'équations
        det = ((x2 - x1) * vy) - ((y2 - y1) * vx)
        t = ((x_pos - x1) * vy - (y_pos - y1) * vx) / det
        s = ((x_pos - x1) * (y2 - y1) - (y_pos - y1) * (x2 - x1)) / det

        # x_point, y_point = x_pos + t*math.cos(angle), y_pos + t*math.sin(angle)
        x_point = x1 + ((((x_pos - x1) * vy) - ((y_pos - y1) * vx)) / det) * (x2 - x1)
        y_point = y1 + ((((x_pos - x1) * vy) - ((y_pos - y1) * vx)) / det) * (y2 - y1)

        if 0 <= t <= 1 and s >= 0:
            return (
                x_point,
                y_point,
                2 * math.atan2(y2 - y1, x2 - x1) - angle,
                v,
            )


def calc_n_bounce(corner_list, x_pos, y_pos, angle, v, n):
    if n == 0:
        return []
    else:
        # Appel à calc_next_point
        new_x, new_y, new_angle, new_v = calc_next_point(
            corner_list, x_pos, y_pos, angle, v
        )

        # Résultat courant
        current = (new_x, new_y, new_angle, new_v)

        # Appel récursif
        rest = calc_n_bounce(corner_list, new_x, new_y, new_angle, new_v, n - 1)

        return [current] + rest


# calculate the snap position between two lines while snapping with a given radius
def calc_snap_pos(ball_a, ball_nx, ball_ny, ball_r, wall_a, wall_x, wall_y):
    rc = wall_y - ball_r * math.sqrt(wall_a**2 + 1)
    wm = wall_a - math.tan(ball_a)
    _x = (wall_a * wall_x - math.tan(ball_a) * ball_nx + ball_ny - rc) / (
        wm + (0.0001 if wm == 0 else 0)
    )
    _y = wall_a * (_x - wall_x) + rc
    return _x, _y


prediction = plt.Circle([0, 0], 0, color="green", fill=True, clip_on=False)
prediction.set_radius(2)
ax.add_artist(prediction)


# main
def animate(_):
    global tick

    for ball in sack_of_balls:
        if tick % 5 == 0:
            trails.append(ball.b.center)
        if len(trails) > 300:
            trails.pop(0)
            scat.set_offsets(trails)

        if ball.delay_log:
            ball.ox, ball.oy = ball.nx, ball.ny

        pred_x, pred_y, rebound, _ = calc_next_point(
            polygon,
            ball.ox,
            ball.oy,
            ball.angle,
            ball.velocity,
        )
        prediction.center = [pred_x, pred_y]
        print("ox", ball.ox, ball.angle)
        print("pred", pred_x, pred_y)

        # cinematics
        ball.b.center = ball.nx, ball.ny
        ball.nx += ball.velocity * math.cos(ball.angle)
        ball.ny += ball.velocity * math.sin(ball.angle)

        # collision with border
        if (
            min(ball.b.center[0], ball.nx) < pred_x < max(ball.b.center[0], ball.nx)
        ) and (
            min(ball.b.center[1], ball.ny) < pred_y < max(ball.b.center[1], ball.ny)
        ):
            ball.nx, ball.ny = pred_x, pred_y
            ball.angle = rebound
            ball.delay_log = True
    tick += 1


# kickstart our masterpiece!! :D
def start(event):
    global ani
    global sack_of_balls
    global trails

    for ball in sack_of_balls:
        ball.remove()

    vis_ball.b.set_visible(False)

    sack_of_balls = [
        Ball(ball_xpos, ball_ypos, ball_radius, ball_velocity, ball_angle, "black")
    ]
    trails = []

    try:
        ani._stop()
    except:
        print("LOL")

    ani = animation.FuncAnimation(
        fig,
        animate,
        np.arange(0.4, 2, 0.1),
        init_func=(lambda: scat.set_facecolors((0, 0, 0, 1)))(),
        interval=16,
        blit=False,
    )

    plt.show()


def update(event):
    global ball_radius
    global ball_velocity
    global ball_angle
    global ball_xpos
    global ball_ypos
    global vis_ball

    vis_ball.remove()
    ball_radius = radius_slider.val
    ball_velocity = velocity_slider.val
    ball_angle = angle_slider.val
    ball_xpos = xpos_slider.val
    ball_ypos = ypos_slider.val
    vis_ball = Ball(ball_xpos, ball_ypos, ball_radius, ball_velocity, ball_angle, "red")


def change_shape(event):
    global polygon

    polygon = {
        3: [(50.0, 100.0), (6.698729810778069, 25.0), (93.30127018922192, 25.0)],
        4: [
            (85.35533905932738, 85.35533905932738),
            (14.64466094067263, 85.35533905932738),
            (14.644660940672615, 14.64466094067263),
            (85.35533905932738, 14.644660940672615),
        ],
        5: [
            (50.0, 100.0),
            (2.447174185242325, 65.45084971874738),
            (19.09830056250527, 11.112360400844446),
            (80.90169943749473, 11.11236040084443),
            (97.55282581475768, 65.45084971874736),
        ],
    }[polygon_slider.val]
    ax.plot(
        list(map(lambda e: e[0], polygon + [polygon[0]])),
        list(map(lambda e: e[1], polygon + [polygon[0]])),
        "black",
    )


vis_ball = Ball(
    DEFAULT_XPOS, DEFAULT_YPOS, DEFAULT_RADIUS, DEFAULT_VEL, DEFAULT_ANGLE, "red"
)

button.on_clicked(start)
radius_slider.on_changed(update)
velocity_slider.on_changed(update)
angle_slider.on_changed(update)
xpos_slider.on_changed(update)
ypos_slider.on_changed(update)
polygon_slider.on_changed(change_shape)

plt.show()

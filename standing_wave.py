import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
import matplotlib.animation as animation

now_wall_x = 20
now_source_x = 0
now_t = 0
u = 5  # 波速
w = 5  # 角速度
gs = 8  # 初始Φ的分子
gx = 16  # 初始Φ的分母
A = 20  # 振幅
wall_type = True  # 墙的种类，0没有半波损失，1有
now_start = False


class Wave:
    def __init__(self, source_x, wall_x):
        # 属性分配
        self.source_x = source_x
        self.wall_x = wall_x
        self.x = np.linspace(source_x, source_x, 300)
        self.y = None
        self.x_fan = np.linspace(wall_x, wall_x, 300)
        self.y_fan = None

    def cal_y(self, t):
        now_x = self.source_x + u * t
        t2 = 0
        have_fan = False
        if now_x >= self.wall_x:
            now_x = self.wall_x
            t2 = t - (self.wall_x - self.source_x) / u
            have_fan = True
        x_fan = 0
        if have_fan:
            x_fan = self.wall_x - t2 * u
            if x_fan <= self.source_x:
                x_fan = self.source_x
                self.x_fan = np.linspace(self.source_x, self.wall_x, 300)
            else:
                self.x_fan = np.linspace(self.wall_x - t2 * u, self.wall_x, 300)
        self.x = np.linspace(self.source_x, now_x, 300)
        if not have_fan:
            self.y = A * np.cos(w * (t - self.x / u) + gs / gx * np.pi)
        else:
            wave_y = A * np.cos(w * (t - self.x / u) + gs / gx * np.pi)
            wave_y_fan = None
            if wall_type:
                wave_y_fan = np.where(self.x >= x_fan,
                                      A * np.cos(w * (t - (2 * self.wall_x - self.x) / u) + gs / gx * np.pi), 0)
            else:
                wave_y_fan = np.where(self.x >= x_fan,
                                      A * np.cos(w * (t - (2 * self.wall_x - self.x) / u) + gs / gx * np.pi + np.pi), 0)
            self.y = wave_y_fan + wave_y


fig, ax = plt.subplots()
fig.set_size_inches(14, 7)
button1 = None
button2 = None
button3 = None
button4 = None
button5 = None
button6 = None
button7 = None
button8 = None
button9 = None
button10 = None


def init():
    global button1
    global button2
    global button3
    global button4
    global button5
    global button6
    global button7
    global button8
    global button9
    global button10
    global ani
    fig.tight_layout(rect=[0.2, 0, 1, 1])

    init_ys = 0.937
    init_yx = 0.917
    button1_ax = plt.axes((0.125, init_ys, 0.015, 0.016))  # 按钮的位置和大小
    button1 = Button(button1_ax, '+')
    button1.on_clicked(on_button1_clicked)
    button2_ax = plt.axes((0.125, init_yx, 0.015, 0.016))  # 按钮的位置和大小
    button2 = Button(button2_ax, '-')
    button2.on_clicked(on_button2_clicked)
    button3_ax = plt.axes((0.125, init_ys - 0.055 * 1, 0.015, 0.016))  # 按钮的位置和大小
    button3 = Button(button3_ax, '+')
    button3.on_clicked(on_button3_clicked)
    button4_ax = plt.axes((0.125, init_yx - 0.055 * 1, 0.015, 0.016))  # 按钮的位置和大小
    button4 = Button(button4_ax, '-')
    button4.on_clicked(on_button4_clicked)
    button5_ax = plt.axes((0.125, init_ys - 0.055 * 2, 0.015, 0.016))  # 按钮的位置和大小
    button5 = Button(button5_ax, '+')
    button5.on_clicked(on_button5_clicked)
    button6_ax = plt.axes((0.125, init_yx - 0.055 * 2, 0.015, 0.016))  # 按钮的位置和大小
    button6 = Button(button6_ax, '-')
    button6.on_clicked(on_button6_clicked)
    button7_ax = plt.axes((0.125, init_ys - 0.055 * 3, 0.015, 0.016))  # 按钮的位置和大小
    button7 = Button(button7_ax, '+')
    button7.on_clicked(on_button7_clicked)
    button8_ax = plt.axes((0.125, init_yx - 0.055 * 3, 0.015, 0.016))  # 按钮的位置和大小
    button8 = Button(button8_ax, '-')
    button8.on_clicked(on_button8_clicked)
    button9_ax = plt.axes((0.125, init_yx - 0.055 * 4, 0.015, 0.036))  # 按钮的位置和大小
    button9 = Button(button9_ax, '●')
    button9.on_clicked(on_button9_clicked)
    button10_ax = plt.axes((0.05, init_yx - 0.055 * 10, 0.07, 0.05))  # 按钮的位置和大小
    button10 = Button(button10_ax, 'Restart')
    button10.on_clicked(on_button10_clicked)
    draw_wave(None)
    plt.show()


wave = Wave(now_source_x, now_wall_x)
num = 0


def draw_wave(frame):
    global now_t
    global num
    ax.clear()
    ax.set_xlim(-1.5, 31.5)
    ax.set_ylim(-65.5, 65.5)
    ax.annotate("\n" * 300, (0, 0), xytext=(-4, -100),
                bbox=dict(boxstyle='square,pad=0.3', fc='grey', alpha=1, linewidth=0.1), fontsize=4)
    wave.cal_y(now_t)
    ax.plot(wave.x, wave.y)
    if wall_type:
        ax.plot([now_wall_x, now_wall_x], [-60, 60], color='red', linewidth=2)
    else:
        ax.plot([now_wall_x, now_wall_x], [-60, 60], color='black', linewidth=2)
    ax.plot([now_source_x, now_source_x], [-60, 60], color='green', linewidth=2)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.plot(0, 0)
    ax.plot(0, 60)
    ax.plot(0, -60)
    ax.plot(30, 0)
    ax.plot(30, 60)
    num += 1
    now_t += 0.04
    ax.text(-10, 60, "ω / rad*s^-1", fontsize=10, ha='center')
    ax.text(-10, 52, "μ / m*s^-1", fontsize=10, ha='center')
    ax.text(-10, 44, "Φ / rad", fontsize=10, ha='center')
    ax.text(-10, 36, "A / cm", fontsize=10, ha='center')
    ax.text(-10, 28, "wall type", fontsize=10, ha='center')
    ax.text(-8, -10, "The range of angular velocity is\n1-15\n"
                     "the range of wave velocity is\n1-15\n"
                     "the range of initial phase is\n0π-31/16π\n"
                     "the range of amplitude is\n5-30 cm\n"
                     "The types of walls are categorized as\ndense medium and rare medium.", fontsize=9, ha='center')
    ax.text(-8, -45, "This system demonstrates\n"
                     "the process of standing wave\n"
                     "formation by the superposition of\n"
                     "reflected waves and incident waves\n"
                     "when waves encounter a wall.\n", fontsize=9, ha='center')
    ax.text(-8, - 55, "Note: Full-screen mode\n"
                      "may cause lagging.", fontsize=10, ha='center')
    # 添加带有框的文本框
    ax.annotate(" " * (9 - int(w / 10) * 2) + str(w), (0, 0), xytext=(-8, 60),
                bbox=dict(boxstyle='square,pad=0.3', fc='lightgrey', alpha=1, linewidth=0.5), fontsize=10)
    ax.annotate(" " * (9 - int(u / 10) * 2) + str(u), (0, 0), xytext=(-8, 52),
                bbox=dict(boxstyle='square,pad=0.3', fc='lightgrey', alpha=1, linewidth=0.5), fontsize=10)
    ax.annotate(" " * (2 - int(gs / 10) * 2) + str(gs) + "/16π", (0, 0), xytext=(-8, 44),
                bbox=dict(boxstyle='square,pad=0.3', fc='lightgrey', alpha=1, linewidth=0.5), fontsize=10)
    ax.annotate(" " * (9 - (len(str(A)) - 1) * 2) + str(A), (0, 0), xytext=(-8, 36),
                bbox=dict(boxstyle='square,pad=0.3', fc='lightgrey', alpha=1, linewidth=0.5), fontsize=10)
    if wall_type:
        ax.annotate(" " * (9 - (len("dense") - 1) * 2) + "dense", (0, 0), xytext=(-8, 28),
                    bbox=dict(boxstyle='square,pad=0.3', fc='lightgrey', alpha=1, linewidth=0.5), fontsize=10)
    else:
        ax.annotate(" " * (9 - (len("rare") - 1) * 2) + "rare", (0, 0), xytext=(-8, 28),
                    bbox=dict(boxstyle='square,pad=0.3', fc='lightgrey', alpha=1, linewidth=0.5), fontsize=10)


def on_button1_clicked(event):
    global now_t
    global w
    now_t = 0
    w += 1
    if w > 15:
        w = 1


def on_button2_clicked(event):
    global now_t
    global w
    now_t = 0
    w -= 1
    if w < 0:
        w = 15


def on_button3_clicked(event):
    global now_t
    global u
    now_t = 0
    u += 1
    if u > 15:
        u = 1


def on_button4_clicked(event):
    global now_t
    global u
    now_t = 0
    u -= 1
    if u < 1:
        u = 15


def on_button5_clicked(event):
    global now_t
    global gs
    now_t = 0
    gs += 1
    if gs > 31:
        gs = 0


def on_button6_clicked(event):
    global now_t
    global gs
    now_t = 0
    gs -= 1
    if gs < 0:
        gs = 31


def on_button7_clicked(event):
    global now_t
    global A
    now_t = 0
    A += 5
    if A > 30:
        A = 5


def on_button8_clicked(event):
    global now_t
    global A
    now_t = 0
    A -= 5
    if A < 5:
        A = 30


def on_button9_clicked(event):
    global now_t
    global wall_type
    now_t = 0
    wall_type = not wall_type


def on_button10_clicked(event):
    global now_t
    now_t = 0
    global now_start
    now_start = True


def main():
    global ani
    ani = animation.FuncAnimation(fig, draw_wave, frames=100, interval=100)
    init()


if __name__ == '__main__':
    main()

import pygame as pg
import math
import numpy as np


def translate(vector, x=0, y=0, z=0):
    t = np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])

    new_vec = np.dot(t, vector)

    return new_vec


def scaled(vector, n):
    s = np.array([
        [n, 0, 0, 0],
        [0, n, 0, 0],
        [0, 0, n, 0],
        [0, 0, 0, 1]
    ])

    new_vector = np.dot(s, vector)
    return new_vector


def rotate(vector, deg_x=0, deg_y=0, deg_z=0):
    x_axis = np.array([
        [1, 0, 0, 0],
        [0, math.cos(deg_x), math.sin(deg_x), 0],
        [0, -math.sin(deg_x), math.cos(deg_x), 0],
        [0, 0, 0, 1]
    ])

    y_axis = np.array([
        [math.cos(deg_y), 0, -math.sin(deg_y), 0],
        [0, 1, 0, 0],
        [math.sin(deg_y), 0, math.cos(deg_y), 0],
        [0, 0, 0, 1]
    ])

    z_axis = np.array([
        [math.cos(deg_z), -math.sin(deg_z), 0, 0],
        [math.sin(deg_z), math.cos(deg_z), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    x = np.dot(vector, x_axis)
    y = np.dot(x, y_axis)
    z = np.dot(y, z_axis)

    return z


def shear(vector, n):
    sh = np.array([
        [n*2, 0, 0, 0],
        [0, n*2, 0, 0],
        [0, 0, 1, 0],
        [0, 0, -1, 0]
    ])

    return np.dot(sh, vector)


points = [i for i in range(8)]

points[0] = [-1, -1, 1, 1]
points[1] = [1, -1, 1, 1]
points[2] = [1, 1, 1, 1]
points[3] = [-1, 1, 1, 1]
points[4] = [-1, -1, -1, 1]
points[5] = [1, -1, -1, 1]
points[6] = [1, 1, -1, 1]
points[7] = [-1, 1, -1, 1]


pg.init()

clock = pg.time.Clock()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)


WIDTH = 500
HEIGHT = 500

cx = WIDTH//2
cy = HEIGHT//2
cz = 1

angle_x = angle_y = angle_z = 0

scale = 50

win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("3D Projection and Transformation")


def connect_points(i, j, point):
    pg.draw.line(win, WHITE, (point[i][0], point[i][1]), (point[j][0], point[j][1]), 1)


def project_2d(vector):
    projection = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0]
    ])

    projected = np.dot(projection, vector)

    return projected


def cube(color, set_vertices=True, set_edges=False):
    line_points = [0 for _ in range(len(points))]
    inx = 0
    for i in range(len(points)):
        rx = rotate(points[i], angle_x, angle_y, angle_z)
        shr = shear(rx, 0.5)
        x = shr[0] + cx
        y = shr[1] + cy

        if set_vertices is True:
            pg.draw.circle(win, color, (x, y), 2)

        line_points[inx] = (x, y)
        inx += 1

    if set_edges is True:
        connect_points(0, 1, line_points)
        connect_points(0, 3, line_points)
        connect_points(0, 4, line_points)
        connect_points(1, 2, line_points)
        connect_points(1, 5, line_points)
        connect_points(2, 6, line_points)
        connect_points(2, 3, line_points)
        connect_points(3, 7, line_points)
        connect_points(4, 5, line_points)
        connect_points(4, 7, line_points)
        connect_points(6, 5, line_points)
        connect_points(6, 7, line_points)


def main():
    global angle_y, angle_z, angle_x
    global scale
    global cx, cy, cz

    run = True

    while run:
        # mx, my = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        keys = pg.key.get_pressed()

        if keys[pg.K_ESCAPE]:
            run = False

        win.fill(BLACK)
        win.blit(win, (50, 50))

        if keys[pg.K_UP]:
            cy -= 1

        if keys[pg.K_DOWN]:
            cy += 1

        if keys[pg.K_RIGHT]:
            cx += 1

        if keys[pg.K_LEFT]:
            cx -= 1

        if keys[pg.K_f]:
            cz += 0.1

        if keys[pg.K_b]:
            cz -= 0.1

        if keys[pg.K_UP] and keys[pg.K_r]:
            angle_x -= 0.01

        if keys[pg.K_DOWN] and keys[pg.K_r]:
            angle_x += 0.01

        if keys[pg.K_RIGHT] and keys[pg.K_r]:
            angle_y += 0.01

        if keys[pg.K_LEFT] and keys[pg.K_r]:
            angle_y -= 0.01

        if keys[pg.K_s] and keys[pg.K_UP]:
            scale += 1

        if keys[pg.K_s] and keys[pg.K_DOWN]:
            scale -= 1

        cube(color=GREEN, set_edges=True)

        pg.display.update()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()

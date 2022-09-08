import pygame as pg
import math
import numpy as np

# function for rotating a 3D cube
def rotate(vector, deg_x=0, deg_y=0, deg_z=0):
    # for x-axis, we use cos and for y-axis we use sin

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

    # Getting rotation for all axis
    x = np.dot(vector, x_axis)
    y = np.dot(x, y_axis)
    z = np.dot(y, z_axis)

    return z

# A matrix for generating a cube
points = [i for i in range(8)]

points[0] = [-1, -1, 1, 1]
points[1] = [1, -1, 1, 1]
points[2] = [1, 1, 1, 1]
points[3] = [-1, 1, 1, 1]
points[4] = [-1, -1, -1, 1]
points[5] = [1, -1, -1, 1]
points[6] = [1, 1, -1, 1]
points[7] = [-1, 1, -1, 1]

# Initializing pygame
pg.init()

# defines frames per second
clock = pg.time.Clock()

# RGB colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Aspect Ratio of screen
WIDTH = 500
HEIGHT = 500

# Position of cube
cx = WIDTH//2
cy = HEIGHT//2
cz = 1

# angle of cube
angle_x = angle_y = angle_z = 0

# scale object
scale = 50

win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("3D Projection and Transformation")

# for connecting vertices
def connect_points(i, j, point):
    pg.draw.line(win, WHITE, (point[i][0], point[i][1]), (point[j][0], point[j][1]), 1)

# for creating a cube
def cube(color, set_vertices=True, set_edges=False):

    # for storing points/vertices
    line_points = [0 for _ in range(len(points))]

    # index for line_points list
    inx = 0

    for i in range(len(points)):
        # this gives a rotated vector [x y z 1]
        rx = rotate(points[i], angle_x, angle_y, angle_z)

        # scaling and translating only the x & y vertices
        x = scale*rx[0] + cx
        y = scale*rx[1] + cy

        # To show vertices
        # if the argument is false then it will only show the connected lines
        if set_vertices is True:
            pg.draw.circle(win, color, (x, y), 2)

        # storing vertices for connecting lines
        line_points[inx] = (x, y)
        inx += 1

    # To show connected lines
    # if the argument is false then it only shows the vertices
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

# Main
def main():
    # Global variables
    global angle_y, angle_z, angle_x
    global scale
    global cx, cy, cz

    # for running program
    run = True

    while run:
        # mx, my = pg.mouse.get_pos()

        # if the event is triggered
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        # if any key is pressed
        keys = pg.key.get_pressed()

        # Breaks the loop an exits program
        if keys[pg.K_ESCAPE]:
            run = False

        # Background color and position of window
        win.fill(BLACK)
        win.blit(win, (50, 50))

        # decrement Y-axis and moves object downwards
        if keys[pg.K_UP]:
            cy -= 1

        # increment Y-axis and moves object upwards
        if keys[pg.K_DOWN]:
            cy += 1

        # increment X-axis and moves object to the right
        if keys[pg.K_RIGHT]:
            cx += 1

        # decrement X-axis and moves object to the left
        if keys[pg.K_LEFT]:
            cx -= 1

        # Rotates object on X-axis anticlockwise
        if keys[pg.K_UP] and keys[pg.K_r]:
            angle_x -= 0.01

        # Rotates object on X-axis clockwise
        if keys[pg.K_DOWN] and keys[pg.K_r]:
            angle_x += 0.01

        # Rotates object on Y-axis clockwise
        if keys[pg.K_RIGHT] and keys[pg.K_r]:
            angle_y += 0.01

        # Rotates object on Y-axis anticlockwise
        if keys[pg.K_LEFT] and keys[pg.K_r]:
            angle_y -= 0.01

        # Scales up object
        if keys[pg.K_s] and keys[pg.K_UP]:
            scale += 1

        # Scales down object
        if keys[pg.K_s] and keys[pg.K_DOWN]:
            scale -= 1

        # function for generating a cube
        cube(color=GREEN, set_edges=True)

        # updates the screen
        pg.display.update()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()

import pygame as pg
import math

pg.init()

clock = pg.time.Clock()

# RGB colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Screen size
WIDTH = 500
HEIGHT = 500

# Horizontal frustum
h_f = math.pi/2

# Vertical frustum
v_f = h_f * (HEIGHT/WIDTH)

# Coordinates X and Y
cx = 0
cy = 0

# Ray angle
ray_angle = 0

# Create Screen
win = pg.display.set_mode((WIDTH, HEIGHT))

# Window Title
pg.display.set_caption("Ray Casting Algorithm")

# 2D Map Size
map_size = 5

# Blocks size
tile_size = 100

# Depth of rays
max_depth = HEIGHT

# Total number of rays
total_rays = 120

# Angle of rays
angle_step = h_f / total_rays


# Main ray casting algorithm
def caste_rays(pos_x, pos_y):
    # starting angle of ray
    start_angle = ray_angle - h_f

    for i in range(total_rays):
        for d in range(max_depth):
            # This displays the rays about given angle
            # This also extends th rays by multiplying with depth
            target_x = pos_x - math.sin(start_angle) * d
            target_y = pos_y + math.cos(start_angle) * d

            # Drawing lines from player position to end points
            pg.draw.line(win, YELLOW, (pos_x, pos_y), (target_x, target_y), 1)

            # Calculating row & column of box/tile
            row = target_x//tile_size
            col = target_y//tile_size

            # if the row and column value is equal to box/tile values
            if row % 2 == 1 and col % 2 == 1:
                # this turns the box in green color when rays are casted
                pg.draw.rect(win, GREEN, (row*tile_size, col*tile_size, tile_size, tile_size))
                break

        # increments angle
        start_angle += angle_step


# function for creating map
def create_map(size, box_size):
    for i in range(size):
        for j in range(size):
            if i % 2 == 0 or j % 2 == 0:
                continue
            r1 = pg.Rect(i*box_size, j*box_size, box_size, box_size)
            pg.draw.rect(win, WHITE, r1, 1)


def main():
    global ray_angle
    run = True

    while run:
        win.fill(BLACK)
        win.blit(win, (50, 50))

        # gets current mouse position
        mx, my = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        # gets keys that are pressed
        keys = pg.key.get_pressed()

        if keys[pg.K_ESCAPE]:
            run = False

        # decreases ray angle
        if keys[pg.K_UP] and keys[pg.K_r]:
            ray_angle -= 0.1

        # increases ray angle
        if keys[pg.K_DOWN] and keys[pg.K_r]:
            ray_angle += 0.1

        create_map(map_size, tile_size)
        pg.draw.circle(win, RED, (mx, my), 5)
        caste_rays(mx, my)

        pg.display.update()

        # Frames per second
        clock.tick(30)


if __name__ == "__main__":
    main()

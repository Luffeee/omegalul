import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import asyncio
import websockets
import threading


async def server(websocket, path):
    async for message in websocket:
        with open("output.txt", 'w') as f:
            f.write(message)


def start_server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    start_server = websockets.serve(server, "192.168.0.102", 3000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def cm2px(cm):
    return int(-9 + cm*1)


def draw_cube():
    vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
    )

    edges = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7)
    )

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def draw_wall(cube_pos):
    cube_x, cube_y, cube_z = cube_pos
    wall_x = -10
    wall_height = 15
    wall_width = 0.2

    glBegin(GL_QUADS)
    glColor3fv((0.5, 0.5, 0.5))
    glVertex3fv((wall_x, cube_y - wall_height / 2,
                cube_z + wall_width / 2))
    glVertex3fv((wall_x, cube_y - wall_height / 2,
                cube_z - wall_width / 2))
    glVertex3fv((wall_x, cube_y + wall_height / 2,
                cube_z - wall_width / 2))
    glVertex3fv((wall_x, cube_y + wall_height / 2,
                cube_z + wall_width / 2))
    glEnd()

    return (wall_x, wall_x, cube_y - wall_height / 2, cube_y + wall_height / 2, cube_z - wall_width / 2, cube_z + wall_width / 2)


def is_colliding(cube_pos, wall_bounds):
    cube_x, cube_y, cube_z = cube_pos
    wall_bounds = -10

    if (cube_x <= wall_bounds+1):
        return True
    return False


def main():
    last_px = 0
    last_i = 0
    threading.Thread(target=start_server, daemon=True).start()
    with open('output.txt', 'r') as f:
        try:
            i = int(f.readline().strip())
            last_i = i
        except:
            i = last_i
    px = cm2px(i)
    f.close()
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -20)

    cube_position = [px, 0, 0]
    camera_angle = [0, 0]
    camera_position = [0, 0, -5]
    mouse_dragging = False
    last_mouse_pos = (0, 0)

    while True:
        with open('output.txt', 'r') as f:
            try:
                i = int(f.readline().strip())
                last_i = i
            except:
                i = last_i
        px = cm2px(i)
        f.close()
        cube_position = [px, 0, 0]

        last_px = px

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_dragging = True
                    last_mouse_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if mouse_dragging:
                    x, y = event.pos
                    dx = x - last_mouse_pos[0]
                    dy = y - last_mouse_pos[1]
                    last_mouse_pos = (x, y)
                    camera_angle[0] += dy * 0.1
                    camera_angle[1] += dx * 0.1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            cube_position[2] -= 0.1
        if keys[pygame.K_UP]:
            cube_position[2] += 0.1
        if keys[pygame.K_a]:
            cube_position[0] -= 0.1
        if keys[pygame.K_d]:
            cube_position[0] += 0.1
        if keys[pygame.K_RIGHT]:
            camera_position[0] -= 0.1
        if keys[pygame.K_LEFT]:
            camera_position[0] += 0.1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glTranslatef(*camera_position)
        glRotatef(camera_angle[0], 1, 0, 0)
        glRotatef(camera_angle[1], 0, 1, 0)
        wall_bounds = draw_wall(cube_position)

        if is_colliding(cube_position, wall_bounds):
            cube_position = [-9, 0, 0]
            print("Collision Detected!")

        glTranslatef(*cube_position)
        draw_cube()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()

import pygame
import pymunk
from sys import exit

pygame.init()

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 800

# pygame setup variables
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption("Double Pyndulum")
clock = pygame.time.Clock()
FPS = 50

# pymunk variables
space = pymunk.Space()
space.gravity = (0, -900)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 255, 0)
YELLOW = (235, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (200, 0, 255)

color_list = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

# fonts
selected_font = pygame.font.Font('assets/font.ttf',
                                 30)  # https://fonts.google.com/specimen/Inconsolata


def convert_coords(point):  # convert to int, transform to pygame y convention
    return int(point[0]), int(SCREEN_HEIGHT - point[1])


def render_text(text, position, color=BLACK):
    rendered_text = selected_font.render(text, True, color)
    screen.blit(rendered_text, position)


def print_fps():
    render_text(str(f'FPS: {int(clock.get_fps())}'), (10, 10))  # https://stackoverflow.com/questions/67946230/show-fps-in-pygame


class PendulumConnector:
    def __init__(self, body, link, link_type='body'):
        self.body = body
        if link_type == 'body':
            self.link = link
        elif link_type == 'static_body':
            self.link = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.link.position = link
        joint = pymunk.PinJoint(self.body, self.link)
        joint.collide_bodies = False
        space.add(joint)

    def draw(self):
        pos1 = convert_coords(self.body.position)
        pos2 = convert_coords(self.link.position)
        pygame.draw.aaline(screen, BLACK, pos1, pos2, 5)
        pygame.draw.circle(screen, BLACK, convert_coords(self.link.position), 5)


class PendulumPoint:
    def __init__(self, x, y, number):
        # pymunk properties
        self.body = pymunk.Body()
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, 10)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.collision_type = 2

        self.radius = 10
        self.color = color_list[number]

        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.circle(screen, self.color, convert_coords(self.body.position), self.radius)

class Pendulum:
    def __init__(self, x1, y1, x2, y2, number, x3=(SCREEN_WIDTH // 2), y3=(SCREEN_HEIGHT // 2), mode=0):
        self.pend_point1 = PendulumPoint(x1, y1, number)
        self.pend_point2 = PendulumPoint(x2, y2, number + 4)
        self.pend_conn1 = PendulumConnector(self.pend_point1.body, (x3, y3), link_type='static_body')
        self.pend_conn2 = PendulumConnector(self.pend_point1.body, self.pend_point2.body, link_type='body')
        self.mode = mode

    def draw(self):
        if self.mode == 1:
            self.pend_conn1.draw()
            self.pend_conn2.draw()
        self.pend_point1.draw()
        self.pend_point2.draw()


# TODO scrap all of this fn, replace with modifying the class properties instead
# def initialize_pendulums():
#     global pendulum1
#     pendulum1 = Pendulum(200, 500, 300, 500, 0)
#     global pendulum2
#     pendulum2 = Pendulum(200, 500, 390, 510, 1)
#     global pendulum_group
#     pendulum_group = []
#     pendulum_group = [pendulum1, pendulum2]
#
# #initialize_pendulums()

pendulum1 = Pendulum(200, 500, 300, 700, number=1, mode=1)

pendulum_group = [pendulum1]

click_counter = 1  # tracks odd and even clicks to generate new pendulums
run = True
play = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # pause and play button
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play = not play
            if event.key == pygame.K_a and FPS > 0:
                FPS -= 1
                print(f'FPS decreased to {FPS}')
            if event.key == pygame.K_d:
                FPS += 1
                print(f'FPS increased to {FPS}')
            if event.key == pygame.K_r:
                #initialize_pendulums()
                print(f'Pendulums reset')
                # TODO Implement interactive pendulam mechanic
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     print("click")
        #     pos1 = pygame.mouse.get_pos()
        #     pos2 = (-1, -1)
        #     while pos2 == (-1, -1):
        #         print(f'{pos2}')
        #         for subevent in pygame.event.get():
        #             if event.type == pygame.MOUSEBUTTONDOWN:
        #                 pos2 = pygame.mouse.get_pos()
        #     pendulum = Pendulum(pos1, pos2, len(pendulum_group) + 1)
        #     pendulum_group.append(pendulum)
        #     print(f'{pos2}')
    screen.fill(WHITE)
    if play:
        space.step(1 / FPS)
        for pendulum in pendulum_group:
            pendulum.draw()
        print_fps()

    else:
        for pendulum in pendulum_group:
            pendulum.draw()
        print_fps()
    clock.tick(FPS)
    pygame.display.update()

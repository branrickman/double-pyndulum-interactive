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
FPS = 10

# pymunk variables
space = pymunk.Space()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def convert_coords(point):  # convert to int, transform to pygame y convention
    return int(point[0], (SCREEN_HEIGHT - point[1]))

class Pendulum:
    def __init__(self, x, y):
        # pymunk properties
        self.body = pymunk.Body()
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, 10)
        self.shape.density = 1
        self.shape.elasticity = 1

        self.radius = 10
        self.color = BLACK

    def draw(self):
        pygame.draw.circle(screen, self.color, convert_coords(self.body.position, self.radius))

    def update(self):
        pass

    def simulate(self):
        pass


pendulum = Pendulum(100, 100)

run = True
play = True
if __name__ == '__main__':
    while run:
        clock.tick(FPS)
        space.step(1 / FPS)
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
                    print(f'Tick speed decreased to {FPS}')
                if event.key == pygame.K_d:
                    FPS += 1
                    print(f'Tick speed increased to {FPS}')
                if event.key == pygame.K_RIGHT:
                    pass
            if pygame.mouse.get_pressed()[0]:
                print("Left mouse click")
                # TODO Pixel flipping seems to be influenced by clock speed (tick_speed). Clicks register, but aren't actually flipping the pixel
                pos = pygame.mouse.get_pos()
                pass
        if play:
            pendulum.update()
        else:
            pendulum.draw()
        pygame.display.update()

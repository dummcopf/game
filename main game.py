import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

clock = pygame.time.Clock()
FPS = 60
running = True

class Gun:
    def __init__(self, rect, color):
        self.rect = pygame.Rect(rect)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Enemy:
    def __init__(self, rect, color):
        middle = (WIDTH/2, HEIGHT/2)
        self.rect = pygame.Rect(rect)
        print(self.rect.x,self.rect.y)
        self.color = color
        self.grow_speed = 1
        self.original_size = self.rect.size




    def grow(self):
        self.rect.w += math.floor(2 * self.grow_speed)
        self.rect.h += math.floor(2 * self.grow_speed)
        self.rect.x -= math.floor(1 * self.grow_speed)
        self.rect.y -= math.floor(1 * self.grow_speed)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def reset(self):
        self.rect.size = self.original_size
        self.rect.x = WIDTH // 2 - 25
        self.rect.y = HEIGHT // 2 - 25
        self.grow_speed = 1


gun = Gun((WIDTH // 2 - 25, HEIGHT // 2 + 250, 50, 50), (255, 255, 255))

enemy = Enemy((random.randint(WIDTH//2-WIDTH//4, WIDTH//2+WIDTH//4), random.randint(HEIGHT//2-HEIGHT//4, HEIGHT//2), 10, 10), (0, 255, 255))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if enemy.rect.collidepoint(mouse_x, mouse_y):
                enemy.reset()
                enemy = Enemy((random.randint(WIDTH // 2 - WIDTH // 4, WIDTH // 2 + WIDTH // 4),
                               random.randint(HEIGHT // 2, HEIGHT // 2 + HEIGHT // 4),
                               10,
                               10),
                              (0, 255, 255))

    enemy.grow()
    if enemy.rect.w >= WIDTH/4:
        enemy.reset()

    screen.fill((0, 0, 0))
    gun.draw(screen)
    enemy.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

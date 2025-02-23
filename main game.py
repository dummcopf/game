import sys

import pygame
import random
import math
import operator

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
FPS = 60
paused = False
paused_time = 0
running = True
my_answer = ""

class Button:
    def __init__(self, rect, color, number):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.number = number

    def is_pressed(self):
        global my_answer
        my_answer = self.number

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        textfont = pygame.font.Font(None, self.rect.width)
        text = textfont.render(str(self.number), True, (255, 255, 255))
        screen.blit(text, self.rect)


class Gun:
    def __init__(self, rect, color):
        self.rect = pygame.Rect(rect)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class Enemy:
    def __init__(self, rect, color):
        middle = (WIDTH / 2, HEIGHT / 2)
        self.rect = pygame.Rect(rect)
        # print(self.rect.x,self.rect.y)
        self.color = color
        self.grow_speed = 0.2
        self.original_size = self.rect.size
        self.x = self.rect.x
        self.y = self.rect.y
        self.w = self.rect.w
        self.h = self.rect.h
        self.problem = math_problem(random.randint(1, 10), random.randint(1, 10))
        self.correct_answer = self.problem[1]
        self.text = font.render(self.problem[0], True, (255, 255, 255))

    def grow(self):
        global paused
        if not paused:
            self.h += 2 * self.grow_speed
            self.w += 2 * self.grow_speed
            self.x -= self.grow_speed
            self.y -= self.grow_speed

            self.rect.w = math.floor(self.w)
            self.rect.h = math.floor(self.h)
            self.rect.x = math.floor(self.x)
            self.rect.y = math.floor(self.y)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

        textfont = pygame.font.Font(None, self.rect.width)
        self.text = textfont.render(self.problem[0], True, (255, 255, 255))
        screen.blit(self.text, (self.rect.x + self.rect.w / 2 - self.text.get_width() / 2,
                                self.rect.y + self.rect.h / 2 - self.text.get_height() / 2))


def math_problem(a, b):
    random_number = random.randint(0, 2)
    operations_dict = {"+": operator.add, "-": operator.sub, "/": operator.truediv, "*": operator.mul}
    type_of_equation = "+"
    if random_number == 1:
        type_of_equation = "+"
    elif random_number == 2:
        type_of_equation = "-"
        while b > a:
            b = random.randint(1, 10)
    else:
        type_of_equation = "*"

    c = operations_dict[type_of_equation](a, b)
    return (f"{a}{type_of_equation}{b}", c)


def spawn_enemy():
    global last_enemy_spawn_time
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),)
    enemies.append(Enemy((random.randint(WIDTH // 2 - WIDTH // 3, WIDTH // 2 + WIDTH // 3),
                          random.randint(HEIGHT // 2 - HEIGHT // 3, HEIGHT // 2 + HEIGHT // 3), 10, 10),
                         (color[0], color[1], color[2])))
    last_enemy_spawn_time = pygame.time.get_ticks()


clicked_enemy : Enemy = Enemy((10,10,10,10), (255,255,255))

buttons = []
j = 0
for i in range(10):
    if i % 3 == 0:
        j += 1
    buttons.append(Button(((i % 3) * 60 + 30, HEIGHT / 2 + j * 60, 50, 50), (0, 255, 0), i))
buttons.append(Button((90, HEIGHT / 2 + 240 , 50, 50), (0, 255, 0), "X"))
buttons.append(Button((150, HEIGHT / 2 + 240, 50, 50), (0, 255, 0), "enter"))
gun = Gun((WIDTH // 2 - 25, HEIGHT // 2 + 250, 50, 50), (255, 255, 255))
last_enemy_spawn_time = pygame.time.get_ticks()
enemy_spawn_cooldown = 1.5
enemies = []
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for enemy in enemies:
                if enemy.rect.collidepoint(mouse_x, mouse_y) and not paused:
                    paused = True
                    paused_time = pygame.time.get_ticks()
                    clicked_enemy = enemy
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for b in buttons:
                if b.rect.collidepoint(mouse_x, mouse_y):
                    if b.number == "X":
                        my_answer = ""
                    elif b.number == "enter":
                        paused = False
                        if my_answer == str(clicked_enemy.correct_answer):
                            print("Correct!")
                        else:
                            print("Incorrect")
                            sys.exit()
                        enemies.remove(clicked_enemy)
                        my_answer = ""
                    else:
                        my_answer += str(b.number)
                    print(my_answer)

    if not paused and pygame.time.get_ticks() - last_enemy_spawn_time >= enemy_spawn_cooldown * 1000:
        spawn_enemy()
    if paused and pygame.time.get_ticks() - paused_time >= 4000:
        paused = False
        print("Out of time!")
        sys.exit()
    gun.draw(screen)
    for enemy in enemies:
        enemy.grow()
        enemy.draw(screen)
        math_problem(random.randint(1, 50), random.randint(1, 50))
        if enemy.rect.w >= WIDTH / 4:
            enemies.remove(enemy)

    for b in buttons:
        b.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

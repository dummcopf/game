import sys

import pygame
import random
import math
import operator

pygame.init()
pygame.mixer.init()


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
score = 0

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
        textfont = pygame.font.Font(None, self.rect.height)
        text = textfont.render(str(self.number), True, (0, 0, 0))
        screen.blit(text, self.rect)


class Gun:
    def __init__(self, rect, folder, color):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.folder = folder
        self.side = "Front"
        self.img = pygame.image.load(f"{self.folder}/{self.side}.png")


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit()



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
    enemies.append(Enemy((random.randint(300, WIDTH // 2 + WIDTH // 3),
                          random.randint(HEIGHT // 2 - HEIGHT // 3, HEIGHT // 2 + HEIGHT // 3), 10, 10),
                         (color[0], color[1], color[2])))
    last_enemy_spawn_time = pygame.time.get_ticks()


def take_damage(dmg):
    global lives
    lives -= dmg
    screen.fill((255,0,0))
    oof = pygame.mixer.Sound("data/sfx/OOF.mp3")
    oof.play()

clicked_enemy = None

buttons = []
j = 0
for i in range(10):
    if i % 3 == 0:
        j += 1
    buttons.append(Button(((i % 3) * 60 + 30, HEIGHT / 2 + j * 60, 50, 50), (0, 255, 0), i))
buttons.append(Button((90, HEIGHT / 2 + 240 , 50, 50), (0, 255, 0), "X"))
buttons.append(Button((150, HEIGHT / 2 + 240, 50, 50), (0, 255, 0), "="))
gun = Gun((WIDTH // 2 - 25, HEIGHT // 2 + 250, 50, 50), (255, 255, 255))
enemy_spawn_cooldown = 3
last_enemy_spawn_time = pygame.time.get_ticks() - enemy_spawn_cooldown * 1000
last_text_change_time = pygame.time.get_ticks()

lives = 5
input_bar = Button((30,HEIGHT/2, 170,50), (255,0,0), "hi")
enemies = []
while running:
    screen.fill((0, 0, 0))
    if my_answer == "Incorrect!" or my_answer == "Correct!" or my_answer == "Out of time!":
        input_bar.number = my_answer
        if pygame.time.get_ticks() - last_text_change_time >= 2000:
            print(pygame.time.get_ticks(), last_text_change_time)
            my_answer = ""

    else:
        input_bar.number = my_answer


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
                    elif b.number == "=":
                        paused = False
                        if clicked_enemy != None:
                            try:
                                ans = int(my_answer)
                            except ValueError as e:
                                print(e)
                                ans = -999
                            if ans == int(clicked_enemy.correct_answer):
                                my_answer = "Correct!"
                                pew = pygame.mixer.Sound("data/sfx/pew.mp3")
                                pew.play()
                                screen.fill((255,255,255))
                                score += 100
                            elif my_answer == "Out of time!":
                                print("e")
                            else:
                                my_answer = "Incorrect!"
                                take_damage(1)

                            last_text_change_time = pygame.time.get_ticks()
                            enemies.remove(clicked_enemy)

                    else:
                        if my_answer == "Correct!" or my_answer == "Incorrect!" or my_answer == "Out of time!":
                            my_answer = ""
                        my_answer += str(b.number)
                    print(my_answer)

    if not paused and pygame.time.get_ticks() - last_enemy_spawn_time >= enemy_spawn_cooldown * 1000:
        spawn_enemy()
    if paused and pygame.time.get_ticks() - paused_time >= 4000:
        paused = False
        if my_answer != "Incorrect!" and my_answer != "Correct!":
            my_answer = "Out of time!"
            take_damage(1)
            screen.fill((255,0,0))
            enemies.remove(clicked_enemy)

            last_text_change_time = pygame.time.get_ticks()
    gun.draw(screen)
    for enemy in enemies:
        enemy.grow()
        enemy.draw(screen)
        math_problem(random.randint(1, 50), random.randint(1, 50))
        if enemy.rect.w >= WIDTH / 4:
            enemies.remove(enemy)
            take_damage(1)

    for b in buttons:
        b.color = (0,255,0)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if b.rect.collidepoint(mouse_x, mouse_y):
            b.color = (0,170,0)
        b.draw(screen)
    input_bar.draw(screen)

    for i in range(lives):
        screen.blit(pygame.image.load("data/sprites/heart.png"),(50 * i + 30, 0),)

    score_text = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_text, (WIDTH / 2, 0))

    if lives <= 0:
        sys.exit()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

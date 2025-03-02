import sys

import pygame
import random
import math
import operator

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
FPS = 240
paused = False
paused_time = 0
running = True
my_answer = ""
score = 0

thruster_hum = pygame.mixer.Sound("data/sfx/Thruster.mp3")
button_sfx = pygame.mixer.Sound("data/sfx/Button.mp3")
ticking_sfx = pygame.mixer.Sound("data/sfx/ticking.mp3")
thruster_hum.set_volume(0.5)

thruster_channel = pygame.mixer.find_channel()
thruster_channel.play(thruster_hum, loops=-1)

game_over = False


class Button:
    def __init__(self, rect, color, number):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.number = number
        self.pressed = False
        self.img = pygame.image.load(f"data/sprites/buttons/{self.pressed}.png")



    def is_pressed(self):
        global my_answer
        my_answer = self.number

    def draw(self, surface):

        self.img = pygame.transform.scale(self.img, (self.rect.width, self.rect.height))
        surface.blit(self.img,self.rect)
        textfont = pygame.font.Font(None, self.rect.height)
        text = textfont.render(str(self.number), True, (255, 255, 255))
        screen.blit(text, (self.rect.x + self.rect.w / 2 - text.get_width() // 2, self.rect.y + self.rect.h / 2 - text.get_height() // 2))


class Gun:
    def __init__(self, rect, folder, color):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.folder = folder
        self.side = "Front"
        self.img = pygame.image.load(f"{self.folder}/{self.side}.png")
        self.rotation = 0
        self.mouse_x_offset = 0
        self.mouse_y_offset = 0

    def draw(self, surface):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if not paused:
            if mouse_x <= WIDTH / 2 - WIDTH / 4:
                self.side = "Left"
            elif mouse_x >= WIDTH / 2 + WIDTH / 4:
                self.side = "Right"
            else:
                self.side = "Front"
            self.mouse_x_offset = (WIDTH / 2 - mouse_x) // 10
            self.mouse_y_offset = -(HEIGHT / 2 - mouse_y) // 10
            self.rotation = (WIDTH / 2 - mouse_x) // 100
        img = pygame.image.load(f"{self.folder}/{self.side}.png")
        self.img = pygame.transform.rotate(img,self.rotation % 360)

        x = WIDTH / 2 -self.img.get_width() / 2 + self.mouse_x_offset
        y = HEIGHT / 2 - self.img.get_height() / 2 + HEIGHT / 4 + self.mouse_y_offset

        surface.blit(self.img, (x,y))


class Enemy:
    def __init__(self, rect, color):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.grow_speed = 0
        self.original_size = self.rect.size
        self.x = self.rect.x
        self.y = self.rect.y
        self.w = self.rect.w
        self.h = self.rect.h
        self.problem = math_problem(random.randint(1, 10), random.randint(1, 10))
        self.correct_answer = self.problem[1]
        self.text = font.render(self.problem[0], True, (255, 255, 255))
        i = random.randint(0,2)
        self.img = pygame.image.load(f"data/sprites/asteroids/asteroid{i}.png")
        self.img = pygame.transform.rotate(self.img, random.randint(0,360))

    def grow(self):
        global paused
        if not paused:
            self.grow_speed += 0.03
            self.h += 2 * self.grow_speed
            self.w += 2 * self.grow_speed
            self.x -= self.grow_speed
            self.y -= self.grow_speed

            self.rect.w = math.floor(self.w)
            self.rect.h = math.floor(self.h)
            self.rect.x = math.floor(self.x)
            self.rect.y = math.floor(self.y)

    def draw(self, surface):
        img = pygame.transform.scale(self.img, (self.rect.w, self.rect.h))
        surface.blit(img, self.rect)
        textfont = pygame.font.Font(None, self.rect.height // 2)
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

    enemies.insert(0,Enemy((random.randint(300, WIDTH // 2 + WIDTH // 3),
                          random.randint(HEIGHT // 2 - HEIGHT // 3, HEIGHT // 2), 10, 10),
                         (color[0], color[1], color[2])))
    last_enemy_spawn_time = pygame.time.get_ticks()


def take_damage(dmg):
    global lives
    lives -= dmg
    screen.fill((255, 0, 0))
    oof = pygame.mixer.Sound("data/sfx/OOF.mp3")
    oof.play()


clicked_enemy = None

buttons = []
j = 0
for i in range(10):
    if i % 3 == 0:
        j += 1
    buttons.append(Button(((i % 3) * 60 + 30, HEIGHT / 2 + j * 60, 50, 50), (0, 255, 0), i))
buttons.append(Button((90, HEIGHT / 2 + 240, 50, 50), (0, 255, 0), "X"))
buttons.append(Button((150, HEIGHT / 2 + 240, 50, 50), (0, 255, 0), "="))
gun = Gun((WIDTH // 2 - 25, HEIGHT // 2 + 250, 50, 50), "data/sprites/Space Ship", (255, 255, 255))
enemy_spawn_cooldown = 3
last_enemy_spawn_time = pygame.time.get_ticks() - enemy_spawn_cooldown * 1000
last_text_change_time = pygame.time.get_ticks()

lives = 5
input_bar = Button((30, HEIGHT / 2, 170, 50), (255, 0, 0), "hi")
enemies = []
bg_image = pygame.image.load("data/sprites/BG/bg.jpg")
bg_image = pygame.transform.scale(bg_image, (WIDTH,HEIGHT))
retry_image = pygame.image.load("data/sprites/buttons/False.png")
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg_image, (0,0))

    if game_over:
        thruster_channel.pause()
        game_over_font = pygame.font.Font(None, 200)
        score_font = pygame.font.Font(None, 50)
        game_over_retry = pygame.rect.Rect(WIDTH / 2 - 400, HEIGHT / 2 - 100, 800,200)
        retry_image = pygame.transform.scale(retry_image, (game_over_retry.w,  game_over_retry.h))
        screen.blit(retry_image, game_over_retry)
        retryText = game_over_font.render("Retry?", True, (255, 255, 255))
        screen.blit(retryText, (game_over_retry.x - retryText.get_width() // 2 + game_over_retry.w // 2, game_over_retry.y - retryText.get_height() // 2 + game_over_retry.h // 2))
        gameOvertext = game_over_font.render("Game Over!", True, (255, 255, 255))
        score_text = score_font.render(f"Score : {str(score)}", True, (255, 255, 255))

        screen.blit(gameOvertext, (WIDTH / 2 - gameOvertext.get_width() / 2, 0))
        screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, gameOvertext.get_height() + 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if game_over_retry.collidepoint(mouse_x,mouse_y):

                    lives = 5
                    game_over = False
                    score = 0
                    thruster_channel.unpause()
                    enemies.clear()
                    button_sfx.play()


    else:

        if my_answer == "Incorrect!" or my_answer == "Correct!" or my_answer == "Out of time!":
            input_bar.number = my_answer
            if pygame.time.get_ticks() - last_text_change_time >= 2000:
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
                        ticking_sfx.play()
                        paused = True
                        thruster_channel.pause()
                        paused_time = pygame.time.get_ticks()
                        clicked_enemy = enemy
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for b in buttons:
                    if b.rect.collidepoint(mouse_x, mouse_y):
                        if b.number == "X":
                            my_answer = ""
                            button_sfx.play()
                        elif b.number == "=":
                            paused = False
                            ticking_sfx.stop()
                            thruster_channel.unpause()
                            if clicked_enemy in enemies:
                                try:
                                    ans = int(my_answer)
                                except ValueError as e:
                                    ans = -999
                                if ans == int(clicked_enemy.correct_answer):
                                    my_answer = "Correct!"
                                    pew = pygame.mixer.Sound("data/sfx/pew.mp3")
                                    pew.play()
                                    screen.fill((255, 255, 255))
                                    score += 100
                                else:
                                    my_answer = "Incorrect!"
                                    take_damage(1)

                                last_text_change_time = pygame.time.get_ticks()
                                enemies.remove(clicked_enemy)

                        else:
                            button_sfx.play()
                            if my_answer == "Correct!" or my_answer == "Incorrect!" or my_answer == "Out of time!":
                                my_answer = ""
                            my_answer += str(b.number)

        if not paused and pygame.time.get_ticks() - last_enemy_spawn_time >= enemy_spawn_cooldown * 1000:
            spawn_enemy()
        if paused and pygame.time.get_ticks() - paused_time >= 5000:
            paused = False
            if my_answer != "Incorrect!" and my_answer != "Correct!":
                my_answer = "Out of time!"
                take_damage(1)
                screen.fill((255, 0, 0))
                enemies.remove(clicked_enemy)

                last_text_change_time = pygame.time.get_ticks()
        for enemy in enemies:
            enemy.grow()
            enemy.draw(screen)
            math_problem(random.randint(1, 50), random.randint(1, 50))
            if enemy.rect.w >= WIDTH / 4:
                enemies.remove(enemy)
                take_damage(1)

        gun.draw(screen)
        for b in buttons:
            b.pressed = False
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if b.rect.collidepoint(mouse_x, mouse_y):
                b.pressed = True
            b.draw(screen)
        input_bar.draw(screen)

        for i in range(lives):
            screen.blit(pygame.image.load("data/sprites/heart.png"), (63 * i + 30, 0), )


        score_font = pygame.font.Font(None, 100)

        score_text = score_font.render(str(score), True, (255, 255, 255))
        screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 0))

        if lives <= 0:
            game_over = True
            paused = False
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

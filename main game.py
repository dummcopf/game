
import pygame
import random
import math
import operator
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

clock = pygame.time.Clock()
FPS = 60
running = True
My_Answer = ""
class Button:
    def __init__(self, rect, color, number):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.number = number

    def is_pressed(self):
        global My_Answer
        My_Answer = self.number




    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


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
        #print(self.rect.x,self.rect.y)
        self.color = color
        self.grow_speed = 0.2
        self.original_size = self.rect.size
        self.x = self.rect.x
        self.y = self.rect.y
        self.w = self.rect.w
        self.h = self.rect.h


    def grow(self):
        self.h += 2 * self.grow_speed
        self.w += 2 * self.grow_speed
        self.x -= 1 * self.grow_speed
        self.y -= 1 * self.grow_speed

        self.rect.w = math.floor(self.w)
        self.rect.h = math.floor(self.h)
        self.rect.x = math.floor(self.x)
        self.rect.y = math.floor(self.y)


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)



def math_problem(a,b):
    is_correct = random.randint(0,1).__bool__()
    random_number = random.randint(0,3)
    operations_dict = {"+":operator.add, "-":operator.sub, "/":operator.truediv, "*": operator.mul}
    type_of_equation = "+"
    if random_number == 1:
        type_of_equation = "+"
    elif random_number == 2:
        type_of_equation = "-"
    elif random_number == 3:
        type_of_equation = "*"
    else:
        type_of_equation = "/"
    c = operations_dict[type_of_equation](a, b)
    if not is_correct:
        c += math.ceil(random.uniform(-c,c))
    #print(f"{a}{type_of_equation}{b}={c} (correct = {is_correct})")
math_problem(random.randint(1,50),random.randint(1,50))

def spawn_enemy():
    global last_enemy_spawn_time
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),)
    enemies.append(Enemy((random.randint(WIDTH // 2 - WIDTH // 3, WIDTH // 2 + WIDTH // 3),random.randint(HEIGHT // 2 - HEIGHT // 3, HEIGHT // 2 + HEIGHT // 3),10,10),(color[0], color[1], color[2])))
    last_enemy_spawn_time = pygame.time.get_ticks()

buttons = []
j = 0
for i in range(10):
    if i%3 == 0:
        j+=1
    buttons.append(Button(((i%3) * 60 + 30, HEIGHT / 2 + j * 60,50,50),(0, 255,0), i))
buttons.append(Button(( 90, HEIGHT / 2,50,50),(0, 255,0), 8000))
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
                if enemy.rect.collidepoint(mouse_x, mouse_y):
                    enemies.remove(enemy)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for b in buttons:
                if b.rect.collidepoint(mouse_x, mouse_y):
                    if b.number != 8000 :
                        My_Answer += str(b.number)
                    else:
                        My_Answer = ""
                    print(My_Answer)

    for b in buttons:
        b.draw(screen)

    if pygame.time.get_ticks() - last_enemy_spawn_time >= enemy_spawn_cooldown * 1000:
       spawn_enemy()


    gun.draw(screen)
    for enemy in enemies:
        enemy.grow()
        enemy.draw(screen)
        math_problem(random.randint(1, 50), random.randint(1, 50))
        if enemy.rect.w >= WIDTH / 4:
            enemies.remove(enemy)


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

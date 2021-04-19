# from Game import Game
from Controller import*
import pygame

# names = ['Димочка', 'Ромс', 'Гандон', 'Сука', 'Пидор', 'Тварь', 'Ублюдок']
# names = ['Димочка', 'Ромс', 'Гандон', 'Сука', 'Пидор', 'Тварь']
# names = ['Димочка', 'Ромс', 'Гандон', 'Сука', 'Пидор']
# names = ['Димочка', 'Ромс', 'Гандон', 'Сука']
# names = ['Миша', 'Леша', 'Яков', 'Саша']
# names = ['Димончик', 'Сука', 'Яков', 'Саша']
# names = ['Димочка', 'Ромс', 'Гандон']
names = ['Димочка', 'Ромс']

WIDTH, HEIGHT, FPS = 0, 0, 60
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
# WIDTH, HEIGHT, FPS = 800, 600, 60
# screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.init()
clock = pygame.time.Clock()

controller = Controller(names, screen)

# import json
# a = {"a": 1, "list": {}}
# output = open("file.txt", "w")
# output.write(json.dumps(a))
# output.close()
# input = open("file.txt", "r")
# b = json.loads(input.readline())
# print(b["list"])
# input.close()
# print(b)
# print(a)

run = True
zooming = False
while run:
    if len(controller.buttons) == 0:
        controller.gameMaster.run()
        run = controller.gameMaster.running
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: controller.clicked(event.pos)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1: controller.mouse_up()
        if event.type == pygame.MOUSEMOTION: controller.move(event.rel)
        if event.type == pygame.MOUSEWHEEL and zooming: controller.zooming_card.set_zoom(event.y)
        if event.type == pygame.MOUSEWHEEL and not zooming: controller.global_zoom(event.y)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f: zooming = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_f: zooming = False

        if zooming: controller.zoom(pygame.mouse.get_pos())
        else: controller.set_zoom(None)

    if keys[pygame.K_ESCAPE]: run = False
    screen.fill((0, 0, 0))
    controller.draw()
    pygame.display.update()
# input("print something")
pygame.quit()

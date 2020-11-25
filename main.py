import pygame
import cards
import random
from datafiles import data
from datafiles import max_ammo

WIDTH = 0
HEIGHT = 0
FPS = 120

PINK = (255, 34, 144)
BLACK = (0, 0, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Citadels')
clcok = pygame.time.Clock()
WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h

run = True

screen.fill(BLACK)
pygame.display.flip()

x = 50
y = 50
width = int(HEIGHT * 1e-1)
height = int(width * 1.5)

char_deck = [pygame.image.load('Sprites/characters/assasin.png'),
             pygame.image.load('Sprites/characters/thief.png'),
             pygame.image.load('Sprites/characters/magician.png'),
             pygame.image.load('Sprites/characters/king.png'),
             pygame.image.load('Sprites/characters/bishop.png'),
             pygame.image.load('Sprites/characters/merchant.png'),
             pygame.image.load('Sprites/characters/architect.png'),
             pygame.image.load('Sprites/characters/warlord.png')]
deck_quar = []
pos_x = WIDTH / 2 - width / 2
pos_y = HEIGHT / 2 - height / 2
for i in range(len(data[0])):
    # rand_x = random.randint(0, WIDTH - width)
    # rand_y = random.randint(0, HEIGHT - height)
    quart = pygame.image.load('Sprites/quarters/' + data[0][i] + '.png')
    for j in range(data[1][i]):
        deck_quar.append(cards.Quartal(pos_x, pos_y, width, height, quart, screen, "unique", 3))


deck_char = []
# game = cards.Game(deck_char, deck_quar, screen) # то как должен выглядить конечный класс игры
game = cards.Game(deck_char, deck_quar, screen, 2)

king_prime = pygame.image.load('Sprites/characters/king.png')
king = pygame.transform.scale(king_prime, (width, height))
king.set_alpha(30)
scale = 1.1

while run:
    clcok.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # game.mouse_down(event.pos)
            game.players[0].mouse_down(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            # game.mouse_up()
            game.players[0].mouse_up()

        if event.type == pygame.MOUSEMOTION:
            # game.mouse_move(event.rel)
            game.players[0].mouse_move(event.rel)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False

    if keys[pygame.K_SPACE]:
        king = pygame.transform.scale(king_prime, (int(width * scale), int(height * scale)))
        scale += 1e-1


    screen.fill(BLACK)
    game.draw()
    screen.blit(king, (510, 510))
    pygame.display.update()


pygame.quit()

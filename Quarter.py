import random
import pygame
from Button import Card, h_koeff
from Docer import doc

class Quarter(Card):
    def __init__(self, name, value, color):
        self.name = name
        self.value = value
        self.color = color
        # то что выше для механики, то что ниже для отрисовки
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.koeff = h_koeff
        self.state = "hide"
        self.primImg = {"open": pygame.image.load("Sprites/quarters/" + name + ".png"),
                        "hide": pygame.image.load("Sprites/quarters/quarter.png")} # загружаем текстуру карты квартала
        self.img = None # чтобы не испортить качество оригинала
    def draw(self, screen):
        screen.blit(self.img[self.state], (self.x, self.y))
    def built(self, player):
        self.state = "open"
    def destroyed(self, player):
        self.state = "hide"
    def bounus(self):
        return self.value

class PlusTwoBonus(Quarter):
    def __init__(self, name, value, color):
        Quarter.__init__(self, name, value, color)
    def bounus(self):
        return self.value + 2

class ActivateQuarter(Quarter):
    def __init__(self, name, value, color, action):
        Quarter.__init__(self, name, value, color)
        self.action = action
    def built(self, player):
        Quarter.built(self, player)
        player.all_actions[self.action] = True
    def destroyed(self, player):
        Quarter.destroyed(self, player)
        player.all_actions[self.action] = False

class ActionQuarter(ActivateQuarter):
    def __init__(self, name, value, color, action):
        ActivateQuarter.__init__(self, name, value, color, action)
    def built(self, player):
        ActivateQuarter.built(self, player)
        player.action_pool.insert(-1, self.action)

class ResourceQuarter(Quarter):
    def __init__(self, name, value, color, resource):
        Quarter.__init__(self, name, value, color)
        self.resource = resource
    def built(self, player):
        Quarter.built(self, player)
        player.take[self.resource] += 1
    def destroyed(self, player):
        Quarter.destroyed(self, player)
        player.take[self.resource] -= 1

deck = []
file = open('quarters.txt', 'r')
color = ''

for line in file:
    if line[0] == '*':
        color = line[1:len(line) - 1]
    else:
        name = line[0:len(line) - 5]
        value = int(line[len(line) - 4: len(line) - 3])
        amount = int(line[len(line) - 2: len(line) - 1])
        for i in range(amount):
            if name == 'dragongate' or name == 'university': deck.append(PlusTwoBonus(name, value, color))
            elif name == 'graveyard': deck.append(ActivateQuarter(name, value, color, 'graveyard_action'))
            elif name == 'greatwall': deck.append(ActivateQuarter(name, value, color, 'greatwall_bonus'))
            elif name == 'library': deck.append(ActivateQuarter(name, value, color, 'library_bonus'))
            elif name == 'schoolofmagic': deck.append(ActivateQuarter(name, value, color, 'schoolofmagic_bonus'))
            elif name == 'hauntedcity': deck.append(ActivateQuarter(name, value, color, 'hauntedcity_bonus'))
            elif name == 'imperialtreasury': deck.append(ActivateQuarter(name, value, color, 'imperialtreasury_bonus'))
            elif name == 'maproom': deck.append(ActivateQuarter(name, value, color, 'maproom_bonus'))
            elif name == 'laboratory': deck.append(ActionQuarter(name, value, color, 'laboratory_action'))
            elif name == 'smithy': deck.append(ActionQuarter(name, value, color, 'smithy_action'))
            elif name == 'observatory': deck.append(ResourceQuarter(name, value, color, 'quarter'))
            else: deck.append(Quarter(name, value, color)) # обычный квартал

random.shuffle(deck)
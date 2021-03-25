import pygame

h_koeff = 0.2
w_koeff = 0.07
text_koeff = 0.03

class Card:
    def __init__(self, screen, primImg):
        self.koeff = h_koeff
        self.x = 0
        self.y = 0
        self.height = int(screen.get_height() * self.koeff)
        self.width = int(screen.get_height() * (self.koeff - w_koeff))
        self.text_editor = None
        self.primImg = primImg
        self.img = self._set_img(primImg, screen)

    def _set_img(self, primImg, screen):
        if type(primImg) == str:
            self.text_editor = pygame.font.SysFont('serif', int(screen.get_height() * text_koeff))
            text = self.text_editor.render(self.primImg, True, (234, 54, 123))
            self.width, self.height = text.get_width(), text.get_height()
            return text
        else:
            return pygame.transform.scale(primImg, (self.width, self.height))

    def update(self):
        width, height = int(self.width), int(self.height)
        if type(self.primImg) == dict:
            self.img["open"] = pygame.transform.scale(self.primImg["open"], (width, height))
            self.img["hide"] = pygame.transform.scale(self.primImg["hide"], (width, height))
        else:
            self.img = pygame.transform.scale(self.primImg, (width, height))

    def resize(self, koeff):
        self.width = int(self.width * koeff)
        self.height = int(self.height * koeff)
        if type(self.primImg) == str:
            self.img = self.text_editor.render(self.primImg, True, (234, 54, 123))
        else:
            self.img = pygame.transform.scale(self.primImg, (self.width, self.height))

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height))
        screen.blit(self.img, (self.x, self.y))

class Button(Card):
    def __init__(self, screen, primImg, value, controller):
        Card.__init__(self, screen, primImg)
        self.value = value
        self.controller = controller

    def click(self):
        self.controller.del_but(self)
        self.controller.gameMaster.global_input(self.value)

class FlagButton(Button):
    def __init__(self, screen, primImg, value, controller):
        Button.__init__(self, screen, primImg, value, controller)
        self.choosen = False

    def click(self):
        self.choosen = not self.choosen
        print(self.choosen)

    def draw(self, screen):
        if self.choosen: koeff = self.height * 0.05
        else: koeff = 0
        pygame.draw.rect(screen, (100, 100, 100), (self.x - koeff, self.y - koeff, self.width + koeff * 2, self.height + koeff * 2))
        screen.blit(self.img, (self.x, self.y))

class ZoomCard(Card):
    def __init__(self, screen):
        self.screen = screen
        self.koeff = h_koeff
        self.zoom_koeff = 1
        self.height = int(screen.get_height() * self.koeff)
        self.width = int(screen.get_height() * (self.koeff - w_koeff))
        self.set_pos(((screen.get_width() - self.width) / 2, (screen.get_height() - self.height) / 2))
        self.primImg = None
        self.img = None
        self.orig_card = None

    def set_zoom(self, wheel):
        if wheel > 0:
            self.zoom_koeff += 0.2 # проверяем вылезла ли карта за пределы экрана
            if self.screen.get_height() <= self.screen.get_height() * self.koeff * (self.zoom_koeff - 0.2):
                self.zoom_koeff -= 0.2
        else: self.zoom_koeff -= 0.2
        if self.zoom_koeff <= 1: self.zoom_koeff = 1 # проверяем нижнюю грань
        self.height = int(self.screen.get_height() * self.koeff * self.zoom_koeff)
        self.width = int(self.screen.get_height() * (self.koeff - w_koeff) * self.zoom_koeff)
        self.set_pos(((self.screen.get_width() - self.width) / 2, (self.screen.get_height() - self.height) / 2))

    def set_img(self, card):
        if card == None:
            self.primImg = None
            self.img = None
            self.orig_card = None
            return
        primImg = card.primImg
        if type(primImg) == str: return
        self.orig_card = card
        if type(primImg) == dict: self.primImg = primImg[card.state]
        else: self.primImg = primImg
        self.img = pygame.transform.scale(self.primImg, (self.width, self.height))

    def set_pos(self, pos):
        self.x, self.y = pos[0], pos[1]

    def draw(self, screen):
        if self.img:
            pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height))
            screen.blit(self.img, (self.x, self.y))

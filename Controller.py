import pygame, random
from Game import Game
from Interface import Interface
from random import shuffle
from Button import ZoomCard, w_koeff, h_koeff
from Docer import doc

class Check:
    def __init__(self, names):
        self.gameMaster = Game(names)
color = (255, 100, 0)
class Controller:
    def __init__(self, names, screen):
        self.screen = screen
        self.gameMaster = Game(names, self)
        self.active_player = self.gameMaster.players[0]
        self.quarters = self._get_quarters()
        self.players = {}
        self.buttons = []
        self.interface = Interface(screen, self, self.gameMaster.active_player())
        self.zooming_card = ZoomCard(screen)
        self.pressed = False
        self.x = 0 #-screen.get_width()
        self.y = 0 #-screen.get_height()
        self.width = screen.get_width()#3 * screen.get_width()
        self.height = screen.get_height() * 4/5#3 * screen.get_height()
        self.color = (25, 25, 25)
        self.dropList = []
        self._set_prime_size()

    def get_width(self):
        return self.screen.get_width()

    def get_height(self):
        return self.screen.get_height()

    def _get_quarters(self):
        quarters = self.gameMaster.deckQuar[:]
        for player in self.gameMaster.players:
            quarters += player.hand[:]
            quarters += player.city[:]
        return quarters

    def _set_prime_size(self):
        # cards = self.quarters + self.gameMaster.deckChar
        for card in self.quarters:
            card.x = (self.get_width() - card.width) / 2
            card.height = int(self.screen.get_height() * h_koeff)
            card.width = int(self.screen.get_height() * (h_koeff - w_koeff))
            open_img = pygame.transform.scale(card.primImg["open"], (card.width, card.height))
            hide_img = pygame.transform.scale(card.primImg["hide"], (card.width, card.height))
            card.img = {"open": open_img, "hide": hide_img}
        for card in self.gameMaster.deckChar:
            card.height = int(self.screen.get_height() * h_koeff)
            card.width = int(self.screen.get_height() * (h_koeff - w_koeff))
            open_img = pygame.transform.scale(card.primImg["open"], (card.width, card.height))
            hide_img = pygame.transform.scale(card.primImg["hide"], (card.width, card.height))
            card.img = {"open": open_img, "hide": hide_img}
        for player in self.gameMaster.players:
            self.players[player.name] = player
            for quar in player.hand:
                quar.x = player.x
                quar.y = player.y + player.height - quar.height
            for i in range(len(player.hand)):
                player.hand[i].x = player.x + player.hand[i].width * i
        self.interface.set_player(self.gameMaster.active_player()) # задаем нужный скеил, чтобы все игроки вместились
        if len(self.gameMaster.players) == 3: self.gameMaster.zoom_players(-.5)
        if len(self.gameMaster.players) == 4: self.gameMaster.zoom_players(-.5)
        if len(self.gameMaster.players) == 5: self.gameMaster.zoom_players(-.6)
        if len(self.gameMaster.players) == 6: self.gameMaster.zoom_players(-.6)
        if len(self.gameMaster.players) == 7: self.gameMaster.zoom_players(-.7)

    def set_zoom(self, primImg):
        self.zooming_card.set_img(primImg)

    def curr_zoom(self, x, y, card):
        if card == None: return False
        if x >= card.x and y >= card.y and x <= card.x + card.width and y <= card.y + card.height:
            return True
        else:
            return False

    def zoom(self, pos):
        x, y = pos[0], pos[1]
        # if self.curr_zoom(x, y, self.zooming_card.orig_card):
        #     return
        #     pass # эта часть кода нужна для оптимизации, но есть небольшой баг, который мне лень фиксить
        cards = self.gameMaster.deckChar + self._get_quarters() + self.interface.get_cards() + self.dropList
        for i in range(len(cards)):
            if self.curr_zoom(x, y, cards[len(cards) - i - 1]):
                self.set_zoom(cards[len(cards) - i - 1])
                return
        self.set_zoom(None)

    def global_zoom(self, plus):
        if plus > 0: koeff = .1
        else: koeff = -.1
        x, y = pygame.mouse.get_pos()
        # if y < self.interface.y: print(x, y, self.interface.y)
        if y >= self.interface.y:
            if x >= self.interface.but_zone.x:
                self.interface.but_zone.scrollContent(koeff * self.interface.but_zone.height)
                return
            else: return
        x, y = x - self.x, y - self.y
        k_x, k_y = x / self.width, y / self.height

        if self.width + self.width * koeff < self.get_width() - self.get_width() * .1:
            return
        if self.width + self.width * koeff > self.get_width() * 6: return
        self.x -= (self.width * koeff) * k_x  # (self.screen.get_width() / mouse_x)
        self.y -= (self.height * koeff) * k_y  # (self.screen.get_height() / mouse_y)
        self.width += self.width * koeff
        self.height += self.height * koeff

        self.gameMaster.zoom_players(koeff)

    def append_drop(self, char):
        char.set_pos(0, 0)
        self.dropList.append(char)

    def draw(self):
        if self.active_player.ai:
            self.active_player.ai.think()
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
        for name in self.players:
            self.players[name].draw(self.screen)

        for i in range(len(self.dropList)):
            self.dropList[i].set_pos(self.x + (self.width - self.dropList[i].width)/ 2,
                                     self.y + (self.height - self.dropList[i].height) / 2 + i * self.dropList[i].height / 5)
            self.dropList[i].draw(self.screen)

        self.interface.draw()
        if not self.active_player.ai:
            for button in self.buttons:
                button.draw(self.screen)

        self.zooming_card.draw(self.screen)

    def mouse_up(self):
        self.pressed = False

    def check_skip_btn(self, coords):
        x, y = coords[0], coords[1]
        width = self.interface.but_zone.x + self.interface.but_zone.width
        height = self.interface.but_zone.y + self.interface.but_zone.height
        if x >= self.interface.but_zone.x and x <= width and y >= self.interface.but_zone.y and y <= height:
            self.active_player.ai.finishCount = self.active_player.ai.finishTime

    def clicked(self, coords):
        ai = self.active_player.ai
        if ai: self.check_skip_btn(coords)
        x, y = coords[0], coords[1]
        but, N = self.buttons, len(self.buttons)
        for index in range(N):
            i = N - index - 1
            width, height = but[i].x + but[i].width, but[i].y + but[i].height
            if x >= but[i].x and x <= width and y >= but[i].y and y <= height and not ai:
                but[i].click()
                self.pressed = False
                return
        if y < self.interface.y:
            self.pressed = True

    def move(self, rel):
        if not self.pressed: return
        x, y = rel[0], rel[1]
        self.x += x
        self.y += y

    def set_gold(self):
        self.interface.set_gold(self.gameMaster.active_player())

    def set_hand(self, hand):
        self.interface.set_hand(hand)

    def set_interface(self):
        # if self.active_player.ai: return
        self.interface.set_player(self.gameMaster.active_player())

    def next_player(self): # метод реализован для этапа выбора персонажа
        N, index = len(self.gameMaster.players), 0
        for i in range(N):
            if self.active_player == self.gameMaster.players[i]:
                index = i + 1
                if index == N:
                    index = 0
        self.active_player = self.gameMaster.players[index]
        self.shuffle()
        # if self.active_player.ai and self.active_player != self.gameMaster.players[0]: #self.active_player != self.gameMaster.players[0]: # если следующий игрок ИИ
        if len(self.buttons) > 0 and self.active_player.ai:
            self.active_player.ai.setSolution("chooseChar")
        self.set_interface()
        self.interface.set_text("")

    def shuffle(self):
        shuffle(self.buttons)
        self.interface.but_zone.normalize()

    def create_buttons(self, buttons, flag):
        for content in buttons:
            img = content[0]  # можно пихать картинки или текст
            value = content[1]  # то что кнопка будет возвращать
            if not flag:
                self.interface.but_zone.create_button(img, value)
            else:
                self.interface.but_zone.create_flag(img, value)
        if flag:
            self.interface.but_zone.create_button("Подтвердить", self.interface.but_zone.buttons)
            self.interface.but_zone.create_button("Отмена", "cancel")
        self.buttons = self.interface.but_zone.buttons
        self.normalize(self.buttons, self.interface.but_zone)

    def del_but(self, button):
        if button == 'all': self.buttons.clear()
        for i in range(len(self.buttons)):
            if self.buttons[i] is button:
                del self.buttons[i]
                self.interface.but_zone.normalize()
                return

    def _define_cards(self, cards):
        img, text = [], []
        for card in cards:
            if type(card.primImg) == str:
                text.append(card)
            else:
                img.append(card)
        return img, text

    def _norm(self, cards, place, padding):
        if len(cards) == 0: return
        for but in cards:
            if but.height > place.height:
                but.resize(0.9 * place.height / but.height)
        for but in cards:
            koeff = 2
            if type(but.primImg) == str: koeff = 1
            but.y = place.y + (place.height - but.height) / koeff
        width = cards[0].width
        h = (place.width) / ((len(cards) + 0) * width)
        if width * h - width < 0:
            koeff = (place.width - width) / (len(cards) - 1)
            for i in range(len(cards)):
                cards[i].x = place.x + i * koeff
        else:
            border = (place.width - width * len(cards)) / 2
            for i in range(len(cards)):
                cards[i].x = place.x + width * i + border + i * padding  # возможно стоит брать ширину каждой кнопки

    def normalize(self, cards, place):
        img, text = self._define_cards(cards)
        if len(img) == 0:
            padding = cards[0].height * 0.2
            N = len(cards)
            for i in range(N):
                cards[i].x = place.x + padding
                cards[i].y = place.y + cards[i].height * i + padding * (i + 1)
        else:
            self._norm(img, place, 0)
            self._norm(text, place, place.width * 0.05)

    def getButton(self, value):
        if value.isdigit():
            return self.buttons[int(value)]
        if value == "random":
            return random.choice(self.buttons)
        for btn in self.buttons:
            if type(btn.value) != str:
                if btn.value.name == value:
                    return btn
            else:
                if btn.value == value:
                    return btn

    def getAllBtn(self):
        values = []
        for btn in self.buttons:
            values.append(btn.value)
        return values
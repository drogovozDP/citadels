from Button import*
from Docer import doc

class Zone:
    def __init__(self, x, y, width, height, interface):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (228, 228, 228)
        self.interface = interface
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


class ButtonZone(Zone):
    def __init__(self, x, y, width, height, interface):
        Zone.__init__(self, x, y, width, height, interface)
        self.color = (12, 143, 51)
        self.buttons = []
        self.text_size = text_koeff
        self.renderer = pygame.font.SysFont('serif', int(self.interface.screen.get_height() * self.text_size * 1.5))
        self.text = self.renderer.render("Продолжить", True, (234, 54, 123))

    def create_button(self, primImg, value):
        screen, controller = self.interface.screen, self.interface.controller
        but = Button(screen, primImg, value, controller)
        self.buttons.append(but)

    def create_flag(self, primImg, value):
        screen, controller = self.interface.screen, self.interface.controller
        flag = FlagButton(screen, primImg, value, controller)
        self.buttons.append(flag)

    def normalize(self):
        if len(self.buttons) == 0: return
        self.interface.normalize(self.buttons, self)

    def set(self, buttons):
        self.buttons = buttons

    def scrollContent(self, dy):
        for btn in self.buttons:
            btn.y += dy

    def draw(self, screen):
        Zone.draw(self, screen)
        ai = self.interface.controller.active_player.ai
        if ai:
            if ai.finishCount != 0:
                pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height))
                screen.blit(self.text, (self.x + (self.width - self.text.get_width()) / 2,
                                        self.y + (self.height - self.text.get_height()) / 2))

class TextZone(Zone):
    def __init__(self, x, y, width, height, interface, screen):
        Zone.__init__(self, x, y, width, height, interface)
        self.color = (200, 200, 150)
        self.text_size = text_koeff
        self.screen = screen
        self.renderer = pygame.font.SysFont('serif', int(screen.get_height() * self.text_size))
        self.text = []

    def set(self, text):
        self.text.clear()
        self.text.append(self.renderer.render(text, True, (0, 0, 0)))

    def add(self, text):
        self.text.append(self.renderer.render(text, True, (0, 0, 0)))

    def draw(self, screen):
        Zone.draw(self, screen)
        N = len(self.text)
        if N == 0: return
        offset = (self.height - N * self.text[0].get_height()) / 2
        for i in range(N):
            width = (self.width - self.text[i].get_width()) / 2
            screen.blit(self.text[i], (self.x + width, self.y + self.text[i].get_height() * i + offset))

class HandZone(Zone):
    def __init__(self, x, y, width, height, interface):
        Zone.__init__(self, x, y, width, height, interface)
        self.color = (134, 23, 134)
        self.hand = []

    def set_hand(self):
        self.hand.clear()
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
        for quar in self.interface.player.hand:
            self.hand.append(Card(self.interface.screen, quar.primImg["open"]))
        for char in self.interface.player.charList:
            if char.alive: text = "open"
            else: text = "hide"
            self.hand.append(Card(self.interface.screen, char.primImg[text]))
        self.normalize()

    def normalize(self):
        if len(self.hand) == 0: return
        self.interface.normalize(self.hand, self)

    def draw(self, screen):
        Zone.draw(self, screen)
        for card in self.hand:
            card.draw(screen)

class GoldZone(Zone):
    def __init__(self, x, y, width, height, interface, screen):
        Zone.__init__(self, x, y, width, height, interface)
        self.gold = 0
        self.color = (65, 12, 150)
        self.gold_color = (215, 195, 0)
        self.text_editor = pygame.font.SysFont('serif', int(screen.get_height() * text_koeff))
        self.text = self.text_editor.render(str(self.gold), True, self.gold_color)

    def set_gold(self):
        self.gold = self.interface.player.gold
        self.text = self.text_editor.render(str(self.gold), True, self.gold_color)

    def draw(self, screen):
        x, y = self.x + self.height * 0.2, self.y + self.height * 0.2
        width, height = self.height * 0.7, self.height * 0.7
        pygame.draw.rect(screen, self.gold_color, (x, y, width, height))
        screen.blit(self.text, (x + width * 1.6, y))

class Interface: # здесь будут храниться все элементы интерфеса
    def __init__(self, screen, controller, player):
        self.controller = controller
        self.player = player
        self.x = 0
        self.y = screen.get_height() * 4/5
        self.width = screen.get_width()
        self.height = screen.get_height() - self.y + 1
        self.screen = screen
        self.color = (65, 12, 150)
        self.but_zone = ButtonZone(self.x + self.width * 0.65,
                                   self.y + self.height * 0.05,
                                   self.width * 0.347,
                                   self.height * 0.9, self)
        self.text_zone = TextZone(self.x + self.width * 0.3,
                                  self.y + self.height * 0.05,
                                  self.width * 0.344,
                                  self.height * 0.9, self, screen)
        self.hand_zone = HandZone(self.x + self.width * 0.005,
                                  self.y + self.height * 0.05,
                                  self.width * 0.29,
                                  self.height * 0.9, self)
        self.gold_zone = GoldZone(self.x, self.y - self.height * 0.2,
                                  self.width * 0.06, self.height * 0.21, self, screen)
    def set_buts(self, buttons):
        self.but_zone.set(buttons)

    def set_text(self, text):
        self.text_zone.set(text)

    def add_text(self, text):
        self.text_zone.add(text)

    def normalize(self, cards, place):
        self.controller.normalize(cards, place)

    def set_player(self, player):
        if self.controller.active_player.ai: return
        self.player = player
        self.hand_zone.set_hand()
        self.gold_zone.set_gold()

    def get_cards(self):
        cards = []
        if len(self.but_zone.buttons) > 0: cards += self.but_zone.buttons
        if len(self.hand_zone.hand) > 0: cards += self.hand_zone.hand
        return cards

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
        self.text_zone.draw(self.screen)
        self.hand_zone.draw(self.screen)
        self.but_zone.draw(self.screen)
        self.gold_zone.draw(self.screen)

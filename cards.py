import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Game():
    def __init__(self, deck_char, deck_quar, screen, p_value):
        self.screen = screen
        self.quarters = deck_quar
        self.deck_char = deck_char
        self.deck_quar = deck_quar
        self.not_picked = True
        self.players = []
        self.create_player(p_value)

    def create_player(self, p_value):
        WIDTH = pygame.display.Info().current_w
        HEIGHT = pygame.display.Info().current_h
        self.players = [Player(WIDTH / 2, HEIGHT - 277, self.deck_quar, WHITE, self.screen), Player(234, 234, self.deck_quar, RED, self.screen)]


    def draw(self):
        for player in self.players:
            player.draw()
        for i in range(len(self.quarters)):
            self.quarters[len(self.quarters) - i - 1].draw()

class Player():
    def __init__(self, x, y, deck, color, screen):
        self.x = x
        self.y = y
        self.width = 234
        self.height = 234
        self.screen = screen
        self.deck = deck
        self.color = color
        self.not_picked = True

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

    def mouse_down(self, event):
        for card in self.deck:
            if self.not_picked:
                self.not_picked = card.mouse_down(event, self.deck)

    def mouse_up(self):
        self.not_picked = True
        for card in self.deck:
            card.mouse_up()

    def mouse_move(self, event):
        for card in self.deck:
            card.move(event)

class Card():
    def __init__(self, x, y, width, height, image, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image_prime = image
        self.image = pygame.transform.scale(self.image_prime, (self.width, self.height))
        self.screen = screen
        self.grab = False
        self.margin = 0

    def resize(self, koeff):
        x = self.x - self.width * koeff
        y = self.y - self.height * koeff
        width = int(self.width + self.width * koeff * 2)
        height = int(self.height + self.height * koeff * 2)
        self.image = pygame.transform.scale(self.image_prime, (width, height))
        return [x, y]

    def card_up(self, deck):
        ind = deck.index(self)
        card = deck[ind]
        for i in range(ind):
            deck[ind - i] = deck[ind - i - 1]
        deck[0] = card

    def mouse_down(self, event, deck):
        if event[0] >= self.x and event[1] >= self.y and event[0] <= self.width + self.x and event[1] <= self.height + self.y:
            self.grab = True
            self.margin = 1e-2
            self.card_up(deck)
            return False
        return True

    def mouse_up(self):
        self.grab = False
        self.margin = 0

    def move(self, event):
        if self.grab:
            self.x += event[0]
            self.y += event[1]

    def draw(self):
        coords = self.resize(self.margin)
        self.screen.blit(self.image, (coords[0], coords[1]))
        if self.grab and self.margin < 2e-2:
            self.margin += 5e-3
    # def draw(self):
    #     if self.grab and self.margin < 2:
    #         self.margin += self.margin * 2e-1
    #     x = self.x - self.margin
    #     y = self.y - self.margin
    #     width = self.width + 2 * self.margin
    #     height = self.height + 2 * self.margin
    #     pygame.draw.rect(self.screen, (0, 255, 0), (x, y, width, height))
    #     pygame.draw.rect(self.screen, self.color, (x + 2, y + 2, width - 4, height - 4))

class Quartal(Card):
    def __init__(self, x, y, width, height, image, screen, type, value):
        Card.__init__(self, x, y, width, height, image, screen)
        self.type = type
        self.value = value

    def build(self, gold):
        sell = self.value - gold
        result = [False, 0]
        if sell >= 0:
            result[0] = True
            result[1] = sell
        else:
            result[1] = gold
        return result


    def destroy(self):
        pass
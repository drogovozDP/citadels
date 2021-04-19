import pygame, random

class field:
    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.screen = screen
        self.gays = []
        self._create_gays(screen)
        self.clicked = False

    def _create_gays(self, screen):
        for i in range(5):
            self.gays.append(Gay(screen, random.randint(0, screen.get_width()),
                                 random.randint(0, screen.get_height()), self, (234, 45, 123)))
            self.gays.append(Gay(screen, self.width * .8, self.height * .3, self, (234, 123, 45)))
    def draw(self):
        pygame.draw.rect(self.screen, (50, 50, 50), (self.x, self.y, self.width, self.height))
        for gay in self.gays:
            gay.run()

    def set_click(self):
        x, y = pygame.mouse.get_pos()
        x, y = x - self.x, y - self.y
        k_x, k_y = x / self.width, y / self.height
        print(k_x * self.width, k_y * self.height , '|||', self.width, self.height)
        self.clicked = not self.clicked

    def delta(self, rel):
        if not self.clicked: return
        x, y = rel[0], rel[1]
        self.x += x
        self.y += y

    def zoom(self, koeff):
        if koeff < 0: koeff = .1
        else: koeff = -.1
        x, y = pygame.mouse.get_pos()
        x, y = x - self.x, y - self.y
        k_x, k_y = x / self.width, y / self.height

        self.x -= (self.width * koeff) * k_x#(self.screen.get_width() / mouse_x)
        self.y -= (self.height * koeff) * k_y#(self.screen.get_height() / mouse_y)
        self.width += self.width * koeff
        self.height += self.height * koeff
        for gay in self.gays:
            gay.x += gay.x * koeff
            gay.y += gay.y * koeff
            gay.width += gay.width * koeff
            gay.height += gay.height * koeff

class Gay:
    def __init__(self, screen, x, y, field, color):
        self.screen = screen
        self.field = field
        self.x = x
        self.y = y
        self.color = color
        self.width = screen.get_height() * .2
        self.height = screen.get_height() * .2

    def run(self):
        x = self.x + self.field.x
        y = self.y + self.field.y
        pygame.draw.rect(self.screen, self.color, (x, y, self.width, self.height))

# from test import*
# running = not not True
# gay_field = field(screen)
#
# while running:
#     clock.tick(FPS)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#             gay_field.set_click()
#         if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
#             gay_field.set_click()
#         if event.type == pygame.MOUSEMOTION:
#             gay_field.delta(event.rel)
#         if event.type == pygame.MOUSEWHEEL:
#             gay_field.zoom(event.y)
#     screen.fill((0, 0, 0))
#     gay_field.draw()
#     pygame.display.update()
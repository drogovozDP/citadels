from Player import Player
from characters import*
from Quarter import deck
import AI, random

colors = [(34, 123, 255), (165, 50, 54), (165, 150, 54), (65, 150, 54),
          (165, 50, 154), (15, 220, 54), (165, 0, 54)] # временно будем использовать для определения где какой игрок

class Game(): # нужны приватные методы, чтобы ограничить возможности игроков
    def __init__(self, names, controller):
        self.running = True
        self.max_city_size = 7
        self.deckQuar = deck # колода кварталов
        self.character = character(None, self, 'noname') # пустой персонаж, он всегда взят
        self.deckChar = [Assassin(None, self, 'Assassin'), Thief(None, self, 'Thief'), Wizard(None, self, 'Wizard'),
                         King(None, self, 'King'), Bishop(None, self, 'Bishop'), Merchant(None, self, 'Merchant'),
                         Architect(None, self, 'Architect'), Warlord(None, self, 'Warlord')] # все персонажи
        self.players = [] # игроки заполняются при вызове self.init()
        self.queue = [None] * 8 # порядок хода игроков
        self.firstConstruct = None # игрок, который первый достроил город

        self.preparing = True
        self.rounding = False
        self.not_choosen = 8
        self.choos_char = True
        self.state = {'choose char': True, 'drop char': False, 'resources': False, 'take quarter': False,
                      'action pool': False, 'build': False, 'character ability': False, 'grave yard': False,
                      'smithy': False, 'laboratory': False}
        self.controller = controller
        self.init(names)



    def init(self, names):
        width = self.controller.get_width()
        height = self.controller.get_height()
        hands = []
        for i in range(len(names)):
            hand = []
            for j in range(4):
                hand.append(self.deckQuar.pop(0))
            hands.append(hand)
        pos = []
        p_width, p_height = width / 3, height / 2.3
        rate = width / len(names)
        step = rate / len(names)
        if len(names) == 2: # высчитываем расположение каждого игрока в зависимости от их количества
            for i in range(len(names)):
                pos.append([rate * i + step - p_width / 2, height / 2 - p_height / 2, p_width, p_height, colors[i]])
        if len(names) == 3:
            pos.append([rate + step * 1.5, p_height / 2, p_width, p_height, colors[0]])
            pos.append([p_width + rate * 2 + step * 1.5,p_height / 2, p_width, p_height, colors[2]])
            pos.append([p_width + rate + step * 1.5 , p_height * 2.65, p_width, p_height, colors[1]])
        if len(names) == 4:
            pos.append([p_width * 1.7, p_height * .5, p_width, p_height, colors[0]])
            # pos.append([p_width, 0, p_width, p_height, colors[0]])
            pos.append([p_width * 3.3, p_height * .5, p_width, p_height, colors[1]])
            pos.append([p_width * 3.3, p_height * 2.5, p_width, p_height, colors[3]])
            pos.append([p_width * 1.7, p_height * 2.5, p_width, p_height, colors[2]])
        if len(names) == 5:
            pos.append([p_width * 2.75 + p_width * .5, p_height * .5, p_width, p_height, colors[0]])
            pos.append([p_width * 4.5, p_height * 2, p_width, p_height, colors[2]])
            pos.append([p_width * 4, p_height * 3.5, p_width, p_height, colors[4]])
            pos.append([p_width * 2.5, p_height * 3.5, p_width, p_height, colors[3]])
            pos.append([p_width * 2, p_height * 2, p_width, p_height, colors[1]])
        if len(names) == 6:
            pos.append([p_width * 2.5, p_height * .5, p_width, p_height, colors[0]])
            pos.append([p_width * 4, p_height * .5, p_width, p_height, colors[1]])
            pos.append([p_width * 4.5, p_height * 2, p_width, p_height, colors[3]])
            pos.append([p_width * 4, p_height * 3.5, p_width, p_height, colors[5]])
            pos.append([p_width * 2.5, p_height * 3.5, p_width, p_height, colors[4]])
            pos.append([p_width * 2, p_height * 2, p_width, p_height, colors[2]])
        if len(names) == 7:
            pos.append([p_width * 4.5, p_height * .5, p_width, p_height, colors[0]])
            pos.append([p_width * 5.5, p_height * 2, p_width, p_height, colors[2]])
            pos.append([p_width * 6, p_height * 3.5, p_width, p_height, colors[4]])
            pos.append([p_width * 5.25, p_height * 5, p_width, p_height, colors[6]])
            pos.append([p_width * 3.75, p_height * 5, p_width , p_height, colors[5]])
            pos.append([p_width * 3, p_height * 3.5, p_width, p_height, colors[3]])
            pos.append([p_width * 3.5, p_height * 2, p_width, p_height, colors[1]])
        self.players.append(Player(names[0], self, hands[0], pos[0], None))
        # self.players.append(Player(names[0], self, hands[0], pos[0], AI.Ai(self, self.controller, names[0])))
        for i in range(len(names) - 1):
            self.players.append(Player(names[i + 1], self, hands[i + 1], pos[i + 1], AI.Ai(self, self.controller, names[i + 1])))
            # self.players.append(Player(names[i + 1], self, hands[i + 1], pos[i + 1], None))

    def zoom_players(self, koeff):
        def set_zoom(cards):
            for card in cards:
                card.x += card.x * koeff
                card.y += card.y * koeff
                card.width += card.width * koeff
                card.height += card.height * koeff
                card.update()
        for player in self.players:
            player.setTextRenderer()
            set_zoom(player.hand)
            set_zoom(player.city)
            # set_zoom(player.charList)
            player.x += player.x * koeff
            player.y += player.y * koeff
            player.width += player.width * koeff
            player.height += player.height * koeff
        set_zoom(self.deckChar)
        set_zoom(self.deckQuar)

    def _random_drop(self, hide):
        self.not_choosen -= 1
        index = random.randint(0, 7)
        while self.deckChar[index].choosen: index = random.randint(0, 7)
        if not hide and index == 3:
            while index == 3:
                print('King! King!! King!!!')
                index = random.randint(0, 7)
                while self.deckChar[index].choosen: index = random.randint(0, 7)
        self.deckChar[index].choosen = True
        self.controller.append_drop(self.deckChar[index])
        if not hide:
            print(self.deckChar[index].name, 'dropped')
            self.deckChar[index].state = "open"
        return index

    def _choosen_drop(self, name):
        # index = self.controller.index_playe1r
        # self.players[index].choose_drop(name)
        self.active_player().choose_drop(name)

    def _give_char(self, player):
        print(player.name, 'выбирает :з')
        index = player.choose_character(self.deckChar)
        self.queue[index] = player
        self.deckChar[index].player = player

    def _reload(self): # забирает у всех игроков карты персонажей, делает колоду персонажей полной, опусташает очередь
        self.not_choosen = 8
        self.controller.dropList.clear()
        self.preparing = True
        game_running = True
        self.set_active_player(self.players[0])
        print("перезагружаем игру")
        for player in self.players:
            player.dropCharList()
            player.character = self.character # отдаем каждому игроку нейтрального персонажа
            if len(player.city) >= self.max_city_size: # проверка на конец игры
                game_running = False
                self._winner()

        for char in self.deckChar:
            char.state = "hide"
            char.choosen = False # делаем каждого персонажа НЕ выбранным
            char.alive = True # делаем каждого персонажа вновь живым(исправляем активити ассасина)
            char.robed = False # делаем каждого необоворованным, чтобы обворовать
            char.player = None # теперь карта персонажа не присовоена игроку
            char.set_pos(0, 0) # забираем персонажей из зон игроков

        for i in range(len(self.queue)): # опусташаем очередь
            self.queue[i] = None
        if game_running: self.state['choose char'] = True # если игра не закончена, то ожидаем выбор персонажа
        self.info()
        self.update_interface()
        self.running = game_running

    def giveCrown(self, player):
        index = 0
        for i in range(len(self.players)):
            if player.name == self.players[i].name:
                index = i
        for i in range(index):
            peasant = self.players[0]
            del self.players[0]
            self.players.append(peasant)
        print('now king is:', self.players[0].name, 'peasants count:', len(self.players) - 1)

    def giveCard(self, count): # даем count карт игроку который вызвал этот метод
        cards = []
        if len(self.deckQuar) < count: count = len(self.deckQuar)
        for i in range(count):
            cards.append(self.deckQuar[0])
            del self.deckQuar[0]
        return cards

    def takeCard(self, cards):
        for card in cards:
            self.deckQuar.append(card)

    def graveYard(self, quarter):
        sold = False
        for player in self.players:
            if not sold:
                sold = player.graveyard_action(quarter)
        if not sold:
            self.takeCard([quarter])

    def _winner(self):
        record = []
        for player in self.players:
            value = 0
            colors = {'pink': False, 'yellow': False, 'blue': False, 'green': False, 'red': False}
            for quarter in player.city:
                if quarter.name != 'hauntedcity_bonus':
                    colors[quarter.color] = True
                value += quarter.bounus()
            color_count = 0
            for col in colors:
                if colors[col]: color_count += 1
            if player.all_actions['hauntedcity_bonus'] and color_count < 5:
                color_count += 1
            if color_count == 5: value += 3
            if len(player.city) >= self.max_city_size: value += 2
            if player.name == self.firstConstruct.name: value += 2
            if player.all_actions['imperialtreasury_bonus']: value += player.gold
            if player.all_actions['maproom_bonus']: value += len(player.hand)
            record.append(value)
            player.info()
        print("\nwinner is:", self.players[record.index(max(record))].name)
        print("score:", max(record))

    def info(self): # просто дает информацию о состоянии игры
        for player in self.players:
            player.info()
        print(self.state)

    def active_player(self):
        player = self.controller.active_player
        return player

    def set_active_player(self, player):
        self.controller.active_player = player

    def set_text(self, text):
        if self.active_player().ai: return
        self.controller.interface.set_text(text)

    def add_text(self, text):
        if self.active_player().ai: return
        self.controller.interface.add_text(text)

    def update_interface(self):
        self.controller.interface.set_player(self.active_player())

    def global_input(self, value): # сюда идут все нажатия на кнопки, которые создал класс game
        # print(self.not_choosen)
        if self.state['choose char']:
            self.active_player().choose_character(value)
            self.update_interface()
            self.not_choosen -= 1
            text = 'выберите персонажа, '
            if self.not_choosen == 6 and len(self.players) == 2:
                self.controller.next_player()
                self.set_text('выберите персонажа, ' + self.active_player().name)
                return
            if len(self.players) == 2:
                self.state['choose char'], self.state['drop char'] = False, True
                self.controller.interface.add_text('сбросьте персонажа')
                return
            elif self.not_choosen == 1 and len(self.players) < 7:
                self.state['choose char'], self.state['drop char'] = False, True
                text = 'сбросьте персонажа, '
                self.set_text(text + self.active_player().name)
                return
            elif self.not_choosen == 1 and len(self.players) == 7:
                char = self.controller.dropList[0]
                self.controller.dropList.clear()
                self.controller.create_buttons([[char.primImg["open"], char.name]], False)

            elif self.not_choosen == 0 and len(self.players) == 7:
                self.not_choosen += 1
                self.state['choose char'], self.state['drop char'] = False, True
                text = 'сбросьте персонажа, '
                self.set_text(text + self.active_player().name)
                return
            self.controller.next_player()
            self.set_text(text + self.active_player().name)
        elif self.state['drop char']:
            self._choosen_drop(value)
            self.state['choose char'], self.state['drop char'] = True, False
            self.controller.next_player()
            if self.not_choosen == 0:
                self.preparing = False
                self.state['choose char'] = False
                self.rounding = True
            else:
                self.set_text('выберите персонажа, ' + self.active_player().name)
        elif self.state['resources']:
            self.active_player().take_resources(value)
        elif self.state['take quarter']:
            self.active_player().take_quarter(value)
        elif self.state['action pool']:
            self.active_player().recive_command(value)
        elif self.state['build']:
            self.active_player().build(value)
        elif self.state['character ability']:
            self.active_player().character.ability(value)
        elif self.state['grave yard']:
            self.active_player().buy_quart(value)
        elif self.state['smithy']:
            self.active_player().smithy_bonus(value)
        elif self.state['laboratory']:
            self.active_player().burn(value)

    def prepareChoosHand(self, hide, open):
        for i in range(hide):
            self._random_drop(True)
        for i in range(open):
            self._random_drop(False)
        chars = []
        for char in self.deckChar:
            if not char.choosen: chars.append([char.primImg["open"], char.name])
        self.controller.create_buttons(chars, False)
        self.set_text('выберите персонажа, ' + self.active_player().name)
        self.controller.shuffle()
        if self.active_player().ai: # если раунд начинает ИИ
            self.active_player().ai.setSolution("chooseChar")

    def prepare_round(self):
        if len(self.players) == 2 or len(self.players) == 3: self.prepareChoosHand(1, 0)
        elif len(self.players) == 4: self.prepareChoosHand(1, 2)
        elif len(self.players) == 5: self.prepareChoosHand(1, 1)
        elif len(self.players) == 6: self.prepareChoosHand(1, 0)
        elif len(self.players) == 7: self.prepareChoosHand(1, 0)

    def round(self): # перед тем как продолжить, нужно сделать так, чтобы постреонные кварталы, золото и закрытые персонажи рисовались
        for i in range(len(self.queue)):
            if self.queue[i]:
                self.controller.active_player = self.queue[i]
                self.active_player().action(i + 1)
                self.queue[i] = None # это вызовит ошибки в дальнейшем, очередь используется в методах персонажей
                return
        print("round is over")
        self.rounding = False

    def run(self):
        if self.preparing: self.prepare_round()
        elif self.rounding: self.round()
        # self._prepare_round()
        # self._round()
        else: self._reload()
        # self.info()

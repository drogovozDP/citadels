import pygame, random
from Button import Card, h_koeff
from Player import Player, translate

class character(Card): # шаблон от которого будем наследоваться
    def __init__(self, player, gameMaster, name):
        self.initiative = 0
        self.choosen = True
        self.player = player
        self.gameMaster = gameMaster
        self.alive = True
        self.robed = False
        self.name = name
        # выше механика, ниже отрисовка
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.koeff = h_koeff
        self.state = "hide"
        self.primImg = {"open": pygame.image.load("Sprites/characters/" + self.name + ".png"),
                        "hide": pygame.image.load("Sprites/characters/character.png")}  # загружаем текстуру карты квартала
        self.img = None
    def ability(self, info):
        print(self.initiative)
    def default(self):
        pass
    def draw(self, screen):
        # if not self.player: return
        screen.blit(self.img[self.state], (self.x, self.y))
    def set_pos(self, x, y):
        self.x = x
        self.y = y
    def finish_ability(self):
        self.gameMaster.controller.del_but('all')  # убрали оставшихся в живвых персонажей
        self.gameMaster.state['character ability'] = False  # теперь ВСЕ состояния должны быть фолс(это важно)
        self.gameMaster.update_interface()
        self.player.activate_action()  # возвращаем оставшийся пулл действий

class Assassin(character):
    def __init__(self, player, gameMaster, name):
        character.__init__(self, player, gameMaster, name)
        self.choosen = False
        self.initiative = 1 # порядок вызова персонажа
    def ability(self, victim):
        if victim:
            victim.alive = False
            self.finish_ability()
        else:
            self.gameMaster.controller.del_but('all')
            buttons, chars = [], self.gameMaster.deckChar
            for i in range(len(chars) - 1):
                buttons.append([chars[i + 1].primImg["open"], chars[i + 1]])
            print(self.player.name, 'wants to kill...')
            self.gameMaster.set_text('Кто сегодня не пойдет на работу?')
            self.gameMaster.controller.create_buttons(buttons, False)
            self.gameMaster.controller.interface.hand_zone.set_hand()

class Thief(character):
    def __init__(self, player, gameMaster, name):
        character.__init__(self, player, gameMaster, name)
        self.choosen = False
        self.initiative = 2
    def ability(self, victim):
        if victim:
            victim.robed = True
            self.finish_ability()
        else:
            self.gameMaster.controller.del_but('all')
            buttons, chars = [], self.gameMaster.deckChar
            for i in range(len(chars) - 2):
                if chars[i + 2].alive:
                    buttons.append([chars[i + 2].primImg["open"], chars[i + 2]])
            print(self.player.name, 'wants to steal')
            self.gameMaster.set_text('Воруй!')
            self.gameMaster.controller.create_buttons(buttons, False)

class Wizard(character):
    def __init__(self, player, gameMaster, name):
        character.__init__(self, player, gameMaster, name)
        self.choosen = False
        self.initiative = 3
    def _exchange_with_deck(self):
        buttons = []
        for card in self.player.hand:
            buttons.append([card.primImg["open"], card])
        self.gameMaster.controller.del_but('all')
        self.gameMaster.controller.create_buttons(buttons, True)
        self.gameMaster.set_text("Выбери те карты, которые")
        self.gameMaster.add_text("ты хочешь обменять с колодой")
    def _exchange_with_player(self, players):
        targets = []
        for player in players:
            if player != self.player:
                targets.append(player)
        buttons = []
        for aim in targets:
            buttons.append([aim.name, aim])
        buttons.append(['Отмена', 'cancel'])
        self.gameMaster.controller.del_but('all')
        self.gameMaster.controller.create_buttons(buttons, False)
        self.gameMaster.set_text('Выбери игрока для обмена')
        print('choose a player to exchange')
    def ability(self, info):
        if info == "cancel":
            self.player.action_pool.append('ability')
            self.finish_ability()
        elif not info:
            self.gameMaster.controller.del_but('all')
            print(self.player.name, 'thinks about who to change with')
            self.gameMaster.set_text('Поменятсья картами')
            self.gameMaster.add_text('с колодой или с игроком?')
            self.gameMaster.controller.create_buttons([['Колода', 'deck'],
                                                       ['Игрок', 'player'],
                                                       ['Отмена', 'cancel']], False)
        elif info == 'deck':
            self._exchange_with_deck()
        elif info == 'player':
            self._exchange_with_player(self.gameMaster.players)
        elif type(info) == Player:
            enemy_cards = info.hand[:]
            self_cards = self.player.hand[:]
            self.player.hand = enemy_cards
            info.hand = self_cards
            self.finish_ability()
        elif type(info) == list:
            info.pop()
            cards, flags = [], []
            for flag in info:
                if flag.choosen:
                    flags.append(flag)
            for flag in flags:
                for i in range(len(self.player.hand)):
                    if flag.value == self.player.hand[i]:
                        print(self.player.hand[i].name)
                        cards.append(self.player.hand.pop(i))
                        break
            self.gameMaster.takeCard(cards)
            print("we have to exchange", len(cards), "cards")
            self.player.hand += self.gameMaster.giveCard(len(cards))[:]
            self.finish_ability()

class King(character):
    def __init__(self, player, gameMaster, name):
        character.__init__(self, player, gameMaster, name)
        self.choosen = False
        self.initiative = 4
    def default(self):
        if self.player.name == self.gameMaster.players[0].name:
            return
        self.gameMaster.giveCrown(self.player)

    def ability(self, info):
        gold = 0
        if self.player.all_actions['schoolofmagic_bonus']: gold += 1
        for card in self.player.city:
            if card.color == 'yellow':
                gold += 1
        print('you recived ' + str(gold) + ' gold!')
        self.player.gold += gold
        self.player.setTextRenderer()
        self.finish_ability()

class Bishop(character):
    def __init__(self, player, gameMaster, name):
        character.__init__(self, player, gameMaster, name)
        self.choosen = False
        self.initiative = 5
    def ability(self, info):
        gold = 0
        if self.player.all_actions['schoolofmagic_bonus']: gold += 1
        for card in self.player.city:
            if card.color == 'blue':
                gold += 1
        print('you recived ' + str(gold) + ' gold!')
        self.player.gold += gold
        self.player.setTextRenderer()
        self.finish_ability()

class Merchant(character):
    def __init__(self, player, gameMaster, name):
        character.__init__(self, player, gameMaster, name)
        self.choosen = False
        self.initiative = 6
    def default(self): # в начале хода получает 1 монетку(после того как обворует вор)
        print('you just recived 1 gold!')
        self.player.gold += 1
        self.player.setTextRenderer()
    def ability(self, info):
        gold = 0
        if self.player.all_actions['schoolofmagic_bonus']: gold += 1
        for card in self.player.city:
            if card.color == 'green':
                gold += 1
        print('you recived ' + str(gold) + ' gold!')
        self.player.gold += gold
        self.player.setTextRenderer()
        self.finish_ability()

class Architect(character):
    def __init__(self, player, gameMaster, name):
        character.__init__(self, player, gameMaster, name)
        self.choosen = False
        self.initiative = 7
    def default(self): # в начале хода должен получить 2 карты квартала
        cards = self.gameMaster.giveCard(2)
        row = ''
        for i in range(len(cards)):
            row += cards[i].name + '(' + str(i + 1) + '), '
            self.player.hand.append(cards[i])
        row = row[0:len(row) - 2]
        print('you just recived', len(cards), 'cards!', row)
    def ability(self, info):
        self.player.action_pool.pop() # убираем выбор "done"
        for i in range(2):
            self.player.action_pool.append('build') # теперь игрок может посмтроить 3 раза
        self.player.action_pool.append('done') # возвращаем в конец "done"
        self.finish_ability()

class Warlord(character):
    def __init__(self, player, gameMaster, name):
        character.__init__(self, player, gameMaster, name)
        self.choosen = False
        self.initiative = 8
        self.ability_pool = {'coins': False, 'destroy': False}
    def default(self):
        for key in self.ability_pool:
            self.ability_pool[key] = True
    def choose_player(self):
        players = self.gameMaster.players  # просто чтобы меньше кода было
        self.gameMaster.set_text('Выебри игрока')
        print('you have', self.player.gold)
        buttons = []
        for player in players:  # пробегаем по всем игрокам
            bishop = False
            for char in player.charList:
                if char.name == 'Bishop' or len(player.city) >= self.gameMaster.max_city_size:
                    bishop = True
            if not bishop:
                buttons.append([player.name, player])
        buttons.append(['Отмена', 'cancel'])
        self.gameMaster.controller.del_but('all')
        self.gameMaster.controller.create_buttons(buttons, False)
    def show_city(self, victim):
        self.gameMaster.controller.del_but('all')
        buttons = []
        for quar in victim.city:
            if quar.value - 1 + victim.greatwall_bonus(quar) <= self.player.gold and quar.name != 'keep':
                buttons.append([quar.primImg["open"], [victim, quar]])
        buttons.append(['Отмена', 'cancel'])
        self.gameMaster.controller.create_buttons(buttons, False)
    def destroy(self, info):
        victim, target = info[:]
        self.player.gold -= target.value - 1 + victim.greatwall_bonus(target)
        self.player.setTextRenderer()
        for i in range(len(victim.city)):
            if victim.city[i] == target:
                victim.city.pop(i)
                break
        print(target.name, "is destroyed")
        target.destroyed(victim)
        self.ability_pool['destroy'] = False
        self.gameMaster.controller.del_but('all')
        self.gameMaster.update_interface()
        self.ability(None)
        self.gameMaster.graveYard(target)
    def take_gold(self):
        gold = 0
        if self.player.all_actions['schoolofmagic_bonus']: gold += 1
        for card in self.player.city:
            if card.color == 'red':
                gold += 1
        print('you recived', gold, 'gold!')
        self.player.gold += gold
        self.player.setTextRenderer()
        self.ability_pool['coins'] = False
        self.ability(None)
        self.gameMaster.update_interface()
    def finish_ability(self, cancel):
        character.finish_ability(self)
        if not cancel:
            for key in self.ability_pool:
                self.ability_pool[key] = False
    def ability(self, info):
        if info == "cancel":
            self.player.action_pool.append('ability')
            self.finish_ability(True)
        elif not info:
            self.gameMaster.controller.del_but('all')
            self.gameMaster.set_text('Разрушить квартал или взять')
            self.gameMaster.add_text('монетки(можно сделать и то и то)?')
            buttons = []
            for key in self.ability_pool:
                if self.ability_pool[key]:
                    buttons.append([translate[key], key])
            if len(buttons) == 0:
                self.finish_ability(False)
                return
            buttons.append(['Отмена', 'cancel'])
            self.gameMaster.controller.create_buttons(buttons, False)
        elif info == "coins":
            self.take_gold()
        elif info == "destroy":
            self.choose_player()
        elif type(info) == Player:
            self.show_city(info)
        elif type(info) == list:
            self.destroy(info)
import pygame
from Button import text_koeff
from Docer import doc

translate = {'done': 'завершить ход', 'build': 'построить', 'ability': 'способность', 'laboratory_action': 'лаборатория',
              'graveyard_action': 'кладбище', 'greatwall_bonus': 'великая стена',
              'observatory_bonus': 'обсерватория', 'smithy_action': 'кузня', 'library_bonus': 'библиотека',
              'schoolofmagic_bonus': 'школа магии', 'hauntedcity_bonus': 'город призраков',
              'imperialtreasury_bonus': 'имперская казна', 'maproom_bonus': 'собрание карт', 'destroy': 'Разрушить',
             'coins': 'Монетки'}

class Player():
    def __init__(self, name, gameMaster, hand, pos, ai):
        self.ai = ai # определяет ИИ это или игрок
        self.name = name
        self.gameMaster = gameMaster  # это эксемпляр игры(у всех он одинаковый), они будут так влиять друг на друга
        self.charList = [] # это нужно для игры вдвоем или втроем. Максимум будет 2 персонажа в этом списке
        self.character = None
        self.city = [] # построенные кварталы
        self.hand = hand # кварталы в руке
        self.gold = 2
        self.take = {'gold': 2, 'quarter': 2} # сколько игрок может взять золота или кварталов
        self.all_actions = {'build': True, 'ability': True, # все действия игроков
                            'laboratory_action': False, 'graveyard_action': False,
                            'greatwall_bonus': False, 'observatory_bonus': False,
                            'smithy_action': False, 'library_bonus': False,
                            'schoolofmagic_bonus': False, 'hauntedcity_bonus': False,
                            'imperialtreasury_bonus': False, 'maproom_bonus': False}
        self.action_pool = []
        self.x = pos[0]
        self.y = pos[1]
        self.width = pos[2]
        self.height = pos[3]
        self.color = pos[4]
        self.text_size = text_koeff
        self.renderer = pygame.font.SysFont('serif', int(gameMaster.controller.get_height() * self.text_size))
        self.textName = self.renderer.render(name, True, self.color)
        self.textGold = self.renderer.render("Золото: " + str(self.gold), True, self.color)
        self.selected = False
        if ai != None: ai.player = self

    def draw(self, screen):
        dx, dy = self.gameMaster.controller.x, self.gameMaster.controller.y
        if self.selected:
            koeff = self.height * 5e-2
            pygame.draw.rect(screen, (150, 150, 150), (self.x + dx - koeff, self.y + dy - koeff, self.width + koeff * 2, self.height + koeff * 2))
        pygame.draw.rect(screen, self.color, (self.x + dx, self.y + dy, self.width, self.height))
        if len(self.hand) > 0: self.gameMaster.controller.normalize(self.hand, self)
        if len(self.city) > 0: self.gameMaster.controller.normalize(self.city, self)
        for i in range(len(self.charList)):
            self.charList[i].x = self.x + i * self.charList[i].width + dx
            self.charList[i].y = self.y - self.charList[i].height + dy
        for card in self.hand:
            card.y += (self.y + self.height) - (card.y + card.height) + dy
            card.x += dx
            card.draw(screen)
        for card in self.city:
            card.y = self.y + dy
            card.x += dx
            card.draw(screen)
        for char in self.charList:
            char.draw(screen)
        screen.blit(self.textName, (self.x + self.width - self.textName.get_width() + dx, self.y - self.textName.get_height()*2 + dy))
        screen.blit(self.textGold, (self.x + self.width - self.textGold.get_width() + dx, self.y - self.textGold.get_height() + dy))

    def setTextRenderer(self):
        self.renderer = pygame.font.SysFont('serif', int(self.gameMaster.controller.height * self.text_size))
        self.textName = self.renderer.render(self.name, True, self.color)
        self.textGold = self.renderer.render("Золото: " + str(self.gold), True, self.color)

    def choose_character(self, char_name):
        for char in self.gameMaster.deckChar:
            if char.name == char_name:
                char.choosen = True
                self.charList.append(char)
                char.player = self
        char = self.charList[-1]
        self.charList[-1].x = self.x + char.width * (len(self.charList) - 1)
        self.charList[-1].y = self.y - char.height
        self.gameMaster.queue[char.initiative - 1] = self
        doc.write(f"->pick: {char_name};")

    def choose_drop(self, char_name):
        for char in self.gameMaster.deckChar:
            if char.name == char_name:
                char.choosen = True
                self.gameMaster.controller.append_drop(char)
        self.gameMaster.not_choosen -= 1

    def _end_action(self):
        self.selected = False
        self.gameMaster.controller.del_but('all')
        print('/done')

    def recive_command(self, command):
        self.action_pool.pop(self.action_pool.index(command)) # убираем это действие из множетсва действий
        self.gameMaster.state['action pool'] = False # теперь мы будем получать сигналы адресованные НЕ выбору дейсвтвия
        if command == 'done':
            self.action_pool.clear()
            self._end_action()
        elif command == 'build':
            self._show_hand()
        elif command == 'ability':
            self._activate_char()
        elif command == 'smithy_action':
            self.smithy_action()
        elif command == 'laboratory_action':
            self.laboratory_action()

    def activate_action(self):
        self.gameMaster.set_text('Выберите действие, ' + self.name)
        self.gameMaster.state['action pool'] = True
        self.gameMaster.controller.del_but('all')
        buttons = []
        for act in self.action_pool:
            buttons.append([translate[act], act])
        self.gameMaster.controller.create_buttons(buttons, False)

    def _activate_char(self):
        self.gameMaster.state['character ability'] = True
        self.character.ability(None)

    def take_quarter(self, quarter):
        self.gameMaster.state['take quarter'] = False
        self.hand.append(quarter)
        for button in self.gameMaster.controller.buttons:
            self.gameMaster.takeCard([button.value])
        self.gameMaster.update_interface()
        self.activate_action()
        doc.write(f"hand({len(self.hand)-1}+1={len(self.hand)}) ~/got: {quarter.name};")

    def _getRow(self, mas):
        str = ""
        for m in mas:
            str += m.name + ', '
        return str[:-2]

    def take_resources(self, kind):
        self.gameMaster.state['resources'] = False
        if kind == 'gold':
            doc.write(f"->resources: gold({self.gold}+{self.take['gold']}={self.gold+self.take['gold']});")
            self.gold += self.take["gold"]
            # print(self.name + ' has gold: ' + str(self.gold) + ", he recived " + str(self.take["gold"]) + " gold")
            self.setTextRenderer() # обновим золото на столе у игрока
            self.activate_action()
        elif kind == 'quarter':
            cards = self.gameMaster.giveCard(self.take['quarter'])
            doc.write(f"->resources: quarter({self.take['quarter']}) ~/{self._getRow(cards)}")
            self.gameMaster.controller.del_but('all')
            if len(cards) == 0:
                self.activate_action()
                return
            if self.all_actions['library_bonus']:
                str = ""
                for quar in cards:
                    str += quar.name + ", "
                    self.hand.append(quar)
                self.gameMaster.update_interface()
                self.activate_action()
                doc.write(f"hand({len(self.hand)-self.take['quarter']}+{self.take['quarter']}="
                          f"{len(self.hand)}) ~/got: {str[:-2]};")
                return
            buttons = []
            for card in cards:
                buttons.append([card.primImg["open"], card])
            self.gameMaster.controller.create_buttons(buttons, False)
            self.gameMaster.state['take quarter'] = True
        self.gameMaster.update_interface()

    def build(self, card):
        self.gameMaster.state['build'] = False
        if card == 'cancel':
            self.action_pool.append('build')
            self.activate_action()
            return
        if card.value > self.gold:
            return
        self.gold -= card.value # нужно обновить золото на интерфейсе
        self.setTextRenderer()
        self.city.append(card)
        self.city[-1].built(self)
        doc.write(f"->build: {card.name};")
        # print(self.name + " have built " + card.name + "(value: " + str(card.value) +")" + ", now he(she) has " + str(self.gold) + " gold")
        for i in range(len(self.hand)):
            if self.hand[i] == card:
                self.hand.pop(i)
                break
        self.activate_action()  # мы вернулись в множество действий, а точнее в его остатки "action pool = True"
        if len(self.city) >= self.gameMaster.max_city_size and self.gameMaster.firstConstruct == None:
            self.gameMaster.firstConstruct = self
        self.gameMaster.update_interface()

    def _show_hand(self):
        if len(self.hand) == 0:
            self.activate_action()
            return
        buttons = []
        for card in self.hand:
            if self.gold >= card.value:
                not_exist = False
                for quar in self.city:
                    if card.name == quar.name:
                        not_exist = True
                if not not_exist:
                    buttons.append([card.primImg["open"], card])
        if len(buttons) == 0:
            self.action_pool.append('build')
            self.activate_action()
            return
        buttons.append(['Отмена', 'cancel'])
        # print('you have', self.gold, 'gold')
        self.gameMaster.set_text(self.name + ', у вас есть ' + str(self.gold) + ' золота')
        self.gameMaster.state['build'] = True
        self.gameMaster.controller.del_but('all')
        self.gameMaster.controller.create_buttons(buttons, False)

    def action(self, initiative):
        for char in self.charList: # выбираем персонажа из множества наших перс-ей относительно инициативы
            if initiative == char.initiative:
                self.character = char
                self.character.state = "open"
        if self.character.alive == False:
            print('oh no, you are dead!') # никто об этом не должен знать
            self.character.state = "hide"
            if self.character.name == 'King':
                self.character.default()
            return
        if self.character.robed: # если персонаж ограблен
            for player in self.gameMaster.players: # смотрим у каждого игрока...
                for char in player.charList: # ...нету ли у него вора(':
                    if char.name == 'Thief' and player != self:
                        player.gold += self.gold
                        player.setTextRenderer()
                        self.gold = 0
                        self.setTextRenderer()
                        self.gameMaster.controller.interface.gold_zone.set_gold()
            print('oh my god, you have lost whole your gold!')
        self.character.default() # применяется свойства персонажа по умолчанию
        # print(self.name + " СЕЙЧАС ДОЛЖЕН ВЗЯТЬ ЗОЛОТО")
        # if self.ai: print(self.ai.solution)
        self.gameMaster.update_interface() # после того как персонаж че-то мог изменить у игрока мог поменяться интерфейс
        for act in self.all_actions: # собираем все действия, которые доступны игроку на данный момент
            if self.all_actions[act]:
                self.action_pool.append(act)
                if act == 'graveyard_action' or act == 'greatwall_bonus' or \
                        act == 'library_bonus' or act == 'schoolofmagic_bonus' or \
                        act == 'hauntedcity_bonus' or act == 'imperialtreasury_bonus' or \
                        act == 'maproom_bonus':
                    self.action_pool.pop()
        self.action_pool.append('done')
        self.gameMaster.state['resources'] = True # теперь гейм будет ждать ответа сбора ресурсов
        self.gameMaster.set_text(self.name +', выберите ' + str(self.take['gold']) + ' золото,')
        self.gameMaster.add_text('либо ' + str(self.take['quarter']) + ' квартала')
        self.gameMaster.controller.create_buttons([['золото', 'gold'], ['кварталы', 'quarter']], False)
        if self.ai: self.ai.setSolution("action")
        self.selected = True

    def laboratory_action(self):
        if len(self.hand) == 0:
            self.burn('cancel')
        else:
            self.gameMaster.set_text(self.name + ', ты можешь сжечь')
            self.gameMaster.add_text('один квартал за две монеты')
            self.gameMaster.state['laboratory'] = True
            self.gameMaster.controller.del_but('all')
            self.gameMaster.controller.create_buttons([['Сжечь', 'burn'], ['Отмена', 'cancel']], False)

    def burn(self, answer):
        if answer == 'cancel':
            self.gameMaster.state['laboratory'] = False
            self.action_pool.append('laboratory_action')
            self.activate_action()
        elif answer == 'burn':
            buttons = []
            for quar in self.hand:
                buttons.append([quar.primImg["open"], [quar]])
            buttons.append(['Отмена', 'cancel'])
            self.gameMaster.controller.del_but('all')
            self.gameMaster.controller.create_buttons(buttons, False)
        elif type(answer) == list:
            self.gold += 2
            self.setTextRenderer()
            card = answer[0]
            for i in range(len(self.hand)):
                if card == self.hand[i]:
                    self.hand.pop(i)
                    break
            self.gameMaster.takeCard(answer)
            self.gameMaster.state['laboratory'] = False
            self.gameMaster.update_interface()
            self.activate_action()

    def smithy_bonus(self, answer):
        if answer == 'cancel' or self.gold < 2 or len(self.gameMaster.deckQuar) < 1:
            self.action_pool.append('smithy_action')
        elif answer == 'pay' and self.gold >= 2:
            cards = self.gameMaster.giveCard(3)
            self.gold -= 2
            self.setTextRenderer()
            for card in cards:
                self.hand.append(card)
            self.gameMaster.update_interface()
        self.gameMaster.controller.del_but('all')
        self.gameMaster.state['smithy'] = False
        self.activate_action()

    def smithy_action(self):
        self.gameMaster.state['smithy'] = True
        self.gameMaster.set_text('Заплати 2 монетки')
        self.gameMaster.add_text('и получи 3 карты ' + self.name)
        buttons = [['Заплатить', 'pay'], ['Отмена', 'cancel']]
        self.gameMaster.controller.del_but('all')
        self.gameMaster.controller.create_buttons(buttons, False)

    def buy_quart(self, quart):
        print("buy or not quarter")
        self.gameMaster.state['grave yard'] = False
        if quart == 'cancel':
            self.gameMaster.takeCard([self.gameMaster.controller.buttons[0].value])
        else:
            self.gold -= 1
            self.setTextRenderer()
            self.hand.append(quart)
        self.gameMaster.controller.del_but('all')
        for player in self.gameMaster.players:
            if player.character.name == 'Warlord':
                self.gameMaster.controller.active_player = player
                player.action_pool.append('ability')
        self.gameMaster.active_player().activate_action()
        self.gameMaster.update_interface()

    def graveyard_action(self, quart):
        if not self.all_actions['graveyard_action'] or self.gold < 1: return False # у игрока нет кладбища или денег
        print("graveYard action!!!")
        self.gameMaster.controller.active_player = self
        self.gameMaster.controller.del_but('all')
        self.gameMaster.controller.create_buttons([[quart.primImg["open"], quart], ['Отмена', 'cancel']], False)
        self.gameMaster.set_text(self.gameMaster.active_player().name + ", ты можешь забрать")
        self.gameMaster.add_text("этот квартал к себе в руку за 1 золото")
        self.gameMaster.state['grave yard'] = True
        self.gameMaster.state['character ability'] = False
        self.gameMaster.state['action pool'] = False
        if self.ai: self.ai.decision("graveyard")
        return True

    def greatwall_bonus(self, quarter):
        if self.all_actions['greatwall_bonus'] and quarter.name != 'greatwall':
            return 1
        else: return 0

    def dropCharList(self):
        self.charList.clear()

    def canBuild(self): # неправильно реализовано
        if len(self.city) == 0 and len(self.hand) > 0: return True
        if len(self.hand) == 0: return False
        exist = []
        for handCard in self.hand:
            for cityCard in self.city:
               if handCard.name == cityCard.name:
                   exist.append(handCard.name)
        if len(exist) == len(self.hand): return False
        else: return True

    def info(self):
        quarters = ""
        built = ""
        for card in self.hand:
            quarters += f"{card.name}, "
        for card in self.city:
            # built += f"{card.name}{card.value, card.color}, "
            built += f"{card.name}, "
        if built == "": built = "None, "
        if quarters == "": quarters = "None, "
        doc.write(self.name +
              ': gold = ' + str(self.gold) +
              '; quarters = ' + quarters[:-2] +
              '; city = ' + built[:-2] + ";")
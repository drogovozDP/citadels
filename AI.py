from Docer import doc
quarColor = ["pink", "yellow", "blue", "green", "red"]
class Ai:
    def __init__(self, gameMaster, controller, name): # name пока что не нужен, но пусть будет
        self.gameMaster = gameMaster
        self.controller = controller
        self.player = None
        self.thinking = 0
        self.solTime = 50
        self.finishCount = 0
        self.finishTime = 6
        self.solution = {"chooseChar": False, "action": False}
        self.favoriteColor = "pink"

    def setText(self, text):
        self.controller.interface.set_text(text)

    def addText(self, text):
        self.controller.interface.add_text(text)

    def _defPlayer(self, name):
        for player in self.gameMaster.players:
            if player.name == name:
                return player

    def setSolution(self, name):
        self.solution[name] = True

    def think(self):
        if self.thinking < self.solTime:
            self.thinking += 1
        else:
            if self.solution["chooseChar"]: self.chooseChar()
            elif self.solution["action"]: self.action()
            else: self.finishAction()
            self.thinking = 0

    def finishAction(self):
        if self.finishCount >= self.finishTime:
            self.controller.getButton("done").click()
            self.finishCount = 0
        else: self.finishCount += 1

    def activeState(self):
        for name in self.gameMaster.state:
            if self.gameMaster.state[name]:
                return name

    def _getColorCount(self, color, place):
        dic = {"pink": 0, "yellow": 0, "green": 0, "blue": 0, "red": 0}
        quarters = []
        if place == "hand": quarters = self.player.hand
        elif place == "city": quarters = self.player.city
        for quar in quarters:
            dic[quar.color] += 1
        return dic[color]

    def chooseChar(self):
        self._getColorCount("green", "hand")
        self.solution["chooseChar"] = False
        if len(self.controller.buttons) == 0: return
        # self.controller.getButton("first").click()
        chars = self.controller.getAllBtn()
        dicChars = {"Assassin": False, "Thief": False, "Wizard": False, "King": False,
                    "Bishop": False, "Merchant": False, "Architect": False, "Warlord": False}
        for char in chars:
            dicChars[char] = True
        if dicChars["Assassin"]: # этап выбора персонажа
            self.controller.getButton("Assassin").click()
        else:
            colorCount = []
            for color in quarColor:
                colorCount.append(self._getColorCount(color, "hand") + self._getColorCount(color, "city"))
            index = colorCount.index(max(colorCount))
            # print(colorCount)
            if index == 1 and dicChars["King"]:
                self.favoriteColor = "yellow"
                self.controller.getButton("King").click()
            elif index == 2 and dicChars["Bishop"]:
                self.favoriteColor = "blue"
                self.controller.getButton("Bishop").click()
            elif index == 3 and dicChars["Merchant"]:
                self.favoriteColor = "green"
                self.controller.getButton("Merchant").click()
            elif index == 4 and dicChars["Warlord"]:
                self.favoriteColor = "red"
                self.controller.getButton("Warlord").click()
            else:
                self.controller.getButton("0").click()
        if self.activeState() == "drop char":
            self.controller.getButton("0").click()

    def _checkMayToBuild(self):
        self.controller.getButton("build").click()
        if self.activeState() == "build":
            self.controller.getButton("cancel").click()
            return True
        else:
            return False

    def action(self):
        if self.activeState() == "resources":
            if self.player.canBuild():
                self.setText(self.player.name +" берет " + str(self.player.take["gold"]) + " золота")
                self.controller.getButton("gold").click()
            else:
                self.controller.getButton("quarter").click()
                self.setText(self.player.name + " берет " + str(self.player.take["quarter"]) + " квартала")
                if self.activeState() == "take quarter":
                    self.controller.getButton("0").click()
        if self.activeState() == "action pool":
            # _checkMayToBuild
            self.controller.getButton("build").click()
            if self.activeState() == "build":
                btns = self.controller.buttons[:-1]
                # print(len(btns), " LENGTH", btns)
                btn = self.controller.getButton("0")
                for quar in btns:
                    if quar.value.color == self.favoriteColor:
                        btn = quar
                        # print(btn.value.color + " ОП ОП ЗАЕБОК!!!")
                        break
                self.addText("Строит " + btn.value.name + " за " + str(btn.value.value) + " золота")
                btn.click()
            self.ability()
        self.solution["action"] = False

    def ability(self):
        charName = self.player.character.name
        if charName == "Assassin":
            self.controller.getButton("ability").click()
            btn = self.controller.getButton("random")
            while btn.value.name in self.player.gameMaster.openChars:
                btn = self.controller.getButton("random")
            # btn = self.controller.getButton("first")
            self.addText("Убивает " + btn.value.name)
            print(btn.value.name)
            btn.click()
        elif charName == "Thief":
            self.controller.getButton("ability").click()
            btn = self.controller.getButton("random")
            self.addText("Ворует у " + btn.value.name)
            print(btn.value.name)
            btn.click()
        elif charName == "Wizard":
            self.controller.getButton("ability").click()
            self.controller.getButton("player").click()
            players = self.player.gameMaster.players.copy()
            print(len(players), len(self.player.gameMaster.players), "COCK")
            for i in range(len(players)-1, -1, -1):
                print(players[i].name, self.player.name)
                if players[i].name == self.player.name:
                    players.pop(i)
            print(len(players), len(self.player.gameMaster.players), "SUCKER")
            maxHand, index = 0, 0
            for i in range(len(players)):
                if maxHand < len(players[i].hand):
                    maxHand = len(players[i].hand)
                    index = i
            if len(self.player.hand) < len(players[index].hand):
                self.controller.getButton(str(index)).click()
            else:
                self.controller.getButton("cancel").click()
        elif charName == "King" or charName == "Bishop" or charName == "Merchant":
            self.controller.getButton("ability").click()
            self.addText("Берет монетки за кварталы")
        elif charName == "Architect":
            self.controller.getButton("ability").click()
            for i in range(2):
                self.controller.getButton("build").click()
                if self.activeState() == "build":
                    btn = self.controller.getButton("0").click()
        elif charName == "Warlord":
            self.controller.getButton("ability").click()
            self.controller.getButton("coins").click()
            self.addText("Берет монетки за кварталы")
            self.controller.getButton("destroy").click()
            btn = self.controller.getButton("0")
            if btn.value != "cancel":
                if btn.value == self.player.name:
                    self.controller.buttons[1].click()
                else:
                    btn.click()
                btn = self.controller.getButton("0")
                if btn.value != "cancel":
                    self.addText("Уничтожает " + btn.value[1].name + "(" + btn.value[0].name + ")")
                btn.click()
            else:
                self.controller.getButton("cancel").click()

    def decision(self, kind):
        if kind == "graveyard":
            self.controller.getButton("0").click()

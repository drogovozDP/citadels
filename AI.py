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

    def chooseChar(self):
        self.solution["chooseChar"] = False
        if len(self.controller.buttons) == 0: return
        # self.controller.getButton("first").click()
        chars = self.controller.getAllBtn()
        gotAssassin = False
        for char in chars:
            if char == "Assassin":
                self.controller.getButton(char).click()
                gotAssassin = True
        if self.solution["action"]: print(1/0)
        if not gotAssassin: self.controller.getButton("first").click()
        if self.activeState() == "drop char":
            self.controller.getButton("first").click()

    def action(self):
        # self.setText("")
        if self.activeState() == "resources":
            if self.player.canBuild():
                self.setText(self.player.name +" берет " + str(self.player.take["gold"]) + " золота")
                self.controller.getButton("gold").click()
            else:
                self.controller.getButton("quarter").click()
                self.setText(self.player.name + " берет " + str(self.player.take["quarter"]) + " квартала")
                if self.activeState() == "take quarter":
                    self.controller.getButton("first").click()
        if self.activeState() == "action pool":
            self.controller.getButton("build").click()
            if self.activeState() == "build":
                btn = self.controller.getButton("first")
                self.addText("Строит " + btn.value.name + " за " + str(btn.value.value) + " золота")
                btn.click()
            self.ability()
        self.solution["action"] = False


    def ability(self):
        charName = self.player.character.name
        if charName == "Assassin":
            self.controller.getButton("ability").click()
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
        elif charName == "King" or charName == "Bishop" or charName == "Merchant":
            self.controller.getButton("ability").click()
            self.addText("Берет монетки за кварталы")
        elif charName == "Warlord":
            self.controller.getButton("ability").click()
            self.controller.getButton("coins").click()
            self.addText("Берет монетки за кварталы")
            self.controller.getButton("destroy").click()
            btn = self.controller.getButton("first")
            if btn.value != "cancel":
                if btn.value == self.player.name:
                    self.controller.buttons[1].click()
                else:
                    btn.click()
                btn = self.controller.getButton("first")
                if btn.value != "cancel":
                    self.addText("Уничтожает " + btn.value[1].name + "(" + btn.value[0].name + ")")
                btn.click()
            else:
                self.controller.getButton("cancel").click()

    def decision(self, kind):
        if kind == "graveyard":
            self.controller.getButton("first").click()

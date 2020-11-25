card_name = []
card_ammo = []
file = open('Sprites/quarters/quarters.txt', 'r')
for line in file:
    card_name.append(line[0: len(line) - 3])
    card_ammo.append(int(line[len(line) - 2: len(line) - 1]))
file.close()
data = [card_name, card_ammo]

max_ammo = 0
for x in card_ammo:
    max_ammo += x



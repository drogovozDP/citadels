info = open('Sprites/quarters/количество кварталов.txt', 'r', encoding='utf-8')
text = []
for line in info:
    line = line[len(line) - 2: len(line) - 1]
    if line == '0' or \
        line == '1' or \
        line == '2' or line == '3' or line == '4' or line == '5' or line == '6' or line == '7':
            text.append(int(line))
info.close()
sum = 0
for x in text:
    print(x)
    sum += x
print(sum)



class Docer:
    def __init__(self):
        pass

    def write(self, text):
        if text[0] == "*":
            print()
        print(text)

doc = Docer()
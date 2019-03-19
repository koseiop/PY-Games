class Player:

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.score2 = 0
        self.choice = ""
        self.hands = [[0], [0]]
        self.list = []
        self.fake = []

    def __str__(self):
        return self.name

    def set_name(self):
        self.name = input(f"{self.name} please input your name: ")
        while not self.name:
            self.name = input("You did not enter anything please try again.: ")

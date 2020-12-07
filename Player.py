class Player(object):
    def __init__(self, cards, playerNum):
        self.cards = cards
        self.playerNum = playerNum
        self.inPot = 0
        self.currentBet = 0
        self.totalBet = 0
        self.dinex = 200

    def __hash__(self):
        return hash(self.playerNum)
    
    def __repr__(self):
        return f'{self.playerNum}'
    

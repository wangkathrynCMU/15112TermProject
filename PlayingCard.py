import random
#created using ideas as in 
# https://www.cs.cmu.edu/~112/notes/notes-oop-part3.html (Playing Card Demo)
class PlayingCard(object):
    rankNames = [ "2", "3", "4", "5", "6", "7",
                   "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    suitNames = ["Clubs", "Diamonds", "Hearts", "Spades"]
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3

    #returns a deck of 52 playing cards
    # shuffled or not based on isShuffled
    # https://www.cs.cmu.edu/~112/notes/notes-oop-part3.html (Playing Card Demo)
    @staticmethod
    def getDeck(isShuffled):
        deck = []

        #places each card in deck in increasing order
        for rank in range(len(PlayingCard.rankNames)):
            for suit in range(len(PlayingCard.suitNames)):
                deck.append(PlayingCard(rank, suit))
        
        #shuffles cards using ran
        if isShuffled:
            random.shuffle(deck)

        return deck
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    #checks if cards are exactly the same (rank and suit)
    def strictlyEquals(self, other):
        if self.rank == other.rank and self.suit == other.suit:
            return True
        else:
            return False


    #in poker, one suit isn't greater than the other,
    # so for determining higher hands, two cards are the same if their rank is
    def __eq__(self, other):
        if self.rank == other.rank:
            return True
        else:
            return False
        
    def __repr__(self):
        rankName = PlayingCard.rankNames[self.rank]
        suitName = PlayingCard.suitNames[self.suit]
        return f'{rankName} of {suitName}'
    
    def __gt__(self, other):
        if self.rank > other.rank:
            return True
        else:
            return False
    
    def __minus__(self, other):
        return self.rank - other.rank
    
    def getHashables(self):
        return (self.rank, self.suit)
    
    def __hash__(self):
        return hash(self.getHashables())
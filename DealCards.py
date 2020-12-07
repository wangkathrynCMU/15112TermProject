from Player import *
from PlayingCard import *

#takes in a number of players and returns a list of players with random cards
def dealCards(numPlayers, deck):
    players = list()
    for i in range(numPlayers):
        cards = list()
        for card in range(2):
            cards.append(deck.pop())
        players.append(Player(cards, i))
    return players

def dealCommunityCards(deck):
    communityCards = []
    for i in range(5):
        communityCards.append(deck.pop())
    return communityCards

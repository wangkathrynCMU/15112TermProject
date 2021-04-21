from Player import *
from PlayingCard import *

#takes in a number of players and returns a list of players with random cards
def dealCards(numPlayers, deck, players):
    startOfGame = False
    if players == None:
        startOfGame = True
    
    newPlayers = []
    for i in range(numPlayers):
        cards = list()
        for card in range(2):
            cards.append(deck.pop())
        if not startOfGame:
            dinexLeft = players[i].dinex
            newPlayers.append(Player(cards, i, dinex = dinexLeft))
        else:
            newPlayers.append(Player(cards, i))
    return newPlayers

def dealCommunityCards(deck):
    communityCards = []
    for i in range(5):
        communityCards.append(deck.pop())
    return communityCards

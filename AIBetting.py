from Player import *
from PlayingCard import *
from HighestHand import *

def computerBets(player, communityCards, currentBet, bettingRound):
    highestH, kickers = findHighestHand(player.cards)
    certainty = kickers[0]
    scale = 1/highestH*certainty/13
    calculatedBet = round(scale*player.dinex,2)
    
    if currentBet >= calculatedBet:
        if(calculatedBet/currentBet >= 0.85):
            difference = currentBet - player.currentBet
            if(player.currentBet == 0):
                player.dinex -= currentBet
                player.totalBet += currentBet
            player.currentBet = currentBet
            player.dinex -= difference
            player.totalBet += difference
            return (1, 0) #call
        else:
            return (0, 0) #fold
    
    if(highestH>bettingRound*2.25):
        if(player.currentBet == 0):
                player.dinex -= currentBet
                player.totalBet += currentBet
        player.dinex -= (calculatedBet-currentBet)
        player.totalBet += (calculatedBet-currentBet)
        player.currentBet = calculatedBet
        return (3, calculatedBet-currentBet) #raise
    elif player.currentBet == currentBet:
        return(2, 0) #check
    else:
        if(player.currentBet == 0):
                player.dinex -= currentBet
                player.totalBet += currentBet
        player.currentBet = currentBet
        return(1, 0) #call
        

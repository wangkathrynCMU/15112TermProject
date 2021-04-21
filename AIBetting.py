from Player import *
from PlayingCard import *
from HighestHand import *

def computerBets(player, communityCards, currentBet, bettingRound, emotion):
    if(emotion == "happy"):
        certainty = 0.9
    elif(emotion == "sad"):
        certainty = 1.1
    else: 
        certainty = 1
    highestH, kickers = findHighestHand(player.cards)
    certainty = certainty * kickers[0]
    if highestH == 1:
        highestH*=1.25
    scale = 1/highestH*certainty/13
    calculatedBet = round(scale*player.dinex,2)
    totalBet = player.totalBet + currentBet
    leniency = 0.45 + (bettingRound*0.1)
    if totalBet >= calculatedBet:
        if(calculatedBet/totalBet >= leniency):
            difference = currentBet - player.currentBet
            if(player.currentBet == 0):
                player.dinex -= currentBet
                player.totalBet += currentBet
            player.currentBet = currentBet
            player.dinex -= difference
            player.totalBet += difference
            player.dinex = round(player.dinex, 2)

            return (1, 0) #call
        else:
            return (0, 0) #fold
    
    if(highestH>bettingRound*2.25 and (totalBet/calculatedBet <= leniency)):
        raiseAmount = calculatedBet - player.totalBet
        if(player.currentBet == 0):
                player.dinex -= currentBet
                player.totalBet += currentBet
        player.dinex -= raiseAmount
        player.totalBet += raiseAmount
        player.currentBet = calculatedBet
        player.dinex = round(player.dinex, 2)
        return (3, calculatedBet-currentBet) #raise
    elif player.currentBet == currentBet:
        return(2, 0) #check
    else:
        if(player.currentBet == 0):
                player.dinex -= currentBet
                player.totalBet += currentBet
        player.dinex = round(player.dinex, 2)
        player.currentBet = currentBet
        return(1, 0) #call
        

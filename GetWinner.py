from PlayingCard import PlayingCard
from HighestHand import findHighestHand

def getWinners(players, communityCards):
    highestHand = 10
    tieBreakers = []
    tiedPlayers = []

    for player in players:
        player.highestHand = findHighestHand(player.cards + communityCards)
        handType, kickers = player.highestHand
        if handType < highestHand:
            highestHand = handType
            tieBreakers= [kickers]
            tiedPlayers = [player]
        elif handType == highestHand:
            tieBreakers.append(kickers)
            tiedPlayers.append(player)


    if len(tiedPlayers) == 1:
        return tiedPlayers
    else:
        return tieBreaker(tieBreakers, tiedPlayers)

def tieBreaker(tieBreakers, tiedPlayers): 
    
    for i in range(len(tieBreakers[0])): #looping on each tie breaker
        #setting the highest as the first player
        highestRank = tieBreakers[0][i]
        newTiedPlayers = [tiedPlayers[0]]

        numTied = len(tiedPlayers)
        for j in range(1, numTied): #checking the rank of the cards of each player
            if(tieBreakers[j][i] > highestRank):
                highestRank = tieBreakers[j][i]
                newTiedPlayers = [tiedPlayers[j]]
            elif(tieBreakers[j][i] == highestRank):
                newTiedPlayers.append(tiedPlayers[j])
                
        tiedPlayers = newTiedPlayers

    return tiedPlayers


    



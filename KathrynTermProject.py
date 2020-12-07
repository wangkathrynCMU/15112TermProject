from dataclasses import make_dataclass
from PlayingCard import PlayingCard
from HighestHand import findHighestHand
from GetWinner import getWinners
from DealCards import *
from Player import Player
from AIBetting import *
import math, copy, random

from cmu_112_graphics import *
class PokerApp(App):

    def appStarted(self):
        self.hasStarted = False
        self.deck = PlayingCard.getDeck(True)

        self.players = None
        self.communityCards = None
        self.winners = None

        self.cardWidth = 70
        self.cardHeight = 110
        self.cardMargin = self.cardWidth/2

        self.pot = 0
        self.bet = 0
        self.checksAndCalls = 0
        self.round = 0
        self.playersTurn = 0
        self.gameOver = False

        self.handNames = [None, 'Straight Flush', 'Four of a Kind', 'Full House',
                            'Flush', 'Straight', 'Three of a Kind', 'Two Pair', 
                                'Pair', 'High Card']

        self.actionNames = ['folded', 'called', 'checked', 'raised']

        #hearts image source: https://en.wikipedia.org/wiki/Heart_symbol
        self.heartsImage = self.loadImage('heart.png')
        self.heartsImage = self.scaleImage(self.heartsImage, 1/30)
        #clubs image source: https://bit.ly/2JuuGKN
        self.clubsImage = self.loadImage('club.png')
        self.clubsImage = self.scaleImage(self.clubsImage, 1/15)
        #diamonds image source: https://emojiterra.com/diamond-suit/
        self.diamondsImage = self.loadImage('diamond.png')
        self.diamondsImage = self.scaleImage(self.diamondsImage, 1/13)
        #spade image source: https://bit.ly/2VLTmR7
        self.spadesImage = self.loadImage('spade.jpg')
        self.spadesImage = self.scaleImage(self.spadesImage, 1/11)

    def keyPressed(self, event):
        if(event.key.isdigit() and not self.hasStarted):
            self.numPlayers = int(event.key) + 1
            self.startGame()
        elif(self.playersTurn == 0 and self.hasStarted and not self.gameOver):
            if(event.key == "c" or event.key == 'k'):
                player = self.players[0]
                difference = self.bet - player.currentBet
                if(player.currentBet == 0):
                    player.dinex -= self.bet
                    player.totalBet += self.bet
                else:
                    player.dinex -= difference
                    player.totalBet += difference
                player.currentBet = self.bet
                self.checksAndCalls += 1
                self.playersTurn +=1
            if(event.key == "f"):
                self.gameOver = True
                self.players.pop(0)
                self.checksAndCalls = self.numPlayers
                self.round = 4
                self.showWinners()

        # if self.checksAndCalls = 
    
    def timerFired(self):
        if(self.hasStarted):
            self.calculatePot()
        if(self.hasStarted and self.checksAndCalls == self.numPlayers):
            self.checksAndCalls = 0
            self.bet = 0
            self.round +=1
            for player in self.players:
                player.currentBet = 0
            if(self.round == 2):
                self.showMessage("The turn has been dealt.")
            elif(self.round == 3):
                self.showMessage("The river has been dealt.")
            elif(self.round == 4):
                self.gameOver = True
                self.showWinners()
        elif self.hasStarted and not self.gameOver:
            self.playersTurn = self.playersTurn % self.numPlayers
            if(self.playersTurn > 0):
                player = self.players[self.playersTurn]
                bet = computerBets(player, self.communityCards[:2+self.round], 
                                                        self.bet, self.round)
                action = bet[0]
                if(action == 3):
                    raisedAmount = bet[1]
                    self.checksAndCalls = 1
                    self.bet += raisedAmount
                    self.showMessage(f'Player {player.playerNum} raised by {bet[1]:.2f} so highest bet = {self.bet}')
                else:
                    self.showMessage(f'Player {player.playerNum} {self.actionNames[action]}')
                    if(action == 0):
                        self.players.remove(player)
                        self.numPlayers -=1
                        self.playersTurn -=1
                        if self.numPlayers <=1:
                            self.gameOver = True 
                    else:
                        self.checksAndCalls += 1
                self.playersTurn+=1
            
            if(self.numPlayers == 1):
                self.gameOver = True
                self.round = 4
                self.showWinners()
        
        
            
    def mousePressed(self, event):
        if self.playersTurn == 0 and self.hasStarted:
            amount = self.getUserInput('How much will you raise by?')
            if (amount == None):
                self.message = 'You canceled!'
            elif(amount.isdigit):
                self.showMessage('You entered: ' + amount)
                amount = float(amount)
                player = self.players[0]
                if(amount > player.dinex):
                    self.showMessage('You do not have enough money!')
                else:
                    self.bet += amount
                    player.currentBet = self.bet
                    player.totalBet += amount
                    player.dinex -= amount
                
                    self.checksAndCalls = 1
                    self.playersTurn+=1

    def calculatePot(self):
        dinex = 0 
        for player in self.players:
            dinex+=player.totalBet
        self.pot = dinex

    def checkEndOfRound(self):
        pass

    def showWinners(self):
        self.winners = getWinners(self.players, self.communityCards)
        for winner in self.winners:
                if winner not in self.players:
                    self.winners.remove(winner) #be carefuly of removing in for loop
                
                numWinners = len(self.winners) 
                winnerString = ''

                for winner in self.winners:
                    winner.dinex+= (self.pot/numWinners)
                    if(winner.playerNum == 0):
                        winnerStr = 'You'
                    else:
                        winnerStr = str(winner.playerNum)
                    winnerString = winnerString + ', ' + winnerStr
                    
                self.showMessage(f'Winners are' + winnerString)
                for winner in self.winners:
                    if(winner.playerNum != 0):
                        hand = findHighestHand(winner.cards + self.communityCards)
                        handName = self.handNames[hand[0]]
                        self.showMessage(f'Player {winner.playerNum} had ' + 
                                            str(winner.cards) + ' which is a ' + handName)
                hand = findHighestHand(self.players[0].cards + self.communityCards)
                handName = self.handNames[hand[0]]
                self.showMessage(f'You had a ' + handName)

            
    def startGame(self):
        self.hasStarted = True
        self.players = dealCards(self.numPlayers, self.deck)
        self.communityCards = dealCommunityCards(self.deck)
        self.winners = getWinners(self.players, self.communityCards)
        self.round = 1

    def redrawAll(self, canvas):
        if self.hasStarted:    
            self.drawCommunity(canvas)
            self.drawPlayerCards(canvas, self.players)
            self.drawBettingInstructions(canvas)
        else:
            canvas.create_text(self.width/2, self.height/2, 
                                text = "Press the number of players you want to play against:", 
                                font="Helvetica 40 bold")

    def drawPlayerCards(self, canvas, players):
        #draw player's cards
        card1, card2 = players[0].cards
        self.drawCard(canvas, card1, self.width/2-self.cardWidth, self.height*3/4) 
        self.drawCard(canvas, card2, self.width/2+self.cardWidth, self.height*3/4)  

        if not self.gameOver:
            pass #draw the other computer player's cards
    
    def drawBettingInstructions(self, canvas):
        canvas.create_text(self.width*4/5, self.height*2.7/4, 
                        text = f'Current bet: {self.bet:.2f} dinex. Your bet: {self.players[0].currentBet:.2f}  ', 
                            font = "Arial 20 bold")
        canvas.create_text(self.width*4/5, self.height*2.8/4, 
                            text = f'You have {self.players[0].dinex:.2f} dinex.', 
                            font = "Arial 20 bold")
        canvas.create_text(self.width*4/5, self.height*2.9/4, 
                            text = "Press K to Check", font = "Arial 20 bold")
        canvas.create_text(self.width*4/5, self.height*3/4, 
                            text = "Press C to Call", font = "Arial 20 bold")
        canvas.create_text(self.width*4/5, self.height*3.1/4, 
                            text = "Press F to Fold", font = "Arial 20 bold")
        canvas.create_text(self.width*4/5, self.height*3.2/4, 
                            text = "Click Mouse to Raise", font = "Arial 20 bold")

    def drawCommunity(self, canvas):
        cx = self.width/2
        cy = self.height/2
        numCards = len(self.communityCards) - 3 + self.round
        if(numCards > 5):
            numCards = 5
        startX = cx - (numCards/2)*self.cardWidth - (numCards-1)/2*self.cardMargin + self.cardWidth/2
        for i in range(numCards):
            self.drawCard(canvas, self.communityCards[i], startX + i*self.cardMargin + i*self.cardWidth, cy)
        textY = cy - self.cardHeight*3/4
        canvas.create_text(self.width/2, textY, text = f"Pot: {self.pot:.2f}", font = "Arial 20 bold")

    def drawCard(self, canvas, card, x, y):
        color = 'red'
        if card.suit == 0 or card.suit == 3:
            color = 'black'
        canvas.create_rectangle(x-self.cardWidth/2, y-self.cardHeight/2, 
                                    x+self.cardWidth/2, y+self.cardHeight/2)
        #draw rank onto top left
        cx = x - self.cardWidth*3/8
        cy = y - self.cardHeight*3/8
        suitHeight = self.cardHeight/20
        suitWidth = self.cardWidth/20
        rank = PlayingCard.rankNames[card.rank]
        if rank.isalpha:
            rank = rank[0]
        
        #draw rank onto lower right
        canvas.create_text(cx, cy, text = rank, fill = color, font = "Arial 16")
        cx = x + self.cardWidth*3/8
        cy = y + self.cardHeight*3/8
        canvas.create_text(cx, cy, text = rank, fill = color, font = "Arial 16")

        #draw suit onto middle
        if(card.suit == PlayingCard.HEARTS):
            canvas.create_image(x, y, image=ImageTk.PhotoImage(self.heartsImage)) 
        if(card.suit == PlayingCard.CLUBS):
            canvas.create_image(x, y, image=ImageTk.PhotoImage(self.clubsImage)) 
        if(card.suit == PlayingCard.DIAMONDS):
            canvas.create_image(x, y, image=ImageTk.PhotoImage(self.diamondsImage)) 
        if(card.suit == PlayingCard.SPADES):
            canvas.create_image(x, y, image=ImageTk.PhotoImage(self.spadesImage)) 
                
        


#################################################
# main
#################################################

PokerApp(width = 1500, height = 1000)

if __name__ == '__main__':
    main()



#Next Steps:
#1. Find highest hand for given set of cards (just use a pyramid of if statements)
#2. Find the highest hand out of all of the players cards (maybe can create a enum in python?)
#3. Then add UX. Add bidding. 
#4. Figure out computer vision
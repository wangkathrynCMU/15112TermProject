from dataclasses import make_dataclass
from PlayingCard import PlayingCard
from HighestHand import findHighestHand
from GetWinner import getWinners
from DealCards import *
from Player import Player
from AIBetting import *
from EmotionDetector import *
import math, copy, random
import cv2
import dlib

from cmu_112_graphics import *
class PokerApp(App):

    def appStarted(self):
        self.hasStarted = False
        self.deck = PlayingCard.getDeck(True)
    

        self.allPlayers = None
        self.players = None
        self.communityCards = None
        self.winners = None 

        self.cardWidth = 70
        self.cardHeight = 110
        self.cardMargin = self.cardWidth/3
        self.margin = 50

        self.pot = 0
        self.bet = 0
        self.checksAndCalls = 0
        self.round = 0
        self.dealer = 0
        self.playersTurn = self.dealer + 1
        self.smallBlind = 2
        self.gameOver = False
        self.firstGameDone = False 
        self.blindsPlaced = False

        self.textColor = "white"

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
        
        #source: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.facebook.com%2FGroupon.US%2Fvideos%2Fearlyblackfriday%2F1065167007265572%2F&psig=AOvVaw0zzl8zqJSOuYY3_pGfhHHR&ust=1607635140464000&source=images&cd=vfe&ved=0CA0QjhxqFwoTCICF-d3pwe0CFQAAAAAdAAAAABAD
        self.tableImage = self.loadImage('poker_table.jpg')
        self.tableImage = self.scaleImage(self.tableImage, 2)
        
        #Got this from: https://www.youtube.com/watch?v=MrRGVOhARYY
        self.cap = cv2.VideoCapture(0)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        
        #Got this from: https://stackoverflow.com/questions/39953263/get-video-dimension-in-python-opencv/39953739
        self.cvWidth  = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)  
        self.cvHeight = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        self.landmarkPoints = []
        self.faceBoxPoints = []
        self.emotionDetector = EmotionDetector()
        self.emotion = ""

    def newGame(self):
        self.deck = PlayingCard.getDeck(True)
        self.communityCards = None
        self.winners = None

        self.pot = 0
        self.bet = 0
        self.checksAndCalls = 0
        self.round = 0
        self.playersTurn = 0
        self.gameOver = False
        self.numPlayers = self.totalPlayers
        self.dealer += 1
        self.playersTurn = self.dealer + 1
        self.blindsPlaced = False

        self.startGame()

    def keyPressed(self, event):
        if(event.key == "r" and self.gameOver):
            self.firstGameDone = True
            self.newGame()
        if(event.key.isdigit() and not self.hasStarted):
            self.numPlayers = self.totalPlayers = int(event.key) + 1
            if not (self.numPlayers > 8):
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
                self.numPlayers -=1

        # if self.checksAndCalls = 
    def playerRaised(self, amount):
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
            smallBlindPlayer = (self.dealer + 1) % self.numPlayers
            bigBlindPlayer = (self.dealer + 2) % self.numPlayers
            if self.playersTurn == 0:
                self.playerEmotion()
                if smallBlindPlayer == 0 and self.blindsPlaced == False:
                    self.playerRaised(self.smallBlind)
                    self.showMessage("You placed the small blind.")
                    
                elif bigBlindPlayer == 0 and self.blindsPlaced == False:
                    self.playerRaised(self.smallBlind*2)
                    self.showMessage("You placed the big blind.")
                    self.blindsPlaced = True
            elif(self.playersTurn > 0):
                player = self.players[self.playersTurn]
                if(self.playersTurn == smallBlindPlayer and not self.blindsPlaced):
                    bet = (3, self.smallBlind)
                    raiseAmount = self.smallBlind
                    player.dinex -= raiseAmount
                    player.totalBet += raiseAmount
                    player.currentBet = raiseAmount
                    player.dinex = round(player.dinex, 2)
                    self.showMessage(f"Player {player.playerNum} placed the small blind of {self.smallBlind} dinex.")
                elif (self.playersTurn == bigBlindPlayer and not self.blindsPlaced):
                    bet = (3, self.smallBlind*2)
                    raiseAmount = self.smallBlind*2
                    player.dinex -= raiseAmount
                    player.totalBet += raiseAmount
                    player.currentBet = raiseAmount
                    self.showMessage(f"Player {player.playerNum} placed the big blind of {self.smallBlind*2} dinex.")
                    self.blindsPlaced = True
                else:
                    bet = computerBets(player, self.communityCards[:2+self.round], 
                                            self.bet, self.round, 
                                            self.emotionDetector.getAvgEmotion())
                action = bet[0]
                if(action == 3):
                    raisedAmount = bet[1]
                    self.checksAndCalls = 1
                    self.bet += raisedAmount
                    if not self.round == 1 or not (self.playersTurn == smallBlindPlayer or self.playersTurn == bigBlindPlayer):
                        self.showMessage(f'Player {player.playerNum} raised by {bet[1]:.2f} so highest bet = {self.bet:.2f}')
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

    #I learned how to use dlib from this video: https://www.youtube.com/watch?v=MrRGVOhARYY
    #The code for finding the landmarks of the face and the bounding box were all from this video
    #This code can also be found here: https://pysource.com/2019/03/12/face-landmarks-detection-opencv-with-python/
    #The predicting data for the 68 landmarks can be found here: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
    def playerEmotion(self):
        _, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        self.landmarkPoints = []
        self.faceBoxPoints = []

        if(len(faces) > 0):
            face = faces[0]
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            self.faceBoxPoints = [x1, y1, x2, y2]
            landmarks = self.predictor(gray, face)

            for i in range(68):
                landmarkX = landmarks.part(i).x
                landmarkY = landmarks.part(i).y
                self.landmarkPoints.append((landmarkX, landmarkY))
        self.emotionDetector.addLandmarks(self.landmarkPoints)
        self.emotion = self.emotionDetector.detectEmotion()

            
    def mousePressed(self, event):
        if self.playersTurn == 0 and self.hasStarted:
            amount = self.getUserInput('How much will you raise by?')
            if (amount == None):
                self.message = 'You canceled!'
            elif(amount.isdigit):
                self.showMessage('You entered: ' + amount)
                amount = float(amount)
                self.playerRaised(amount)

    def calculatePot(self):
        dinex = 0 
        for player in self.allPlayers:
            dinex+=player.totalBet
        self.pot = dinex

    def showWinners(self):
        self.winners = getWinners(self.players, self.communityCards)
        for winner in self.winners:
            if winner not in self.players:
                self.winners.remove(winner) #be carefuly of removing in for loop
            
            numWinners = len(self.winners) 
            winnerString = ''
            self.calculatePot
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
            self.showMessage(f'At the end of the game, you had a ' + handName)
            
    def startGame(self):
        self.hasStarted = True
        self.players = dealCards(self.numPlayers, self.deck, players = self.allPlayers)
        self.allPlayers = copy.copy(self.players)
        self.communityCards = dealCommunityCards(self.deck)
        self.winners = getWinners(self.players, self.communityCards)
        self.round = 1

    def redrawAll(self, canvas):
        canvas.create_image(self.width/2, self.height/2, 
                            image=ImageTk.PhotoImage(self.tableImage))
        if self.hasStarted:    
            self.drawCommunity(canvas)
            self.drawPlayerCards(canvas, self.players)
            self.drawBettingInstructions(canvas)
            if not self.gameOver:
                self.drawPlayerFace(canvas)
            else:
                canvas.create_text(self.width/2, self.margin/2, text = "Press R to replay",
                                font = "Times 25 bold")
        else:
            if not self.firstGameDone:
                self.drawSplashPage(canvas)
                
    
    def drawSplashPage(self, canvas):
        canvas.create_text(self.width/2, self.height*0.8/2, text = "Poker Face",
                             font="Times 60 bold", fill = 'firebrick2')
        canvas.create_text(self.width/2, self.height/2, 
                                text = "To start, press the number of players you want to play against", 
                                font="Times 30 italic")
        
    def drawPlayerCards(self, canvas, players):
        #draw player's cards
        card1, card2 = players[0].cards
        # self.drawCard(canvas, card1, self.width/2-self.cardWidth, self.height*3/4) 
        # self.drawCard(canvas, card2, self.width/2+self.cardWidth, self.height*3/4)  
        
        radius = self.height/3.5 #(self.height - self.margin*2)/2
        angleIncrement = 2*math.pi/(self.numPlayers)
        startingAngle = -math.pi/2
        for i in range(self.numPlayers):
            player = self.players[i]
            angle = startingAngle + i*angleIncrement
            cx = self.width/2
            cy = self.height/2
            x = cx - radius * math.cos(angle)
            y = cy - radius * math.sin(angle)
            card1, card2 = player.cards
            playerName = 'Player ' + str(player.playerNum)
            if(player.playerNum == 0):
                playerName = 'You'
            canvas.create_text(x, y-self.cardHeight*3/4, text = playerName, 
                                font = 'Times 20 italic', fill = self.textColor)
            self.drawCard(canvas, card1, x-(self.cardWidth*3/4), y)
            self.drawCard(canvas, card2, x+(self.cardWidth*3/4), y)

            canvas.create_text(x, y+self.cardHeight*3/4, text = str(player.dinex) + ' dinex', 
                                font = 'Times 20 italic', fill = self.textColor)

            if not self.gameOver and player.playerNum != 0:
                self.drawCard(canvas, card1, x-(self.cardWidth*3/4), y, covered = True)
                self.drawCard(canvas, card2, x+(self.cardWidth*3/4), y, covered = True)
    
    def drawPlayerFace(self, canvas):
        
        boxStartX = self.margin/2
        boxStartY = self.height*2/3 - self.margin
        boxEndY = self.height - self.margin*2
        boxHeight = boxEndY - boxStartY

        scale = boxHeight/self.cvHeight
        boxWidth = scale * self.cvWidth

        canvas.create_rectangle(boxStartX, boxStartY, 
                                boxStartX + boxWidth, 
                                self.height - self.margin*2, fill = "white")
        
        # canvas.create_text(self.width/2, self.height/2, 
        #                     text = self.emotion, font = "Times 20 bold")

        canvas.create_text(boxStartX+boxWidth/2, boxStartY - (self.margin/2), 
                            text = self.emotion, fill = "white", 
                            font = "Times 30 bold")
        
        if(len(self.faceBoxPoints) == 4):
            x1, y1, x2, y2 = [coor*scale for coor in self.faceBoxPoints]
            canvas.create_rectangle(boxStartX + x1, boxStartY + y1, 
                                    boxStartX + x2, boxStartY + y2)
        
        if len(self.landmarkPoints) == 68:
            prevX = boxStartX + self.landmarkPoints[0][0]*scale
            prevY = boxStartY +self.landmarkPoints[0][1]*scale
            for i in range(1,68):
                if(i in {17, 22, 27, 31, 36, 42, 48}):
                    prevX = boxStartX + self.landmarkPoints[i][0]*scale
                    prevY = boxStartY +self.landmarkPoints[i][1]*scale
                else:
                    currX = boxStartX + self.landmarkPoints[i][0]*scale
                    currY = boxStartY + self.landmarkPoints[i][1]*scale
                    canvas.create_line(prevX, prevY, currX, currY, fill = "blue")
                    prevX = currX
                    prevY = currY
            
            #connect ends of eyes to the beginning
            #right eye:
            prevX = boxStartX + self.landmarkPoints[36][0]*scale
            prevY = boxStartY + self.landmarkPoints[36][1]*scale
            currX = boxStartX + self.landmarkPoints[41][0]*scale
            currY = boxStartY + self.landmarkPoints[41][1]*scale

            canvas.create_line(prevX, prevY, currX, currY, fill = "blue")

            #left eye:
            prevX = boxStartX + self.landmarkPoints[42][0]*scale
            prevY = boxStartY + self.landmarkPoints[42][1]*scale
            currX = boxStartX + self.landmarkPoints[47][0]*scale
            currY = boxStartY + self.landmarkPoints[47][1]*scale
            
            canvas.create_line(prevX, prevY, currX, currY, fill = "blue")

            #connect end of mouth to beginning
            prevX = boxStartX + self.landmarkPoints[48][0]*scale
            prevY = boxStartY + self.landmarkPoints[48][1]*scale
            currX = boxStartX + self.landmarkPoints[67][0]*scale
            currY = boxStartY + self.landmarkPoints[67][1]*scale
            
            canvas.create_line(prevX, prevY, currX, currY, fill = "blue")      
        
        

    def drawBettingInstructions(self, canvas):
        canvas.create_text(self.width*4.25/5, self.height*4.75/6, 
                        text = f'Current bet: {self.bet:.2f} dinex. Your bet: {self.players[0].currentBet:.2f}  ', 
                            font = "Times 20 bold", fill = self.textColor)
        canvas.create_text(self.width*4.25/5, self.height*4.9/6, 
                            text = f'You have {self.players[0].dinex:.2f} dinex.', 
                            font = "Times 20 bold", fill = self.textColor)
        canvas.create_text(self.width*4.25/5, self.height*5.05/6, 
                            text = "Press K to Check", font = "Times 20 bold",
                            fill = self.textColor)
        canvas.create_text(self.width*4.25/5, self.height*5.2/6, 
                            text = "Press C to Call", font = "Times 20 bold", 
                            fill = self.textColor)
        canvas.create_text(self.width*4.25/5, self.height*5.35/6, 
                            text = "Press F to Fold", font = "Times 20 bold", 
                            fill = self.textColor)
        canvas.create_text(self.width*4.25/5, self.height*5.5/6, 
                            text = "Click Mouse to Raise", font = "Times 20 bold",
                            fill = self.textColor)

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
        canvas.create_text(self.width/2, textY, text = f"Pot: {self.pot:.2f}", 
                        font = "Times 20 bold", fill = self.textColor)

    def drawCard(self, canvas, card, x, y, covered = False):
        if covered:
            canvas.create_rectangle(x-self.cardWidth/2, y-self.cardHeight/2, 
                                    x+self.cardWidth/2, y+self.cardHeight/2, 
                                    fill = 'firebrick3')
            return None
        
        color = 'red'
        if card.suit == 0 or card.suit == 3:
            color = 'black'
        canvas.create_rectangle(x-self.cardWidth/2, y-self.cardHeight/2, 
                                    x+self.cardWidth/2, y+self.cardHeight/2, fill = 'white')
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

PokerApp(width = 1700, height = 950)

#Next Steps:
#1. Find highest hand for given set of cards (just use a pyramid of if statements)
#2. Find the highest hand out of all of the players cards (maybe can create a enum in python?)
#3. Then add UX. Add bidding. 
#4. Figure out computer vision
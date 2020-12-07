from PlayingCard import PlayingCard
from operator import attrgetter

#takes in a list of cards
def findHighestHand(cards):
    cards = sortCards(cards)
    highestHand = hasFlush(hasStraight(cards))
    if highestHand != []:
        return (1, [highestHand[0].rank])
    fourRank = fourOfAKind(cards)
    if fourRank[0] != -1:
        return (2, fourRank)
    FH = fullHouse(cards)
    if FH[0] != -1 and FH[1] !=-1:
        return (3, FH)
    flush = hasFlush(cards)
    if flush != []:
        return (4, flush)
    straight = hasStraight(cards)
    if straight!= []:
        return (5, [straight[0].rank])
    three = threeOfAKind(cards)
    if three[0]!= -1:
        return (6, three)
    twoP = twoPair(cards)
    if twoP[1] != -1:
        return (7, twoP)
    oneP = onePair(cards)
    if oneP[0] != -1:
        return (8, oneP)
    
    return (9, [card.rank for card in reversed(cards)])


#takes in a list of cards and returns a dictionary mapping values to occurences
def rankCount(cards):
    ranks = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
    for card in cards:
        ranks[card.rank]+=1
    return ranks

#use sorted function for objects as in here: 
# https://wiki.python.org/moin/HowTo/Sorting#Key_Functions
def sortCards(cards):
    return sorted(cards, key=lambda PlayingCard: PlayingCard.rank)

#returns the rank of any four of a kind in given cards and highest other card
#if no four of a kind, returns -1
def fourOfAKind(cards):
    ranks = rankCount(cards)
    fourRank = -1
    highestOther = -1 #highest other card (not four of a kind)
    for i in reversed(range(13)):
        if ranks[i] == 4:
            fourRank = i
        elif ranks[i] >= 1 and highestOther == -1:
            highestOther = i
    return (fourRank, highestOther)

#only works if already checked there isn't a four of a kind
def threeOfAKind(cards):
    ranks = rankCount(cards)
    tripleRank = -1
    highestOthers = [-1, -1]
    for i in reversed(range(13)):
        if ranks[i] == 3 and tripleRank == -1:
            tripleRank = i
        elif ranks[i] >= 1:
            if highestOthers[0] == -1:
                highestOthers[0] = i
            elif highestOthers[1] == -1:
                highestOthers[1] = i

    return [tripleRank, highestOthers[0], highestOthers[1]]

#only works if already checked there aren't two pairs
def onePair(cards):
    ranks = rankCount(cards)
    pairRank = -1
    otherHighest = [-1, -1, -1]
    for i in reversed(range(13)):
        if(ranks[i] == 2):
            pairRank = i
        elif(ranks[i] == 1):
            for j in range(3):
                if otherHighest[j] == -1:
                    otherHighest[j] = i
                    break
    return [pairRank] + otherHighest

def twoPair(cards):
    ranks = rankCount(cards)
    firstPair = -1
    secondPair = -1
    highestOther = -1
    for i in reversed(range(13)):
        if ranks[i] == 2 and secondPair == -1:
            if(firstPair == -1):
                firstPair = i
            else:
                secondPair = i
        elif ranks[i] >= 1 and highestOther == -1:
            highestOther = i
    return [firstPair, secondPair, highestOther]

def highestCard(cards):
    return cards[len(cards)-1].rank

#only works if already checked no four of a kind
def fullHouse(cards):
    ranks = rankCount(cards)
    triple = -1
    pair = -1

    for i in reversed(range(13)):
        if ranks[i] == 3 and triple == -1:
            triple = i
        elif ranks[i] >= 2 and pair == -1:
            pair = i
    return (triple, pair)


#takes in a set of sorted cards
# returns the set of cards that makes a straight, empty if no straight in hand
def hasStraight(cards):
    straightCards = []

    #since Aces can be played either low or high (rank before 2 or after King)
    # if there is an Ace in the hand, then we append a new card with rank -1
    # which allows us to check later on if it is used in a straight formation
    negativeAces = []
    for card in cards:
        if(card.rank == 12):
            negativeAces.append(PlayingCard(-1, card.suit))
    
    cards = negativeAces + cards

    #checks for straights
    i = 0
    while i < len(cards) - 4:
        isStraight = True
        j = 1
        multipleCards = 0
        while j < 5:
            if i + j >= len(cards):
                isStraight = False
                break
            elif(cards[i+j].rank == cards[i+j-1].rank): 
                #if the ranks are equal, we must keep comparing past five cards 
                # and count how many multiples there are 
                # so we can include them all in the hand we return
                i +=1
                j -=1
                multipleCards +=1
            elif not (cards[i+j].rank - cards[i+j-1].rank == 1):
                isStraight = False #if ranks difference != 1, then not straight
            j+=1
        if isStraight:
             #include duplicate ranks to check for straight flush later
            straightCards = cards[i-multipleCards:i+5]
        i +=1

    #if low ace is used, removes -1 rank and adds ace rank to final hand
    i = 0
    while i < len(straightCards):
        if(straightCards[i].rank == -1):
            straightCards.append(PlayingCard(12, straightCards[i].suit))
            straightCards.remove(straightCards[i])
            i-=1
        i+=1
    
    #remove the temporary -1 cards from overall card deck
    i = 0
    while i < len(cards):
        if(cards[i].rank == -1):
            cards.remove(cards[i])
            i-=1
        i+=1

    return straightCards

#cards must be sorted --> returns the 5 highest cards that contain flush
# does not work if there are two different suits of flushes (10 or more cards)
def hasFlush(cards):
    flushCount = dict()
    flushCards = dict()

    #creates a dictionary mapping each suit to the number of cards of that suit
    #and another dictionary mapping the suit to a list of the cards of that suit
    for card in cards:
        if not card.suit in flushCount:
            flushCount[card.suit] = 0
            flushCards[card.suit] = []
        flushCount[card.suit] +=1
        flushCards[card.suit].append(card)
    
    #returns the list of cards for the suit with count of over 5
    for suit in flushCount:
        if(flushCount[suit] >= 5):
            flushCards = sortCards(flushCards[suit])
            total = len(flushCards)
            return [card.rank for card in flushCards[total-5:total]]
    #if none over 5, then returns empty list
    return []

def testFlush():
    print("Testing Flush...")
    five = PlayingCard(3, 1)
    four = PlayingCard(2, 1)
    three = PlayingCard(1, 1)
    two = PlayingCard(0, 1)
    king = PlayingCard(11, 1) 
    queen = PlayingCard(11, 2) 
    queen2 = PlayingCard(11, 1)

    cards = [two, three, four, five, queen, king]
    assert(hasFlush(cards) == [two, three, four, five, king])
    # check non-destructive
    assert(cards == [two, three, four, five, queen, king])
    cards = [two, three, four, five, queen, queen2, king]
    assert(hasFlush(cards) == [two, three, four, five, queen, king])
    # check non-destructive
    assert(cards == [two, three, four, five, queen, queen2, king])
    print("Passed!")

def testStraight():
    print("Testing Straight...")
    #straight test case
    ace = PlayingCard(12, 1) 
    ace2 = PlayingCard(12, 2) 
    king = PlayingCard(11, 1) 
    queen = PlayingCard(10, 1) 
    jack = PlayingCard(9, 1)
    ten = PlayingCard(8, 1)
    ten2 = PlayingCard(8, 2)
    six = PlayingCard(4, 1)
    five = PlayingCard(3, 1)
    four = PlayingCard(2, 1)
    four2 = PlayingCard(2, 2)
    three = PlayingCard(1, 1)
    two = PlayingCard(0, 1)

    cards = [two, six, ten, jack, queen, king, ace]
    assert(hasStraight(cards) == [ten, jack, queen, king, ace])
    cards = [two, three, five, six, ten, queen, king]
    assert(hasStraight(cards) == [])
    cards = [two, three, four, five, ten, ace]
    assert(hasStraight(cards) == [two, three, four, five, ace])
    assert(cards == [two, three, four, five, ten, ace]) #test non-destructive

    #test straights with multiple occurences
    cards = [two, three, four, five, ten, ten2, ace, ace2]
    assert(hasStraight(cards) == [two, three, four, five, ace, ace2])
    #test non-destructive
    assert(cards == [two, three, four, five, ten, ten2, ace, ace2])

    cards = [two, three, four, four2, five, ten, ten2, queen, king, ace, ace2]
    assert(hasStraight(cards) == [two, three, four, four2, five, ace, ace2])
    
    sevenD = PlayingCard(5, 1)
    nineH = PlayingCard(7, 2)
    print([sevenD, nineH])
    sevenH = PlayingCard(5, 2)
    fiveS = PlayingCard(5, 3)
    community = [PlayingCard(9, 0), PlayingCard(6, 0), PlayingCard(2, 1), 
                    PlayingCard(8, 0), PlayingCard(7, 1)]
    print(community)
    print(hasStraight([sevenD, nineH] + community))
    

    print("Passed!")

def onePairTest():
    print("Testing OnePair...")
    queen2 = PlayingCard(10, 2) 
    queen1 = PlayingCard(10, 1) 
    jack = PlayingCard(9, 1) 
    king = PlayingCard(11, 1) 
    ten = PlayingCard(8, 3) 
    four = PlayingCard(2, 3) 
    three = PlayingCard(1, 3) 
    cards = [three, four, ten, jack, queen1, queen2, king]
    assert(onePair(cards) == [10, 11, 9, 8])
    print("Passed!")

def twoPairTest():
    print("Testing twoPair...")
    ace = PlayingCard(12, 1) 
    ace2 = PlayingCard(12, 2) 
    king = PlayingCard(11, 1) 
    queen = PlayingCard(10, 1) 
    ten = PlayingCard(8, 1)
    ten2 = PlayingCard(8, 2)
    six = PlayingCard(4, 1)
    cards = [six, ten, ten2, queen, king, ace, ace2]

    assert(twoPair(cards) == [12, 8, 11])

    #test when single rank is higher than the double
    king2 = PlayingCard(11, 2) 
    cards = [six, ten, ten2, queen, king, king2, ace]

    assert(twoPair(cards) == [11, 8, 12])
    print("Passed!")

def threeOfAKindTest():
    print("Testing threeOfAKind...")
    queen3 = PlayingCard(10, 3) 
    queen2 = PlayingCard(10, 2) 
    queen1 = PlayingCard(10, 1) 
    jack = PlayingCard(9, 1) 
    four = PlayingCard(2, 1) 
    nine = PlayingCard(7, 1) 
    six = PlayingCard(4, 1) 
    cards = sortCards([six, nine, jack, four, queen1, queen2, queen3])
    
    assert(threeOfAKind(cards) == [10, 9, 7])

    jack2 = PlayingCard(9, 2)
    jack3 = PlayingCard(9, 3)

    cards = sortCards([four, jack, jack2, jack3, queen1, queen2, queen3])
    
    assert(threeOfAKind(cards) == [10, 9, 2])
    print("Passed!")

def fourOfAKindTest():
    print("Testing fourOfAKind...")
    queen4 = PlayingCard(11, 0) 
    queen3 = PlayingCard(11, 3) 
    queen2 = PlayingCard(11, 2) 
    queen1 = PlayingCard(11, 1) 
    jack = PlayingCard(10, 1) 
    king = PlayingCard(12, 1) 
    cards = sortCards([king, jack, queen1, queen2, queen3, queen4])
    assert(fourOfAKind(cards) == (11, 12))
    assert(fourOfAKind([jack, king, queen1, queen2, queen3])[0] == -1)
    print("Passed!")

def singleTest():
    print("Testing highestCard...")
    queen = PlayingCard(11, 1) 
    jack = PlayingCard(10, 1) 
    king = PlayingCard(12, 1) 
    cards = sortCards([queen, jack, king])
    assert(highestCard(cards) == 12)
    print("Passed!")

def fullHouseTest():
    print("Testing fullHouse...")
    queen3 = PlayingCard(10, 3) 
    queen2 = PlayingCard(10, 2) 
    queen1 = PlayingCard(10, 1) 
    jack2 = PlayingCard(9, 2) 
    jack1 = PlayingCard(9, 1) 
    nine = PlayingCard(7, 1) 
    four = PlayingCard(2, 1) 

    cards = [four, nine, jack1, jack2, queen1, queen2, queen3]

    assert(fullHouse(cards) == (10, 9))

    #testing when pair is greater than the triple
    king1 = PlayingCard(11, 1) 
    king2 = PlayingCard(11, 1) 
    two = PlayingCard(0, 1) 
    cards = [two, jack1, queen1, queen2, queen3, king1, king2]

    assert(fullHouse(cards) == (10, 11))

    print("Passed!")

def highestHandTest():
    queen3 = PlayingCard(10, 3) 
    queen2 = PlayingCard(10, 2) 
    queen1 = PlayingCard(10, 1) 
    jack2 = PlayingCard(9, 2) 
    jack1 = PlayingCard(9, 1) 
    nine = PlayingCard(7, 1) 
    four = PlayingCard(2, 1) 
    cards = [four, nine, jack1, jack2, queen1, queen2, queen3]
    print(findHighestHand(cards))

# highestHandTest()
# fullHouseTest()
# singleTest()
# fourOfAKindTest()
# threeOfAKindTest()
# twoPairTest()
# onePairTest()
# testStraight()
# testFlush()

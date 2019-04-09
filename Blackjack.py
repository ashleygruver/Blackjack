# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
outcome = ''
question = 'deal?'
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        
    def __str__(self):
        strCards = ''
        for c in range(len(self.cards)):
            strCards += str(self.cards[c]) + ' '
        return 'Hand contains ' + str(strCards)

    def add_card(self, card):
        self.cards.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        handValue = 0
        for i in range(len(self.cards)):
            handValue += VALUES[str(self.cards[i])[1]]
        for i in range(len(self.cards)):
            if str(self.cards[i])[1] == 'A':
                if handValue <= 11:
                    handValue += 10
        return handValue
                
   
    def draw(self, c, pos):
        for i in range(len(self.cards)):
            self.cards[i].draw(c, (pos))
            pos[0] += 73
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append (Card(suit, rank))
        
    def shuffle(self):
        # add cards back to deck and shuffle
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        strDeck = ''
        for i in range(len(self.deck)):
            strDeck += str(self.deck[i]) + ' '
        return strDeck    



#define event handlers for buttons
def deal():
    global outcome, in_play, playerHand, dealerHand, deck, score

    # your code goes here
    if not in_play:
        deck = Deck()
        deck.shuffle()
        playerHand = Hand()
        dealerHand = Hand()
        for i in range(2):
            playerHand.add_card(deck.deal_card())
            dealerHand.add_card(deck.deal_card())
        in_play = True
        outcome = ''
    else:
        outcome = 'Don\'t be too hasty'
        score -= 1
        in_play = False
        
def hit():
    global in_play, playerHand, score, outcome
    # if the hand is in play, hit the player
    if in_play:
        playerHand.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
        if playerHand.get_value() > 21:
            outcome = 'BUSTED!!'
            in_play = False
            score -= 1
            
def stand():
    global in_play, dealerHand, score, outcome
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        busted = False
        while int(dealerHand.get_value()) < 17:
            dealerHand.add_card(deck.deal_card())
            if dealerHand.get_value() > 21:
                outcome = 'Dealer busted.'
                score += 1
                busted = True
                in_play = False
        if int(dealerHand.get_value()) >= int(playerHand.get_value()) and not busted:
            outcome = 'Dealer won.'
            score -= 1
            in_play = False
        elif int(playerHand.get_value()) > int(dealerHand.get_value()) and not busted:
            outcome = 'You won.'
            score += 1
            in_play = False
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    playerHand.draw(canvas, [0, 502])
    dealerHand.draw(canvas, [0, 0])
    canvas.draw_text(outcome, (0,300), 20, 'purple')
    canvas.draw_text('score = ' + str(score), (0, 320), 20, 'purple')
    canvas.draw_text('Blackjack',(150, 300), 90, 'purple')
    if in_play:
        canvas.draw_text('Hit or stay?', (0, 280), 20, 'purple')
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, CARD_CENTER, CARD_SIZE) 
    else:
        canvas.draw_text('Deal again?', (0, 280), 20, 'purple')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("pink")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
frame.start()
playerHand = Hand()
dealerHand = Hand()


# remember to review the gradic rubric
import random
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 7 20:00:00 2020

@author: sdste
"""

# CARD
# SUIT,RANK,VALUE

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
# score function logic must provide for ace:1 case
bjvalues = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

# DECK
# The top of the deck is on the left, [0]

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = bjvalues[rank]
        
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    
    def __init__(self):
        self.all_cards = [] # list of card objects
        
        for suit in suits:
            for rank in ranks:
                # create the card object
                created_card = Card(suit,rank)
                
                self.all_cards.append(created_card)
                
    def shuffle(self):
        
        random.shuffle(self.all_cards)
        
    def deal_one(self):
        # Top of the deck is on the left
        return self.all_cards.pop(0)

# PLAYERS

class Player:
    
    def __init__(self,name):
        self.name = name
        self.chips = 0
        self.hand = [] # list of card objects

    # both the house and the human player win in the same way
    def win(self,amount):
        self.chips = self.chips + amount

    def hit(self,new_cards):
    # probably no reason to provide for more than one card per hit but this supports it anyway
    # return the player's hand after a hit
        if type(new_cards) == type([]):
            self.hand.extend(new_cards)
        else:
            self.hand.append(new_cards)
        #return self.hand
    
    # used to show the first house hand where the first card is face down
    def show_cards(self):
        print(f'{self.name}\'s hand:\n***HIDDEN***')
        print('\n'.join(map(str,self.hand[1:])))

    # shows the human player all their cards
    def show_all_cards(self):
        print(f'{self.name}\'s hand:')
        print('\n'.join(map(str,self.hand)))

    def __str__(self):
        return f'{self.name} has {self.chips} chips.'

class Human(Player):
    # Human players can run out of money
    def bet(self,amount):
        if self.chips < amount:
            # this should end the game
            return f'Player {self.name} only has {self.chips} chips.'
        self.chips = self.chips - amount
        return amount

    # human and house have different ways of deciding to hit or stand
    # prompt for hit decision
    def decide_to_hit(self,score):
        decision = input(f'Your score is {score}. Enter h to hit or any key to stand? ')
        if decision == ('h' or 'H'):
            return True
        else:
            return False

class House(Player):
    # House has unlimited money, so no if statement
    # House.chips tracks how much the house won or lost vs Human
    def bet(self,amount):
        self.chips = self.chips - amount
        return amount

    # human and house have different ways of deciding to hit or stand
    # applies dealer rule to hit below 17
    def decide_to_hit(self,score):
        if score < 17:
            return True
        else:
            return False

def start_round(min_bet):
    # This starts a round and returns T/F whether the round can be played
    # Keeps asking until the gambler bets enough or quits
    betting = True
    while betting:
        bet = int(input('How much do you want to bet? '))
        if bet >= min_bet:
            break
        if input(f'The minimum bet is {min_bet}. Are you sure you want to play (y)?') != ('y' or 'Y'):
            return False,bet
    return True,bet

def score(cards):
    # returns the total value of a list of card objects
    # handles aces
    total = 0
    aces = 0
    for card in cards:
        if  card.rank == 'Ace':
            aces += 1
        total += card.value
    while (total > 21) and (aces > 0):
        # converts each ace from 11 to 1 until the score is < 21 or there are no more aces
        total -= 10
        aces -= 1
    return total

def winner(player,bet):
    print(f'{player.name} wins this round.')
    player.chips += bet

def discard(hands):
    cards = []
    for hand in hands:
        cards.extend(hand)
    return cards

# print game intro
print('\nWelcome to Taz\'s house of Blackjack!')
print('This is single deck blackjack played by one person against the house.')
print('Bet returned for push.')
print('Spent cards are shuffled into the dealer deck after half the deck is used.')
print('Game does not support splits or doubles')

# setup players
house = House('Taz')
gambler = Human(input('What is your name? '))
gambler.chips = int(input('How many chips do you have? '))

# Tries to keep the game lenght the same no matter how much money the gambler has
buy_in = round(gambler.chips / 20)
print(f'The minimum bet is {buy_in}.')

game_on = True
round_count = 0

# create the deck and shuffle
dealer = Deck()
dealer.shuffle()
discard_pile = []

while game_on:

    bet = 0 # table bet for each round

    house.hand = []
    gambler.hand = []

    # on round 2+, check if the gambler still has money
    if round_count > 0:
        if gambler.chips < buy_in:
            print(f'\nYou\'re out of chips. The minimum is {buy_in} and you have {gambler.chips}')
        elif input(f'\nPress enter to play again or q to quit: ') == ('q' or 'Q'):
            break

    round_count += 1

    # start the round and take bets
    game_on,bet = start_round(buy_in)
    if not game_on :
        break
    gambler.bet(bet)

    print(f'Your bet of {bet} is accepted. You have {gambler.chips} chips remaining.\n\nRound {round_count} begins.\n')

    # DEAL from left to right and SHOW initial hands
    for n in range(2):
        house.hit(dealer.deal_one())
        gambler.hit(dealer.deal_one())

    house.show_cards()
    print('\n')
    gambler.show_all_cards()
    #print(f'score - {score(gambler.hand)}')
    print('\n')


    gambler_bust = False
    turn = True
    while turn:
        if score(gambler.hand) > 21:
            gambler_bust = True
            break
        elif score(gambler.hand) == 21:
            break
        else:
            turn = gambler.decide_to_hit(score(gambler.hand))
            if turn:
                gambler.hit(dealer.deal_one())
                print('\n')
                gambler.show_all_cards()

    if gambler_bust:
        print(f'{gambler.name} busts.')
        winner(house,bet)
        print(gambler)
        discard_pile = discard([house.hand,gambler.hand])
        continue

    gambler_score = score(gambler.hand)
    print(f'{gambler.name}\'s round score is {gambler_score}')


    print('\n')


    house_bust = False
    turn = True
    hit_count = 0
    while turn:
        if score(house.hand) > 21:
            house_bust = True
            break
        elif score(house.hand) == 21:
            break
        else:
            turn = house.decide_to_hit(score(house.hand))
            if turn:
                house.hit(dealer.deal_one())
                hit_count += 1

    house.show_all_cards()

    if hit_count > 0:
        print(f'{house.name} hit {hit_count} times.')
    else:
        print(f'{house.name} stands.')

    house_score = score(house.hand)
    print(f'{house.name}\'s round score is {house_score}')

    if house_bust:
        print(f'{house.name} busts.')
        winner(gambler,bet)
        print(gambler)
        discard_pile = discard([house.hand,gambler.hand])
        continue

    print('\n')

    
    if gambler_score > house_score:
        winner(gambler,bet)
    elif gambler_score < house_score:
        winner(house,bet)
    else:
        print(f'Push. Bet returned.')
        gambler.chips += bet
        print(gambler)

    discard_pile = discard([house.hand,gambler.hand])

    if len(discard_pile) >= 26:
        print(f'\nShuffling {len(discard_pile)} discarded cards back into the deck...\n')
        dealer.all_cards.extend(discard_pile)
        dealer.shuffle()


print('\nFinal chips:')
print(gambler)
print(house)
print('Thanks for playing!')




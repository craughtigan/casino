"""
This file creates the classes for cards and decks of cards.
"""

import random as rnd

C_TYPES = ('ace', 'king', 'queen', 'jack', '10', '9', '8', '7', '6', '5', '4', '3', '2')
SUITS = ('diamonds', 'hearts', 'spades', 'clubs')


class Card:
    def __init__(self, c_type, suit):
        c_type = c_type.lower()
        assert c_type in C_TYPES
        self.c_type = c_type
        assert suit in SUITS
        self.suit = suit

    def describe(self):
        print("{} of {}".format(self.c_type, self.suit))


class Deck:
    def __init__(self, deck_count=1):
        self.deck_count = deck_count
        self.cards = []
        self.init_deck()

    def init_deck(self):
        """
        Create a list of cards based on a count of the standard deck
        """
        for xx in range(self.deck_count):
            for c_type in C_TYPES:
                for suit in SUITS:
                    self.cards.append(Card(c_type, suit))

    def chance(self, c_type):
        """
        Calculate the chance of pulling a card type from the deck.
        """
        c_type = c_type.lower()
        assert c_type in C_TYPES

        count = 0
        for card in self.cards:
            count += (card.c_type is c_type)
        return count / len(self.cards)

    def draw_card(self):
        """
        Draw random card from the deck. Theoretically this is same as pulling from a shuffled deck.

        :return: Card
        """
        return self.cards.pop(rnd.randint(0, len(self.cards)-1))

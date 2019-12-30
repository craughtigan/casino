from card_deck import *
from blackjack_book import *


class PlayerHand:
    """
    Represents a hand of cards and is used to calculate the value of the hand.
    """
    def __init__(self, cards=[]):
        """
        :param cards: List of Card objects
        """
        self.cards = cards
        self.soft = False
        self.value = self.value_cards()

    def receive_card(self, deck):
        """
        Add cards to the hand from a deck and update the hand value
        :param deck: The deck to take a card from
        :return:
        """
        self.cards.append(deck.draw_card())
        self.value = self.value_cards()

    def value_cards(self):
        """
        Calculate the value of the hand based on the card-types
        :return: value fo the hand
        """
        val = 0
        for card in self.cards:
            if card.c_type in ('king', 'queen', 'jack'):
                val += 10
            elif card.c_type == 'ace':
                continue
            else:
                val += int(card.c_type)

        for card in self.cards:
            if card.c_type == 'ace':
                if val + 11 < 22:
                    val += 11
                    self.soft = True
                else:
                    val += 1
                    self.soft = False
        return val


class Player:
    """
    Track the hands of the player and the moves to make on each hand.
    """
    def __init__(self, hand_count=1):
        assert hand_count > 0
        self.hand_count = hand_count
        self.hands = []
        self.set_hands()

    def set_hands(self):
        """
        Clear the players hands.
        """
        for xx in range(self.hand_count):
            self.hands.append(PlayerHand([]))

    def play(self, dealer_show, deck):
        for xx in range(len(self.hands)):
            hand = self.hands[xx]
            stand = 0
            hand_value = hand.value
            while (stand == 0) & (hand_value < 21):
                if hand.soft:
                    move = BOOK_KEY[SOFT_BOOK[hand_value-1][dealer_show-1]]
                else:
                    move = BOOK_KEY[HARD_BOOK[hand_value-1][dealer_show-1]]

                if move == 'hit':
                    hand.receive_card(deck)
                elif move == 'stand':
                    stand = 1
                elif move == 'double':
                    hand.receive_card(deck)
                    stand = 1
                elif move == 'surrender':
                    stand = 1

                hand_value = hand.value


class Dealer(Player):
    """
    Track the hand of the dealer and the moves to make on the hand
    """
    def __init__(self):
        super().__init__()

    def play(self, dealer_show, deck):
        for xx in range(len(self.hands)):
            hand = self.hands[xx]
            stand = 0
            while stand == 0:
                hand_value = hand.value
                if hand_value < 17:
                    print('Hit!')
                    hand.receive_card(deck)
                elif hand_value > 21:
                    print('Bust!')
                    stand = 1
                else:
                    print('Stand!')
                    stand = 1


class Blackjack:
    """
    The game of blackjack.

    Tracks all players in the game and the deck of cards
    """
    def __init__(self, players=[Player()], deck_count=1):
        self.players = players
        self.players.append(Dealer())
        assert deck_count > 0
        self.deck = Deck(deck_count)

    def deal(self):
        for xx in range(2):
            for player in self.players:
                for hand in player.hands:
                    hand.receive_card(self.deck)

    def hand_values(self):
        for player in self.players:
            for hand in player.hands:
                print(hand.value)

    def play(self):
        dealer_card = self.players[-1].hands[0].cards[0]
        d_card_val = show_card_value(dealer_card)
        for player in self.players:
            player.play(d_card_val, self.deck)


def show_card_value(card):
    if card.c_type in ('king', 'queen', 'jack'):
        return 10
    elif card.c_type == 'ace':
        return 11
    else:
        return int(card.c_type)
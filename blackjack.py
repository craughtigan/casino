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

    def reset_hand(self):
        self.cards = []
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
        Set the players hands.
        """
        for xx in range(self.hand_count):
            self.hands.append(PlayerHand([]))

    def reset_hands(self):
        """
        Re-set the player's hands.
        """
        for xx in range(self.hand_count):
            self.hands[xx] = PlayerHand([])

    def play(self, dealer_show, deck):
        for xx in range(len(self.hands)):
            hand = self.hands[xx]
            stand = 0
            hand_value = hand.value
            while (stand == 0) & (hand_value < 21):
                if hand.soft:
                    move = BOOK_KEY[SOFT_BOOK[hand_value][dealer_show-1]]
                else:
                    move = BOOK_KEY[HARD_BOOK[hand_value][dealer_show-1]]

                if move == 'hit':
                    print('Player hit! {}'.format(hand_value))
                    hand.receive_card(deck)
                elif move == 'stand':
                    print('Player stand! {}'.format(hand_value))
                    stand = 1
                elif move == 'double':
                    print('Player double! {}'.format(hand_value))
                    hand.receive_card(deck)
                    stand = 1
                elif move == 'surrender':
                    print('Player surrender! {}'.format(hand_value))
                    hand.reset_hand()
                    stand = 1

                hand_value = hand.value

            if hand.value > 21:
                print('Player bust ! {}'.format(hand_value))
                hand.reset_hand()


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
            hand_value = hand.value
            while (stand == 0) & (hand_value < 21):
                if hand_value < 17:
                    print('Dealer Hit! {}'.format(hand_value))
                    hand.receive_card(deck)
                else:
                    print('Dealer Stand! {}'.format(hand_value))
                    stand = 1
                hand_value = hand.value

            if hand.value > 21:
                print('Dealer Bust! {}'.format(hand_value))
                hand.reset_hand()


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

    def full_round(self):
        self.deal()
        self.hand_values()
        self.play()
        self.results()
        self.clear_hands()

    def deal(self):
        if len(self.deck.cards) < (len(self.players) * 4):
            print('Shuffling!')
            self.deck.init_deck()

        print('Dealing Cards')
        for xx in range(2):
            for player in self.players:
                for hand in player.hands:
                    hand.receive_card(self.deck)

    def hand_values(self):
        for xx in range(len(self.players) - 1):
            player = self.players[xx]
            for hand in player.hands:
                print(hand.value)

    def play(self):
        dealer_card = self.players[-1].hands[0].cards[0]
        d_card_val = show_card_value(dealer_card)
        print('Dealer showing {}'.format(d_card_val))
        print('\n')
        for player in self.players:
            player.play(d_card_val, self.deck)
        print('\n')

    def results(self):
        dealer_hand = self.players[-1].hands[0].value
        if dealer_hand == 0:
            print('Dealer busted!')
        else:
            print('Dealer Stand with {}'.format(dealer_hand))

        for xx in range(len(self.players) - 1):
            player = self.players[xx]
            for hand in player.hands:
                hand_value = hand.value
                if hand_value == 0:
                    continue
                else:
                    if hand_value > 21:
                        print('Player bust! {}'.format(hand_value))
                    elif hand_value == dealer_hand:
                        print('Player push! {}'.format(hand_value))
                    elif hand_value < dealer_hand:
                        print('Player loss! {}'.format(hand_value))
                    elif hand_value > dealer_hand:
                        print('Player win! {}'.format(hand_value))
                    else:
                        print('!!! Forgot something !!!')

    def clear_hands(self):
        for player in self.players:
            player.reset_hands()


def show_card_value(card):
    if card.c_type in ('king', 'queen', 'jack'):
        return 10
    elif card.c_type == 'ace':
        return 11
    else:
        return int(card.c_type)

game = Blackjack([Player(), Player()], 1)

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

    def check_split(self):
        """
        Make sure that the cards are the same type to split
        """
        if len(self.cards) != 2:
            return False
        else:
            return ((len(self.cards) == 2)
                    & (self.cards[0].c_type == self.cards[1].c_type))

    def value_cards(self):
        """
        Calculate the value of the hand based on the card-types
        :return: value fo the hand
        """
        val = 0
        for card in self.cards:
            if card.c_type in ('K', 'Q', 'J'):
                val += 10
            elif card.c_type == 'A':
                continue
            else:
                val += int(card.c_type)

        for card in self.cards:
            if card.c_type == 'A':
                if val + 11 < 22:
                    val += 11
                    self.soft = True
                else:
                    val += 1
                    self.soft = False
        self.value = val
        return val

    def print_cards(self):
        return "Hand: " + ", ".join([card.c_type for card in self.cards])


class Player:
    """
    Track the hands of the player and the moves to make on each hand.
    """
    def __init__(self, hand=None):
        self.hands = []
        if hand is None:
            self.set_hands()
        else:
            self.input_hand(hand)

    def set_hands(self):
        """
        Set the players hand.
        """
        self.hands.append(PlayerHand([]))

    def input_hand(self, hand):
        """
        Set the players hand as the input hand.
        """
        self.hands.append(hand)

    def reset_hands(self):
        """
        Re-set the player's hand.
        """
        self.hands = [PlayerHand([])]

    def split_hand(self, hand_idx):
        """
        Split a hand where the cards value matches.
        :param hand_idx: The index of the hand to split
        """
        new_hand = PlayerHand([self.hands[hand_idx].cards.pop()])
        self.hands.insert(hand_idx + 1, new_hand)
        self.hands[hand_idx].value_cards()

    def play(self, dealer_show, deck):
        """
        Go through each hand and make moves by the book

        :param dealer_show: The dealers car that is showing
        :param deck: The deck to pull from
        """

        # Track total hands in order to increment for splits
        total_hands = len(self.hands)
        xx = 0
        while xx < total_hands:
            hand = self.hands[xx]
            done = 0
            hand_value = hand.value
            while (done == 0) & (hand_value < 21):
                # Always hit after a split
                print('Player Value: {} {}'.format(hand_value, hand.print_cards()))
                move = input("What is your move?")

                # Execute the moves
                if move == 'hit':
                    print('Player Hit!')
                    hand.receive_card(deck)
                elif move == 'stand':
                    print('Player Stand!')
                    done = 1
                elif move == 'double':
                    print('Player Double!')
                    # todo: disallowed double after first move
                    hand.receive_card(deck)
                    done = 1
                elif move == 'split':
                    print('Player Split!')
                    self.split_hand(xx)
                    total_hands += 1
                elif move == 'surrender':
                    print('Player Surrender!')
                    hand.reset_hand()
                    done = 1

                hand_value = hand.value
            xx += 1

            # Clear cards on a bust
            if hand.value > 21:
                print('Player Bust! Value: {} {}'.format(hand_value, hand.print_cards()))
                hand.reset_hand()

        return 0


class NPC(Player):
    """
    Track the hand of the dealer and the moves to make on the hand
    """
    def __init__(self):
        super().__init__()

    def play(self, dealer_show, deck):
        """
        Go through each hand and make moves by the book

        :param dealer_show: The dealers car that is showing
        :param deck: The deck to pull from
        """

        # Track total hands in order to increment for splits
        total_hands = len(self.hands)
        xx = 0
        while xx < total_hands:
            hand = self.hands[xx]
            done = 0
            hand_value = hand.value
            while (done == 0) & (hand_value < 21):
                # Always hit after a split
                if len(hand.cards) == 1:
                    move = 'hit'
                # Use split book when cards match
                elif hand.check_split() and (hand_value not in (10, 20)):
                    c_type = hand.cards[0].c_type
                    move = BOOK_KEY[SPLIT_BOOK[c_type][dealer_show-2]]
                # Soft book when there is a soft ace
                elif hand.soft:
                    move = BOOK_KEY[SOFT_BOOK[hand_value][dealer_show-2]]
                # Hard book for all other moves
                else:
                    move = BOOK_KEY[HARD_BOOK[hand_value][dealer_show-2]]

                # Execute the moves
                if move == 'hit':
                    print('NPC Hit! Value: {} {}'.format(hand_value, hand.print_cards()))
                    hand.receive_card(deck)
                elif move == 'stand':
                    print('NPC Stand! Value: {} {}'.format(hand_value, hand.print_cards()))
                    done = 1
                elif move == 'double':
                    print('NPC Double! Value: {} {}'.format(hand_value, hand.print_cards()))
                    hand.receive_card(deck)
                    done = 1
                elif move == 'split':
                    print('NPC Split! Value: {} {}'.format(hand_value, hand.print_cards()))
                    self.split_hand(xx)
                    total_hands += 1
                elif move == 'surrender':
                    print('NPC Surrender! Value: {} {}'.format(hand_value, hand.print_cards()))
                    hand.reset_hand()
                    done = 1

                hand_value = hand.value
            xx += 1

            # Clear cards on a bust
            if hand.value > 21:
                print('NPC Bust! Value: {} {}'.format(hand_value, hand.print_cards()))
                hand.reset_hand()

        return 0


class Dealer(Player):
    """
    Track the hand of the dealer and the moves to make on the hand
    """
    def __init__(self):
        super().__init__()

    def play(self, dealer_show, deck):
        """
        The dealer makes moves based on the hand.

        :param deck: the deck to pull from
        :return:
        """
        for xx in range(len(self.hands)):
            hand = self.hands[xx]
            done = 0
            hand_value = hand.value
            while (done == 0) & (hand_value < 21):
                # todo: Implement soft 17 hit
                if hand_value < 17:
                    print('Dealer Hit! {}'.format(hand_value))
                    hand.receive_card(deck)
                else:
                    print('Dealer Stand! {}'.format(hand_value))
                    done = 1
                hand_value = hand.value

            # Hand cleared when dealer bust
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
        """
        Run through an entire round of NPCs playing by the book
        """
        self.deal()
        self.hand_values()
        self.play()
        self.results()
        self.clear_hands()

    def deal(self):
        """
        Deal two cards to each player and dealer in order
        """
        if len(self.deck.cards) < (len(self.players) * 5):
            print('Shuffling!')
            self.deck.init_deck()

        print('Dealing Cards')
        for xx in range(2):
            for player in self.players:
                for hand in player.hands:
                    hand.receive_card(self.deck)

    def hand_values(self):
        """
        Print values of hands for NPCs but not the dealer
        """
        # todo: print the cards that the players have
        for xx in range(len(self.players) - 1):
            player = self.players[xx]
            for hand in player.hands:
                print("Value: " + str(hand.value) + " " + hand.print_cards())

    def play(self):
        """
        Each player makes the moves for their hands
        """
        dealer_card = self.players[-1].hands[0].cards[0]
        d_card_val = show_card_value(dealer_card)
        print('Dealer showing {}'.format(dealer_card.c_type))
        print('\n')
        for player in self.players:
            player.play(d_card_val, self.deck)
        print('\n')

    def results(self):
        """
        Print the results for remaining hands at end of the round
        """
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
        print('\n')

    def clear_hands(self):
        for player in self.players:
            player.reset_hands()


def show_card_value(card):
    if card.c_type in ('K', 'Q', 'J'):
        return 10
    elif card.c_type == 'A':
        return 11
    else:
        return int(card.c_type)


game = Blackjack([Player(), NPC()], 2)
for xx in range(1000):
    game.full_round()


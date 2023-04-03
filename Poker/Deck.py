from random import shuffle
from itertools import combinations
card_suit = {0: "Clubs", 1: "Hearts", 2: "Diamonds", 3: "Spades"}
card_value = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight",
              9: "Nine", 10: "Ten", 11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    def __repr__(self):
        return card_value[self.value] + " of " + card_suit[self.suit]


def determine_strength(pool):
    def check_pair(cards):
        for combination in combinations(cards, 2):
            if len(set([card.value for card in combination])) == 1:
                return combination
        return None

    def check_two_pairs(cards):
        for two_pairs in combinations(cards, 4):
            for first_pair in combinations(two_pairs, 2):
                second_pair = set(two_pairs) - set(first_pair)
                combination = check_pair(first_pair) and check_pair(second_pair)
                if not combination:
                    return combination
        return None

    def check_three_of_a_kind(cards):
        for combination in combinations(cards, 3):
            if len(set([card.value for card in combination])) == 1:
                return combination
        return None

    def check_straight(cards):
        for combination in combinations(cards, 5):
            values = sorted([card.value for card in combination])


        return None

    def check_flush(cards):
        return len(set([card.suit for card in cards])) == 1

    def check_full_house(cards):
        return False

    def check_four_of_a_kind(cards):
        for combination in combinations(cards, 4):
            if len(set([card.value for card in combination])) == 1:
                return True, combination
        return False, None

    def check_straight_flush(cards):
        return check_straight(cards) and check_flush()


class DeckIter:
    def __init__(self, deck_class, current_index=0):
        self._cards = deck_class.cards
        self._deck_size = len(deck_class.cards)
        self._current_index = current_index

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_index < self._deck_size:
            member = self._cards[self._current_index]
            self._current_index += 1
            return member
        raise StopIteration


class Deck:
    def __init__(self):
        self.cards = [Card(j, i) for i in range(4) for j in range(2, 15)]

    def shuffle(self):
        shuffle(self.cards)

    def __iter__(self):
        return DeckIter(self)

    def give_cards(self, number=1):
        return [self.cards.pop() for i in range(number)]


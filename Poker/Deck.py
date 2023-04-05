from random import shuffle
from itertools import combinations, islice
card_suit = {0: "Clubs", 1: "Hearts", 2: "Diamonds", 3: "Spades"}
card_value = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight",
              9: "Nine", 10: "Ten", 11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __lt__(self, other):
        return self.value < other.value
    def __repr__(self):
        return card_value[self.value] + " of " + card_suit[self.suit]



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

class Combination:
    __combination_strength = {"royal_flush": 9, "straight_flush": 8, "four_of_a_kind": 7,
                              "full_house": 6, "flush": 5, "straight": 4, "three_of_a_kind": 3,
                              "two_pairs": 2, "pair": 1, "high_card": 0}
    __combination_len = 5
    def __init__(self, pool):
        self.pool = pool
        self.name_of_highest_combination = None  # name of combination
        self.highest_combination = None  # combination itself (all cards in one set) (for high_card all 5 cards)
        self.kicker = None  # other cards from 5 without combination
    def __lt__(self, other):
        comb1_name = self.name_of_highest_combination
        comb2_name = other.name_of_highest_combination
        if comb1_name is None and comb2_name is None:
            return False
        if comb1_name is None:
            return True
        if comb2_name is None:
            return False
        if self.__combination_strength[comb1_name] < self.__combination_strength[comb2_name]:
            return True
        if self.__combination_strength[comb1_name] > self.__combination_strength[comb2_name]:
            return False

        # Now we know that combinations are same
        comb1 = self.highest_combination
        comb2 = other.highest_combination
        kicker1 = self.highest_combination
        kicker2 = other.kicker
        match comb1_name:
            case "royal_flush":
                return False
            case "straight_flush" | "straight":
                ...
            case "four_of_a_kind" | "three_of_a_kind":
                return next(iter(comb1)) < next(iter(comb2))
            case "full_house":
                ...
            case "flush" | "high_card":
                return max(comb1) < max(comb2)
            case "two_pairs":
                ...
            case "pair":
                ...


    def determine_strength(self):
        def find_pair(cards):
            for combination in combinations(cards, 2):
                if len(set([card.value for card in combination])) == 1:
                    return set(combination)
            return set()

        def find_two_pairs(cards):
            for combination in combinations(cards, 4):
                for first_pair in combinations(combination, 2):
                    second_pair = set(combination) - set(first_pair)
                    if find_pair(first_pair) and find_pair(second_pair):
                        return set(combination)
            return set()

        def find_three_of_a_kind(cards):
            for combination in combinations(cards, 3):
                if len(set([card.value for card in combination])) == 1:
                    return set(combination)
            return set()

        def find_straight(cards):
            for combination in combinations(cards, 5):
                values = sorted([card.value for card in combination])
                if values == [2, 3, 4, 5, 14] or set([values[i] - values[0] - i for i in range(5)]) == {0}:
                    return set(combination)
            return set()

        def find_flush(cards):
            for combination in combinations(cards, 5):
                if len(set([card.suit for card in combination])) == 1:
                    return set(combination)
            return set()

        def find_full_house(cards):
            for combination in combinations(cards, 5):
                for pair in combinations(combination, 2):
                    triple = set(combination) - set(pair)
                    if find_pair(pair) and find_three_of_a_kind(triple):
                        return set(combination)
            return set()

        def find_four_of_a_kind(cards):
            for combination in combinations(cards, 4):
                if len(set([card.value for card in combination])) == 1:
                    return set(combination)
            return set()

        def find_straight_flush(cards):
            for combination in combinations(cards, 5):
                if find_straight(combination) and find_flush(combination):
                    return set(combination)
            return set()

        def find_royal_flush(cards) -> set:
            for combination in combinations(cards, 5):
                if sorted(list(combination))[0].value == 10 and find_straight_flush(combination):
                    return set(combination)
            return set()

        all_combinations = ["royal_flush", "straight_flush", "four_of_a_kind", "full_house",
                            "flush", "straight", "three_of_a_kind", "two_pairs", "pair"]
        combinations_finders = [find_royal_flush, find_straight_flush, find_four_of_a_kind, find_full_house,
                                 find_flush, find_straight, find_three_of_a_kind, find_two_pairs, find_pair]
        for combination, combinations_finder in zip(all_combinations, combinations_finders):
            if combinations_finder(self.pool):
                self.name_of_highest_combination, self.highest_combination = combination, combinations_finder(self.pool)
                self.kicker = set(self.pool) - set(self.highest_combination)
                self.kicker = set(islice(sorted(self.kicker),
                                         len(self.kicker) - (self.__combination_len - len(self.highest_combination)),
                                         len(self.kicker)))
                return
        self.name_of_highest_combination, self.kicker = "high_card", set()
        self.highest_combination = set(islice(sorted(self.pool), len(self.pool) - self.__combination_len, len(self.pool)))


d = Deck()
d.shuffle()
a = Combination(d.give_cards(7))
a.determine_strength()
print(a.pool, a.name_of_highest_combination, a.highest_combination, a.kicker, sep="\n")


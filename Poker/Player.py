class Player:
    def __init__(self, name="NoName"):
        self.name = name
        self.chips = 0
        self.hand = []

    def change_chips(self, chips):
        self.chips += chips

    def give_card(self, card):
        self.hand.append(card)

    def make_bid(self, chips_to_bid=0):
        if chips_to_bid > self.chips:
            chips_to_bid = self.chips  # maybe do something else
        self.chips -= chips_to_bid
        # TODO: proceed def bid in class Game


class Bot(Player):
    def change_strategy(self):
        ...
        # TODO: be able to change strategy of making decisions


class Rational(Bot):
    ...


class Agressive(Bot):
    ...

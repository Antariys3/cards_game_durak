class Card:
    def __init__(self, name, suit, value, trump_card=False):
        self.name = name
        self.suit = suit
        self.value = value
        self.trump_suit = trump_card

    def __repr__(self):
        return f"{self.suit} {self.name}"

    def __str__(self):
        return f"{self.suit} {self.name}"

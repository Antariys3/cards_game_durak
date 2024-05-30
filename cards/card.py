class Card:
    name: str
    suit: str
    value: str
    trump_card: bool

    def __init__(self, name, suit, value, trump_card=False):
        self.name = name
        self.suit = suit
        self.value = value
        self.trump_card = trump_card

    def is_trump_card(self, trump_suit):
        return self.suit == trump_suit

    def set_card_as_trump_card(self):
        self.trump_card = True

    def __str__(self):
        return f"{self.suit} {self.name}"

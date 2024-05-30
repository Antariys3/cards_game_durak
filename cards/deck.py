import random

from cards.card import Card
from cards.constants import CARD_VALUES, SUITS


class Deck:
    cards: list
    trump_suit: str
    cards_on_table: list[Card]

    def __init__(self):
        self.create_deck()
        self.cards_on_table = []

    def create_deck(self) -> None:
        values = range(6, 15)
        self.cards = [
            Card(name, suit, value)
            for suit in SUITS
            for name, value in zip(CARD_VALUES, values)
        ]
        random.shuffle(self.cards)

    def set_trump(self):
        self.trump_suit = self.cards[-1].suit
        print(f"Trump suit for this game is chosen: {self.trump_suit}.\n")

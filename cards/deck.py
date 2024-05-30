from cards.card import Card


class Deck:
    def __init__(self):
        self.cards: list[Card] = self.create_card()
        self.trump_card: Card | None = None
        self.cards_on_table: list[Card] = []

    def create_card(self) -> list:
        names = ['6', '7', '8', '9', '10', 'Валет', 'Дама', 'Король', 'Туз']
        suits = ['♦', '♠', '♥', '♣']
        values = range(6, 15)
        return [Card(name, suit, value) for suit in suits for name, value in zip(names, values)]

    def deal_card(self):
        return self.cards.pop()

    def set_trump_cards(self):
        for card in self.cards:
            if card.suit == self.trump_card.suit:
                card.trump_card = True

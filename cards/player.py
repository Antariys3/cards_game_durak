class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.move = False
        self.took_cards = False

    def draw_cards(self, deck):
        while len(self.hand) < 6 and len(deck.cards) > 0:
            self.hand.append(deck.cards.pop())
        self.sort_cards()

    def pick_up_card(self, deck):

        if not deck.cards:
            return

        self.hand.extend(deck.cards_on_table)
        deck.cards_on_table.clear()

    def sort_cards(self):
        # сортируем карты так, чтобы козырные карты были слева по этому
        # отделяем их в отдельный список
        trump_cards = [card for card in self.hand if card.trump_card]
        trump_cards.sort(key=lambda card: card.value)

        # создаём отдельный список не козырных карт и сортируем его.
        not_trump_cards = [card for card in self.hand if not card.trump_card]
        not_trump_cards.sort(key=lambda card: card.value)

        self.hand = trump_cards + not_trump_cards

    def has_trump_card(self, trump):
        return True if trump in self.hand else False

    def get_highest_trump_card(self, trump):
        return self.hand[0] if self.has_trump_card(trump) else False

    def __str__(self):
        return self.name

class Player(Bot, ):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.move = False
        self.took_cards = False

    def draw_cards(self, deck):
        while len(self.hand) < 6 and len(deck.cards) > 0:
            self.hand.append(deck.cards.pop())

    def pick_up_card(self, deck):
        self.hand.extend(deck.cards_on_table)
        deck.cards_on_table.clear()

    def sorting_cards(self):
        # сортируем карты так, чтобы козырные карты были слева по этому отделяем их в отдельный список
        list_trump = [card for card in self.hand if card.trump_card]
        list_trump.sort(key=lambda card: card.value)
        # создаём отдельный список не козырных карт и сортируем его.
        list_not_trump = [card for card in self.hand if not card.trump_card]
        list_not_trump.sort(key=lambda card: card.value)
        self.hand = list_trump + list_not_trump

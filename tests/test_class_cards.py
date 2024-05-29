import random

from cards.card import Card
from cards.deck import Deck
from cards.player import Player


class TestCards:
    def test_deck_length(self):
        cards = Deck()
        assert len(Deck.create_card(cards)) == 36

    def test_trump_card(self):
        deck_cards = Deck()
        random.shuffle(deck_cards.cards)
        last_card = deck_cards.cards[0]
        deck_cards.trump_card = last_card
        assert last_card == deck_cards.trump_card
        assert len(deck_cards.cards) == 36

    def test_trump_cards(self):
        # проверка количества козырных карт в колоде и метода .set_trump_cards()
        deck_cards = Deck()
        random.shuffle(deck_cards.cards)
        deck_cards.trump_card = deck_cards.cards[0]
        deck_cards.set_trump_cards()
        # инициализация козырных кар
        count_trump_cards = sum(1 for card in deck_cards.cards if card.trump_card)
        assert count_trump_cards == 9


class TestPlayer:
    def test_draw_cards(self):
        deck_cards = Deck()
        random.shuffle(deck_cards.cards)
        player = Player("Player_1")
        player.draw_cards(deck_cards)
        assert len(player.hand) == 6

    def test_empty_draw_cards(self):
        deck_cards = Deck()
        deck_cards.cards = []
        random.shuffle(deck_cards.cards)
        player = Player("Player_1")
        player.draw_cards(deck_cards)
        assert len(player.hand) == 0

    def test_pick_up_cards(self):
        # Создание начальных карт на столе
        cards_1 = [
            Card('6', '♦', 6), Card('7', '♦', 7), Card('8', '♦', 8),
            Card('9', '♦', 9), Card('10', '♦', 10), Card('Валет', '♦', 11),
        ]
        # Создание начальных карт в руке игрока
        cards_2 = [
            Card('Дама', '♦', 12), Card('Кароль', '♦', 13), Card('Туз', '♦', 14),
        ]

        # Настройка колоды и проверка количества карт на столе
        deck_cards = Deck()
        deck_cards.cards_on_table = cards_1
        assert len(deck_cards.cards_on_table) == 6

        # Создание игрока и проверка количества карт в руке
        player = Player("Player_1")
        player.hand = cards_2
        assert len(player.hand) == 3

        # Игрок подбирает карты со стола и проверка изменений
        player.pick_up_card(deck_cards)
        assert len(player.hand) == 9
        assert len(deck_cards.cards_on_table) == 0

    def test_sorting_cards(self):
        player = Player("Player_1")
        cards = [
            Card('7', '♦', 7),
            Card('Валет', '♦', 11, trump_card=True),
            Card('10', '♦', 10),
            Card('9', '♦', 9, trump_card=True),
            Card('8', '♦', 8),
            Card('6', '♦', 6),
        ]
        player.hand = cards.copy()
        player.sorting_cards()
        assert player.hand[0] == cards[3]
        assert player.hand[1] == cards[1]
        assert player.hand[2] == cards[5]
        assert player.hand[3] == cards[0]
        assert player.hand[4] == cards[4]
        assert player.hand[5] == cards[2]

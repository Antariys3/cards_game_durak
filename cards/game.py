import os
import random

from cards.card import Card
from cards.deck import Deck
from cards.player import Player


class Game:
    def __init__(self):
        self.deck = Deck()
        self.players: [Player] = [Player("User"), Player("Bot")]
        self.initialize_game()

    def initialize_game(self):
        while True:
            random.shuffle(self.deck.cards)
            self.deck.trump_card = self.deck.cards[0]
            self.deck.set_trump_cards()
            self.draw_cards()
            if self.first_move():
                break
            self.__init__()

    @staticmethod
    def clear_terminal():
        os.system('clear')

    def draw_cards(self):
        [player.draw_cards(self.deck) for player in self.players]
        [player.sorting_cards() for player in self.players]

    def next_turn(self):
        user = self.players[0]
        bot = self.players[1]
        self.deck.cards_on_table.clear()
        self.draw_cards()
        if user.move and not bot.took_cards:
            user.move = False
            bot.move = True
        elif user.move and bot.took_cards:
            bot.took_cards = False
        elif user.move is False and not user.took_cards:
            user.move = True
            bot.move = False
        elif user.move is False and user.took_cards:
            user.took_cards = False

    def first_move(self):
        player = self.players[0]
        pl_card = player.hand[0]
        bot = self.players[1]
        b_card = bot.hand[0]
        if pl_card.trump_suit and b_card.trump_suit:
            if pl_card.value < b_card.value:
                player.move = True
                return True
            else:
                bot.move = True
                return True

        elif pl_card.trump_suit or b_card.trump_suit:
            if pl_card.trump_suit:
                player.move = True
                return True

            else:
                bot.move = True
                return True

        else:
            return False
            # print("Козырных карт не оказалось, пересдача колоды")
            # self.initialize_game()

    def announce_first_move(self):
        # Объявление первого хода
        if len(self.deck.cards) == 24:
            if self.players[0].move:
                print("У Вас козырь, вы ходите первые")
                return
            print(f"У бота {self.players[1].hand[0]} он походил первый")

    def show_table(self):
        # self.clear_terminal()
        print("Карты бота")
        for card in self.players[1].hand:
            print(card, end=" | ")
        print()

        print(f"Козырная карта: {self.deck.trump_card}")
        print()

        if self.deck.cards_on_table:
            print("Карты на столе: ")
            for card in self.deck.cards_on_table:
                print(card, end=" | ")
            print()
            print()

        print("Мои карты")
        for card in self.players[0].hand:
            print(card, end=" | ")
        print()
        self.announce_first_move()
        print("_" * 60)

    def user_input(self):
        check_list = [i for i in range(0, len(self.players[0].hand) + 1)]
        while True:
            user = input(f"0 - отбой или забрать карты. Выбери карту 1-{len(check_list)}: ")
            if user.isdigit() and int(user) in check_list:
                return int(user)
            print("Ошибка, такой команды нету")

    def move(self):
        if self.players[0].move:
            self.move_user()
        else:
            self.move_bot()

    def move_user(self):
        user = self.players[0]
        bot = self.players[1]

        while user.move:
            user_input = self.user_input()
            if user_input != 0:
                self.move_player_attack(user_input)
                self.move_bot_defense()
            elif user_input == 0 and self.deck.cards_on_table and not bot.took_cards:
                self.next_turn()
            if bot.took_cards and user_input == 0:
                bot.pick_up_card(deck=self.deck)
                self.next_turn()

    def move_player_attack(self, user_input):
        user_card: Card = self.players[0].hand[user_input - 1]
        if not self.deck.cards_on_table:
            self.deck.cards_on_table.append(self.players[0].hand.pop(user_input - 1))
            return
        for card in self.deck.cards_on_table:
            if card.value == user_card.value:
                self.deck.cards_on_table.append(self.players[0].hand.pop(user_input - 1))
                return

    def move_bot_defense(self):
        bot = self.players[1]
        card_table = self.deck.cards_on_table[-1]
        if not bot.took_cards:
            # не козырная карта бьёт не козырную
            for index, card in enumerate(bot.hand):
                if card_table.suit == card.suit and card_table.value < card.value and not card_table.trump_suit:
                    self.deck.cards_on_table.append(bot.hand.pop(index))
                    return
            if 4 < len(self.deck.cards) < 15:
                # козырная карта меньше Вальта бьёт не козырную
                for index, card in enumerate(bot.hand):
                    if card.trump_suit and card.value < 11 and not card_table.trump_suit:
                        self.deck.cards_on_table.append(bot.hand.pop(index))
                        return
            if len(self.deck.cards) < 4:
                # козырная карта бьёт не козырную
                for index, card in enumerate(bot.hand):
                    if card.trump_suit and not card_table.trump_suit:
                        self.deck.cards_on_table.append(bot.hand.pop(index))
                        return
            if len(self.deck.cards) < 4:
                # козырная карта бьёт козырную
                for index, card in enumerate(bot.hand):
                    if card_table.trump_suit and card.trump_suit and card.value > card_table.value:
                        self.deck.cards_on_table.append(bot.hand.pop(index))
                        return
            print("Бот берёт карты, подкидываем или отбой?")
            bot.took_cards = True

    def move_bot(self):
        user = self.players[0]
        bot = self.players[1]

        while bot.move:
            if not self.deck.cards_on_table:
                self.move_bot_attack()
                self.move_player_defense()

            if self.deck.cards_on_table:
                self.bot_flip_cards()
                self.move_player_defense()

            if user.took_cards and not bot.move:
                user.pick_up_card(deck=self.deck)
                self.next_turn()
            elif self.deck.cards_on_table and not bot.move:
                self.next_turn()

    def move_bot_attack(self):
        bot = self.players[1]
        for index, card in enumerate(bot.hand):
            if not card.trump_suit:
                # если пустой стол, ходим первой не козырной картой
                self.deck.cards_on_table.append(bot.hand.pop(index))
                return
        for index, card in enumerate(bot.hand):
            # если ничем не походили когда пустой стол, то ходим козырной картой
            self.deck.cards_on_table.append(bot.hand.pop(index))
            return

    def bot_flip_cards(self):
        bot = self.players[1]
        cards_table = self.deck.cards_on_table
        if self.players[0].took_cards:
            for card_table in cards_table:
                for index, card_bot in enumerate(bot.hand):
                    # если в колоде больше 12 карт, то подкидываем всё кроме козырей и ниже Вальтов
                    if len(self.deck.cards) > 12 and card_bot.value < 10:
                        if not card_bot.trump_suit and card_table.value == card_bot.value:
                            self.deck.cards_on_table.append(bot.hand.pop(index))
                    # если в колоде меньше 12 карт, то подкидываем всё кроме козырей
                    elif 4 < len(self.deck.cards) < 12:
                        if not card_bot.trump_suit and card_table.value == card_bot.value:
                            self.deck.cards_on_table.append(bot.hand.pop(index))
                    # если в колоде меньше 4 карт, то подкидываем всё
                    elif len(self.deck.cards) < 4 and card_table.value == card_bot.value:
                        self.deck.cards_on_table.append(bot.hand.pop(index))
            else:
                print("Отбой!")
                bot.move = False
            return

        for card_table in cards_table:
            for index, card_bot in enumerate(bot.hand):
                # если в колоде больше 12 карт, то подкидываем всё кроме козырей и ниже Вальтов
                if len(self.deck.cards) > 12 and card_bot.value < 10:
                    if not card_bot.trump_suit and card_table.value == card_bot.value:
                        self.deck.cards_on_table.append(bot.hand.pop(index))
                        return
                # если в колоде меньше 12 карт, то подкидываем всё кроме козырей
                elif 4 < len(self.deck.cards) < 12:
                    if not card_bot.trump_suit and card_table.value == card_bot.value:
                        self.deck.cards_on_table.append(bot.hand.pop(index))
                        return
                # если в колоде меньше 4 карт, то подкидываем всё
                elif len(self.deck.cards) < 4 and card_table.value == card_bot.value:
                    self.deck.cards_on_table.append(bot.hand.pop(index))
                    return
        else:
            print("Отбой!")
            bot.move = False

    def move_player_defense(self):
        user = self.players[0]
        while True:
            self.show_table()
            user_input = self.user_input()
            if user_input == 0 or user.took_cards:
                user.took_cards = True
                break

            if user_input != 0:
                card_table = self.deck.cards_on_table[-1]
                player_card: Card = user.hand[user_input - 1]
                if (card_table.suit == player_card.suit and card_table.value < player_card.value or
                        not card_table.trump_suit and player_card.trump_suit):
                    self.deck.cards_on_table.append(user.hand.pop(user_input - 1))
                    break
            print("Вы ввели не корректные данные. Выберете другой вариант")

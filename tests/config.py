from cards.card import Card


def comparison_lists_cards(res_list: list[Card], expected_list: list[Card]):
    for j, i in zip(res_list, expected_list):
        assert j.name == i.name
        assert j.suit == i.suit
        assert j.value == i.value
        assert j.trump_suit == i.trump_suit

from typing import Sequence
from unittest.mock import Mock

import pytest

from balatro_gym.cards.interfaces import PlayingCard, Suit
from balatro_gym.cards.joker import Joker
from balatro_gym.game.scoring import get_poker_hand
from balatro_gym.interfaces import PokerHandType


def _make_board(jokers: Sequence[Joker] = []) -> Mock:
    board = Mock()
    board.jokers = jokers
    return board


STRAIGHT_FLUSH = [PlayingCard(i, Suit.HEARTS, None, None, None) for i in range(1, 6)]
ROYAL_FLUSH = [PlayingCard(i, Suit.HEARTS, None, None, None) for i in [13, 12, 11, 10, 1]]
FLUSH_FIVE = [PlayingCard(10, Suit.HEARTS, None, None, None) for _ in range(5)]
FLUSH = [PlayingCard(i, Suit.SPADES, None, None, None) for i in [2, 5, 7, 11, 13]]
FLUSH_HOUSE = [PlayingCard(1, Suit.SPADES, None, None, None)] * 2 + [PlayingCard(5, Suit.SPADES, None, None, None)] * 3
STRAIGHT = [
    PlayingCard(1, Suit.HEARTS, None, None, None),
    PlayingCard(2, Suit.SPADES, None, None, None),
    PlayingCard(3, Suit.DIAMONDS, None, None, None),
    PlayingCard(4, Suit.SPADES, None, None, None),
    PlayingCard(5, Suit.HEARTS, None, None, None),
]
FIVE_SET = [
    PlayingCard(1, Suit.HEARTS, None, None, None),
    PlayingCard(1, Suit.SPADES, None, None, None),
    PlayingCard(1, Suit.DIAMONDS, None, None, None),
    PlayingCard(1, Suit.SPADES, None, None, None),
    PlayingCard(1, Suit.HEARTS, None, None, None),
]
FULL_HOUSE = [
    PlayingCard(1, Suit.HEARTS, None, None, None),
    PlayingCard(1, Suit.SPADES, None, None, None),
    PlayingCard(1, Suit.DIAMONDS, None, None, None),
    PlayingCard(4, Suit.SPADES, None, None, None),
    PlayingCard(4, Suit.HEARTS, None, None, None),
]
FOUR_SET = [
    PlayingCard(2, Suit.HEARTS, None, None, None),
    PlayingCard(2, Suit.SPADES, None, None, None),
    PlayingCard(2, Suit.DIAMONDS, None, None, None),
    PlayingCard(2, Suit.SPADES, None, None, None),
]
THREE_SET = [
    PlayingCard(2, Suit.HEARTS, None, None, None),
    PlayingCard(2, Suit.SPADES, None, None, None),
    PlayingCard(2, Suit.DIAMONDS, None, None, None),
]
TWO_PAIR = [
    PlayingCard(2, Suit.HEARTS, None, None, None),
    PlayingCard(2, Suit.SPADES, None, None, None),
    PlayingCard(5, Suit.DIAMONDS, None, None, None),
    PlayingCard(5, Suit.SPADES, None, None, None),
    PlayingCard(6, Suit.HEARTS, None, None, None),
]
PAIR = [
    PlayingCard(2, Suit.HEARTS, None, None, None),
    PlayingCard(2, Suit.SPADES, None, None, None),
    PlayingCard(5, Suit.DIAMONDS, None, None, None),
    PlayingCard(11, Suit.SPADES, None, None, None),
    PlayingCard(6, Suit.HEARTS, None, None, None),
]
HIGH_CARD = [
    PlayingCard(1, Suit.HEARTS, None, None, None),
    PlayingCard(11, Suit.SPADES, None, None, None),
]


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_hand_type",
    [
        [STRAIGHT_FLUSH, PokerHandType.STRAIGHT_FLUSH],
        [ROYAL_FLUSH, PokerHandType.ROYAL_FLUSH],
        [FLUSH_FIVE, PokerHandType.FLUSH_FIVE],
        [FIVE_SET, PokerHandType.FIVE_SET],
        [STRAIGHT, PokerHandType.STRAIGHT],
        [FLUSH, PokerHandType.FLUSH],
        [FLUSH_HOUSE, PokerHandType.FLUSH_HOUSE],
        [FULL_HOUSE, PokerHandType.FULL_HOUSE],
        [FOUR_SET, PokerHandType.FOUR_SET],
        [THREE_SET, PokerHandType.THREE_SET],
        [TWO_PAIR, PokerHandType.TWO_PAIR],
        [PAIR, PokerHandType.PAIR],
        [HIGH_CARD, PokerHandType.HIGH_CARD],
    ],
)
def test_hand_types(hand: Sequence[PlayingCard], expected_hand_type: PokerHandType) -> None:
    _, hand_type = get_poker_hand(hand, _make_board())
    assert hand_type == expected_hand_type

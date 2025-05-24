from collections.abc import Sequence
from typing import Optional
from unittest.mock import Mock

import pytest

from balatro_gym.cards.interfaces import Edition, Enhancement, PlayingCard, Rank, Seal, Suit
from balatro_gym.cards.joker import Joker
from balatro_gym.cards.utils import get_flush, get_straight, is_consecutive, is_royal


def _make_card(
    rank: Rank = Rank.ACE,
    suit: Suit = Suit.HEARTS,
    enhancement: Optional[Enhancement] = None,
    edition: Optional[Edition] = None,
    seal: Optional[Seal] = None,
) -> PlayingCard:
    return PlayingCard(rank, suit, enhancement, edition, seal)


def _make_board(jokers: Sequence[Joker] = []) -> Mock:
    board = Mock()
    board.jokers = jokers
    return board


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_len",
    [
        [[_make_card(Rank.ACE)], 0],
        [[_make_card(Rank.ACE)] * 2, 0],
        [[_make_card(Rank.ACE)] * 3, 0],
        [[_make_card(Rank.ACE)] * 4, 0],
        [[_make_card(Rank.ACE)] * 5, 5],
        [
            [
                _make_card(Rank.ACE),
                _make_card(Rank.KING),
                _make_card(Rank.QUEEN),
                _make_card(Rank.JACK),
                _make_card(Rank.TEN),
            ],
            5,
        ],
        [[_make_card(Rank.ACE), _make_card(suit=Suit.DIAMONDS)], 0],
        [[_make_card(Rank.ACE), _make_card(suit=Suit.DIAMONDS), _make_card(suit=Suit.DIAMONDS)], 0],
    ],
)
def test_get_flush(hand: Sequence[PlayingCard], expected_len: int) -> None:
    assert len(get_flush(hand, _make_board())) == expected_len


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_len",
    [
        [[_make_card(Rank.ACE)], 1],
        [[_make_card(Rank.ACE)] * 2, 0],
        [[_make_card(Rank.ACE)] * 3, 0],
        [[_make_card(Rank.ACE)] * 4, 0],
        [[_make_card(Rank.ACE)] * 5, 0],
        [
            [
                _make_card(Rank.ACE),
                _make_card(Rank.KING),
                _make_card(Rank.QUEEN),
                _make_card(Rank.JACK),
                _make_card(Rank.TEN),
            ],
            5,
        ],
    ],
)
def test_get_straight(hand: Sequence[PlayingCard], expected_len: int) -> None:
    assert len(get_straight(hand, _make_board())) == expected_len


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected",
    [
        [[_make_card(Rank.ACE)], True],
        [[_make_card(Rank.ACE)] * 2, False],
        [[_make_card(Rank.ACE)] * 3, False],
        [[_make_card(Rank.ACE)] * 4, False],
        [[_make_card(Rank.ACE)] * 5, False],
        [
            [
                _make_card(Rank.NINE),
                _make_card(Rank.KING),
                _make_card(Rank.QUEEN),
                _make_card(Rank.JACK),
                _make_card(Rank.TEN),
            ],
            True,
        ],
        [
            [
                _make_card(Rank.ACE),
                _make_card(Rank.KING),
                _make_card(Rank.QUEEN),
                _make_card(Rank.JACK),
                _make_card(Rank.TEN),
            ],
            False,
        ],
    ],
)
def test_get_is_consecutive(hand: Sequence[PlayingCard], expected: bool) -> None:
    sorted_ranks = sorted([card.rank.value.order for card in hand])
    assert is_consecutive(sorted_ranks) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected",
    [
        [[_make_card(Rank.ACE)], False],
        [[_make_card(Rank.ACE)] * 2, False],
        [[_make_card(Rank.ACE)] * 3, False],
        [[_make_card(Rank.ACE)] * 4, False],
        [[_make_card(Rank.ACE)] * 5, False],
        [
            [
                _make_card(Rank.NINE),
                _make_card(Rank.KING),
                _make_card(Rank.QUEEN),
                _make_card(Rank.JACK),
                _make_card(Rank.TEN),
            ],
            False,
        ],
        [
            [
                _make_card(Rank.ACE),
                _make_card(Rank.KING),
                _make_card(Rank.QUEEN),
                _make_card(Rank.JACK),
                _make_card(Rank.TEN),
            ],
            True,
        ],
    ],
)
def test_is_royal(hand: Sequence[PlayingCard], expected: bool) -> None:
    assert is_royal(hand, _make_board()) == expected

from collections.abc import Sequence
from typing import Optional
from unittest.mock import Mock

import pytest

from balatro_gym.cards.interfaces import Edition, Enhancement, PlayingCard, Rank, Seal, Suit
from balatro_gym.cards.joker import (
    CrazyJoker,
    GluttonousJoker,
    GreedyJoker,
    Joker,
    JollyJoker,
    LustyJoker,
    MadJoker,
    WrathfulJoker,
    ZanyJoker,
)
from balatro_gym.interfaces import JokerBase, PokerHandType, Type


def _make_card(
    rank: Rank = Rank.ACE,
    suit: Suit = Suit.HEARTS,
    enhancement: Optional[Enhancement] = None,
    edition: Optional[Edition] = None,
    seal: Optional[Seal] = None,
) -> PlayingCard:
    return PlayingCard(rank, suit, enhancement, edition, seal)


@pytest.mark.unit
def test_base_joker() -> None:
    # The base joker should return noop values as appropriate. E.g. 0 for additive, and 1 for multiplicative effects
    j = JokerBase()
    assert j.base_cost == 1
    assert j.get_money(Mock()) == 0
    assert j.get_mult_card(Mock(), Mock()) == 0
    assert j.get_chips_hand(Mock(), Mock()) == 0
    assert j.get_multiplication(Mock(), Mock(), Mock()) == 1.0
    assert j.get_chips_card(Mock(), Mock()) == 0
    assert j.get_chips_hand(Mock(), Mock()) == 0


@pytest.mark.unit
def test_joker() -> None:
    j = Joker()
    assert j.joker_type == Type.ADDITIVE_MULT
    assert j.get_mult(Mock(), Mock(), Mock()) == 4


@pytest.mark.unit
@pytest.mark.parametrize("num_suit", list(range(0, 5)))
def test_greedy_joker(num_suit: int) -> None:
    j = GreedyJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    scored_cards = [_make_card(suit=Suit.DIAMONDS)] * num_suit
    assert j.get_mult(scored_cards, Mock(), Mock()) == 3 * num_suit


@pytest.mark.unit
@pytest.mark.parametrize("num_suit", list(range(0, 5)))
def test_lusty_joker(num_suit: int) -> None:
    j = LustyJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    scored_cards = [_make_card(suit=Suit.HEARTS)] * num_suit
    assert j.get_mult(scored_cards, Mock(), Mock()) == 3 * num_suit


@pytest.mark.unit
@pytest.mark.parametrize("num_suit", list(range(0, 5)))
def test_wrathful_joker(num_suit: int) -> None:
    j = WrathfulJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    scored_cards = [_make_card(suit=Suit.CLUBS)] * num_suit
    assert j.get_mult(scored_cards, Mock(), Mock()) == 3 * num_suit


@pytest.mark.unit
@pytest.mark.parametrize("num_suit", list(range(0, 5)))
def test_gluttonous_joker(num_suit: int) -> None:
    j = GluttonousJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    scored_cards = [_make_card(suit=Suit.SPADES)] * num_suit
    assert j.get_mult(scored_cards, Mock(), Mock()) == 3 * num_suit


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_score",
    [
        [[_make_card()], 0],
        [[_make_card()] * 2, 8],  # Pair
        [[_make_card()] * 3, 8],  # Three Set
        [[_make_card()] * 4, 8],  # Four Set
        [[_make_card()] * 5, 8],  # Flush Five Set
        [
            [
                _make_card(),
                _make_card(),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
            ],
            8,  # Full House
        ],
        [
            [
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS, rank=Rank.EIGHT),
            ],
            8,
        ],  # Flush
    ],
)
def test_jolly_joker(hand: Sequence[PlayingCard], expected_score: int) -> None:
    j = JollyJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    blind = Mock()
    blind.hand = hand
    assert j.get_mult(Mock(), blind, Mock()) == expected_score


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_score",
    [
        [[_make_card()], 0],
        [[_make_card()] * 2, 0],  # Pair
        [[_make_card()] * 3, 12],  # Three Set
        [[_make_card()] * 4, 12],  # Four Set
        [[_make_card()] * 5, 12],  # Flush Five Set
        [
            [
                _make_card(),
                _make_card(),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
            ],
            12,  # Full House
        ],
        [
            [
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS, rank=Rank.EIGHT),
            ],
            12,
        ],  # Flush
    ],
)
def test_zany_joker(hand: Sequence[PlayingCard], expected_score: int) -> None:
    j = ZanyJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    blind = Mock()
    blind.hand = hand
    assert j.get_mult(Mock(), blind, Mock()) == expected_score


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_score",
    [
        [[_make_card()], 0],
        [[_make_card()] * 2, 0],  # Pair
        [[_make_card()] * 4, 0],  # Four Set
        [[_make_card()] * 5, 0],  # Flush Five Set
        [
            [
                _make_card(),
                _make_card(),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
            ],
            10,  # Full House
        ],
        [
            [
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS, rank=Rank.EIGHT),
            ],
            0,
        ],  # Flush, but with the same ranks
        [
            [
                _make_card(rank=Rank.ACE),
                _make_card(rank=Rank.ACE),
                _make_card(rank=Rank.TEN),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
            ],
            10,
        ],  # Flush, but with different ranks
    ],
)
def test_mad_joker(hand: Sequence[PlayingCard], expected_score: int) -> None:
    j = MadJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    blind = Mock()
    blind.hand = hand
    assert j.get_mult(Mock(), blind, Mock()) == expected_score


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand_type,expected_score",
    [
        [PokerHandType.HIGH_CARD, 0],
        [PokerHandType.PAIR, 0],
        [PokerHandType.TWO_PAIR, 0],
        [PokerHandType.THREE_SET, 0],
        [PokerHandType.FULL_HOUSE, 0],
        [PokerHandType.FLUSH_HOUSE, 0],
        [PokerHandType.FOUR_SET, 0],
        [PokerHandType.FIVE_SET, 0],
        [PokerHandType.FLUSH, 0],
        [PokerHandType.ROYAL_FLUSH, 12],
        [PokerHandType.STRAIGHT, 12],
        [PokerHandType.STRAIGHT_FLUSH, 12],
        [PokerHandType.FLUSH_FIVE, 0],
    ],
)
def test_crazy_joker(hand_type: PokerHandType, expected_score: int) -> None:
    j = CrazyJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    assert j.get_mult(Mock(), Mock(), hand_type) == expected_score

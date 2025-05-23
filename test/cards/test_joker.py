from collections.abc import Sequence
from typing import Optional
from unittest.mock import Mock

import pytest

from balatro_gym.cards.interfaces import Edition, Enhancement, PlayingCard, Rank, Seal, Suit
from balatro_gym.cards.joker import (
    CrazyJoker,
    DrollJoker,
    GluttonousJoker,
    GreedyJoker,
    Joker,
    JollyJoker,
    LustyJoker,
    MadJoker,
    SlyJoker,
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
    assert j.base_cost == 0
    assert j.get_money(Mock()) == 0
    assert j.get_mult_card(Mock(), Mock()) == 0
    assert j.get_chips_hand(Mock(), Mock(), Mock()) == 0
    assert j.get_multiplication(Mock(), Mock(), Mock()) == 1.0
    assert j.get_chips_card(Mock(), Mock()) == 0


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
    "hand_type,expected_score",
    [
        [PokerHandType.HIGH_CARD, 0],
        [PokerHandType.PAIR, 8],
        [PokerHandType.TWO_PAIR, 0],
        [PokerHandType.THREE_SET, 0],
        [PokerHandType.FULL_HOUSE, 0],
        [PokerHandType.FLUSH_HOUSE, 0],
        [PokerHandType.FLUSH_FIVE, 0],
        [PokerHandType.FOUR_SET, 0],
        [PokerHandType.FIVE_SET, 0],
        [PokerHandType.FLUSH, 0],
        [PokerHandType.ROYAL_FLUSH, 0],
        [PokerHandType.STRAIGHT, 0],
        [PokerHandType.STRAIGHT_FLUSH, 0],
        [PokerHandType.FLUSH_FIVE, 0],
    ],
)
def test_jolly_joker(hand_type: PokerHandType, expected_score: int) -> None:
    j = JollyJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    assert j.get_mult(Mock(), Mock(), hand_type) == expected_score


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand_type,expected_score",
    [
        [PokerHandType.HIGH_CARD, 0],
        [PokerHandType.PAIR, 0],
        [PokerHandType.TWO_PAIR, 0],
        [PokerHandType.THREE_SET, 12],
        [PokerHandType.FULL_HOUSE, 0],
        [PokerHandType.FLUSH_HOUSE, 0],
        [PokerHandType.FOUR_SET, 0],
        [PokerHandType.FIVE_SET, 0],
        [PokerHandType.FLUSH, 0],
        [PokerHandType.ROYAL_FLUSH, 0],
        [PokerHandType.STRAIGHT, 0],
        [PokerHandType.STRAIGHT_FLUSH, 0],
        [PokerHandType.FLUSH_FIVE, 0],
    ],
)
def test_zany_joker(hand_type: PokerHandType, expected_score: int) -> None:
    j = ZanyJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    assert j.get_mult(Mock(), Mock(), hand_type) == expected_score


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand_type,expected_score",
    [
        [PokerHandType.HIGH_CARD, 0],
        [PokerHandType.PAIR, 0],
        [PokerHandType.TWO_PAIR, 10],
        [PokerHandType.THREE_SET, 0],
        [PokerHandType.FULL_HOUSE, 0],
        [PokerHandType.FLUSH_HOUSE, 0],
        [PokerHandType.FOUR_SET, 0],
        [PokerHandType.FIVE_SET, 0],
        [PokerHandType.FLUSH, 0],
        [PokerHandType.ROYAL_FLUSH, 0],
        [PokerHandType.STRAIGHT, 0],
        [PokerHandType.STRAIGHT_FLUSH, 0],
        [PokerHandType.FLUSH_FIVE, 0],
    ],
)
def test_mad_joker(hand_type: PokerHandType, expected_score: int) -> None:
    j = MadJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    assert j.get_mult(Mock(), Mock(), hand_type) == expected_score


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


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand_type,expected_score",
    [
        [PokerHandType.HIGH_CARD, 0],
        [PokerHandType.PAIR, 0],
        [PokerHandType.TWO_PAIR, 0],
        [PokerHandType.THREE_SET, 0],
        [PokerHandType.FULL_HOUSE, 0],
        [PokerHandType.FLUSH_HOUSE, 10],
        [PokerHandType.FOUR_SET, 0],
        [PokerHandType.FIVE_SET, 0],
        [PokerHandType.FLUSH, 10],
        [PokerHandType.ROYAL_FLUSH, 10],
        [PokerHandType.STRAIGHT, 0],
        [PokerHandType.STRAIGHT_FLUSH, 10],
        [PokerHandType.FLUSH_FIVE, 10],
    ],
)
def test_droll_joker(hand_type: PokerHandType, expected_score: int) -> None:
    j = DrollJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    assert j.get_mult(Mock(), Mock(), hand_type) == expected_score


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_chips",
    [
        [[_make_card(Rank.ACE)], 0],
        [[_make_card(Rank.ACE), _make_card(Rank.ACE)], 50],
        [[_make_card(Rank.ACE)] * 2, 50],
        [[_make_card(Rank.ACE)] * 3, 50],
        [[_make_card(Rank.ACE)] * 4, 50],
    ],
)
def test_sly_joker(hand: Sequence[PlayingCard], expected_chips: int) -> None:
    j = SlyJoker()
    assert j.joker_type == Type.CHIPS
    assert j.get_chips_hand(hand, Mock(), Mock()) == expected_chips

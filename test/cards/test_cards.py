from typing import (
    Optional,
)
from unittest.mock import Mock, patch

import pytest

import balatro_gym.cards.interfaces
from balatro_gym.cards.interfaces import (
    BonusCard,
    Edition,
    Enhancement,
    GlassCard,
    GoldCard,
    LuckyCard,
    MultCard,
    PlayingCard,
    Rank,
    Seal,
    SteelCard,
    StoneCard,
    Suit,
    WildCard,
)
from balatro_gym.game.scoring import get_poker_hand, score_hand
from balatro_gym.interfaces import BoardState


def _make_card(
    rank: Rank = Rank.ACE,
    suit: Suit = Suit.HEARTS,
    enhancement: Optional[Enhancement] = None,
    edition: Optional[Edition] = None,
    seal: Optional[Seal] = None,
) -> PlayingCard:
    return PlayingCard(rank, suit, enhancement, edition, seal)


@pytest.mark.unit
def test_enhancement_bonus() -> None:
    enhancement = BonusCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert card.get_chips() == 50 + card._base_chips


@pytest.mark.unit
def test_enhancement_mult() -> None:
    enhancement = MultCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert card.get_mult() == 4


@pytest.mark.unit
def test_enhancement_wild() -> None:
    enhancement = WildCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert len(set(card.suit)) == len(Suit)


@pytest.mark.unit
def test_enhancement_glass() -> None:
    enhancement = GlassCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert card.get_multiplication() == 2


@pytest.mark.unit
def test_enhancement_glass_scoring() -> None:
    enhancement = GlassCard()
    card = _make_card(enhancement=enhancement)
    board = BoardState()
    board.jokers = []
    blind_mock = Mock()
    blind_mock.hand = []
    submitted_hand = [card]
    score = score_hand(submitted_hand, board, blind_mock)
    _, hand_type = get_poker_hand(submitted_hand)
    expected_score = (hand_type.value.chips + card.get_chips()) * hand_type.value.mult * card.get_multiplication()
    assert score == expected_score


@pytest.mark.unit
def test_enhancement_steel() -> None:
    enhancement = SteelCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert card.get_multiplication() == 1.5


@pytest.mark.unit
def test_enhancement_steel_scoring() -> None:
    # Submit a single card as a hand with a single steel card held in hand
    enhancement = SteelCard()
    held_card = _make_card(enhancement=enhancement)
    submitted_card = _make_card()
    submitted_hand = [submitted_card]
    board = BoardState()
    board.jokers = []
    blind_mock = Mock()
    blind_mock.hand = [held_card]
    score = score_hand(submitted_hand, board, blind_mock)
    _, hand_type = get_poker_hand(submitted_hand)
    expected_score = (
        (hand_type.value.chips + submitted_card.get_chips())
        * hand_type.value.mult
        * submitted_card.get_multiplication()
        * held_card.get_multiplication()
    )
    assert score == expected_score


@pytest.mark.unit
def test_enhancement_stone() -> None:
    enhancement = StoneCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert enhancement.get_chips() == 50
    assert card.get_chips() == 50
    assert len(card.suit) == 0


@pytest.mark.unit
def test_enhancement_stone_scoring() -> None:
    # Submit a single stone card
    enhancement = StoneCard()
    card = _make_card(enhancement=enhancement)
    board = BoardState()
    board.jokers = []
    blind_mock = Mock()
    blind_mock.hand = []
    submitted_hand = [card]
    score = score_hand(submitted_hand, board, blind_mock)
    _, hand_type = get_poker_hand(submitted_hand)
    expected_score = (hand_type.value.chips + card.get_chips()) * hand_type.value.mult * card.get_multiplication()
    assert score == expected_score


@pytest.mark.unit
def test_enhancement_gold() -> None:
    enhancement = GoldCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert card.get_scored_money() == 0
    assert card.get_end_money() == 3


@pytest.mark.unit
def test_enhancement_lucky() -> None:
    enhancement = LuckyCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    with patch.object(balatro_gym.cards.interfaces, "np") as mock:
        random_mock = Mock()
        mock.random.random = random_mock
        # Test degenerate cases
        random_mock.return_value = 1
        assert enhancement.get_mult() == 0
        assert enhancement.get_scored_money() == 0
        random_mock.return_value = 0
        assert enhancement.get_mult() == 20
        assert enhancement.get_scored_money() == 20


@pytest.mark.unit
@pytest.mark.parametrize("probability_modifier", [1, 2, 10])
def test_enhancement_lucky_modifiers(probability_modifier: int) -> None:
    enhancement = LuckyCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    with patch.object(balatro_gym.cards.interfaces, "np") as mock:
        random_mock = Mock()
        mock.random.random = random_mock

        # Verify that the base probabilities are correct
        random_mock.return_value = min(probability_modifier / 5, 1)
        assert enhancement.get_mult(probability_modifier) == 20
        random_mock.return_value = min(probability_modifier / 15, 1)
        assert enhancement.get_scored_money(probability_modifier) == 20

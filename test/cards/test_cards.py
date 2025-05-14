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
    GoldCard,
    LuckyCard,
    MultCard,
    PlayingCard,
    Rank,
    Seal,
    StoneCard,
    Suit,
    WildCard,
)


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
    enhancement = MultCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert card.get_mult() == 4


@pytest.mark.unit
def test_enhancement_steel() -> None:
    pass


@pytest.mark.unit
def test_enhancement_stone() -> None:
    enhancement = StoneCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert enhancement.get_chips() == 50
    assert card.get_chips() == 50  # This is wrong, base chips shouldn't be in the sum
    assert len(card.suit) == 0


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
        # Verify that the base probabilities are correct
        random_mock.return_value = 1 / 5
        assert enhancement.get_mult() == 20
        random_mock.return_value = 1 / 15
        assert enhancement.get_scored_money() == 20


@pytest.mark.unit
def test_enhancement_lucky_modifiers() -> None:
    pass

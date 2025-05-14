from typing import (
    Optional,
)

import pytest

from balatro_gym.cards.interfaces import (
    BonusCard,
    Edition,
    Enhancement,
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
    assert card.get_chips() == 50
    assert len(card.suit) == 0

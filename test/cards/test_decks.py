from collections import Counter

import pytest

from balatro_gym.cards.decks import STANDARD_DECK


@pytest.mark.unit
def test_standard_deck() -> None:
    # Standard deck should be 52 cards, 4 suits of all ranks
    deck = STANDARD_DECK
    assert len(deck) == 52
    # assert uniqueness of each card
    assert len(Counter(deck).most_common()) == 52

import pytest

from balatro_gym.cards.interfaces import (
    BonusCard,
    Enhancement,
    GlassCard,
    LuckyCard,
    MultCard,
    SteelCard,
    WildCard,
)
from balatro_gym.cards.planet import Mercury
from balatro_gym.cards.tarot import Chariot, Empress, Fool, Hierophant, Justice, Lovers, Magician
from balatro_gym.interfaces import BoardState, Tarot
from balatro_gym.testing_utils import make_card


@pytest.mark.unit
def test_fool() -> None:
    tarot = Fool()
    board_state = BoardState()
    # can't apply since no planet or tarot card used
    assert not board_state.use_consumable(tarot, [])
    planet_card = Mercury()
    board_state.consumable.consumables = [planet_card, tarot]
    assert board_state.use_consumable(planet_card, [])
    assert isinstance(board_state.last_used_consumable, Mercury)
    assert len(board_state.consumable.consumables) == 1
    assert isinstance(board_state.consumable.consumables[0], Fool)
    assert board_state.use_consumable(tarot, [])
    assert len(board_state.consumable.consumables) == 1
    assert isinstance(board_state.consumable.consumables[0], Mercury)


@pytest.mark.unit
@pytest.mark.parametrize("tarot,max_selection,enhancement", [
    [Magician(), 2, LuckyCard()],
    [Empress(), 2, MultCard()],
    [Hierophant(), 2, BonusCard()],
    [Lovers(), 1, WildCard()],
    [Chariot(), 1, SteelCard()],
    [Justice(), 1, GlassCard()],
])
def test_enhancement_tarot_cards(tarot: Tarot, max_selection: int, enhancement: Enhancement) -> None:
    cards = [make_card() for _ in range(4)]
    board_state = BoardState()
    assert not tarot.apply([], board_state)
    assert not tarot.apply(cards, board_state)
    assert tarot.apply(cards[:max_selection], board_state)
    assert all([card.enhancement == enhancement for card in cards[:max_selection]])

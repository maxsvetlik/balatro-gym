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
from balatro_gym.cards.tarot import (
    Chariot,
    Emperor,
    Empress,
    Fool,
    Hermit,
    Hierophant,
    HighPriestess,
    Justice,
    Lovers,
    Magician,
)
from balatro_gym.interfaces import BoardState, PlanetCard, Tarot
from test.utils import _make_card


@pytest.mark.unit
def test_fool() -> None:
    tarot = Fool()
    board_state = BoardState()
    # can't apply since no planet or tarot card used
    board_state.acquire_consumable(tarot)
    assert not board_state.use_consumable(tarot, [])
    planet_card = Mercury()
    for consumable in [planet_card]:
        board_state.acquire_consumable(consumable)
    assert board_state.use_consumable(planet_card, [])
    assert isinstance(board_state.last_used_consumable, Mercury)
    assert len(board_state.consumable.consumables) == 1
    # Use fool
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
    cards = [_make_card()] * 4
    board_state = BoardState()
    assert not tarot.apply([], board_state)
    assert not tarot.apply(cards, board_state)
    assert tarot.apply(cards[:max_selection], board_state)
    assert all([card.enhancement == enhancement for card in cards[:max_selection]])


@pytest.mark.unit
def test_high_priestess() -> None:
    tarot = HighPriestess()
    board_state = BoardState()
    board_state.acquire_consumable(tarot)
    board_state.use_consumable(tarot, [])
    assert [isinstance(card, PlanetCard) for card in board_state.consumable.consumables]
    # Can't use high priestess since there are not slots free
    assert not tarot.apply([], board_state)


@pytest.mark.unit
def test_emperor() -> None:
    tarot = Emperor()
    board_state = BoardState()
    board_state.acquire_consumable(tarot)
    board_state.use_consumable(tarot, [])
    assert [isinstance(card, Tarot) for card in board_state.consumable.consumables]
    assert not tarot.apply([], board_state)


@pytest.mark.unit
def test_hermit() -> None:
    tarot = Hermit()
    board_state = BoardState()
    initial_money = 20
    board_state.set_money(initial_money)
    board_state.use_consumable(tarot, [])
    assert board_state.money == initial_money * 2
    max_money_added = 20
    board_state.use_consumable(tarot, [])
    assert board_state.money == initial_money * 2 + max_money_added

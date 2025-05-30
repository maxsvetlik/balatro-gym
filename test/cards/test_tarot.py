import pytest

from balatro_gym.cards.interfaces import (
    BaseEdition,
    BonusCard,
    Enhancement,
    Foil,
    GlassCard,
    GoldCard,
    Holographic,
    LuckyCard,
    MultCard,
    Polychrome,
    Rank,
    SteelCard,
    StoneCard,
    Suit,
    WildCard,
)
from balatro_gym.cards.joker.effect_joker import OopsAll6s
from balatro_gym.cards.joker.joker import Joker, TheDuo
from balatro_gym.cards.planet import Mercury
from balatro_gym.cards.tarot import (
    Chariot,
    Death,
    Devil,
    Emperor,
    Empress,
    Fool,
    HangedMan,
    Hermit,
    Hierophant,
    HighPriestess,
    Judgement,
    Justice,
    Lovers,
    Magician,
    Moon,
    Star,
    Strength,
    Sun,
    Temperance,
    Tower,
    WheelOfFortune,
    World,
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
    [Devil(), 1, GoldCard()],
    [Tower(), 1, StoneCard()]
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


@pytest.mark.unit
def test_wheel_of_fortune() -> None:
    tarot = WheelOfFortune()
    board_state = BoardState()
    # No jokers so can't use the cared
    assert not board_state.use_consumable(tarot, [])
    joker = Joker()
    board_state.acquire_joker(joker)
    while isinstance(joker.edition, BaseEdition):
        board_state.use_consumable(tarot, [])
    assert (
        isinstance(joker.edition, Foil) or
        isinstance(joker.edition, Holographic) or
        isinstance(joker.edition, Polychrome)
    )

    # Two oops guarantees an edition with a WheelOfFortune
    board_state.jokers = [OopsAll6s(), OopsAll6s()]
    assert (isinstance(board_state.jokers[0].edition, BaseEdition) or
            isinstance(board_state.jokers[1].edition, BaseEdition))
    board_state.use_consumable(tarot, [])
    assert (
        isinstance(board_state.jokers[0].edition, Foil) or
        isinstance(board_state.jokers[0].edition, Holographic) or
        isinstance(board_state.jokers[0].edition, Polychrome) or
        isinstance(board_state.jokers[1].edition, Foil) or
        isinstance(board_state.jokers[1].edition, Holographic) or
        isinstance(board_state.jokers[1].edition, Polychrome)
    )


@pytest.mark.unit
@pytest.mark.parametrize("rank,new_rank", [
    [Rank.ACE, Rank.TWO],
    [Rank.TWO, Rank.THREE],
    [Rank.THREE, Rank.FOUR],
    [Rank.FOUR, Rank.FIVE],
    [Rank.FIVE, Rank.SIX],
    [Rank.SIX, Rank.SEVEN],
    [Rank.SEVEN, Rank.EIGHT],
    [Rank.EIGHT, Rank.NINE],
    [Rank.NINE, Rank.TEN],
    [Rank.TEN, Rank.JACK],
    [Rank.JACK, Rank.QUEEN],
    [Rank.QUEEN, Rank.KING],
    [Rank.KING, Rank.ACE],
])
def test_strength(rank: Rank, new_rank: Rank) -> None:
    tarot = Strength()
    board_state = BoardState()
    cards = [_make_card(rank=rank)]
    assert not board_state.use_consumable(tarot, [])
    assert board_state.use_consumable(tarot, cards)
    assert cards[0].rank == new_rank


@pytest.mark.unit
def test_hanged_man() -> None:
    tarot = HangedMan()
    board_state = BoardState()
    assert len(board_state.deck.cards_remaining) == 52
    num_cards_deleted = 2
    cards = board_state.deck.deal(num_cards_deleted)
    assert all([card in board_state.deck.cards_played for card in cards])
    board_state.use_consumable(tarot, cards)
    assert len(board_state.deck.cards_remaining) + len(board_state.deck.cards_played) == 52 - num_cards_deleted
    for card in cards:
        assert card not in board_state.deck.cards_played


@pytest.mark.unit
def test_death() -> None:
    tarot = Death()
    board_state = BoardState()
    assert len(board_state.deck.cards_remaining) == 52
    board_state.deck.shuffle()
    cards = board_state.deck.deal(2)
    card_to_duplicate = cards[1]
    base_suit = card_to_duplicate.base_suit
    rank = card_to_duplicate.rank
    assert all([card in board_state.deck.cards_played for card in cards])
    board_state.use_consumable(tarot, cards)
    assert len(board_state.deck.cards_remaining) + len(board_state.deck.cards_played) == 52
    assert cards[0].base_suit == cards[1].base_suit == base_suit
    assert cards[0].rank == cards[1].rank == rank
    assert board_state.deck.cards_played[0] == cards[0]
    assert board_state.deck.cards_played[1] == cards[1]


@pytest.mark.unit
def test_temperance() -> None:
    tarot = Temperance()
    board_state = BoardState()
    initial_money = 0
    board_state.set_money(initial_money)
    board_state.use_consumable(tarot, [])
    assert board_state.money == 0
    joker = Joker()
    for _ in range(2):
        board_state.acquire_joker(Joker())
    board_state.use_consumable(tarot, [])
    assert board_state.money == joker.sell_value(board_state.vouchers) * len(board_state.jokers)

    board_state.set_money(initial_money)
    # Sell value > 50
    board_state.jokers = [TheDuo()] * 15
    board_state.use_consumable(tarot, [])
    assert board_state.money == 50


@pytest.mark.unit
@pytest.mark.parametrize("tarot,target_suit", [
    [Star(), Suit.DIAMONDS],
    [Moon(), Suit.CLUBS],
    [Sun(), Suit.HEARTS],
    [World(), Suit.SPADES],
])
def test_suit_cards(tarot: Tarot, target_suit: Suit) -> None:
    cards = [_make_card(suit=suit) for suit in Suit]
    board_state = BoardState()
    assert not tarot.apply([], board_state)
    assert not tarot.apply(cards, board_state)
    assert tarot.apply(cards[:3], board_state)
    assert all([card.base_suit == target_suit for card in cards[:3]])


@pytest.mark.unit
def test_judgement() -> None:
    tarot = Judgement()
    board_state = BoardState()
    assert len(board_state.jokers) == 0
    for i in range(board_state.num_joker_slots):
        assert board_state.use_consumable(tarot, [])
        assert len(board_state.jokers) == i + 1
    assert not board_state.use_consumable(tarot, [])

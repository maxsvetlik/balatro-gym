from __future__ import annotations

import dataclasses
from collections.abc import Sequence
from enum import Enum, auto
from typing import Any, Optional, Protocol, Union, runtime_checkable

from .cards.decks import STANDARD_DECK
from .cards.interfaces import Deck, HasCost, PlayingCard
from .constants import DEFAULT_NUM_CONSUMABLE, DEFAULT_START_MONEY
from .game.blinds import BlindInfo
from .mixins import HasReset

__all__ = [
    "Tag",
    "Voucher",
    "Spectral",
    "Tarot",
    "Rarity",
    "Activation",
    "Type",
    "PokerScale",
    "PokerHandType",
    "JokerBase",
    "PlanetCard",
]


class Tag:
    pass


@dataclasses.dataclass(frozen=True)
class Voucher:
    dependency: Optional["Voucher"]

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __eq__(self, obj: Any) -> bool:
        return obj._class__.__name__ == self.__class__.__name__


class Spectral(HasCost):
    pass


class BoosterPack:
    pass


@runtime_checkable
class Booster(Protocol):
    cost: int
    n_cards: int
    n_choice: int

    def sample(self) -> Sequence[HasCost]:
        raise NotImplementedError


class Rarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    LEGENDARY = "legendary"


class Activation(Enum):
    ON_SCORED = "scored"
    INDEPENDENT = "indep"
    ON_HELD = "held"


class Type(Enum):
    CHIPS = auto()
    ADDITIVE_MULT = auto()
    MULTIPLICATIVE = auto()
    EFFECT = auto()
    RETRIGGER = auto()
    ECONOMY = auto()


@dataclasses.dataclass(frozen=True)
class PokerScale:
    mult: int
    chips: int
    delta_mult: int
    delta_chips: int


class PokerHandType(Enum):
    HIGH_CARD = PokerScale(1, 5, 1, 10)
    PAIR = PokerScale(2, 10, 1, 15)
    TWO_PAIR = PokerScale(2, 20, 1, 20)
    THREE_SET = PokerScale(3, 30, 2, 20)
    FULL_HOUSE = PokerScale(4, 40, 2, 25)
    FLUSH_HOUSE = PokerScale(14, 140, 4, 40)
    FOUR_SET = PokerScale(7, 60, 3, 30)
    FIVE_SET = PokerScale(12, 120, 3, 35)
    FLUSH = PokerScale(4, 35, 2, 15)
    ROYAL_FLUSH = PokerScale(8, 100, 4, 40)
    STRAIGHT = PokerScale(4, 30, 3, 30)
    STRAIGHT_FLUSH = PokerScale(8, 100, 4, 40)
    FLUSH_FIVE = PokerScale(16, 160, 3, 50)


@dataclasses.dataclass
class PokerHand:
    hand_type: PokerHandType
    level: int
    num_played: int

    @property
    def score(self) -> PokerScale:
        return PokerScale(
            self.hand_type.value.mult + self.hand_type.value.delta_mult * (self.level - 1),
            self.hand_type.value.chips + self.hand_type.value.delta_chips * (self.level - 1),
            self.hand_type.value.delta_mult,
            self.hand_type.value.delta_chips,
        )


class PlanetCard(HasCost):
    @property
    def _hand_type(self) -> PokerHandType:
        raise NotImplementedError

    def increase_level(self, poker_hands: Sequence[PokerHand]) -> PokerHand:
        for hand in poker_hands:
            if hand.hand_type == self._hand_type:
                hand.level += 1
                return hand

        raise RuntimeError("Hand not found, could not change hand level. This should not happen.")

    def decrease_level(self, poker_hands: Sequence[PokerHand]) -> PokerHand:
        for hand in poker_hands:
            if hand.hand_type == self._hand_type:
                if hand.level > 1:
                    hand.level -= 1
                return hand

        raise RuntimeError("Hand not found, could not change hand level. This should not happen.")


class Tarot(HasCost):
    def apply(self, selected_cards: Sequence[PlayingCard], board_state: BoardState) -> bool:
        """Returns true if the card was used successfully"""
        raise NotImplementedError


ConsumableCardBase = Union[PlanetCard, Tarot]


@dataclasses.dataclass
class BlindState:
    hand: Sequence[PlayingCard]
    required_score: int
    current_score: int
    num_hands_remaining: int
    num_discards_remaining: int
    reward: int


class ConsumableState(HasReset):
    num_slots: int
    consumables: list[ConsumableCardBase]

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.num_slots = DEFAULT_NUM_CONSUMABLE
        self.consumables = []

    def __eq__(self, obj: Any) -> bool:
        if isinstance(obj, ConsumableState):
            return self.consumables == obj.consumables and self.num_slots == obj.num_slots
        return False


class JokerBase(HasCost):

    _base_cost: int = 0

    @property
    def joker_type(self) -> Type:
        raise NotImplementedError

    @property
    def base_cost(self) -> int:
        return self._base_cost

    def cost(self, vouchers: Sequence[Voucher]) -> int:
        # TODO. Voucher impl doesn't exist yet, which may impact this.
        return self._base_cost

    @property
    def rarity(self) -> Rarity:
        raise NotImplementedError

    def get_money(self, state: BlindState) -> int:
        return 0

    def get_mult_card(self, card: PlayingCard, state: BlindState) -> int:
        return 0

    def get_mult_hand(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        return 0

    def get_multiplication(
        self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType
    ) -> float:
        return 1.0

    def get_chips_card(self, card: PlayingCard, state: BlindState) -> int:
        return 0

    def get_chips_hand(self, state: BlindState, scored_hand: PokerHandType) -> int:
        return 0


@dataclasses.dataclass
class BoardState(HasReset):
    consumable: ConsumableState
    deck: Deck
    money: int
    jokers: Sequence[JokerBase]
    ante_num: int
    round_num: int
    num_hands: int
    num_discards: int
    hand_size: int
    vouchers: Sequence[Voucher]
    poker_hands: dict[str, PokerHand]
    completed_blinds: Sequence[BlindInfo]
    """Shows all blinds that have been completed, ordered."""
    round_blinds: Sequence[BlindInfo]
    """Contains the three blinds for the round."""
    last_used_consumable: Optional[ConsumableCardBase]
    """Last tarot or planet card used."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.consumable = ConsumableState()
        self.deck = Deck(STANDARD_DECK)
        self.money = DEFAULT_START_MONEY
        self.jokers = []
        self.ante_num = 0
        self.round_num = 0
        self.num_hands = 4
        self.num_discards = 3
        self.hand_size = 8
        self.vouchers = []
        self.poker_hands = {poker_hand_type.name: PokerHand(poker_hand_type, 1, 0) for poker_hand_type in PokerHandType}
        self.completed_blinds = []
        self.round_blinds = []
        self.last_used_consumable = None

    def get_poker_hand(self, poker_hand_type: PokerHandType) -> PokerHand:
        return self.poker_hands[poker_hand_type.name]

    def use_consumable(self, card: ConsumableCardBase, selected_cards: Sequence[PlayingCard]) -> bool:
        assert isinstance(card, PlanetCard) or isinstance(card, Tarot)
        if isinstance(card, Tarot) and card.apply(selected_cards, self):
            self.last_used_consumable = card
            self.remove_consumable(card)
            return True
        elif isinstance(card, PlanetCard):
            card.increase_level(list(self.poker_hands.values()))
            self.remove_consumable(card)
            return True
        return False

    def remove_consumable(self, card: ConsumableCardBase) -> None:
        # Needed to consume or sell a consumable
        assert card in self.consumable.consumables
        self.consumable.consumables.remove(card)

    def acquire_consumable(self, card: ConsumableCardBase) -> None:
        # Needed to buy or acquire a consumable
        assert self.consumable.num_slots > len(self.consumable.consumables)
        self.consumable.consumables.append(card)

    def set_money(self, amount: int) -> None:
        self.money = amount

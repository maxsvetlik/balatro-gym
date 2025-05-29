from __future__ import annotations

import dataclasses
from collections.abc import Sequence
from enum import Enum, auto
from typing import Any, Optional, Protocol, Union, runtime_checkable

from .cards.decks import STANDARD_DECK
from .cards.interfaces import BaseEdition, Deck, Edition, Foil, HasCost, Holographic, Negative, PlayingCard, Polychrome
from .cards.voucher import Voucher
from .constants import DEFAULT_NUM_CONSUMABLE, DEFAULT_NUM_JOKER_SLOTS, DEFAULT_START_MONEY
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
    "BoardState",
]


class Tag:
    pass


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
    def is_valid(self, selected_cards: Sequence[PlayingCard], board_state: BoardState) -> bool:
        """Check if the consumable can be applied"""
        raise NotImplementedError

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
    _edition: Edition = BaseEdition()

    @property
    def joker_type(self) -> Type:
        raise NotImplementedError

    @property
    def base_cost(self) -> int:
        edition_cost = 0
        if isinstance(self.edition, Foil):
            edition_cost = 2
        elif isinstance(self.edition, Holographic):
            edition_cost = 3
        elif isinstance(self.edition, Polychrome) or isinstance(self.edition, Negative):
            edition_cost = 5
        return self._cost + edition_cost

    @property
    def edition(self) -> Edition:
        return self._edition

    @property
    def rarity(self) -> Rarity:
        raise NotImplementedError

    def set_edition(self, edition: Edition) -> None:
        self._edition = edition

    def get_money(self, state: BlindState) -> int:
        """The money earned by the player from selling this Joker."""
        return 0

    def get_mult_card(self, card: PlayingCard, blind: BlindState, board: "BoardState") -> int:
        """Get any additional mult value of a given card based on the Joker's effects.
        Note that mult is intended to be additive, so in the base case, return 0."""
        return 0

    def get_mult_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: "BoardState", scored_hand: PokerHandType
    ) -> int:
        """Get any additional mult value of a given hand based on the Joker's effects.
        Note that mult is intended to be additive, so in the base case, return 0."""

        return 0

    def get_multiplication(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: "BoardState", scored_hand: PokerHandType
    ) -> float:
        """Get any additional multiplication value of a given hand based on the Joker's effects.
        Note that multiplication is intended to be multiplicative, so in the base case, return 1."""

        return 1.0

    def get_chips_card(self, card: PlayingCard, blind: BlindState, board: "BoardState") -> int:
        """Get any additional chips value of a given card based on the Joker's effects.
        Note that chips are intended to be additive, so in the base case, return 0."""
        return 0

    def get_chips_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: "BoardState", scored_hand: PokerHandType
    ) -> int:
        """Get any additional chip value of a given hand based on the Joker's effects.
        Note that chips are intended to be additive, so in the base case, return 0."""
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
    num_joker_slots: int
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
        self.num_joker_slots = DEFAULT_NUM_JOKER_SLOTS
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
            # If the object is in the consumables list, we're using a consumable from the board and we need to remove it
            if card in self.consumable.consumables:
                self.remove_consumable(card)
            return True
        elif isinstance(card, PlanetCard):
            self.last_used_consumable = card
            card.increase_level(list(self.poker_hands.values()))
            # If the object is in the consumables list, we're using a consumable from the board and we need to remove it
            if card in self.consumable.consumables:
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

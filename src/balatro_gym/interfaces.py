import dataclasses
from collections.abc import Sequence
from enum import Enum, auto
from typing import Any, Optional

from .cards.decks import STANDARD_DECK
from .cards.interfaces import Card, Deck, PlayingCard
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
]


class Tag:
    pass


@dataclasses.dataclass
class Voucher:
    dependency: Optional["Voucher"]


class Spectral(Card):
    pass


class Tarot(Card):
    pass


class BoosterPack:
    pass


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


class PokerHandType(Enum):
    HIGH_CARD = PokerScale(1, 5)
    PAIR = PokerScale(2, 10)
    TWO_PAIR = PokerScale(2, 20)
    THREE_SET = PokerScale(3, 30)
    FULL_HOUSE = PokerScale(4, 40)
    FLUSH_HOUSE = PokerScale(14, 140)
    FOUR_SET = PokerScale(7, 60)
    FIVE_SET = PokerScale(12, 120)
    FLUSH = PokerScale(4, 35)
    ROYAL_FLUSH = PokerScale(8, 100)
    STRAIGHT = PokerScale(4, 30)
    STRAIGHT_FLUSH = PokerScale(8, 100)
    FLUSH_FIVE = PokerScale(16, 160)


class ConsumableCardBase: ...


@dataclasses.dataclass
class PokerHand:
    hand_type: PokerHandType
    level: int
    num_played: int

    @property
    def base_score(self) -> PokerScale:
        return PokerScale(
            self.hand_type.value.mult * self.level,
            self.hand_type.value.chips * self.level,
        )


class PlanetCard(Card):
    _hand_type: PokerHandType

    def increase_level(self, poker_hands: Sequence[PokerHand]) -> PokerHand:
        for hand in poker_hands:
            if hand.hand_type == self._hand_type:
                hand.level += 1
                return hand

        raise RuntimeError("Hand not found, could not change hand level. This should not happen.")

    def decrease_level(self, poker_hands: Sequence[PokerHand]) -> PokerHand:
        for hand in poker_hands:
            if hand.hand_type == self._hand_type:
                hand.level -= 1
                return hand

        raise RuntimeError("Hand not found, could not change hand level. This should not happen.")


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
    consumables: Sequence[ConsumableCardBase]

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.num_slots = DEFAULT_NUM_CONSUMABLE
        self.consumables = []

    def __eq__(self, obj: Any) -> bool:
        if isinstance(obj, ConsumableState):
            return self.consumables == obj.consumables and self.num_slots == obj.num_slots
        return False


class JokerBase(Card):

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
    poker_hands: Sequence[PokerHand]
    completed_blinds: Sequence[BlindInfo]
    """Shows all blinds that have been completed, ordered."""
    round_blinds: Sequence[BlindInfo]
    """Contains the three blinds for the round."""

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
        self.poker_hands = []
        self.completed_blinds = []
        self.round_blinds = []

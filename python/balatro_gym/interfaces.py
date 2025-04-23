from collections.abc import Sequence
from enum import Enum, auto
import dataclasses

from .mixins import HasReset
from .constants import DEFAULT_NUM_CONSUMMABLE, DEFAULT_START_MONEY
from .cards.interfaces import PlayingCard, Deck
from .cards.decks import STANDARD_DECK
from .game.blinds import BlindInfo

__all__ = [
    "Tag",
    "Voucher",
    "Spectral",
    "Tarot",
    "Shop",
    "Rarity",
    "Activation",
    "Type",
    "PokerScale",
    "PokerHandType",
    "JokerBase",
]


class Tag:
    pass


class Voucher:
    pass


class Spectral:
    pass


class Tarot:
    pass


class Shop:
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
    HIGH_CARD = PokerScale(1, 10)
    PAIR = PokerScale(1, 15)
    THREE_SET = PokerScale(2, 20)
    FULL_HOUSE = PokerScale(4, 40)
    FLUSH_HOUSE = PokerScale(3, 50)
    FOUR_SET = PokerScale(3, 30)
    FIVE_SET = PokerScale(3, 35)
    ROYAL_FIVE_SET = PokerScale(3, 50)
    FLUSH = PokerScale(2, 15)
    ROYAL_FLUSH = PokerScale(2, 15)
    STRAIGHT = PokerScale(3, 30)
    STRAIGHT_FLUSH = PokerScale(4, 40)


class ConsummableCardBase: ...


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


class PlanetCard:
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
    round_score: int
    num_hands_remaining: int
    num_discareds_reamining: int


class ConsummableState(HasReset):
    num_slots: int
    consummables: Sequence[ConsummableCardBase]

    def reset(self) -> None:
        self.num_slots = DEFAULT_NUM_CONSUMMABLE
        self.consummables = []


class JokerBase:

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

    def get_mult(self, state: BlindState, scored_hand: PokerHandType) -> int:
        return 0

    def get_x(self, state: BlindState) -> float:
        return 1.0

    def get_chips(self, state: BlindState) -> int:
        return 0


@dataclasses.dataclass
class BoardState(HasReset):
    consummable: ConsummableState
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

    def reset(self) -> None:
        self.consummable.reset()
        self.deck = Deck(STANDARD_DECK)
        self.money = DEFAULT_START_MONEY
        self.jokers = []
        self.ante_num = 1
        self.round_num = 1
        self.num_hands = 4
        self.num_discards = 3
        self.hand_size = 8
        self.vouchers = []
        self.poker_hands = []

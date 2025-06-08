import copy
import random
from collections import deque
from collections.abc import Sequence
from enum import Enum, auto
from typing import Any, Protocol, Union, runtime_checkable

import numpy as np

from ..mixins import (
    HasChips,
    HasCreatePlanet,
    HasCreateTarot,
    HasIsDestroyed,
    HasMoney,
    HasMult,
    HasMultiplier,
    HasReset,
    HasRetrigger,
)
from .voucher import ClearanceSale, Liquidation, Voucher

__all__ = ["HasCost", "Edition", "Foil", "Holographic", "Polychrome", "Negative"]


class Suit(Enum):
    SPADES = auto()
    CLUBS = auto()
    DIAMONDS = auto()
    HEARTS = auto()


class RankVal:
    """An annoying workaround to allow using an Enum since aenum doesn't have good typing support."""

    _val: int
    _order: int

    def __init__(self, val: int, order: int) -> None:
        self._val = val
        self._order = order

    @property
    def value(self) -> int:
        return self._val

    @property
    def order(self) -> int:
        return self._order


class Rank(Enum):
    ACE = RankVal(11, 1)
    KING = RankVal(10, 13)
    QUEEN = RankVal(10, 12)
    JACK = RankVal(10, 11)
    TEN = RankVal(10, 10)
    NINE = RankVal(9, 9)
    EIGHT = RankVal(8, 8)
    SEVEN = RankVal(7, 7)
    SIX = RankVal(6, 6)
    FIVE = RankVal(5, 5)
    FOUR = RankVal(4, 4)
    THREE = RankVal(3, 3)
    TWO = RankVal(2, 2)

    @staticmethod
    def from_int(int_rank: int) -> "Rank":
        int_to_rank_map = {
            1: Rank.ACE,
            2: Rank.TWO,
            3: Rank.THREE,
            4: Rank.FOUR,
            5: Rank.FIVE,
            6: Rank.SIX,
            7: Rank.SEVEN,
            8: Rank.EIGHT,
            9: Rank.NINE,
            10: Rank.TEN,
            11: Rank.JACK,
            12: Rank.QUEEN,
            13: Rank.KING,
        }
        return int_to_rank_map[int_rank]

    def __deepcopy__(self, memo: Any) -> "Rank":
        # Return the same enum instance—skip deepcopy
        return self


# Editions
class Edition(HasChips, HasMult, HasMultiplier, Protocol):
    def is_negative(self) -> bool:
        return False


class BaseEdition(Edition):
    def __hash__(self) -> int:
        return hash(None)

    def __eq__(self, obj: Any) -> bool:
        if isinstance(obj, BaseEdition):
            return True
        return False


class Foil(Edition):
    def get_chips(self) -> int:
        return 50


class Holographic(Edition):
    def get_mult(self, probability_modifier: int = 1) -> int:
        return 10


class Polychrome(Edition):
    def get_multiplication(self) -> float:
        return 1.5


class Negative(Edition):
    def is_negative(self) -> bool:
        return True


# Enhancements
class Enhancement(HasChips, HasMult, HasMultiplier, HasMoney, HasIsDestroyed, Protocol):
    def get_suit(self, card: "PlayingCard") -> Sequence[Suit]:
        return [card.base_suit]

    def __eq__(self, other: Any) -> bool:
        return self.__class__.__name__ == other.__class__.__name__


class BaseEnhancement(Enhancement):
    def __hash__(self) -> int:
        return hash(None)

    def __eq__(self, obj: Any) -> bool:
        if isinstance(obj, BaseEnhancement):
            return True
        return False


class BonusCard(Enhancement):
    def get_chips(self) -> int:
        return 50


class MultCard(Enhancement):
    def get_mult(self, probability_modifier: int = 1) -> int:
        return 4


class WildCard(Enhancement):
    def get_suit(self, card: "PlayingCard") -> Sequence[Suit]:
        return [suit for suit in Suit]


class GlassCard(Enhancement):
    _base_destruction_probability: float = 1 / 4

    def get_multiplication(self) -> float:
        # When scored
        return 2.0

    def is_destroyed(self, probability_modifier: int = 1) -> bool:
        if np.random.random() <= min(self._base_destruction_probability * probability_modifier, 1):
            return True
        return False


class SteelCard(Enhancement):
    def get_multiplication(self) -> float:
        # When card is in hand
        return 1.5


class StoneCard(Enhancement):
    # N.B. StoneCards also always get scored
    def get_chips(self) -> int:
        return 50

    def get_suit(self, card: "PlayingCard") -> Sequence[Suit]:
        return []


class GoldCard(Enhancement):
    def get_end_money(self, probability_modifier: int = 1) -> int:
        return 3


class LuckyCard(Enhancement):
    _base_mult_probability = 1 / 5
    _base_money_probability = 1 / 15

    def get_mult(self, probability_modifier: int = 1) -> int:
        if np.random.random() <= min(self._base_mult_probability * probability_modifier, 1):
            return 20
        return 0

    def get_scored_money(self, probability_modifier: int = 1) -> int:
        if np.random.random() <= min(self._base_money_probability * probability_modifier, 1):
            return 20
        return 0


class Bonus(Enhancement):
    def get_chips(self) -> int:
        return 50


class Seal(HasMoney, HasRetrigger, HasCreatePlanet, HasCreateTarot):
    pass


class BaseSeal(Seal):
    # Added for parity with other "Base" types
    def __hash__(self) -> int:
        return hash(None)

    def __eq__(self, obj: Any) -> bool:
        if isinstance(obj, BaseSeal):
            return True
        return False


class GoldSeal(Seal):
    def get_scored_money(self, probability_modifier: int = 1) -> int:
        return 3


class RedSeal(Seal):
    def retrigger(self) -> bool:
        # TODO When scored
        return True


class BlueSeal(Seal):
    def create_planet(self) -> bool:
        # TODO When scored
        return True


class PurpleSeal(Seal):
    def create_tarot(self) -> bool:
        # TODO When scored
        return True


@runtime_checkable
class HasCost(Protocol):
    _cost: int = 1

    @property
    def base_cost(self) -> int:
        return self._cost

    def cost(self, vouchers: Sequence[Voucher]) -> int:
        cost: float = self.base_cost
        if any([isinstance(voucher, Liquidation) for voucher in vouchers]):
            cost -= cost * 0.5
        elif any([isinstance(voucher, ClearanceSale) for voucher in vouchers]):
            cost -= cost * 0.25
        return max(int(cost), 1)

    def sell_value(self, vouchers: Sequence[Voucher]) -> int:
        sell_value: float = self.base_cost
        if any([isinstance(voucher, Liquidation) for voucher in vouchers]):
            sell_value -= sell_value * 0.5
        elif any([isinstance(voucher, ClearanceSale) for voucher in vouchers]):
            sell_value -= sell_value * 0.25
        return max(int(sell_value * 0.5), 1)


class PlayingCard(HasChips, HasCost):
    _rank: Rank
    _base_suit: Suit
    _enhancement: Enhancement
    _edition: Edition
    _seal: Seal
    _base_chips: int
    _added_chips: int

    def __init__(
        self,
        rank: Union[Rank, int],
        base_suit: Suit,
        enhancement: Enhancement = BaseEnhancement(),
        edition: Edition = BaseEdition(),
        seal: Seal = BaseSeal(),
    ):
        self._rank = rank if isinstance(rank, Rank) else Rank.from_int(rank)
        self._base_suit = base_suit
        self._enhancement = enhancement
        self._edition = edition
        self._seal = seal
        self._base_chips = self._rank.value.value
        self._added_chips = 0

    @property
    def rank(self) -> Rank:
        return self._rank

    def set_rank(self, rank: Rank) -> None:
        self._rank = rank

    @property
    def base_suit(self) -> Suit:
        return self._base_suit

    def set_base_suit(self, suit: Suit) -> None:
        self._base_suit = suit

    @property
    def suit(self) -> Sequence[Suit]:
        if self._enhancement:
            return self._enhancement.get_suit(self)
        return [self._base_suit]

    @property
    def enhancement(self) -> Enhancement:
        return self._enhancement

    @property
    def edition(self) -> Edition:
        return self._edition

    @property
    def seal(self) -> Seal:
        return self._seal

    @property
    def added_chips(self) -> int:
        return self._added_chips

    def get_chips(self) -> int:
        enhancement_chips = 0
        if self._enhancement:
            if isinstance(self._enhancement, StoneCard):
                return 50
            enhancement_chips += self._enhancement.get_chips()
        return self._base_chips + self._added_chips + enhancement_chips

    def get_mult(self) -> float:
        if isinstance(self.enhancement, HasMult):
            return self.enhancement.get_mult()
        return 0.0

    def get_multiplication(self) -> float:
        if isinstance(self.enhancement, HasMultiplier):
            return self.enhancement.get_multiplication()
        return 1.0

    def get_scored_money(self) -> int:
        if isinstance(self.enhancement, HasMoney):
            return self.enhancement.get_scored_money()
        return 0

    def get_end_money(self) -> int:
        if isinstance(self.enhancement, HasMoney):
            return self.enhancement.get_end_money()
        return 0

    def set_enhancement(self, enhancement: Enhancement) -> None:
        self._enhancement = enhancement

    def set_edition(self, edition: Edition) -> None:
        self._edition = edition

    def set_seal(self, seal: Seal) -> None:
        self._seal = seal

    def add_chips(self, num_chips: int) -> None:
        self._added_chips += num_chips

    def is_face_card(self, has_pareidolia: bool) -> bool:
        return self._rank in [Rank.KING, Rank.QUEEN, Rank.JACK] or has_pareidolia

    def increase_rank(self) -> None:
        new_order = 1 if self._rank.value.order == 13 else self._rank.value.order + 1
        self._rank = Rank.from_int(new_order)

    def __eq__(self, value: Any) -> bool:
        if isinstance(value, PlayingCard):
            return (
                self._rank == value._rank
                and self._added_chips == value._added_chips
                and self._base_chips == value._base_chips
                and self._base_suit == value._base_suit
                and self._edition == value._edition
                and self._seal == value._seal
                and self._enhancement == value.enhancement
            )
        return False

    def __str__(self) -> str:
        return f"{self._rank.name} of {self.base_suit.name}"

    def __repr__(self) -> str:
        return f"{self._rank.name} of {self.base_suit.name}"

    def __hash__(self) -> int:
        return (
            hash(self._base_suit)
            + hash(self._enhancement)
            + hash(self._edition)
            + hash(self._base_chips)
            + hash(self._seal)
            + hash(self._added_chips)
        )


class Deck(HasReset):
    _cards_remaining: deque[PlayingCard]
    _cards_played: deque[PlayingCard]

    def __init__(self, cards: Sequence[PlayingCard]) -> None:
        self._cards_played = deque()
        self._cards_remaining = deque(cards)

    @property
    def cards_remaining(self) -> Sequence[PlayingCard]:
        return [*self._cards_remaining]

    @property
    def cards_played(self) -> Sequence[PlayingCard]:
        return [*self._cards_played]

    @property
    def cards(self) -> Sequence[PlayingCard]:
        return [*self._cards_remaining] + [*self._cards_played]

    def reset(self) -> None:
        self._cards_remaining = deque([*self._cards_remaining, *self._cards_played])
        self.shuffle()

    def add(self, cards: Sequence[PlayingCard]) -> None:
        self._cards_remaining.extend(cards)
        self.shuffle()

    def deal(self, num: int) -> Sequence[PlayingCard]:
        delt = [self._cards_remaining.pop() for i in range(num)]
        self._cards_played.extend(delt)
        return delt

    def destroy(self, cards: Sequence[PlayingCard]) -> None:
        """Destroyed cards are removed permanently."""
        for card in cards:
            # Required since cards can get destroyed via the HangedMan tarot card
            if card in self._cards_remaining:
                self._cards_remaining.remove(card)
            try:
                self._cards_played.remove(card)
            except ValueError:
                print("Attempted to destroy card that wasn't played. This is unexpected.")

    def shuffle(self) -> None:
        cards = list(copy.deepcopy(self._cards_remaining))
        random.shuffle(cards)
        self._cards_remaining = deque(cards)

    def get_num_remaining(self) -> int:
        return len(self._cards_remaining)

    def __eq__(self, obj: Any) -> bool:
        if isinstance(obj, Deck):
            return self._cards_remaining == obj._cards_remaining and self._cards_played == obj._cards_played
        return False

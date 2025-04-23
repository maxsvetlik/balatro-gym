from collections.abc import Sequence
from enum import Enum, auto
import random
from typing import Optional, Protocol

import numpy as np

from ..mixins import HasChips, HasMult, HasMultiplier, HasMoney, HasReset, HasRetrigger, HasCreatePlanet, HasCreateTarot


class Suit(Enum):
    SPADES = auto()
    CLUBS = auto()
    DIAMONDS = auto()
    HEARTS = auto()


class Rank(Enum):
    ACE = 11
    KING = 10
    QUEEN = 10
    JACK = 10
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2
    ONE = 1


############# Editions
class Edition(HasChips, HasMult, HasMultiplier, Protocol):
    def is_negative(self) -> bool:
        return False


class BaseEdition(Edition):
    pass


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


############# Enhancements
class Enhancement(HasChips, HasMult, HasMultiplier, HasMoney, Protocol):
    def get_suit(self, card: "PlayingCard") -> Sequence[Suit]:
        return [card.suit]


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
    def get_multiplication(self) -> float:
        return 2.0


class SteelCard(Enhancement):
    def get_multiplication(self) -> float:
        # TODO : When card is in hand
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
    _base_mult_probability = 0.25
    _base_money_probability = 0.0666666

    def get_mult(self, probability_modifier: int = 1) -> int:
        if np.random.random() <= self._base_mult_probability * probability_modifier:
            return 20
        return 0

    def get_scored_money(self, probability_modifier: int = 1) -> int:
        if np.random.random() <= self._base_money_probability * probability_modifier:
            return 20
        return 0


class Bonus(Enhancement):
    def get_chips(self) -> int:
        return 50


class Seal(HasMoney, HasRetrigger, HasCreatePlanet, HasCreateTarot):
    pass


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


class PlayingCard(HasChips):
    _rank: Rank
    _base_suit: Suit
    _enhancement: Optional[Enhancement]
    _edition: Optional[Edition]
    _seal: Optional[Seal]
    _base_chips: int
    _added_chips: int

    def __init__(
        self,
        rank: Rank,
        base_suit: Suit,
        enhancement: Optional[Enhancement],
        edition: Optional[Edition],
        seal: Optional[Seal],
    ):
        self._rank = rank
        self._base_suit = base_suit
        self._enhancement = enhancement
        self._edition = edition
        self._seal = seal
        self._base_chips = rank.value
        self._added_chips = 0

    @property
    def rank(self) -> Rank:
        return self._rank

    @property
    def suit(self) -> Suit:
        return self._base_suit

    @property
    def enhancement(self) -> Optional[Enhancement]:
        return self._enhancement

    @property
    def edition(self) -> Optional[Edition]:
        return self._edition

    @property
    def seal(self) -> Optional[Seal]:
        return self._seal

    def get_chips(self) -> int:
        return self._base_chips + self._added_chips

    def set_enhancement(self, enhancement: Optional[Enhancement]) -> None:
        self._enhancement = enhancement

    def set_edition(self, edition: Optional[Edition]) -> None:
        self._edition = edition

    def set_seal(self, seal: Optional[Seal]) -> None:
        self._seal = seal

    def add_chips(self, num_chips: int) -> None:
        self._added_chips += num_chips

    def is_face_card(self) -> bool:
        return self._rank in [Rank.KING, Rank.QUEEN, Rank.JACK]


class Deck(HasReset):
    _cards_remaining: Sequence[PlayingCard]
    _cards_played: Sequence[PlayingCard]

    def __init__(self, cards: Sequence[PlayingCard]) -> None:
        self._cards = cards

    def reset(self) -> None:
        self._cards_remaining = [*self._cards_remaining, *self._cards_played]
        self.shuffle()

    def add(self, cards: Sequence[PlayingCard]) -> None:
        self._cards = [*self._cards, *cards]
        self.shuffle()

    def deal(self, num: int) -> Sequence[PlayingCard]:
        delt: list[PlayingCard] = []
        for _ in range(num):
            selected = random.choice(self._cards)
            self._remove([selected])
            self._cards_played = [*self._cards_played, selected]
            delt.append(selected)
        return delt

    def _remove(self, cards: Sequence[PlayingCard]) -> None:
        for card in cards:
            list(self._cards).remove(card)

    def destroy(self, cards: Sequence[PlayingCard]) -> None:
        self._remove(cards)

    def shuffle(self) -> None:
        random.shuffle(list(self._cards))

    def get_num_remaining(self) -> int:
        return len(self._cards_remaining)

import dataclasses
import enum
import random
from typing import NamedTuple, Sequence

from balatro_gym.cards.decks import STANDARD_DECK
from balatro_gym.cards.interfaces import Card
from balatro_gym.cards.joker import JOKERS
from balatro_gym.cards.planet import PLANET_CARDS
from balatro_gym.cards.spectral import SPECTRAL_CARDS
from balatro_gym.cards.tarot import TAROT_CARDS
from balatro_gym.interfaces import Booster

__all__ = [
    "StandardPack", "ArcanaPack", "CelestialPack", "BuffoonPack", "SpectralPack"
]

class PackInfo(NamedTuple):
    cash_value: int
    n_cards: int
    n_choice: int


class PackType(enum.Enum):
    NORMAL = "NORMAL"
    JUMBO = "JUMBO"
    MEGA = "MEGA"


JOKER_SPECTRAL_PACK_INFO = {
    PackType.NORMAL: PackInfo(cash_value=4, n_cards=2, n_choice=1),
    PackType.JUMBO: PackInfo(cash_value=6, n_cards=4, n_choice=1),
    PackType.MEGA: PackInfo(cash_value=8, n_cards=4, n_choice=2),
}


PLANET_TAROT_CARD_PACK_INFO = {
    PackType.NORMAL: PackInfo(cash_value=4, n_cards=3, n_choice=1),
    PackType.JUMBO: PackInfo(cash_value=6, n_cards=5, n_choice=1),
    PackType.MEGA: PackInfo(cash_value=8, n_cards=5, n_choice=2),
}


@dataclasses.dataclass
class StandardPack(Booster):
    cash_value: int
    n_cards: int
    n_choice: int

    def sample(self) -> Sequence[Card]:
        # TODO: add enhancements
        return random.sample(STANDARD_DECK, self.n_cards)


@dataclasses.dataclass
class ArcanaPack(Booster):
    cash_value: int
    n_cards: int
    n_choice: int

    def sample(self) -> Sequence[Card]:
        return random.sample(TAROT_CARDS, self.n_cards)


@dataclasses.dataclass
class CelestialPack(Booster):
    cash_value: int
    n_cards: int
    n_choice: int

    def sample(self) -> Sequence[Card]:
        return random.sample(PLANET_CARDS, self.n_cards)


@dataclasses.dataclass
class BuffoonPack(Booster):
    cash_value: int
    n_cards: int
    n_choice: int

    def sample(self) -> Sequence[Card]:
        # TODO: add enhancements and consider joker rarity
        return random.sample(JOKERS, self.n_cards)


@dataclasses.dataclass
class SpectralPack(Booster):
    cash_value: int
    n_cards: int
    n_choice: int

    def sample(self) -> Sequence[Card]:
        return random.sample(SPECTRAL_CARDS, self.n_cards)


class BoosterType(enum.Enum):
    StandardPack = StandardPack
    CelestialPack = CelestialPack
    ArcanaPack = ArcanaPack
    BuffoonPack = BuffoonPack
    SpectralPack = SpectralPack


BOOSTER_TO_PACK_INFO = {
    BoosterType.SpectralPack: JOKER_SPECTRAL_PACK_INFO,
    BoosterType.BuffoonPack: JOKER_SPECTRAL_PACK_INFO,
    BoosterType.ArcanaPack: PLANET_TAROT_CARD_PACK_INFO,
    BoosterType.CelestialPack: PLANET_TAROT_CARD_PACK_INFO,
    BoosterType.StandardPack: PLANET_TAROT_CARD_PACK_INFO,
}

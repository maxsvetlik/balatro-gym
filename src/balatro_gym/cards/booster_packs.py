import dataclasses
import enum
import random
from typing import NamedTuple, Sequence

from balatro_gym.cards.decks import STANDARD_DECK
from balatro_gym.cards.interfaces import HasCost
from balatro_gym.cards.joker.effect_joker import Showman
from balatro_gym.cards.joker.utils import sample_jokers
from balatro_gym.cards.planet import PLANET_CARDS
from balatro_gym.cards.spectral import SPECTRAL_CARDS
from balatro_gym.cards.tarot import TAROT_CARDS
from balatro_gym.cards.voucher import Voucher
from balatro_gym.interfaces import Booster, JokerBase

__all__ = ["StandardPack", "ArcanaPack", "CelestialPack", "BuffoonPack", "SpectralPack"]


class PackInfo(NamedTuple):
    cost: int
    n_cards: int
    n_choice: int


class PackType(enum.Enum):
    NORMAL = "NORMAL"
    JUMBO = "JUMBO"
    MEGA = "MEGA"


JOKER_SPECTRAL_PACK_INFO = {
    PackType.NORMAL: PackInfo(cost=4, n_cards=2, n_choice=1),
    PackType.JUMBO: PackInfo(cost=6, n_cards=4, n_choice=1),
    PackType.MEGA: PackInfo(cost=8, n_cards=4, n_choice=2),
}


PLANET_TAROT_CARD_PACK_INFO = {
    PackType.NORMAL: PackInfo(cost=4, n_cards=3, n_choice=1),
    PackType.JUMBO: PackInfo(cost=6, n_cards=5, n_choice=1),
    PackType.MEGA: PackInfo(cost=8, n_cards=5, n_choice=2),
}


@dataclasses.dataclass
class StandardPack(Booster):
    cost: int
    n_cards: int
    n_choice: int

    def sample(self, jokers: Sequence[JokerBase], vouchers: Sequence[Voucher]) -> Sequence[HasCost]:
        # TODO: add enhancements
        return random.sample(STANDARD_DECK, self.n_cards)


@dataclasses.dataclass
class ArcanaPack(Booster):
    cost: int
    n_cards: int
    n_choice: int

    def sample(self, jokers: Sequence[JokerBase], vouchers: Sequence[Voucher]) -> Sequence[HasCost]:
        allow_repeat = any([isinstance(j, Showman) for j in jokers])
        if allow_repeat:
            return [card() for card in random.choices(TAROT_CARDS, k=self.n_cards)]
        else:
            return [card() for card in random.sample(TAROT_CARDS, self.n_cards)]


@dataclasses.dataclass
class CelestialPack(Booster):
    cost: int
    n_cards: int
    n_choice: int

    def sample(self, jokers: Sequence[JokerBase], vouchers: Sequence[Voucher]) -> Sequence[HasCost]:
        allow_repeat = any([isinstance(j, Showman) for j in jokers])
        if allow_repeat:
            return [card() for card in random.choices(PLANET_CARDS, k=self.n_cards)]
        else:
            return [card() for card in random.sample(PLANET_CARDS, self.n_cards)]


@dataclasses.dataclass
class BuffoonPack(Booster):
    cost: int
    n_cards: int
    n_choice: int

    def sample(self, jokers: Sequence[JokerBase], vouchers: Sequence[Voucher]) -> Sequence[HasCost]:
        return sample_jokers(jokers, vouchers, self.n_cards)


@dataclasses.dataclass
class SpectralPack(Booster):
    cost: int
    n_cards: int
    n_choice: int

    def sample(self, jokers: Sequence[JokerBase], vouchers: Sequence[Voucher]) -> Sequence[HasCost]:
        allow_repeat = any([isinstance(j, Showman) for j in jokers])
        if allow_repeat:
            return [card() for card in random.choices(SPECTRAL_CARDS, k=self.n_cards)]
        else:
            return [card() for card in random.sample(SPECTRAL_CARDS, self.n_cards)]


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

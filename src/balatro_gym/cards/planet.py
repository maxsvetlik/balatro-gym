
from balatro_gym.interfaces import PlanetCard, PokerHandType


class Pluto(PlanetCard):
    @property
    def _hand_type(self) -> PokerHandType:
        return PokerHandType.HIGH_CARD


class Mercury(PlanetCard):
    @property
    def _hand_type(self) -> PokerHandType:
        return PokerHandType.PAIR


class Uranus(PlanetCard):
    @property
    def _hand_type(self) -> PokerHandType:
        return PokerHandType.TWO_PAIR


class Venus(PlanetCard):
    @property
    def _hand_type(self) -> PokerHandType:
        return PokerHandType.THREE_SET


class Saturn(PlanetCard):
    @property
    def _hand_type(self) -> PokerHandType:
        return PokerHandType.STRAIGHT


class Jupiter(PlanetCard):
    @property
    def _hand_type(self) -> PokerHandType:
        return PokerHandType.FLUSH


class Earth(PlanetCard):
    @property
    def _hand_type(self) -> PokerHandType:
        return PokerHandType.FULL_HOUSE


class Mars(PlanetCard):
    @property
    def _hand_type(self) -> PokerHandType:
        return PokerHandType.FOUR_SET


class Neptune(PlanetCard):
    @property
    def _hand_type(self) -> PokerHandType:
        return PokerHandType.STRAIGHT_FLUSH


class PlanetX(PlanetCard):
    @property
    def _hand_type(self) -> PokerHandType:
        return PokerHandType.FIVE_SET


class Ceres(PlanetCard):
    @property
    def _hand_type(self) -> PokerHandType:
        return PokerHandType.FLUSH_HOUSE


class Eris(PlanetCard):
    @property
    def _hand_type(self) -> PokerHandType:
        return PokerHandType.FLUSH_FIVE


PLANET_CARDS: list[type[PlanetCard]] = [
    Pluto,
    Mercury,
    Uranus,
    Venus,
    Saturn,
    Jupiter,
    Earth,
    Mars,
    Neptune,
    PlanetX,
    Ceres,
    Eris,
]

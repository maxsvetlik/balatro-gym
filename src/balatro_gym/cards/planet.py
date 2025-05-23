from typing import Sequence

from balatro_gym.interfaces import PlanetCard, PokerHandType


class Pluto(PlanetCard):
    @property
    def _hand_type(self) -> PokerHandType:
        return PokerHandType.HIGH_CARD


PLANET_CARDS: Sequence[PlanetCard] = [Pluto()]

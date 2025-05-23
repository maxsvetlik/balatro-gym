from typing import Sequence

from balatro_gym.interfaces import Tarot


class Fool(Tarot):
    pass


TAROT_CARDS: Sequence[Tarot] = [Fool()]

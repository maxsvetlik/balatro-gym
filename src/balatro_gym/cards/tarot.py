
from balatro_gym.interfaces import Tarot


class Fool(Tarot):
    pass


TAROT_CARDS: set[Tarot] = {Fool()}

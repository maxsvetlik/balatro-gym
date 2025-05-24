
from balatro_gym.interfaces import Tarot


class Fool(Tarot):
    pass


# TODO: Temporary until more tarot cards are added to avoid test failing
TAROT_CARDS: list[type[Tarot]] = [Fool, Fool]

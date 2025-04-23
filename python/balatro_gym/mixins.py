from typing import Protocol, TypeVar


class HasChips(Protocol):
    def get_chips(self) -> int:
        return 0


class HasMult(Protocol):
    def get_mult(self, probability_modifier: int = 1) -> int:
        # This is expected to be actively added. Thus we return 0 in the base case.
        return 0


class HasMultiplier(Protocol):
    def get_multiplication(self) -> float:
        # This is expected to be actively multiplied. Thus we return 1.0 in the base case.
        return 1.0


class HasMoney(Protocol):
    def get_scored_money(self, probability_modifier: int = 1) -> int:
        return 0

    def get_end_money(self) -> int:
        return 0


class HasCreatePlanet(Protocol):
    def create_planet(self) -> bool:
        return False


class HasCreateTarot(Protocol):
    def create_tarot(self) -> bool:
        return False


class HasRetrigger(Protocol):
    def retrigger(self) -> bool:
        return False


_T = TypeVar("_T")


class HasReset(Protocol):
    def reset(self) -> None:
        raise NotImplementedError

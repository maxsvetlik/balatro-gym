from typing import Protocol, TypeVar, runtime_checkable


@runtime_checkable
class HasChips(Protocol):
    def get_chips(self) -> int:
        return 0


@runtime_checkable
class HasIsDestroyed(Protocol):
    def is_destroyed(self, probability_modifier: int = 1) -> bool:
        return False


@runtime_checkable
class HasMult(Protocol):
    def get_mult(self, probability_modifier: int = 1) -> int:
        # This is expected to be actively added. Thus we return 0 in the base case.
        return 0


@runtime_checkable
class HasMultiplier(Protocol):
    def get_multiplication(self) -> float:
        # This is expected to be actively multiplied. Thus we return 1.0 in the base case.
        return 1.0


@runtime_checkable
class HasMoney(Protocol):
    def get_scored_money(self, probability_modifier: int = 1) -> int:
        return 0

    def get_end_money(self) -> int:
        return 0


@runtime_checkable
class HasCreatePlanet(Protocol):
    def create_planet(self) -> bool:
        return False


@runtime_checkable
class HasCreateTarot(Protocol):
    def create_tarot(self) -> bool:
        return False


@runtime_checkable
class HasRetrigger(Protocol):
    def retrigger(self) -> bool:
        return False


_T = TypeVar("_T")


@runtime_checkable
class HasReset(Protocol):
    def reset(self) -> None:
        raise NotImplementedError

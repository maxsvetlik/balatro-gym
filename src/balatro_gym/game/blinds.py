import dataclasses
from enum import Enum, IntEnum
from math import floor
from typing import Optional, Sequence

from ..constants import BLIND_ANTE_TO_BASE, NUM_SUPPORTED_ANTE


class BlindType(IntEnum):
    # Note: Int values chosen out of convenience for modulo maths.
    BOSS = 0
    SMALL = 1
    LARGE = 2


class BossBlindEffect(Enum): ...


@dataclasses.dataclass
class BlindInfo:
    blind_type: BlindType
    reward: int
    required_score: int
    effect: Optional[BossBlindEffect]


def get_blind_reward(blind_type: BlindType, ante: int) -> int:
    if blind_type == BlindType.SMALL:
        return 3
    if blind_type == BlindType.LARGE:
        return 4
    else:
        if ante >= 8:
            return 8
        return 5


def get_blind_required_score(ante: int) -> int:
    # The actual formula should account for boss' special abilities as well as the
    # stake. But nominally the scale is 1.0x, 1.5x and 2x.
    base = BLIND_ANTE_TO_BASE.get(ante)
    if base is None:
        raise RuntimeError("Requested an ante that isn't supported.")
    return int(base)


def generate_run_blinds() -> Sequence[BlindInfo]:
    blinds: list[BlindInfo] = []
    for i in range(1, NUM_SUPPORTED_ANTE + 1):
        blind_type = BlindType(i % 3)
        ante = max(floor(i / len(BlindType)), 1)
        reward = get_blind_reward(blind_type, ante)
        req_score = get_blind_required_score(ante)
        boss_effect = None
        blinds.append(BlindInfo(blind_type, reward, req_score, boss_effect))
    return blinds

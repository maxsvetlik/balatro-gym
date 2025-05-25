from collections.abc import Mapping

DEFAULT_NUM_CONSUMABLE = 2
DEFAULT_START_MONEY = 4
DEFAULT_NUM_JOKER_SLOTS = 5

BLIND_ANTE_TO_BASE: Mapping[int, float] = {
    0: 100,
    1: 300,
    2: 800,
    3: 2000,
    4: 5000,
    5: 11000,
    6: 20000,
    7: 35000,
    8: 50000,
    9: 110000,
    10: 560000,
    11: 7200000,
    12: 3e9,
    13: 4.7e10,
    14: 2.9e13,
    15: 7.7e16,
    16: 8.6e20,
}
NUM_SUPPORTED_ANTE = len(BLIND_ANTE_TO_BASE.keys())

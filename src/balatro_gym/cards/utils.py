from collections import Counter
from collections.abc import Sequence

from balatro_gym.cards.interfaces import PlayingCard, Rank


def get_max_rank(hand: Sequence[PlayingCard]) -> Sequence[tuple[Rank, int]]:
    counter: Counter = Counter([card.rank for card in hand])
    return counter.most_common(2)


def contains_one_pair(counts: Sequence[tuple[Rank, int]]) -> bool:
    if len(counts) > 0:
        mc_rank, mc_count = counts[0]
        if mc_count >= 2:
            return True
    return False


def contains_two_pair(counts: Sequence[tuple[Rank, int]]) -> bool:
    if len(counts) >= 2:
        mc_rank, mc_count = counts[0]
        smc_rank, smc_count = counts[1]

        if mc_count >= 2 and smc_count >= 2:
            return True
    return False


def contains_three_set(counts: Sequence[tuple[Rank, int]]) -> bool:
    if len(counts) > 0:
        _, mc_count = counts[0]
        return mc_count >= 3
    return False

from collections import Counter
from collections.abc import Sequence

from balatro_gym.cards.interfaces import PlayingCard, Rank
from balatro_gym.cards.joker.effect_joker import FourFingers
from balatro_gym.interfaces import BoardState


def contains_three_set(hand: Sequence[PlayingCard]) -> int:
    counter = Counter(hand)
    return sum(count // 3 for count in counter.values()) == 1


def get_flush(hand: Sequence[PlayingCard], board: BoardState) -> Sequence[PlayingCard]:
    req_length = 4 if any(isinstance(joker, FourFingers) for joker in board.jokers) else 5
    counter: Counter = Counter()
    for card in hand:
        if card.enhancement is not None:
            counter.update(card.enhancement.get_suit(card))
        else:
            counter.update(card.suit)
    count = 0
    most_common_list = counter.most_common(1)
    if len(most_common_list) > 0:
        # In some situations there may not be a suit played. For instance a single StoneCard.
        _, count = most_common_list[0]

    if count >= req_length:
        return hand
    return []


def get_straight(hand: Sequence[PlayingCard], board: BoardState) -> Sequence[PlayingCard]:
    req_length = 4 if any(isinstance(joker, FourFingers) for joker in board.jokers) else 5
    sorted_ranks = sorted([card.rank.value.order for card in hand])
    if is_consecutive(sorted_ranks) or is_royal(hand, board) and len(sorted_ranks) >= req_length:
        return hand
    return []


def is_consecutive(ordered_ranks: Sequence[int]) -> bool:
    prev_rank = ordered_ranks[0]
    for rank in ordered_ranks[1:]:
        if not (rank == prev_rank + 1):
            return False
        prev_rank = rank
    return True


def is_royal(hand: Sequence[PlayingCard], board: BoardState) -> bool:
    valid = [{1, 10, 11, 12, 13}]
    if any(isinstance(joker, FourFingers) for joker in board.jokers):
        valid.extend([{10, 11, 12, 13}, {1, 11, 12, 13}])
    return set([card.rank.value.order for card in hand]) in valid


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

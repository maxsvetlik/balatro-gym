from collections import Counter
from typing import Sequence
from balatro_gym.interfaces import BoardState, PokerHandType
from balatro_gym.cards.interfaces import PlayingCard, Rank


def score_hand(hand: Sequence[PlayingCard], state: BoardState) -> float:
    """
    Scoring goes something like this:

        for card in scored_hand:
                score card:
                    1) take chips value
                    2) take mult value
                    3) ...
                for joker in jokers:
                    score joker:
                        1) take chips | card
                        2) take mult | card
                        3) take retrigger | card
            for card in non_scored_hand:
                score card:
                    1) take multiplication

            for joker in jokers:
                score joker:
                    1) take chips | scored_hand
                    2) take mult | scored_hand
                    3) take mulitiplcation | scored_hand
                    4) take money | scored_hand
                update joker:
                    1) add chips | scored_hand
                    2) add mult | scored_hand
                    3) add multiplication | scored_hand
                    4) subtract multiplication | round
    """

    return 0.0


###### These are broken out for testability


def _get_flush(hand: Sequence[PlayingCard]) -> Sequence[PlayingCard]:
    counter: Counter = Counter()
    for card in hand:
        if card.enhancement is not None:
            counter.update(card.enhancement.get_suit(card))
        else:
            counter.update([card.suit])

    common_suit, count = counter.most_common(1)[0]
    if count >= 5:
        return hand
    return []


def _get_straight(hand: Sequence[PlayingCard]) -> Sequence[PlayingCard]:
    return []


def _is_royal(hand: Sequence[PlayingCard]) -> bool:
    return all([card.is_face_card() for card in hand])


def _get_max_rank(hand: Sequence[PlayingCard]) -> Sequence[tuple[Rank, int]]:
    counter: Counter = Counter([card.rank for card in hand])
    return counter.most_common(2)


def _is_full_house(counts: Sequence[tuple[Rank, int]]) -> bool:
    mc_rank, mc_count = counts[0]
    smc_rank, smc_count = counts[1]

    if mc_count == 3 and smc_count == 2:
        return True
    return False


def _extract_largest_set(hand: Sequence[PlayingCard], counts: Sequence[tuple[Rank, int]]) -> Sequence[PlayingCard]:
    mc_rank, mc_count = counts[0]
    return [card for card in hand if card.rank == mc_rank]


def get_poker_hand(hand: Sequence[PlayingCard]) -> tuple[Sequence[PlayingCard], PokerHandType]:
    """
    Order of poker hand precedence:
        Straight flush, straight, flush, five set, four set, flush house, full house, three set, two set, one set
    """
    counts = _get_max_rank(hand)
    flush = _get_flush(hand)
    straight = _get_straight(hand)
    is_full = _is_full_house(counts)
    is_royal = _is_royal(hand)
    max_set = _extract_largest_set(hand, counts)

    if flush and straight:
        return hand, PokerHandType.STRAIGHT_FLUSH
    elif straight:
        return hand, PokerHandType.STRAIGHT
    elif flush:
        return hand, PokerHandType.FLUSH
    elif len(max_set) == 5:
        return max_set, PokerHandType.FIVE_SET
    elif len(max_set) == 4:
        return max_set, PokerHandType.FOUR_SET
    elif is_full:
        return hand, PokerHandType.FULL_HOUSE
    elif len(max_set) == 3:
        return max_set, PokerHandType.THREE_SET
    elif len(max_set) == 2:
        return max_set, PokerHandType.FIVE_SET
    else:
        return max_set, PokerHandType.HIGH_CARD

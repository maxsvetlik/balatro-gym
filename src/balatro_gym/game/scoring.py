from collections import Counter
from typing import Sequence

from balatro_gym.cards.interfaces import LuckyCard, PlayingCard, Rank, RedSeal
from balatro_gym.cards.joker import JokerBase
from balatro_gym.interfaces import BlindState, BoardState, PokerHandType


def _process_joker_card(
    joker: JokerBase,
    card: PlayingCard,
    hand_type: PokerHandType,
    board_state: BoardState,
    blind_state: BlindState,
) -> tuple[int, float]:
    chips_sum = 0
    mult_sum = 0.0
    chips_sum += joker.get_chips_card(card, blind_state)
    mult_sum += joker.get_mult_card(card, blind_state)
    return chips_sum, mult_sum


def score_hand(hand: Sequence[PlayingCard], board_state: BoardState, blind_state: BlindState) -> float:
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
    cards, hand_type = get_poker_hand(hand)
    hand_val = hand_type.value
    chips_sum = hand_val.chips
    mult_sum: float = hand_val.mult
    money_sum = 0

    for card in cards:
        num_card_retriggers = 2 if isinstance(card.seal, RedSeal) else 1
        chips_sum += card.get_chips() * num_card_retriggers
        mult_sum += card.get_mult() * num_card_retriggers
        mult_sum *= card.get_multiplication() * num_card_retriggers
        if isinstance(card.enhancement, LuckyCard):
            money_sum += card.enhancement.get_scored_money()  # TODO See #25. %his should be influenced by jokers
        if card.enhancement:
            if card.enhancement.is_destroyed():  # TODO See #25. This should be influenced by jokers
                board_state.deck.destroy([card])

        for joker in board_state.jokers:
            # TODO track retriggers on jokers
            chips, mult = _process_joker_card(joker, card, hand_type, board_state, blind_state)
            chips_sum += chips
            mult_sum += mult
        for unplayed_card in blind_state.hand:
            num_card_retriggers = 2 if isinstance(unplayed_card.seal, RedSeal) else 1
            mult_sum *= unplayed_card.get_multiplication() * num_card_retriggers
        for joker in board_state.jokers:
            chips_sum += joker.get_chips_hand(blind_state, hand_type)
            mult_sum += joker.get_mult_hand(cards, blind_state, hand_type)
            mult_sum *= joker.get_multiplication(cards, blind_state, hand_type)
            money_sum += joker.get_money(blind_state)
            # TODO update joker. E.g. num hands played influences chips
    return chips_sum * mult_sum


# These are broken out for testability


def _get_flush(hand: Sequence[PlayingCard]) -> Sequence[PlayingCard]:
    counter: Counter = Counter()
    for card in hand:
        if card.enhancement is not None:
            counter.update(card.enhancement.get_suit(card))
        else:
            counter.update(card.suit)

    most_common_list = counter.most_common(1)
    count = 0
    if len(most_common_list) > 0:
        # In some situations there may not be a suit played. For instance a single StoneCard.
        _, count = most_common_list[0]

    if count >= 5:
        return hand
    return []


def is_consecutive(ordered_ranks: Sequence[int]) -> bool:
    prev_rank = ordered_ranks[0]
    for rank in ordered_ranks[1:]:
        if not (rank == prev_rank + 1):
            return False
        prev_rank = rank
    return True


def _get_straight(hand: Sequence[PlayingCard]) -> Sequence[PlayingCard]:
    sorted_ranks = sorted([card.rank.value.order for card in hand])
    if is_consecutive(sorted_ranks) or _is_royal(hand):
        return hand
    return []


def _is_royal(hand: Sequence[PlayingCard]) -> bool:
    return set([card.rank.value.order for card in hand]) == {1, 10, 11, 12, 13}


def _get_max_rank(hand: Sequence[PlayingCard]) -> Sequence[tuple[Rank, int]]:
    counter: Counter = Counter([card.rank for card in hand])
    return counter.most_common(2)


def _is_full_house(counts: Sequence[tuple[Rank, int]]) -> bool:
    if len(counts) < 2:
        # Only a single card was played, so there aren't multiple counts
        return False

    mc_rank, mc_count = counts[0]
    smc_rank, smc_count = counts[1]

    if mc_count == 3 and smc_count == 2:
        return True
    return False


def _is_two_pair(counts: Sequence[tuple[Rank, int]]) -> bool:
    if len(counts) < 2:
        # Only a single card was played, so there aren't multiple counts
        return False

    mc_rank, mc_count = counts[0]
    smc_rank, smc_count = counts[1]

    if mc_count == 2 and smc_count == 2:
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
    flush = len(_get_flush(hand)) == 5
    straight = len(_get_straight(hand)) == 5
    is_full = _is_full_house(counts)
    is_two_pair = _is_two_pair(counts)
    is_royal = _is_royal(hand)
    max_set = _extract_largest_set(hand, counts)

    if is_royal and flush and straight:
        return hand, PokerHandType.ROYAL_FLUSH
    elif flush and straight:
        return hand, PokerHandType.STRAIGHT_FLUSH
    elif flush and is_full:
        return hand, PokerHandType.FLUSH_HOUSE
    elif flush and len(max_set) == 5:
        return hand, PokerHandType.FLUSH_FIVE
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
    elif is_two_pair:
        return [card for card in hand if card.rank in set([counts[0][0], counts[1][0]])], PokerHandType.TWO_PAIR
    elif len(max_set) == 2:
        return max_set, PokerHandType.PAIR
    else:
        return max_set, PokerHandType.HIGH_CARD

from collections import Counter
from typing import Sequence

from balatro_gym.cards.interfaces import LuckyCard, PlayingCard, Rank, RedSeal, StoneCard
from balatro_gym.cards.joker.effect_joker import Hack, Mime
from balatro_gym.cards.utils import contains_two_pair, get_flush, get_straight, is_royal
from balatro_gym.interfaces import BlindState, BoardState, JokerBase, PokerHandType


def _process_joker_card(
    joker: JokerBase,
    card: PlayingCard,
    hand_type: PokerHandType,
    board_state: BoardState,
    blind_state: BlindState,
) -> tuple[int, float]:
    chips_sum = 0
    mult_sum = 0.0
    chips_sum += joker.get_chips_card(card, blind_state, board_state)
    mult_sum += float(joker.get_mult_card(card, blind_state, board_state))
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
                    3) take multiplication | scored_hand
                    4) take money | scored_hand
                update joker:
                    1) add chips | scored_hand
                    2) add mult | scored_hand
                    3) add multiplication | scored_hand
                    4) subtract multiplication | round
    """
    played_cards, hand_type = get_poker_hand(hand, board_state)
    poker_scale = board_state.get_poker_hand(hand_type).score
    chips_sum = poker_scale.chips
    mult_sum: float = poker_scale.mult
    money_sum = 0
    for card in played_cards:
        num_card_retriggers = 2 if isinstance(card.seal, RedSeal) else 1
        if (any(isinstance(j, Hack) for j in board_state.jokers) and
                card.rank in [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE]):
            num_card_retriggers += 1
        for _ in range(num_card_retriggers):
            chips_sum += card.get_chips() + card.edition.get_chips()
            mult_sum += card.get_mult() + card.edition.get_mult()
            mult_sum *= card.get_multiplication() * card.edition.get_multiplication()
        if isinstance(card.enhancement, LuckyCard):
            money_sum += card.enhancement.get_scored_money()  # TODO See #25. this should be influenced by jokers
        if card.enhancement.is_destroyed():  # TODO See #25. This should be influenced by jokers
            board_state.deck.destroy([card])

        for unplayed_card in blind_state.hand:
            num_card_retriggers = 2 if isinstance(unplayed_card.seal, RedSeal) else 1
            num_card_retriggers += 1 if Mime() in board_state.jokers else 0
            mult_sum *= unplayed_card.get_multiplication() ** num_card_retriggers

        for joker in board_state.jokers:
            # TODO track retriggers on jokers
            chips, mult = _process_joker_card(joker, card, hand_type, board_state, blind_state)
            chips_sum += chips
            mult_sum += mult

    for joker in board_state.jokers:
        chips_sum += joker.get_chips_hand(played_cards, blind_state, board_state, hand_type)
        mult_sum += joker.get_mult_hand(played_cards, blind_state, board_state, hand_type)
        mult_sum *= joker.get_multiplication(played_cards, blind_state, board_state, hand_type)
        money_sum += joker.get_money(blind_state)

        # Handle Edition, if any
        mult_sum += joker.edition.get_mult()
        chips_sum += joker.edition.get_chips()
        mult_sum *= joker.edition.get_multiplication()
        # TODO update joker. E.g. num hands played influences chips
    return chips_sum * mult_sum


# These are broken out for testability


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


def _extract_largest_set(hand: Sequence[PlayingCard], counts: Sequence[tuple[Rank, int]]) -> Sequence[PlayingCard]:
    if len(counts) == 0:
        return []
    mc_rank, mc_count = counts[0]
    return [card for card in hand if card.rank == mc_rank]


def get_poker_hand(hand: Sequence[PlayingCard], board: BoardState) -> tuple[Sequence[PlayingCard], PokerHandType]:
    """
    Order of poker hand precedence:
        Straight flush, straight, flush, five set, four set, flush house, full house, three set, two set, one set
    """
    counts = _get_max_rank(hand)
    flush = len(get_flush(hand, board)) > 0
    straight = len(get_straight(hand, board)) > 0
    is_full = _is_full_house(counts)
    is_two_pair = contains_two_pair(counts)
    is_royal_res = is_royal(hand, board)
    max_set = _extract_largest_set(hand, counts)
    # Though not used in hands, stone cards should still be included in a played hand
    base_hand: list[PlayingCard] = []
    for card in hand:
        if card.enhancement == StoneCard():
            base_hand.append(card)
    if is_royal_res and flush and straight:
        return [*base_hand, *hand], PokerHandType.ROYAL_FLUSH
    elif flush and straight:
        return [*base_hand, *hand], PokerHandType.STRAIGHT_FLUSH
    elif flush and is_full:
        return [*base_hand, *hand], PokerHandType.FLUSH_HOUSE
    elif flush and len(max_set) == 5:
        return [*base_hand, *hand], PokerHandType.FLUSH_FIVE
    elif straight:
        return [*base_hand, *hand], PokerHandType.STRAIGHT
    elif flush:
        return [*base_hand, *hand], PokerHandType.FLUSH
    elif len(max_set) == 5:
        return max_set, PokerHandType.FIVE_SET
    elif len(max_set) == 4:
        return [*base_hand, *max_set], PokerHandType.FOUR_SET
    elif is_full:
        return hand, PokerHandType.FULL_HOUSE
    elif len(max_set) == 3:
        return [*base_hand, *max_set], PokerHandType.THREE_SET
    elif is_two_pair:
        if len(counts) == 1:
            return [*base_hand, *[card for card in hand if card.rank in set([counts[0][0]])]], PokerHandType.TWO_PAIR
        else:
            return [
                *base_hand,
                *[card for card in hand if card.rank in set([counts[0][0], counts[1][0]])],
            ], PokerHandType.TWO_PAIR

    elif len(max_set) == 2:
        return [*base_hand, *max_set], PokerHandType.PAIR
    else:
        # N.B. stone card would already be included here, so don't extend `base_hand`
        return max_set, PokerHandType.HIGH_CARD

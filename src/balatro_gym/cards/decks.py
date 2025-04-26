import copy
from typing import Sequence
from .interfaces import PlayingCard, Rank, Suit

import itertools

STANDARD_DECK: Sequence[PlayingCard] = [
    PlayingCard(rank, suit, None, None, None)
    for suit, rank in itertools.product([suit for suit in Suit], [rank for rank in Rank])
]


def discard(
    current_hand: Sequence[PlayingCard], discarded: Sequence[PlayingCard], new_cards: Sequence[PlayingCard]
) -> Sequence[PlayingCard]:
    _current_hand = list(copy.deepcopy(current_hand))
    for card in discarded:
        _current_hand.remove(card)
    _current_hand.extend(new_cards)
    return _current_hand

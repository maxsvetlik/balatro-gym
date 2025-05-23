import itertools
from typing import Sequence

from .interfaces import PlayingCard, Rank, Suit

STANDARD_DECK: Sequence[PlayingCard] = [
    PlayingCard(rank, suit, None, None, None)
    for suit, rank in itertools.product([suit for suit in Suit], [rank for rank in Rank])  # type: ignore
]


def discard(
    current_hand: Sequence[PlayingCard], discarded: Sequence[PlayingCard], new_cards: Sequence[PlayingCard]
) -> Sequence[PlayingCard]:
    current_hand = list(current_hand)
    for card in discarded:
        current_hand.remove(card)
    current_hand.extend(new_cards)
    return current_hand

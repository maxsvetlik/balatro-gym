from collections.abc import Sequence
from typing import Optional
from unittest.mock import Mock

from balatro_gym.cards.interfaces import Edition, Enhancement, PlayingCard, Rank, Seal, Suit
from balatro_gym.cards.joker.joker import Joker


def _make_card(
    rank: Rank = Rank.ACE,
    suit: Suit = Suit.HEARTS,
    enhancement: Optional[Enhancement] = None,
    edition: Optional[Edition] = None,
    seal: Optional[Seal] = None,
) -> PlayingCard:
    return PlayingCard(rank, suit, enhancement, edition, seal)


def _make_board(jokers: Sequence[Joker] = []) -> Mock:
    board = Mock()
    board.jokers = jokers
    return board

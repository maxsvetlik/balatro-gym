from collections.abc import Sequence
from typing import Optional

from balatro_gym.cards.interfaces import Edition, Enhancement, PlayingCard, Rank, Seal, Suit
from balatro_gym.cards.joker.joker import Joker
from balatro_gym.interfaces import BoardState


def _make_card(
    rank: Rank = Rank.ACE,
    suit: Suit = Suit.HEARTS,
    enhancement: Optional[Enhancement] = None,
    edition: Optional[Edition] = None,
    seal: Optional[Seal] = None,
) -> PlayingCard:
    return PlayingCard(rank, suit, enhancement, edition, seal)


def _make_board(jokers: Sequence[Joker] = []) -> BoardState:
    board = BoardState()
    board.jokers = jokers
    return board

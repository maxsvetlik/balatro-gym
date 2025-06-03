from balatro_gym.cards.interfaces import (
    BaseEdition,
    BaseEnhancement,
    BaseSeal,
    Edition,
    Enhancement,
    PlayingCard,
    Rank,
    Seal,
    Suit,
)
from balatro_gym.interfaces import BoardState, JokerBase


def _make_card(
    rank: Rank = Rank.ACE,
    suit: Suit = Suit.HEARTS,
    enhancement: Enhancement = BaseEnhancement(),
    edition: Edition = BaseEdition(),
    seal: Seal = BaseSeal(),
) -> PlayingCard:
    return PlayingCard(rank, suit, enhancement, edition, seal)


def _make_board(jokers: list[JokerBase] = []) -> BoardState:
    board = BoardState()
    board.jokers = jokers
    return board

from collections.abc import Sequence

from balatro_gym.cards.utils import (
    contains_one_pair,
    contains_three_set,
    contains_two_pair,
    get_flush,
    get_max_rank,
    get_straight,
)

from ...interfaces import BlindState, BoardState, JokerBase, PokerHandType, Rarity, Type
from ..interfaces import PlayingCard, Suit


class Joker(JokerBase):
    _cost: int = 2

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        return 4


class GreedyJoker(JokerBase):
    _cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        return sum([3 if Suit.DIAMONDS in card.suit else 0 for card in scored_cards])


class LustyJoker(JokerBase):
    _cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        return sum([3 if Suit.HEARTS in card.suit else 0 for card in scored_cards])


class WrathfulJoker(JokerBase):
    _cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        return sum([3 if Suit.CLUBS in card.suit else 0 for card in scored_cards])


class GluttonousJoker(JokerBase):
    _cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        return sum([3 if Suit.SPADES in card.suit else 0 for card in scored_cards])


class JollyJoker(JokerBase):
    _cost: int = 3

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult_hand(
        self, scored_cards: Sequence[PlayingCard], state: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        if contains_one_pair(get_max_rank(scored_cards)):
            return 8
        return 0


class ZanyJoker(JokerBase):
    _cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult_hand(
        self, scored_cards: Sequence[PlayingCard], state: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        if contains_three_set(scored_cards):
            return 12
        return 0


class MadJoker(JokerBase):
    _cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        if contains_two_pair(get_max_rank(scored_cards)):
            return 10
        return 0


class CrazyJoker(JokerBase):
    _cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        if len(get_straight(scored_cards, board)) > 0:
            return 12
        return 0


class DrollJoker(JokerBase):
    _cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        if len(get_flush(scored_cards, board)) > 0:
            return 10
        return 0


class SlyJoker(JokerBase):
    _cost: int = 3

    @property
    def joker_type(self) -> Type:
        return Type.CHIPS

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_chips_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        return 50 if contains_one_pair(get_max_rank(scored_cards)) >= 1 else 0


class WilyJoker(JokerBase):
    _cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.CHIPS

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_chips_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        return 100 if contains_three_set(scored_cards) else 0


class CleverJoker(JokerBase):
    _cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.CHIPS

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_chips_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        return 80 if contains_two_pair(get_max_rank(scored_cards)) else 0


class DeviousJoker(JokerBase):
    _cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.CHIPS

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_chips_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        return 100 if len(get_straight(scored_cards, board)) == 5 else 0


class CraftyJoker(JokerBase):
    _cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.CHIPS

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_chips_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        return 80 if len(get_flush(scored_cards, board)) > 0 else 0


class HalfJoker(JokerBase):
    _cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult_hand(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> int:
        return 20 if len(scored_cards) <= 3 else 0


class JokerStencil(JokerBase):
    _cost: int = 8

    @property
    def joker_type(self) -> Type:
        return Type.MULTIPLICATIVE

    @property
    def rarity(self) -> Rarity:
        return Rarity.UNCOMMON

    def get_multiplication(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> float:
        num_negative = sum([joker.edition.is_negative() for joker in board.jokers])
        num_jokers = len(board.jokers)
        return board.num_joker_slots - num_jokers + num_negative

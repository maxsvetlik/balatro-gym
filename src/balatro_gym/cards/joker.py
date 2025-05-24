from collections.abc import Sequence

from balatro_gym.cards.utils import contains_three_set, get_flush, get_num_pairs, get_straight
from balatro_gym.constants import DEFAULT_JOKER_SLOTS

from ..interfaces import BlindState, BoardState, JokerBase, PokerHandType, Rarity, Type
from .interfaces import PlayingCard, Suit

JOKERS: Sequence[JokerBase] = []


class Joker(JokerBase):
    _base_cost: int = 2

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        return 4


class GreedyJoker(JokerBase):
    _base_cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        return sum([3 if Suit.DIAMONDS in card.suit else 0 for card in scored_cards])


class LustyJoker(JokerBase):
    _base_cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        return sum([3 if Suit.HEARTS in card.suit else 0 for card in scored_cards])


class WrathfulJoker(JokerBase):
    _base_cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        return sum([3 if Suit.CLUBS in card.suit else 0 for card in scored_cards])


class GluttonousJoker(JokerBase):
    _base_cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        return sum([3 if Suit.SPADES in card.suit else 0 for card in scored_cards])


class JollyJoker(JokerBase):
    _base_cost: int = 3

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        if scored_hand == PokerHandType.PAIR:
            return 8
        return 0


class ZanyJoker(JokerBase):
    _base_cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        if scored_hand == PokerHandType.THREE_SET:
            return 12
        return 0


class MadJoker(JokerBase):
    _base_cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        if scored_hand == PokerHandType.TWO_PAIR:
            return 10
        return 0


class CrazyJoker(JokerBase):
    _base_cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        if (
            scored_hand == PokerHandType.STRAIGHT
            or scored_hand == PokerHandType.STRAIGHT_FLUSH
            or scored_hand == PokerHandType.ROYAL_FLUSH
        ):
            return 12
        return 0


class DrollJoker(JokerBase):
    _base_cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        if (
            scored_hand == PokerHandType.FLUSH
            or scored_hand == PokerHandType.FLUSH_FIVE
            or scored_hand == PokerHandType.FLUSH_HOUSE
            or scored_hand == PokerHandType.STRAIGHT_FLUSH
        ):
            return 10
        return 0


class SlyJoker(JokerBase):
    _base_cost: int = 3

    @property
    def joker_type(self) -> Type:
        return Type.CHIPS

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_chips_hand(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        return 50 if get_num_pairs(scored_cards) >= 1 else 0


class WilyJoker(JokerBase):
    _base_cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.CHIPS

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_chips_hand(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        return 100 if contains_three_set(scored_cards) else 0


class CleverJoker(JokerBase):
    _base_cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.CHIPS

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_chips_hand(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        return 80 if get_num_pairs(scored_cards) >= 2 else 0


class DeviousJoker(JokerBase):
    _base_cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.CHIPS

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_chips_hand(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        return 100 if len(get_straight(scored_cards)) == 5 else 0


class CraftyJoker(JokerBase):
    _base_cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.CHIPS

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_chips_hand(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        return 80 if len(get_flush(scored_cards)) > 0 else 0


class HalfJoker(JokerBase):
    _base_cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        return 20 if len(scored_cards) <= 3 else 0


class JokerStencil(JokerBase):
    _base_cost: int = 8

    @property
    def joker_type(self) -> Type:
        return Type.MULTIPLICATIVE

    @property
    def rarity(self) -> Rarity:
        return Rarity.UNCOMMON

    def get_multiplication(
        self, scored_cards: Sequence[PlayingCard], blind: BlindState, board: BoardState, scored_hand: PokerHandType
    ) -> float:
        # Maybe this should be baked into BoardState, but its derived data based on negative jokers afaik.
        num_negative = sum([joker.edition.is_negative() for joker in board.jokers])
        num_jokers = len(board.jokers)
        return DEFAULT_JOKER_SLOTS - num_jokers + num_negative

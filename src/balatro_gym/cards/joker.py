from collections.abc import Sequence

from balatro_gym.cards.utils import contains_two_pair, get_max_rank

from ..interfaces import BlindState, JokerBase, PokerHandType, Rarity, Type
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
        print(get_max_rank(state.hand))
        if contains_two_pair(get_max_rank(state.hand)):
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

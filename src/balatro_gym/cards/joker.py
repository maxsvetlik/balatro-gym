from collections.abc import Sequence

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
        return sum([3 if card.suit == Suit.DIAMONDS else 0 for card in state.hand])


class LustyJoker(JokerBase):
    _base_cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        return sum([3 if card.suit == Suit.HEARTS else 0 for card in state.hand])


class WrathfulJoker(JokerBase):
    _base_cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        return sum([3 if card.suit == Suit.CLUBS else 0 for card in state.hand])


class GluttonousJoker(JokerBase):
    _base_cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.ADDITIVE_MULT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON

    def get_mult(self, scored_cards: Sequence[PlayingCard], state: BlindState, scored_hand: PokerHandType) -> int:
        return sum([3 if card.suit == Suit.SPADES else 0 for card in state.hand])


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

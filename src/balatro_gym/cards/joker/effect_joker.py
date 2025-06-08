import random
from typing import Sequence

from balatro_gym.cards.interfaces import PlayingCard
from balatro_gym.interfaces import BlindState, BoardState, JokerBase, PokerHandType, Rarity, Type

"""This modules exists outside of the `joker` module because generally Effect based
jokers will be processed elsewhere, like in scoring logic. So Effect jokers may need to be
imported, which otherwise may cause circular dependencies."""


class FourFingers(JokerBase):
    _cost: int = 7

    @property
    def joker_type(self) -> Type:
        return Type.EFFECT

    @property
    def rarity(self) -> Rarity:
        return Rarity.UNCOMMON


class Mime(JokerBase):
    _cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.RETRIGGER

    @property
    def rarity(self) -> Rarity:
        return Rarity.UNCOMMON


class Showman(JokerBase):
    _cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.EFFECT

    @property
    def rarity(self) -> Rarity:
        return Rarity.UNCOMMON


class OopsAll6s(JokerBase):
    _cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.EFFECT

    @property
    def rarity(self) -> Rarity:
        return Rarity.UNCOMMON


class ChaosTheClown(JokerBase):
    _cost: int = 4

    @property
    def joker_type(self) -> Type:
        return Type.EFFECT

    @property
    def rarity(self) -> Rarity:
        return Rarity.COMMON


class Hack(JokerBase):
    _cost: int = 6

    @property
    def joker_type(self) -> Type:
        return Type.RETRIGGER

    @property
    def rarity(self) -> Rarity:
        return Rarity.UNCOMMON


class Pareidolia(JokerBase):
    _cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.EFFECT

    @property
    def rarity(self) -> Rarity:
        return Rarity.UNCOMMON


class SpaceJoker(JokerBase):
    _cost: int = 5

    @property
    def joker_type(self) -> Type:
        return Type.EFFECT

    @property
    def rarity(self) -> Rarity:
        return Rarity.UNCOMMON

    def on_hand_scored(
        self,
        scored_cards: Sequence[PlayingCard],
        blind: BlindState,
        board: BoardState,
        scored_hand: PokerHandType
    ) -> None:
        # 1 in 4 chance to upgrade the hand
        if random.random() < 0.25:
            hand = board.poker_hands[scored_hand.name]
            hand.level += 1

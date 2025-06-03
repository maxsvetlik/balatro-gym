from balatro_gym.interfaces import JokerBase, Rarity, Type

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

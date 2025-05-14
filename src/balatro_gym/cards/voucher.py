import dataclasses
from typing import Optional

from balatro_gym.interfaces import Voucher


@dataclasses.dataclass
class Overstock(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class OverstockPlus(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=Overstock)


@dataclasses.dataclass
class ClearanceSale(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Liquidation(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=ClearanceSale)


@dataclasses.dataclass
class Hone(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class GlowUp(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=Hone)


@dataclasses.dataclass
class RerollSurplus(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class RerollGlut(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=RerollSurplus)


@dataclasses.dataclass
class CrystalBall(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class OmenGlobe(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=CrystalBall)


@dataclasses.dataclass
class Telescope(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Observatory(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=Telescope)


@dataclasses.dataclass
class Grabber(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class NachoTong(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=Grabber)


@dataclasses.dataclass
class Wasteful(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Recyclomancy(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=Wasteful)


@dataclasses.dataclass
class TarotMerchant(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class TarotTycoon(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=TarotMerchant)


@dataclasses.dataclass
class PlanetMerchant(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class PlanetTycoon(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=PlanetMerchant)


@dataclasses.dataclass
class SeedMoney(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class MoneyTree(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=SeedMoney)


@dataclasses.dataclass
class Blank(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Antimatter(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=Blank)


@dataclasses.dataclass
class MagicTrick(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Illusion(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=MagicTrick)


@dataclasses.dataclass
class Hieroglyph(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Petroglyph(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=Hieroglyph)


@dataclasses.dataclass
class DirectorsCut(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Retcon(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=DirectorsCut)


@dataclasses.dataclass
class PaintBrush(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Palette(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=PaintBrush)


ALL_VOUCHERS = [
    Overstock(),
    OverstockPlus(),
    ClearanceSale(),
    Liquidation(),
    Hone(),
    GlowUp(),
    RerollSurplus(),
    RerollGlut(),
    CrystalBall(),
    OmenGlobe(),
    Telescope(),
    Observatory(),
    Grabber(),
    NachoTong(),
    Wasteful(),
    Recyclomancy(),
    TarotMerchant(),
    TarotTycoon(),
    PlanetMerchant(),
    PlanetTycoon(),
    SeedMoney(),
    MoneyTree(),
    Blank(),
    Antimatter(),
    MagicTrick(),
    Illusion(),
    Hieroglyph(),
    Petroglyph(),
    DirectorsCut(),
    Retcon(),
    PaintBrush(),
    Palette(),
]

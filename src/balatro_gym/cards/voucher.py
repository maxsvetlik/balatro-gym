import dataclasses
from typing import Optional

from balatro_gym.interfaces import Voucher


@dataclasses.dataclass(frozen=True)
class Overstock(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class OverstockPlus(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=Overstock)


@dataclasses.dataclass(frozen=True)
class ClearanceSale(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class Liquidation(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=ClearanceSale)


@dataclasses.dataclass(frozen=True)
class Hone(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class GlowUp(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=Hone)


@dataclasses.dataclass(frozen=True)
class RerollSurplus(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class RerollGlut(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=RerollSurplus)


@dataclasses.dataclass(frozen=True)
class CrystalBall(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class OmenGlobe(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=CrystalBall)


@dataclasses.dataclass(frozen=True)
class Telescope(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class Observatory(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=Telescope)


@dataclasses.dataclass(frozen=True)
class Grabber(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class NachoTong(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=Grabber)


@dataclasses.dataclass(frozen=True)
class Wasteful(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class Recyclomancy(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=Wasteful)


@dataclasses.dataclass(frozen=True)
class TarotMerchant(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class TarotTycoon(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=TarotMerchant)


@dataclasses.dataclass(frozen=True)
class PlanetMerchant(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class PlanetTycoon(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=PlanetMerchant)


@dataclasses.dataclass(frozen=True)
class SeedMoney(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class MoneyTree(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=SeedMoney)


@dataclasses.dataclass(frozen=True)
class Blank(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class Antimatter(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=Blank)


@dataclasses.dataclass(frozen=True)
class MagicTrick(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class Illusion(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=MagicTrick)


@dataclasses.dataclass(frozen=True)
class Hieroglyph(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class Petroglyph(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=Hieroglyph)


@dataclasses.dataclass(frozen=True)
class DirectorsCut(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class Retcon(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=DirectorsCut)


@dataclasses.dataclass(frozen=True)
class PaintBrush(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass(frozen=True)
class Palette(Voucher):
    dependency: Optional[Voucher] = dataclasses.field(default_factory=PaintBrush)


ALL_VOUCHERS = set([
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
])

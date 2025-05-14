import dataclasses
from typing import Optional

from balatro_gym.interfaces import Voucher


@dataclasses.dataclass
class Overstock(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class OverstockPlus(Voucher):
    dependency: Optional[Voucher] = Overstock()


@dataclasses.dataclass
class ClearanceSale(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Liquidation(Voucher):
    dependency: Optional[Voucher] = ClearanceSale()


@dataclasses.dataclass
class Hone(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class GlowUp(Voucher):
    dependency: Optional[Voucher] = Hone()


@dataclasses.dataclass
class RerollSurplus(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class RerollGlut(Voucher):
    dependency: Optional[Voucher] = RerollSurplus()


@dataclasses.dataclass
class CrystalBall(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class OmenGlobe(Voucher):
    dependency: Optional[Voucher] = CrystalBall()


@dataclasses.dataclass
class Telescope(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Observatory(Voucher):
    dependency: Optional[Voucher] = Telescope()


@dataclasses.dataclass
class Grabber(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class NachoTong(Voucher):
    dependency: Optional[Voucher] = Grabber()


@dataclasses.dataclass
class Wasteful(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Recyclomancy(Voucher):
    dependency: Optional[Voucher] = Wasteful()


@dataclasses.dataclass
class TarotMerchant(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class TarotTycoon(Voucher):
    dependency: Optional[Voucher] = TarotMerchant()


@dataclasses.dataclass
class PlanetMerchant(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class PlanetTycoon(Voucher):
    dependency: Optional[Voucher] = PlanetMerchant()


@dataclasses.dataclass
class SeedMoney(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class MoneyTree(Voucher):
    dependency: Optional[Voucher] = SeedMoney()


@dataclasses.dataclass
class Blank(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Antimatter(Voucher):
    dependency: Optional[Voucher] = Blank()


@dataclasses.dataclass
class MagicTrick(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Illusion(Voucher):
    dependency: Optional[Voucher] = MagicTrick()


@dataclasses.dataclass
class Hieroglyph(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Petroglyph(Voucher):
    dependency: Optional[Voucher] = Hieroglyph()


@dataclasses.dataclass
class DirectorsCut(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Retcon(Voucher):
    dependency: Optional[Voucher] = DirectorsCut()


@dataclasses.dataclass
class PaintBrush(Voucher):
    dependency: Optional[Voucher] = None


@dataclasses.dataclass
class Palette(Voucher):
    dependency: Optional[Voucher] = PaintBrush()


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

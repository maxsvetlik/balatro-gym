import dataclasses
import random
from typing import Sequence

from balatro_gym.cards.interfaces import Card
from balatro_gym.cards.voucher import ALL_VOUCHERS
from balatro_gym.interfaces import BoosterPack, Voucher


@dataclasses.dataclass
class ShopState:
    buyable_cards: Sequence[Card]
    vouchers: Sequence[Voucher]
    booster_packs: Sequence[BoosterPack]


class Shop:

    def __init__(self,
    num_buyable_slots: int = 2,
    num_vouchers: int = 1,
    num_booster_packs: int = 2,
    reroll_price: int = 5):
        self.num_buyable_slots = num_buyable_slots
        self.num_vouchers = num_vouchers
        self.num_booster_packs = num_booster_packs
        self.reroll_price = reroll_price
        self.vouchers: Sequence[Voucher] = []
        self.bought_vouchers: set[Voucher] = set()
        self.current_state = None

    def increase_num_buyable_slots(self) -> None:
        self.num_vouchers += 1

    def set_voucher_limit(self, num_vouchers: int) -> None:
        self.num_vouchers = num_vouchers

    def set_reroll_price(self, price: int) -> None:
        self.reroll_price = price

    def buy_voucher(self, voucher: Voucher) -> None:
        self.bought_vouchers.add(voucher)
        if voucher in self.vouchers:
            self.vouchers = [v for v in self.vouchers if v != voucher]

    def reroll(self) -> ShopState:
        return ShopState([], self.vouchers, [])

    def voucher_generator(self) -> Sequence[Voucher]:
        valid_vouchers = []
        for voucher in ALL_VOUCHERS - self.bought_vouchers:
            dependency_met = any([isinstance(voucher.dependency, v.__class__) for v in self.bought_vouchers])
            check_dependency = voucher.dependency is None or dependency_met
            if check_dependency and voucher not in self.bought_vouchers:
                valid_vouchers.append(voucher)
        return random.sample(valid_vouchers, self.num_vouchers)

    def generate_shop_state(self, round: int) -> ShopState:
        # Generate new voucher only on the first run of the ante
        # TODO: Generate a new voucher when a voucher tag is used
        if (round - 1) % 3 == 0:
            self.vouchers = self.voucher_generator()
        return ShopState(
            vouchers=self.vouchers,
            buyable_cards=[],
            booster_packs=[],
        )

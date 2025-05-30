import dataclasses
import random
from typing import Sequence

from balatro_gym.cards.booster_packs import (
    BOOSTER_TO_PACK_INFO,
    JOKER_SPECTRAL_PACK_INFO,
    BoosterType,
    BuffoonPack,
    PackType,
)
from balatro_gym.cards.interfaces import HasCost
from balatro_gym.cards.joker.effect_joker import Showman
from balatro_gym.cards.joker.utils import sample_jokers
from balatro_gym.cards.planet import PLANET_CARDS
from balatro_gym.cards.tarot import TAROT_CARDS
from balatro_gym.cards.voucher import ALL_VOUCHERS
from balatro_gym.interfaces import Booster, JokerBase, Voucher

__all__ = ["Shop"]


@dataclasses.dataclass
class ShopState:
    buyable_cards: Sequence[HasCost]
    vouchers: Sequence[Voucher]
    booster_packs: Sequence[Booster]


# Based on the info at https://balatrogame.fandom.com/wiki/Booster_Packs
PROBABILITY_MAPPING = {
    BoosterType.StandardPack: {PackType.NORMAL: 4.0, PackType.JUMBO: 2.0, PackType.MEGA: 0.5},
    BoosterType.ArcanaPack: {PackType.NORMAL: 4.0, PackType.JUMBO: 2.0, PackType.MEGA: 0.5},
    BoosterType.CelestialPack: {PackType.NORMAL: 4.0, PackType.JUMBO: 2.0, PackType.MEGA: 0.5},
    BoosterType.BuffoonPack: {PackType.NORMAL: 1.2, PackType.JUMBO: 0.6, PackType.MEGA: 0.15},
    BoosterType.SpectralPack: {PackType.NORMAL: 0.6, PackType.JUMBO: 0.3, PackType.MEGA: 0.07},
}


class Shop:
    def __init__(
        self,
        num_buyable_slots: int = 2,
        num_vouchers: int = 1,
        num_booster_packs: int = 2,
        reroll_price: int = 5,
        allow_duplicates: bool = False,
    ):
        self.num_buyable_slots = num_buyable_slots
        self.num_vouchers = num_vouchers
        self.num_booster_packs = num_booster_packs
        self.reroll_price = reroll_price
        self.vouchers: Sequence[Voucher] = []
        self.bought_vouchers: set[Voucher] = set()
        self.current_state = None
        self.allow_duplicates = allow_duplicates

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

    def generate_shop_state(self, round: int, jokers: Sequence[JokerBase]) -> ShopState:
        # Generate new voucher only on the first run of the ante
        # TODO: Generate a new voucher when a voucher tag is used
        if (round - 1) % 3 == 0:
            self.vouchers = self.voucher_generator()
        return ShopState(
            vouchers=self.vouchers,
            buyable_cards=self.generate_buyable_cards(jokers),
            booster_packs=self.generate_booster_packs(round),
        )

    def generate_booster_packs(self, round: int) -> Sequence[Booster]:
        potential_packs = []
        probabilities = []
        for pack_type in PackType:
            for booster_type in BoosterType:
                pack_info_map = BOOSTER_TO_PACK_INFO[booster_type]
                pack_info = pack_info_map[pack_type]
                potential_packs.append(booster_type.value(pack_info.cost, pack_info.n_cards, pack_info.n_choice))
                probabilities.append(PROBABILITY_MAPPING[booster_type][pack_type])

        # On the first round, one normal buffoon pack is guaranteed
        if round == 1:
            pack_info = JOKER_SPECTRAL_PACK_INFO[PackType.NORMAL]
            random_booster = random.choices(potential_packs, weights=probabilities, k=self.num_booster_packs - 1)
            return [BuffoonPack(pack_info.cost, pack_info.n_cards, pack_info.n_choice)] + random_booster
        return random.choices(potential_packs, weights=probabilities, k=self.num_booster_packs)

    def generate_buyable_cards(self, jokers: Sequence[JokerBase]) -> Sequence[HasCost]:
        sampled_cards: list[HasCost]
        n_tarots, n_planets, n_jokers = 0, 0, 0
        for _ in range(self.num_buyable_slots):
            rand = random.random()
            # The probabilities are based on numbers provided by https://balatrogame.fandom.com/wiki/The_Shop
            if rand < 1 / 7:
                n_tarots += 1
            elif rand < 2 / 7:
                n_planets += 1
            else:
                n_jokers += 1

        allow_repeat = any([isinstance(j, Showman) for j in jokers])
        sampled_tarot_and_planets: Sequence[type[HasCost]]
        if allow_repeat:
            sampled_tarot_and_planets = (random.choices(PLANET_CARDS, k=n_planets) +
                                         random.choices(TAROT_CARDS, k=n_tarots))
        else:
            sampled_tarot_and_planets = random.sample(PLANET_CARDS, n_planets) + random.sample(TAROT_CARDS, n_tarots)

        sampled_jokers: Sequence[HasCost] = sample_jokers(jokers, self.vouchers, n_jokers)
        sampled_cards = [card() for card in list(sampled_tarot_and_planets)] + list(sampled_jokers)
        assert [isinstance(c, HasCost) for c in sampled_cards]
        return sampled_cards

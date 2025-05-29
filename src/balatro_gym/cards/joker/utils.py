import random
from typing import Sequence

from balatro_gym.cards.interfaces import BaseEdition, Edition, Foil, Holographic, Polychrome
from balatro_gym.cards.joker.constants import JOKERS
from balatro_gym.cards.joker.effect_joker import Showman
from balatro_gym.cards.voucher import GlowUp, Hone, Voucher
from balatro_gym.interfaces import JokerBase, Rarity


def sample_jokers(jokers: Sequence[JokerBase], vouchers: Sequence[Voucher], n_jokers: int) -> list[JokerBase]:
    sampled_jokers: list[JokerBase] = []
    for _ in range(n_jokers):
        prob_rarity = random.random()

        # Get edition
        prob_edition_modifier = 1.0
        if any([isinstance(v, GlowUp) for v in vouchers]):
            prob_edition_modifier = 4.0
        elif any([isinstance(v, Hone) for v in vouchers]):
            prob_edition_modifier = 2.0

        prob_edition = random.random()
        edition: Edition = BaseEdition()
        poly_prob = 0.003 * prob_edition_modifier
        holo_prob = 0.014 * prob_edition_modifier
        foil_prob = 0.02 * prob_edition
        if prob_edition < poly_prob:
            edition = Polychrome()
        elif prob_edition < poly_prob + holo_prob:
            edition = Holographic()
        elif prob_edition < poly_prob + holo_prob + foil_prob:
            edition = Foil()

        if prob_rarity < 0.70:
            rarity = Rarity.COMMON
        elif prob_rarity < 0.95:
            rarity = Rarity.UNCOMMON
        else:
            rarity = Rarity.RARE

        jokers_target_rarity = JOKERS[rarity]
        allow_repeat = any([isinstance(j, Showman) for j in jokers])
        if not allow_repeat:
            jokers_in_use = list(jokers) + sampled_jokers
            jokers_target_rarity = [j for j in jokers_target_rarity
                                    if all([j != owned_j.__class__ for owned_j in jokers_in_use])]
        sampled_joker = random.choice(jokers_target_rarity)()
        sampled_joker.set_edition(edition)
        sampled_jokers.append(sampled_joker)
    return sampled_jokers

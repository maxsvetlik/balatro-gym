import random
from typing import Sequence

from balatro_gym.cards.interfaces import BaseEdition, Foil, Holographic, Polychrome, Edition
from balatro_gym.cards.joker.constants import JOKERS
from balatro_gym.cards.voucher import GlowUp, Hone, Voucher
from balatro_gym.interfaces import JokerBase, Rarity


def sample_joker(jokers: Sequence[JokerBase], vouchers: Sequence[Voucher], allow_repeat: bool = False) -> JokerBase:
    # TODO: adjust sell price
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
    if not allow_repeat:
        jokers_target_rarity = [j for j in jokers_target_rarity if all([j != owned_j.__class__ for owned_j in jokers])]
    sampled_joker = random.choice(jokers_target_rarity)()
    sampled_joker.set_edition(edition)
    return sampled_joker

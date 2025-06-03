from collections.abc import Sequence
from typing import Mapping

import balatro_gym.cards.joker.effect_joker as ejoker
import balatro_gym.cards.joker.joker as joker
from balatro_gym.interfaces import JokerBase, Rarity

JOKERS: Mapping[Rarity, Sequence[type[JokerBase]]] = {
    Rarity.COMMON: [
        joker.Joker,
        joker.GreedyJoker,
        joker.LustyJoker,
        joker.WrathfulJoker,
        joker.GluttonousJoker,
        joker.JollyJoker,
        joker.ZanyJoker,
        joker.MadJoker,
        joker.CraftyJoker,
        joker.DrollJoker,
        joker.SlyJoker,
        joker.WilyJoker,
        joker.CleverJoker,
        joker.DeviousJoker,
        joker.CraftyJoker,
        joker.HalfJoker,
    ],
    Rarity.UNCOMMON: [
        joker.JokerStencil,
        ejoker.FourFingers,
        ejoker.Mime,
        ejoker.OopsAll6s,
    ],
    Rarity.RARE: [
        joker.TheDuo,
    ],
}

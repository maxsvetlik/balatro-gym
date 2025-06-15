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
        ejoker.ChaosTheClown,
        joker.ScaryFace,
        joker.AbstractJoker,
        joker.DelayedGratification,
        joker.GrosMichel,
        joker.EvenSteven,
        joker.OddTodd,
        joker.Scholar,
        joker.BusinessCard,
        joker.Supernova,
        joker.RideTheBus,
        joker.Egg,
    ],
    Rarity.UNCOMMON: [
        joker.JokerStencil,
        ejoker.FourFingers,
        ejoker.Mime,
        ejoker.OopsAll6s,
        joker.Fibonacci,
        joker.SteelJoker,
        ejoker.Hack,
        joker.Pareidolia,
        ejoker.SpaceJoker,
        ejoker.Burglar,
        joker.Blackboard,
    ],
    Rarity.RARE: [
        joker.TheDuo,
    ],
}

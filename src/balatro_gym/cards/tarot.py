import random
from typing import Sequence

from balatro_gym.cards.interfaces import (
    BaseEdition,
    BonusCard,
    Foil,
    GlassCard,
    Holographic,
    LuckyCard,
    MultCard,
    PlayingCard,
    Polychrome,
    SteelCard,
    WildCard,
)
from balatro_gym.cards.planet import PLANET_CARDS
from balatro_gym.interfaces import BoardState, Tarot


class Fool(Tarot):
    def apply(self, selected_cards: Sequence[PlayingCard], board_state: BoardState) -> bool:
        last_consumed_card = board_state.last_used_consumable
        if last_consumed_card is None or isinstance(last_consumed_card, Fool):
            return False
        board_state.acquire_consumable(last_consumed_card)
        return True


class Magician(Tarot):
    def apply(self, selected_cards: Sequence[PlayingCard], board_state: BoardState) -> bool:
        if len(selected_cards) > 2 or len(selected_cards) == 0:
            return False
        for card in selected_cards:
            card.set_enhancement(LuckyCard())
        return True


class HighPriestess(Tarot):
    def apply(self, selected_cards: Sequence[PlayingCard], board_state: BoardState) -> bool:
        num_slots = board_state.consumable.num_slots
        n_consumables = len(board_state.consumable.consumables)
        if num_slots > n_consumables:
            return False
        n_cards_to_generate = min(2, num_slots - n_consumables)
        # TODO: Make sure ceres, planetx and eris are only sampled once the associated hand is played once
        for planet_card in random.sample(PLANET_CARDS, n_cards_to_generate):
            board_state.acquire_consumable(planet_card())
        return True


class Empress(Tarot):
    def apply(self, selected_cards: Sequence[PlayingCard], board_state: BoardState) -> bool:
        if len(selected_cards) > 2 or len(selected_cards) == 0:
            return False
        for card in selected_cards:
            card.set_enhancement(MultCard())
        return True


class Emperor(Tarot):
    def apply(self, selected_cards: Sequence[PlayingCard], board_state: BoardState) -> bool:
        num_slots = board_state.consumable.num_slots
        n_consumables = len(board_state.consumable.consumables)
        if num_slots > n_consumables:
            return False
        n_cards_to_generate = min(2, num_slots - n_consumables)
        for tarot_card in random.sample(TAROT_CARDS, n_cards_to_generate):
            board_state.acquire_consumable(tarot_card())
        return True


class Hierophant(Tarot):
    def apply(self, selected_cards: Sequence[PlayingCard], board_state: BoardState) -> bool:
        if len(selected_cards) > 2 or len(selected_cards) == 0:
            return False
        for card in selected_cards:
            card.set_enhancement(BonusCard())
        return True


class Lovers(Tarot):
    def apply(self, selected_cards: Sequence[PlayingCard], board_state: BoardState) -> bool:
        if len(selected_cards) > 1 or len(selected_cards) == 0:
            return False
        selected_cards[0].set_enhancement(WildCard())
        return True


class Chariot(Tarot):
    def apply(self, selected_cards: Sequence[PlayingCard], board_state: BoardState) -> bool:
        if len(selected_cards) > 1 or len(selected_cards) == 0:
            return False
        selected_cards[0].set_enhancement(SteelCard())
        return True


class Justice(Tarot):
    def apply(self, selected_cards: Sequence[PlayingCard], board_state: BoardState) -> bool:
        if len(selected_cards) > 1 or len(selected_cards) == 0:
            return False
        selected_cards[0].set_enhancement(GlassCard())
        return True


class Hermit(Tarot):
    def apply(self, selected_cards: Sequence[PlayingCard], board_state: BoardState) -> bool:
        earn = min(20, board_state.money * 2)
        board_state.set_money(board_state.money + earn)
        return True


class WheelOfFortune(Tarot):
    def apply(self, selected_cards: Sequence[PlayingCard], board_state: BoardState) -> bool:
        non_enhanced_jokers = [joker for joker in board_state.jokers if joker.edition != BaseEdition]
        if len(non_enhanced_jokers) < 1:
            return False

        prob = random.random()
        if prob < 0.25:
            editions = [Foil(), Holographic(), Polychrome()]
            probabilities = [0.5, 0.35, 0.15]
            selected_edition = random.choices(editions, weights=probabilities, k=1)[0]
            selected_joker = random.choice(non_enhanced_jokers)
            selected_joker.set_edition(selected_edition)
        return True


class Strength(Tarot):
    pass


TAROT_CARDS: list[type[Tarot]] = [
    Fool, Magician, HighPriestess, Empress, Emperor, Hierophant, Lovers, Chariot, Justice, Hermit, WheelOfFortune
]

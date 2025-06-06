from typing import (
    Sequence,
)
from unittest.mock import Mock, patch

import pytest

import balatro_gym.cards.interfaces
from balatro_gym.cards.interfaces import (
    BonusCard,
    Deck,
    Edition,
    Foil,
    GlassCard,
    GoldCard,
    Holographic,
    LuckyCard,
    MultCard,
    Negative,
    Polychrome,
    SteelCard,
    StoneCard,
    Suit,
    WildCard,
)
from balatro_gym.cards.joker.joker import GreedyJoker, Joker
from balatro_gym.cards.planet import Mercury, Pluto
from balatro_gym.cards.voucher import ClearanceSale, Liquidation, Voucher
from balatro_gym.game.scoring import get_poker_hand, score_hand
from balatro_gym.interfaces import BoardState, PokerHand, PokerHandType
from test.utils import _make_board, _make_card


@pytest.mark.unit
def test_enhancement_bonus() -> None:
    enhancement = BonusCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert card.get_chips() == 50 + card._base_chips


@pytest.mark.unit
def test_enhancement_mult() -> None:
    enhancement = MultCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert card.get_mult() == 4


@pytest.mark.unit
def test_enhancement_wild() -> None:
    enhancement = WildCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert len(set(card.suit)) == len(Suit)


@pytest.mark.unit
def test_enhancement_glass() -> None:
    enhancement = GlassCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert card.get_multiplication() == 2


@pytest.mark.unit
def test_enhancement_glass_scoring() -> None:
    enhancement = GlassCard()
    card = _make_card(enhancement=enhancement)
    board = BoardState()
    board.jokers = []
    blind_mock = Mock()
    blind_mock.hand = []
    submitted_hand = [card]
    score = score_hand(submitted_hand, board, blind_mock)
    _, hand_type = get_poker_hand(submitted_hand, _make_board())
    expected_score = (hand_type.value.chips + card.get_chips()) * hand_type.value.mult * card.get_multiplication()
    assert score == expected_score


@pytest.mark.unit
@pytest.mark.parametrize("probability_modifier", [1, 2, 10])
def test_enhancement_glass_destroy(probability_modifier: int) -> None:
    enhancement = GlassCard()
    card = _make_card(enhancement=enhancement)
    deck = Deck([card])
    submitted_hand = deck.deal(1)
    assert card in deck.cards_played
    board_mock = Mock()
    board_mock.get_poker_hand.return_value = PokerHand(PokerHandType.HIGH_CARD, 1, 0)
    board_mock.jokers = []  # TODO See #25. This can influence probabilities and should be tested.
    board_mock.deck = deck
    blind_mock = Mock()
    blind_mock.hand = []
    with patch.object(balatro_gym.cards.interfaces, "np") as mock:
        random_mock = Mock()
        mock.random.random = random_mock
        random_mock.return_value = 0
        score_hand(submitted_hand, board_mock, blind_mock)
        assert card not in board_mock.deck.cards_played


@pytest.mark.unit
def test_enhancement_steel() -> None:
    enhancement = SteelCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert card.get_multiplication() == 1.5


@pytest.mark.unit
def test_enhancement_steel_scoring() -> None:
    # Submit a single card as a hand with a single steel card held in hand
    enhancement = SteelCard()
    held_card = _make_card(enhancement=enhancement)
    submitted_card = _make_card()
    submitted_hand = [submitted_card]
    board = BoardState()
    board.jokers = []
    blind_mock = Mock()
    blind_mock.hand = [held_card]
    score = score_hand(submitted_hand, board, blind_mock)
    _, hand_type = get_poker_hand(submitted_hand, _make_board())
    expected_score = (
        (hand_type.value.chips + submitted_card.get_chips())
        * hand_type.value.mult
        * submitted_card.get_multiplication()
        * held_card.get_multiplication()
    )
    assert score == expected_score


@pytest.mark.unit
def test_enhancement_stone() -> None:
    enhancement = StoneCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert enhancement.get_chips() == 50
    assert card.get_chips() == 50
    assert len(card.suit) == 0


@pytest.mark.unit
def test_enhancement_stone_scoring() -> None:
    # Submit a single stone card
    enhancement = StoneCard()
    card = _make_card(enhancement=enhancement)
    board = BoardState()
    board.jokers = []
    blind_mock = Mock()
    blind_mock.hand = []
    submitted_hand = [card]
    score = score_hand(submitted_hand, board, blind_mock)
    _, hand_type = get_poker_hand(submitted_hand, _make_board())
    expected_score = (hand_type.value.chips + card.get_chips()) * hand_type.value.mult * card.get_multiplication()
    assert score == expected_score


@pytest.mark.unit
def test_enhancement_gold() -> None:
    enhancement = GoldCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    assert card.get_scored_money() == 0
    assert card.get_end_money() == 3


@pytest.mark.unit
def test_enhancement_lucky() -> None:
    enhancement = LuckyCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    with patch.object(balatro_gym.cards.interfaces, "np") as mock:
        random_mock = Mock()
        mock.random.random = random_mock
        # Test degenerate cases
        random_mock.return_value = 1
        assert enhancement.get_mult() == 0
        assert enhancement.get_scored_money() == 0
        random_mock.return_value = 0
        assert enhancement.get_mult() == 20
        assert enhancement.get_scored_money() == 20


@pytest.mark.unit
@pytest.mark.parametrize("probability_modifier", [1, 2, 10])
def test_enhancement_lucky_modifiers(probability_modifier: int) -> None:
    enhancement = LuckyCard()
    card = _make_card(enhancement=enhancement)
    assert card.enhancement == enhancement
    with patch.object(balatro_gym.cards.interfaces, "np") as mock:
        random_mock = Mock()
        mock.random.random = random_mock

        # Verify that the base probabilities are correct
        random_mock.return_value = min(probability_modifier / 5, 1)
        assert enhancement.get_mult(probability_modifier) == 20
        random_mock.return_value = min(probability_modifier / 15, 1)
        assert enhancement.get_scored_money(probability_modifier) == 20


@pytest.mark.unit
def test_planet_cards() -> None:
    pluto = Pluto()
    initial_level_high_card = 2
    initial_level_pair = 1
    poker_hands = [
        PokerHand(hand_type=PokerHandType.HIGH_CARD, level=initial_level_high_card, num_played=0),
        PokerHand(hand_type=PokerHandType.PAIR, level=initial_level_pair, num_played=0),
    ]
    pluto.increase_level(poker_hands)

    # Only increase the high card hand
    assert poker_hands[0].level == initial_level_high_card + 1
    assert poker_hands[1].level == initial_level_pair

    mercury = Mercury()
    mercury.decrease_level(poker_hands)
    assert poker_hands[0].level == initial_level_high_card + 1
    assert poker_hands[1].level == initial_level_pair

    pluto.decrease_level(poker_hands)
    assert poker_hands[0].level == initial_level_high_card
    assert poker_hands[1].level == initial_level_pair


@pytest.mark.unit
def test_sell_and_cost_value() -> None:
    cost = 5
    joker = GreedyJoker()

    vouchers: Sequence[Voucher] = []
    assert joker.cost(vouchers) == cost == joker.base_cost
    assert joker.sell_value(vouchers) == 5 // 2

    vouchers = [ClearanceSale()]
    # 25% off
    assert joker.cost(vouchers) == 3
    assert joker.sell_value(vouchers) == 1

    vouchers = [ClearanceSale(), Liquidation()]
    # 50% off
    assert joker.cost(vouchers) == 5 // 2
    assert joker.sell_value(vouchers) == 1


@pytest.mark.unit
@pytest.mark.parametrize(
    "edition,edition_cost",
    [
        [Foil(), 2],
        [Holographic(), 3],
        [Polychrome(), 5],
        [Negative(), 5],
    ],
)
def test_sell_and_cost_joker_with_edition(edition: Edition, edition_cost: int) -> None:
    joker = Joker()
    base_cost = joker.base_cost
    joker.set_edition(edition)
    assert joker.cost([]) == base_cost + edition_cost
    assert joker.sell_value([]) == (base_cost + edition_cost) // 2
    assert joker.cost([Liquidation()]) == (base_cost + edition_cost) // 2
    assert joker.sell_value([Liquidation()]) == min(1, (base_cost + edition_cost) // 4)

from collections.abc import Sequence
from unittest.mock import Mock

import pytest

from balatro_gym.cards.interfaces import PlayingCard, Rank, Suit
from balatro_gym.cards.joker.effect_joker import ChaosTheClown, FourFingers
from balatro_gym.cards.joker.joker import (
    CleverJoker,
    CraftyJoker,
    CrazyJoker,
    DeviousJoker,
    DrollJoker,
    GluttonousJoker,
    GreedyJoker,
    HalfJoker,
    Joker,
    JokerStencil,
    JollyJoker,
    LustyJoker,
    MadJoker,
    SlyJoker,
    TheDuo,
    WilyJoker,
    WrathfulJoker,
    ZanyJoker,
)
from balatro_gym.cards.joker.utils import sample_jokers
from balatro_gym.cards.utils import get_flush, get_straight, is_royal
from balatro_gym.constants import DEFAULT_NUM_JOKER_SLOTS
from balatro_gym.game.shop import Shop
from balatro_gym.interfaces import JokerBase, PokerHandType, Rarity, Type
from test.utils import _make_board, _make_card


@pytest.mark.unit
def test_base_joker() -> None:
    # The base joker should return noop values as appropriate. E.g. 0 for additive, and 1 for multiplicative effects
    j = JokerBase()
    assert j.base_cost == 1
    assert j.get_money(Mock()) == 0
    assert j.get_mult_card(Mock(), Mock(), Mock()) == 0
    assert j.get_chips_hand(Mock(), Mock(), Mock(), Mock()) == 0
    assert j.get_multiplication(Mock(), Mock(), Mock(), Mock()) == 1.0
    assert j.get_chips_card(Mock(), Mock(), Mock()) == 0


@pytest.mark.unit
def test_joker() -> None:
    j = Joker()
    assert j.joker_type == Type.ADDITIVE_MULT
    assert j.get_mult_hand(Mock(), Mock(), Mock(), Mock()) == 4


@pytest.mark.unit
@pytest.mark.parametrize("num_suit", list(range(0, 5)))
def test_greedy_joker(num_suit: int) -> None:
    j = GreedyJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    scored_cards = [_make_card(suit=Suit.DIAMONDS)] * num_suit
    assert j.get_mult_hand(scored_cards, Mock(), Mock(), Mock()) == 3 * num_suit


@pytest.mark.unit
@pytest.mark.parametrize("num_suit", list(range(0, 5)))
def test_lusty_joker(num_suit: int) -> None:
    j = LustyJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    scored_cards = [_make_card(suit=Suit.HEARTS)] * num_suit
    assert j.get_mult_hand(scored_cards, Mock(), Mock(), Mock()) == 3 * num_suit


@pytest.mark.unit
@pytest.mark.parametrize("num_suit", list(range(0, 5)))
def test_wrathful_joker(num_suit: int) -> None:
    j = WrathfulJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    scored_cards = [_make_card(suit=Suit.CLUBS)] * num_suit
    assert j.get_mult_hand(scored_cards, Mock(), Mock(), Mock()) == 3 * num_suit


@pytest.mark.unit
@pytest.mark.parametrize("num_suit", list(range(0, 5)))
def test_gluttonous_joker(num_suit: int) -> None:
    j = GluttonousJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    scored_cards = [_make_card(suit=Suit.SPADES)] * num_suit
    assert j.get_mult_hand(scored_cards, Mock(), Mock(), Mock()) == 3 * num_suit


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_score",
    [
        [[_make_card()], 0],
        [[_make_card()] * 2, 8],  # Pair
        [[_make_card()] * 3, 8],  # Three Set
        [[_make_card()] * 4, 8],  # Four Set
        [[_make_card()] * 5, 8],  # Flush Five Set
        [
            [
                _make_card(),
                _make_card(),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
            ],
            8,  # Full House
        ],
        [
            [
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS, rank=Rank.EIGHT),
            ],
            8,
        ],  # Flush
    ],
)
def test_jolly_joker(hand: Sequence[PlayingCard], expected_score: int) -> None:
    j = JollyJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    assert j.get_mult_hand(hand, Mock(), Mock(), Mock()) == expected_score


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_score",
    [
        [[_make_card()], 0],
        [[_make_card()] * 2, 0],  # Pair
        [[_make_card()] * 3, 12],  # Three Set
        [[_make_card()] * 4, 12],  # Four Set
        [[_make_card()] * 5, 12],  # Flush Five Set
        [
            [
                _make_card(),
                _make_card(),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
            ],
            12,  # Full House
        ],
        [
            [
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS, rank=Rank.EIGHT),
            ],
            12,
        ],  # Flush
    ],
)
def test_zany_joker(hand: Sequence[PlayingCard], expected_score: int) -> None:
    j = ZanyJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    assert j.get_mult_hand(hand, Mock(), Mock(), Mock()) == expected_score


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_score",
    [
        [[_make_card()], 0],
        [[_make_card()] * 2, 0],  # Pair
        [[_make_card()] * 4, 0],  # Four Set
        [[_make_card()] * 5, 0],  # Flush Five Set
        [
            [
                _make_card(),
                _make_card(),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
            ],
            10,  # Full House
        ],
        [
            [
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS, rank=Rank.EIGHT),
            ],
            0,
        ],  # Flush, but with the same ranks
        [
            [
                _make_card(rank=Rank.ACE),
                _make_card(rank=Rank.ACE),
                _make_card(rank=Rank.TEN),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
            ],
            10,
        ],  # Flush, but with different ranks
    ],
)
def test_mad_joker(hand: Sequence[PlayingCard], expected_score: int) -> None:
    j = MadJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    blind = Mock()
    blind.hand = hand
    assert j.get_mult_hand(Mock(), blind, Mock(), Mock()) == expected_score


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_score",
    [
        [[_make_card(Rank.ACE)], 0],
        [[_make_card(Rank.ACE)] * 2, 0],
        [
            [
                _make_card(Rank.ACE),
                _make_card(Rank.KING),
                _make_card(Rank.QUEEN),
                _make_card(Rank.JACK),
                _make_card(Rank.TEN),
            ],
            12,
        ],  # Royal Flush
        [
            [
                _make_card(Rank.NINE),
                _make_card(Rank.KING),
                _make_card(Rank.QUEEN),
                _make_card(Rank.JACK),
                _make_card(Rank.TEN),
            ],
            12,
        ],  # Stright Flush
        [[_make_card(Rank.ACE)] * 5, 0],  # Flush five
    ],
)
def test_crazy_joker(hand: Sequence[PlayingCard], expected_score: int) -> None:
    j = CrazyJoker()
    board = Mock()
    board.jokers = []
    assert j.joker_type == Type.ADDITIVE_MULT
    assert j.get_mult_hand(hand, Mock(), board, Mock()) == expected_score


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_score",
    [
        [[_make_card(Rank.ACE)], 0],
        [[_make_card(Rank.ACE)] * 2, 0],
        [
            [
                _make_card(Rank.ACE),
                _make_card(Rank.KING),
                _make_card(Rank.QUEEN),
                _make_card(Rank.JACK),
                _make_card(Rank.TEN),
            ],
            10,
        ],  # Royal Flush
        [
            [
                _make_card(Rank.NINE),
                _make_card(Rank.KING),
                _make_card(Rank.QUEEN),
                _make_card(Rank.JACK),
                _make_card(Rank.TEN),
            ],
            10,
        ],  # Stright Flush
        [[_make_card(Rank.ACE)] * 5, 10],  # Flush five
    ],
)
def test_droll_joker(hand: Sequence[PlayingCard], expected_score: int) -> None:
    j = DrollJoker()
    board = Mock()
    board.jokers = []
    assert j.joker_type == Type.ADDITIVE_MULT
    assert j.get_mult_hand(hand, Mock(), board, Mock()) == expected_score


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_chips",
    [
        [[_make_card(Rank.ACE)], 0],
        [[_make_card(Rank.ACE)] * 2, 50],
        [[_make_card(Rank.ACE)] * 3, 50],
        [[_make_card(Rank.ACE)] * 4, 50],
    ],
)
def test_sly_joker(hand: Sequence[PlayingCard], expected_chips: int) -> None:
    j = SlyJoker()
    assert j.joker_type == Type.CHIPS
    assert j.get_chips_hand(hand, Mock(), _make_board(), Mock()) == expected_chips


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_chips",
    [
        [[_make_card(Rank.ACE)], 0],
        [[_make_card(Rank.ACE)] * 2, 0],
        [[_make_card(Rank.ACE)] * 3, 100],
        [[_make_card(Rank.ACE)] * 4, 100],
    ],
)
def test_wily_joker(hand: Sequence[PlayingCard], expected_chips: int) -> None:
    j = WilyJoker()
    assert j.joker_type == Type.CHIPS
    assert j.get_chips_hand(hand, Mock(), _make_board(), Mock()) == expected_chips


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_chips",
    [
        [[_make_card(Rank.ACE)], 0],
        [[_make_card(Rank.ACE)] * 2, 0],
        [[_make_card(Rank.ACE)] * 3, 0],
        [[_make_card(Rank.ACE)] * 4, 0],
        [[_make_card(Rank.ACE), _make_card(Rank.ACE), _make_card(Rank.KING), _make_card(Rank.KING)], 80],
    ],
)
def test_clever_joker(hand: Sequence[PlayingCard], expected_chips: int) -> None:
    j = CleverJoker()
    assert j.joker_type == Type.CHIPS
    assert j.get_chips_hand(hand, Mock(), _make_board(), Mock()) == expected_chips


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_chips",
    [
        [[_make_card(Rank.ACE)], 0],
        [[_make_card(Rank.ACE)] * 2, 0],
        [
            [
                _make_card(Rank.ACE),
                _make_card(Rank.KING),
                _make_card(Rank.QUEEN),
                _make_card(Rank.JACK),
                _make_card(Rank.TEN),
            ],
            100,
        ],
    ],
)
def test_devious_joker(hand: Sequence[PlayingCard], expected_chips: int) -> None:
    j = DeviousJoker()
    assert j.joker_type == Type.CHIPS
    assert j.get_chips_hand(hand, Mock(), _make_board(), Mock()) == expected_chips


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_chips",
    [
        [[_make_card(Rank.ACE)], 0],
        [[_make_card(Rank.ACE)] * 2, 0],
        [[_make_card(Rank.ACE)] * 3, 0],
        [[_make_card(Rank.ACE)] * 4, 0],
        [[_make_card(Rank.ACE)] * 5, 80],
    ],
)
def test_crafty_joker(hand: Sequence[PlayingCard], expected_chips: int) -> None:
    j = CraftyJoker()
    assert j.joker_type == Type.CHIPS
    assert j.get_chips_hand(hand, Mock(), _make_board(), Mock()) == expected_chips


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_chips",
    [
        [[_make_card(Rank.ACE)], 20],
        [[_make_card(Rank.ACE)] * 2, 20],
        [[_make_card(Rank.ACE)] * 3, 20],
        [[_make_card(Rank.ACE)] * 4, 0],
        [[_make_card(Rank.ACE)] * 5, 0],
    ],
)
def test_half_joker(hand: Sequence[PlayingCard], expected_chips: int) -> None:
    j = HalfJoker()
    assert j.joker_type == Type.ADDITIVE_MULT
    assert j.get_mult_hand(hand, Mock(), Mock(), Mock()) == expected_chips


@pytest.mark.unit
def test_joker_stencil() -> None:
    j = JokerStencil()
    assert j.joker_type == Type.MULTIPLICATIVE

    board = Mock()
    joker = Mock()
    joker.edition.is_negative.return_value = False
    jokers = [joker] * 5
    board.jokers = jokers
    board.num_joker_slots = DEFAULT_NUM_JOKER_SLOTS
    assert j.get_multiplication(Mock(), Mock(), board, Mock()) == 0

    joker.edition.is_negative.return_value = True
    assert j.get_multiplication(Mock(), Mock(), board, Mock()) == DEFAULT_NUM_JOKER_SLOTS


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_hand",
    [
        [[_make_card(Rank.ACE)] * 4, PokerHandType.FLUSH],
        [
            [
                _make_card(Rank.TEN, suit=Suit.CLUBS),
                _make_card(Rank.NINE),
                _make_card(Rank.QUEEN),
                _make_card(Rank.JACK),
            ],
            PokerHandType.STRAIGHT,
        ],
        [
            [
                _make_card(Rank.KING),
                _make_card(Rank.QUEEN),
                _make_card(Rank.JACK),
                _make_card(Rank.TEN),
            ],
            PokerHandType.ROYAL_FLUSH,
        ],
        [
            [_make_card(Rank.ACE), _make_card(Rank.KING), _make_card(Rank.QUEEN), _make_card(Rank.JACK)],
            PokerHandType.ROYAL_FLUSH,
        ],
    ],
)
def test_four_fingers(hand: Sequence[PlayingCard], expected_hand: PokerHandType) -> None:
    j = FourFingers()
    assert j.joker_type == Type.EFFECT

    board = Mock()
    board.jokers = [j]
    flush = get_flush(hand, board)
    straight = get_straight(hand, board)
    royal = is_royal(hand, board)
    poker_hand: PokerHandType
    if royal:
        poker_hand = PokerHandType.ROYAL_FLUSH
    elif len(straight) > 0:
        poker_hand = PokerHandType.STRAIGHT
    elif len(flush) > 0:
        poker_hand = PokerHandType.FLUSH
    else:
        assert False
    assert expected_hand == poker_hand


@pytest.mark.unit
def test_chaos_the_clown() -> None:
    j = ChaosTheClown()
    shop = Shop()
    assert shop.get_reroll_price([]) == 5
    assert shop.get_reroll_price([j]) == 0
    shop.reroll([j])
    assert shop.get_reroll_price([j]) == 5
    shop.reroll([j])
    assert shop.get_reroll_price([j]) == 6


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_score",
    [
        [[_make_card()], 1],
        [[_make_card()] * 2, 2],  # Pair
        [[_make_card()] * 3, 2],  # Three Set
        [[_make_card()] * 4, 2],  # Four Set
        [[_make_card()] * 5, 2],  # Flush Five Set
        [
            [
                _make_card(),
                _make_card(),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
                _make_card(rank=Rank.KING),
            ],
            2,  # Full House
        ],
        [
            [
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS),
                _make_card(suit=Suit.CLUBS, rank=Rank.EIGHT),
            ],
            2,
        ],  # Flush
    ],
)
def test_the_duo(hand: Sequence[PlayingCard], expected_score: int) -> None:
    j = TheDuo()
    assert j.joker_type == Type.MULTIPLICATIVE
    assert j.get_multiplication(hand, Mock(), Mock(), Mock()) == expected_score


@pytest.mark.unit
def test_sampler_joker() -> None:
    jokers = [Joker(), HalfJoker(), JokerStencil(), FourFingers(), DeviousJoker()]
    common_count, uncommon_count, rare_count = 0, 0, 0
    for _ in range(100):
        joker = sample_jokers(jokers=jokers, vouchers=[], n_jokers=1)[0]
        assert joker.__class__ not in [j.__class__ for j in jokers]
        if joker.rarity == Rarity.COMMON:
            common_count += 1
        elif joker.rarity == Rarity.UNCOMMON:
            uncommon_count += 1
        else:
            rare_count += 1

    assert common_count > uncommon_count > rare_count

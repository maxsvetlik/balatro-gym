from collections.abc import Sequence
from unittest.mock import Mock, patch

import pytest

from balatro_gym.cards.interfaces import PlayingCard, Rank, SteelCard, Suit
from balatro_gym.cards.joker.effect_joker import ChaosTheClown, FourFingers, Pareidolia, SpaceJoker
from balatro_gym.cards.joker.joker import (
    AbstractJoker,
    BusinessCard,
    CleverJoker,
    CraftyJoker,
    CrazyJoker,
    DelayedGratification,
    DeviousJoker,
    DrollJoker,
    Egg,
    EvenSteven,
    Fibonacci,
    GluttonousJoker,
    GreedyJoker,
    GrosMichel,
    HalfJoker,
    Joker,
    JokerStencil,
    JollyJoker,
    LustyJoker,
    MadJoker,
    OddTodd,
    RideTheBus,
    ScaryFace,
    Scholar,
    SlyJoker,
    SteelJoker,
    Supernova,
    TheDuo,
    WilyJoker,
    WrathfulJoker,
    ZanyJoker,
)
from balatro_gym.cards.joker.utils import sample_jokers
from balatro_gym.cards.utils import get_flush, get_straight, is_royal
from balatro_gym.constants import DEFAULT_NUM_JOKER_SLOTS
from balatro_gym.game.shop import Shop
from balatro_gym.interfaces import BoardState, JokerBase, PokerHandType, Rarity, Type
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
    assert j.get_mult_hand(hand, blind, Mock(), Mock()) == expected_score


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
def test_fibonacci() -> None:
    j = Fibonacci()
    trigger_ranks = [Rank.ACE, Rank.TWO, Rank.THREE, Rank.FIVE, Rank.EIGHT]
    for rank in range(1, 14):
        if Rank.from_int(rank) in trigger_ranks:
            assert j.get_mult_card(_make_card(rank=Rank.from_int(rank)), Mock(), Mock()) == 8
        else:
            assert j.get_mult_card(_make_card(rank=Rank.from_int(rank)), Mock(), Mock()) == 0


@pytest.mark.unit
def test_steel_joker() -> None:
    j = SteelJoker()
    for n_steels in range(5):
        cards = [_make_card(enhancement=SteelCard())
                 for _ in range(n_steels)] + [_make_card() for _ in range(5 - n_steels)]
        board = Mock()
        board.deck = Mock(cards=cards)
        assert j.get_multiplication(Mock(), Mock(), board, Mock()) == 1 + 0.2 * n_steels


@pytest.mark.unit
def test_scary_face() -> None:
    j = ScaryFace()
    trigger_ranks = [Rank.KING, Rank.QUEEN, Rank.JACK]
    for rank in range(1, 14):
        if Rank.from_int(rank) in trigger_ranks:
            assert j.get_chips_card(_make_card(rank=Rank.from_int(rank)), Mock(), Mock(jokers=[])) == 30
        else:
            assert j.get_chips_card(_make_card(rank=Rank.from_int(rank)), Mock(), Mock(jokers=[])) == 0


@pytest.mark.unit
def test_abstract_joker() -> None:
    j = AbstractJoker()
    for n_jokers in range(5):
        board = Mock(jokers=[Joker()] * n_jokers)
        assert j.get_mult_hand(Mock(), Mock(), board, Mock()) == 3 * n_jokers


@pytest.mark.unit
@pytest.mark.parametrize(
    "num_discards,discards_left,expected_cash",
    [
        [5, 5, 10],
        [5, 4, 0],
        [2, 2, 4],
    ],
)
def test_delayed_gratification(num_discards: int, discards_left: int, expected_cash: int) -> None:
    j = DelayedGratification()
    board = Mock(num_discards=num_discards)
    blind = Mock(num_discards_remaining=discards_left)
    assert j.get_end_of_round_money(blind, board) == expected_cash


@pytest.mark.unit
def test_pareidolia() -> None:
    j = ScaryFace()
    for rank in range(1, 14):
        assert j.get_chips_card(_make_card(rank=Rank.from_int(rank)), Mock(), Mock(jokers=[Pareidolia()])) == 30


@pytest.mark.unit
def test_gros_michel() -> None:
    j = GrosMichel()
    board = Mock(jokers=[j])
    while len(board.jokers):
        assert j.get_mult_hand(Mock(), Mock(), board, Mock()) == 15
    assert len(board.jokers) == 0


@pytest.mark.unit
def test_even_steven() -> None:
    j = EvenSteven()
    trigger_ranks = [Rank.TWO, Rank.FOUR, Rank.SIX, Rank.EIGHT, Rank.TEN]
    for rank in range(1, 14):
        if Rank.from_int(rank) in trigger_ranks:
            assert j.get_mult_card(_make_card(rank=Rank.from_int(rank)), Mock(), Mock(jokers=[])) == 4
        else:
            assert j.get_mult_card(_make_card(rank=Rank.from_int(rank)), Mock(), Mock(jokers=[])) == 0


@pytest.mark.unit
def test_odd_todd() -> None:
    trigger_ranks = [Rank.ACE, Rank.NINE, Rank.SEVEN, Rank.FIVE, Rank.THREE]
    j = OddTodd()
    for rank in range(1, 14):
        if Rank.from_int(rank) in trigger_ranks:
            assert j.get_chips_card(_make_card(rank=Rank.from_int(rank)), Mock(), Mock(jokers=[])) == 31
        else:
            assert j.get_chips_card(_make_card(rank=Rank.from_int(rank)), Mock(), Mock(jokers=[])) == 0


@pytest.mark.unit
def test_scholar() -> None:
    j = Scholar()
    for rank in range(1, 14):
        card = _make_card(rank=Rank.from_int(rank))
        chips = j.get_chips_card(card, Mock(), Mock(jokers=[]))
        mult = j.get_mult_card(card, Mock(), Mock(jokers=[]))
        if Rank.from_int(rank) == Rank.ACE:
            assert chips == 20
            assert mult == 4
        else:
            assert chips == 0
            assert mult == 0


@pytest.mark.unit
def test_business_card() -> None:
    j = BusinessCard()
    face_ranks = [Rank.JACK, Rank.QUEEN, Rank.KING]
    # Patch random.random to control output
    with patch("random.random", return_value=0.4):
        for rank in face_ranks:
            card = _make_card(rank=rank)
            assert j.get_money_card(card, Mock(), Mock(jokers=[])) == 2
    with patch("random.random", return_value=0.6):
        for rank in face_ranks:
            card = _make_card(rank=rank)
            assert j.get_money_card(card, Mock(), Mock(jokers=[])) == 0
    # Non-face cards never give money
    for rank_idx in range(1, 11):
        card = _make_card(rank=Rank.from_int(rank_idx))
        assert j.get_money_card(card, Mock(), Mock(jokers=[])) == 0


@pytest.mark.unit
def test_supernova() -> None:
    j = Supernova()
    board = Mock()
    # Simulate get_poker_hand returning (None, PokerHandType.FLUSH)
    with patch("balatro_gym.cards.joker.joker.get_poker_hand", return_value=(None, PokerHandType.FLUSH)):
        board.get_amount_hand_scored = {PokerHandType.FLUSH: 42}
        result = j.get_mult_hand(Mock(), Mock(), board, Mock())
        assert result == 42


@pytest.mark.unit
def test_ride_the_bus() -> None:
    j = RideTheBus()
    board = Mock()
    board.jokers = []
    blind = Mock()
    # No face cards in hand
    hand = [_make_card(rank=Rank.FOUR), _make_card(rank=Rank.FIVE)]
    for i in range(1, 4):
        assert j.get_mult_hand(hand, blind, board, Mock()) == i
    # Add a face card, should reset
    hand_with_face = [_make_card(rank=Rank.KING)]
    assert j.get_mult_hand(hand_with_face, blind, board, Mock()) == 0
    # No face card again, should increment from 1
    assert j.get_mult_hand(hand, blind, board, Mock()) == 1


def test_space_joker_on_hand_scored_upgrade() -> None:
    joker = SpaceJoker()
    scored_hand = PokerHandType.FLUSH
    board = BoardState()
    # Patch random.random to never trigger upgrade
    with patch("random.random", return_value=0.5):
        joker.on_hand_scored([], Mock(), board, scored_hand)
        assert board.poker_hands[scored_hand.name].level == 1

    # Patch random.random to always trigger upgrade
    with patch("random.random", return_value=0.1):
        joker.on_hand_scored([], Mock(), board, scored_hand)
        assert board.poker_hands[scored_hand.name].level == 2


def test_egg_on_round_end_increases_sell_value() -> None:
    board = _make_board()
    egg = Egg()
    assert egg.base_cost == 4
    # Simulate end of round
    egg.on_round_end(board)
    assert egg.base_cost == 7
    egg.on_round_end(board)
    assert egg.base_cost == 10


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

from typing import Sequence
from unittest.mock import Mock

import pytest

from balatro_gym.cards.interfaces import (
    GlassCard,
    Holographic,
    MultCard,
    PlayingCard,
    Polychrome,
    Rank,
    RedSeal,
    SteelCard,
    StoneCard,
    Suit,
    WildCard,
)
from balatro_gym.cards.joker.joker import Joker, JollyJoker
from balatro_gym.game.scoring import _extract_largest_set, _get_max_rank, get_poker_hand, score_hand
from balatro_gym.interfaces import BlindState, JokerBase, PokerHandType
from test.utils import _make_board, _make_card

STRAIGHT_FLUSH = [PlayingCard(i, Suit.HEARTS) for i in range(1, 6)]
ROYAL_FLUSH = [PlayingCard(i, Suit.HEARTS) for i in [13, 12, 11, 10, 1]]
FLUSH_FIVE = [PlayingCard(10, Suit.HEARTS) for _ in range(5)]
FLUSH = [PlayingCard(i, Suit.SPADES) for i in [2, 5, 7, 11, 13]]
FLUSH_HOUSE = [PlayingCard(1, Suit.SPADES)] * 2 + [PlayingCard(5, Suit.SPADES)] * 3
STRAIGHT = [
    PlayingCard(1, Suit.HEARTS),
    PlayingCard(2, Suit.SPADES),
    PlayingCard(3, Suit.DIAMONDS),
    PlayingCard(4, Suit.SPADES),
    PlayingCard(5, Suit.HEARTS),
]
FIVE_SET = [
    PlayingCard(1, Suit.HEARTS),
    PlayingCard(1, Suit.SPADES),
    PlayingCard(1, Suit.DIAMONDS),
    PlayingCard(1, Suit.SPADES),
    PlayingCard(1, Suit.HEARTS),
]
FULL_HOUSE = [
    PlayingCard(1, Suit.HEARTS),
    PlayingCard(1, Suit.SPADES),
    PlayingCard(1, Suit.DIAMONDS),
    PlayingCard(4, Suit.SPADES),
    PlayingCard(4, Suit.HEARTS),
]
FOUR_SET = [
    PlayingCard(2, Suit.HEARTS),
    PlayingCard(2, Suit.SPADES),
    PlayingCard(2, Suit.DIAMONDS),
    PlayingCard(2, Suit.SPADES),
]
THREE_SET = [
    PlayingCard(2, Suit.HEARTS),
    PlayingCard(2, Suit.SPADES),
    PlayingCard(2, Suit.DIAMONDS),
]
TWO_PAIR = [
    PlayingCard(2, Suit.HEARTS),
    PlayingCard(2, Suit.SPADES),
    PlayingCard(5, Suit.DIAMONDS),
    PlayingCard(5, Suit.SPADES),
    PlayingCard(6, Suit.HEARTS),
]
PAIR = [
    PlayingCard(2, Suit.HEARTS),
    PlayingCard(2, Suit.SPADES),
    PlayingCard(5, Suit.DIAMONDS),
    PlayingCard(11, Suit.SPADES),
    PlayingCard(6, Suit.HEARTS),
]
HIGH_CARD = [
    PlayingCard(1, Suit.HEARTS),
    PlayingCard(11, Suit.SPADES),
]
WILD_FLUSH = [
    PlayingCard(10, Suit.HEARTS, WildCard()),
    PlayingCard(7, Suit.HEARTS, WildCard()),
    PlayingCard(5, Suit.HEARTS, WildCard()),
    PlayingCard(5, Suit.HEARTS, WildCard()),
    PlayingCard(7, Suit.HEARTS, WildCard()),
]


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_hand_type",
    [
        [STRAIGHT_FLUSH, PokerHandType.STRAIGHT_FLUSH],
        [ROYAL_FLUSH, PokerHandType.ROYAL_FLUSH],
        [FLUSH_FIVE, PokerHandType.FLUSH_FIVE],
        [FIVE_SET, PokerHandType.FIVE_SET],
        [STRAIGHT, PokerHandType.STRAIGHT],
        [FLUSH, PokerHandType.FLUSH],
        [FLUSH_HOUSE, PokerHandType.FLUSH_HOUSE],
        [FULL_HOUSE, PokerHandType.FULL_HOUSE],
        [FOUR_SET, PokerHandType.FOUR_SET],
        [THREE_SET, PokerHandType.THREE_SET],
        [TWO_PAIR, PokerHandType.TWO_PAIR],
        [PAIR, PokerHandType.PAIR],
        [HIGH_CARD, PokerHandType.HIGH_CARD],
        [WILD_FLUSH, PokerHandType.FLUSH],
    ],
)
def test_hand_types(hand: Sequence[PlayingCard], expected_hand_type: PokerHandType) -> None:
    _, hand_type = get_poker_hand(hand, _make_board())
    assert hand_type == expected_hand_type


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_val",
    [
        [[_make_card()], [(Rank.ACE, 1)]],
        [[_make_card()] * 2, [(Rank.ACE, 2)]],
        [[_make_card()] * 3, [(Rank.ACE, 3)]],
        [[_make_card()] * 4, [(Rank.ACE, 4)]],
        [[_make_card()] * 5, [(Rank.ACE, 5)]],
        [FULL_HOUSE, [(Rank.ACE, 3), (Rank.FOUR, 2)]],
    ],
)
def test_get_max_rank(hand: Sequence[PlayingCard], expected_val: tuple[Rank, int]) -> None:
    assert _get_max_rank(hand) == expected_val


@pytest.mark.unit
@pytest.mark.parametrize(
    "hand,expected_val",
    [
        [[_make_card()], [_make_card()] * 1],
        [[_make_card()] * 2, [_make_card()] * 2],
        [[_make_card()] * 3, [_make_card()] * 3],
        [[_make_card()] * 4, [_make_card()] * 4],
        [[_make_card()] * 5, [_make_card()] * 5],
        [
            [
                PlayingCard(1, Suit.HEARTS),
                PlayingCard(1, Suit.SPADES),
                PlayingCard(1, Suit.DIAMONDS),
                PlayingCard(4, Suit.SPADES),
                PlayingCard(4, Suit.HEARTS),
            ],
            [
                PlayingCard(1, Suit.HEARTS),
                PlayingCard(1, Suit.SPADES),
                PlayingCard(1, Suit.DIAMONDS),
            ],
        ],
    ],
)
def test_extract_largest_set(hand: Sequence[PlayingCard], expected_val: Sequence[PlayingCard]) -> None:
    assert _extract_largest_set(hand, _get_max_rank(hand)) == expected_val


@pytest.mark.unit
@pytest.mark.parametrize(
    "remaining_hand,played_hand,jokers,expected",
    [
        [
            [_make_card(enhancement=SteelCard())],
            [_make_card(rank=Rank.ACE)],
            [Joker()],
            88,
        ],  # Check order of multiplication and in-hand trigger
        [
            [_make_card(enhancement=SteelCard(), seal=RedSeal())],
            [_make_card(rank=Rank.ACE)],
            [Joker()],
            100,
        ],  # Check order of multiplication and in-hand trigger with retrigger
        [
            [],
            WILD_FLUSH,
            [],
            276,
        ],  # Check that wild cards get processed correctly as a whole
        [
            [],
            [_make_card(rank=Rank.ACE), _make_card(rank=Rank.ACE)],
            [JollyJoker()],
            320,
        ],  # Check order of multiplication for scored-hand based jokers
        [
            [],
            [_make_card(rank=Rank.ACE, enhancement=MultCard()), _make_card(rank=Rank.ACE)],
            [JollyJoker()],
            448,
        ],  # Check order of multiplication for scored-hand based jokers
        [
            [_make_card(enhancement=SteelCard())],
            [_make_card(rank=Rank.ACE, enhancement=MultCard())],
            [Joker()],
            184,
        ],  # Check order of joker and in-hand triggers
        [
            [_make_card(enhancement=SteelCard())],
            [_make_card(rank=Rank.ACE, enhancement=MultCard())],
            [Joker(edition=Polychrome())],
            276,
        ],  # Check order of joker effects, in-hand triggers and joker editions
        [
            [_make_card(enhancement=SteelCard())],
            [_make_card(rank=Rank.ACE, enhancement=MultCard(), edition=Holographic())],
            [Joker(edition=Polychrome())],
            636,
        ],  # Check order of joker effects, in-hand triggers, joker editions and playing card editions
        [
            [],
            [_make_card(enhancement=StoneCard())],
            [],
            55,
        ],  # Check scoring of stone
        [
            [],
            [_make_card(enhancement=StoneCard()), _make_card(rank=Rank.SIX), _make_card(rank=Rank.SIX)],
            [],
            144,
        ],  # Check scoring of stone in a scored hand
        [
            [],
            [_make_card(rank=Rank.SIX, enhancement=GlassCard()), _make_card(rank=Rank.SIX, enhancement=GlassCard())],
            [],
            176,
        ],  # Check scoring of glass card
    ],
)
def test_score_hand(
    remaining_hand: Sequence[PlayingCard],
    played_hand: Sequence[PlayingCard],
    jokers: Sequence[JokerBase],
    expected: float,
) -> None:
    # A lot of the low level scoring of cards is captured elsewhere. In order to test the scoring ordering logic
    # test a number of hands with known scores
    board = _make_board(jokers=list(jokers))
    blind = Mock(BlindState)
    blind.hand = remaining_hand
    assert score_hand(played_hand, board, blind) == expected

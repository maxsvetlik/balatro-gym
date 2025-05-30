from typing import Sequence
from unittest.mock import Mock

import pytest

from balatro_gym.cards.interfaces import PlayingCard, Rank, RedSeal, SteelCard, Suit, WildCard
from balatro_gym.cards.joker.joker import Joker, JollyJoker
from balatro_gym.game.scoring import _extract_largest_set, _get_max_rank, get_poker_hand, score_hand
from balatro_gym.interfaces import BlindState, PokerHandType
from test.utils import _make_board, _make_card

STRAIGHT_FLUSH = [PlayingCard(i, Suit.HEARTS, None, None, None) for i in range(1, 6)]
ROYAL_FLUSH = [PlayingCard(i, Suit.HEARTS, None, None, None) for i in [13, 12, 11, 10, 1]]
FLUSH_FIVE = [PlayingCard(10, Suit.HEARTS, None, None, None) for _ in range(5)]
FLUSH = [PlayingCard(i, Suit.SPADES, None, None, None) for i in [2, 5, 7, 11, 13]]
FLUSH_HOUSE = [PlayingCard(1, Suit.SPADES, None, None, None)] * 2 + [PlayingCard(5, Suit.SPADES, None, None, None)] * 3
STRAIGHT = [
    PlayingCard(1, Suit.HEARTS, None, None, None),
    PlayingCard(2, Suit.SPADES, None, None, None),
    PlayingCard(3, Suit.DIAMONDS, None, None, None),
    PlayingCard(4, Suit.SPADES, None, None, None),
    PlayingCard(5, Suit.HEARTS, None, None, None),
]
FIVE_SET = [
    PlayingCard(1, Suit.HEARTS, None, None, None),
    PlayingCard(1, Suit.SPADES, None, None, None),
    PlayingCard(1, Suit.DIAMONDS, None, None, None),
    PlayingCard(1, Suit.SPADES, None, None, None),
    PlayingCard(1, Suit.HEARTS, None, None, None),
]
FULL_HOUSE = [
    PlayingCard(1, Suit.HEARTS, None, None, None),
    PlayingCard(1, Suit.SPADES, None, None, None),
    PlayingCard(1, Suit.DIAMONDS, None, None, None),
    PlayingCard(4, Suit.SPADES, None, None, None),
    PlayingCard(4, Suit.HEARTS, None, None, None),
]
FOUR_SET = [
    PlayingCard(2, Suit.HEARTS, None, None, None),
    PlayingCard(2, Suit.SPADES, None, None, None),
    PlayingCard(2, Suit.DIAMONDS, None, None, None),
    PlayingCard(2, Suit.SPADES, None, None, None),
]
THREE_SET = [
    PlayingCard(2, Suit.HEARTS, None, None, None),
    PlayingCard(2, Suit.SPADES, None, None, None),
    PlayingCard(2, Suit.DIAMONDS, None, None, None),
]
TWO_PAIR = [
    PlayingCard(2, Suit.HEARTS, None, None, None),
    PlayingCard(2, Suit.SPADES, None, None, None),
    PlayingCard(5, Suit.DIAMONDS, None, None, None),
    PlayingCard(5, Suit.SPADES, None, None, None),
    PlayingCard(6, Suit.HEARTS, None, None, None),
]
PAIR = [
    PlayingCard(2, Suit.HEARTS, None, None, None),
    PlayingCard(2, Suit.SPADES, None, None, None),
    PlayingCard(5, Suit.DIAMONDS, None, None, None),
    PlayingCard(11, Suit.SPADES, None, None, None),
    PlayingCard(6, Suit.HEARTS, None, None, None),
]
HIGH_CARD = [
    PlayingCard(1, Suit.HEARTS, None, None, None),
    PlayingCard(11, Suit.SPADES, None, None, None),
]
WILD_FLUSH = [
    PlayingCard(10, Suit.HEARTS, WildCard(), None, None),
    PlayingCard(7, Suit.HEARTS, WildCard(), None, None),
    PlayingCard(5, Suit.HEARTS, WildCard(), None, None),
    PlayingCard(5, Suit.HEARTS, WildCard(), None, None),
    PlayingCard(7, Suit.HEARTS, WildCard(), None, None),
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
                PlayingCard(1, Suit.HEARTS, None, None, None),
                PlayingCard(1, Suit.SPADES, None, None, None),
                PlayingCard(1, Suit.DIAMONDS, None, None, None),
                PlayingCard(4, Suit.SPADES, None, None, None),
                PlayingCard(4, Suit.HEARTS, None, None, None),
            ],
            [
                PlayingCard(1, Suit.HEARTS, None, None, None),
                PlayingCard(1, Suit.SPADES, None, None, None),
                PlayingCard(1, Suit.DIAMONDS, None, None, None),
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
        # 11+5 * ((1 * 1.5) + 4)
        [
            [_make_card(enhancement=SteelCard(), seal=RedSeal())],
            [_make_card(rank=Rank.ACE)],
            [Joker()],
            100,
        ],  # Check order of multiplication and in-hand trigger with retrigger
        # 11+5 * ((1 * 1.5 * 1.5) + 4)
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
        # 2,10 = 11 + 11 + 10 * (10+8)
    ],
)
def test_score_hand(
    remaining_hand: Sequence[PlayingCard], played_hand: Sequence[PlayingCard], jokers: Sequence[Joker], expected: float
) -> None:
    # A lot of the low level scoring of cards is captured elsewhere. In order to test the scoring ordering logic
    # test a number of hands with known scores
    board = _make_board(jokers=jokers)
    blind = Mock(BlindState)
    blind.hand = remaining_hand
    assert score_hand(played_hand, board, blind) == expected

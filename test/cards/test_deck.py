import pytest

from balatro_gym.cards.decks import STANDARD_DECK
from balatro_gym.cards.interfaces import Deck, PlayingCard, Rank, Suit

ACE_HEART = PlayingCard(Rank.ACE, Suit.HEARTS, None, None, None)


@pytest.mark.unit
def test_deck_shuffle() -> None:
    initial_cards = STANDARD_DECK
    deck = Deck(initial_cards)
    assert deck.cards_remaining == initial_cards
    deck.shuffle()
    assert deck.cards_remaining != initial_cards


def _count_cards(deck: Deck, card: PlayingCard) -> int:
    total = 0
    for c in deck.cards_remaining:
        if c == card:
            total += 1
    return total


@pytest.mark.unit
def test_add() -> None:
    initial_cards = STANDARD_DECK
    deck = Deck(initial_cards)
    assert len(deck.cards_remaining) == len(initial_cards)
    assert _count_cards(deck, ACE_HEART) == 1
    deck.add([ACE_HEART])
    assert len(deck.cards_remaining) == len(initial_cards) + 1
    assert _count_cards(deck, ACE_HEART) == 2


@pytest.mark.unit
def test_deal() -> None:
    initial_cards = STANDARD_DECK
    deck = Deck(initial_cards)
    delt = deck.deal(5)
    assert len(initial_cards) == len(deck.cards_played) + len(deck.cards_remaining)
    assert delt == deck.cards_played


@pytest.mark.unit
def test_destroy() -> None:
    initial_cards = STANDARD_DECK
    deck = Deck(initial_cards)
    deck.destroy([])
    assert len(initial_cards) == len(deck.cards_remaining)
    destroy_cards = [ACE_HEART]
    deck.destroy(destroy_cards)
    assert len(initial_cards) == len(deck.cards_remaining) + len(destroy_cards)


@pytest.mark.unit
def test_eq_ordering() -> None:
    initial_cards = STANDARD_DECK
    deck1 = Deck(initial_cards)
    deck2 = Deck(initial_cards)
    assert deck1 == deck2
    deck2.shuffle()
    assert deck1 != deck2


@pytest.mark.unit
def test_eq_card_action() -> None:
    initial_cards = STANDARD_DECK
    deck1 = Deck(initial_cards)
    deck2 = Deck(initial_cards)
    assert deck1 == deck2
    deck1._cards_remaining.append(ACE_HEART)
    assert deck1 != deck2
    deck2._cards_remaining.append(ACE_HEART)
    assert deck1 == deck2


@pytest.mark.unit
def test_reset() -> None:
    initial_cards = STANDARD_DECK
    deck = Deck(initial_cards)
    assert deck.cards_remaining == initial_cards
    assert len(deck._cards_played) == 0
    deck.deal(1)
    assert deck.cards_remaining != initial_cards
    deck.reset()
    assert all(x in deck.cards_remaining for x in initial_cards)

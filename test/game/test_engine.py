import copy
from unittest.mock import patch

import pytest

from balatro_gym.game.engine import BoardAction, GameAction, GameState, HandAction, Run
from balatro_gym.interfaces import BoardState


@pytest.mark.unit
def test_game_reset() -> None:
    run = Run()
    run.game_reset()
    assert run.game_state == GameState.IN_BLIND_SELECT
    assert run.blind_state is None
    assert run.board_state == BoardState()
    assert len(run.blinds) > 0
    assert run.action_counter == 0

@pytest.mark.unit
def test_process_board_action_state_transition() -> None:
    run = Run()
    assert run.game_state == GameState.IN_BLIND_SELECT
    run._process_board_action(GameAction(BoardAction.START_ROUND, []))
    assert run.game_state == GameState.IN_ANTE

    run._process_board_action(GameAction(BoardAction.VIEW_SHOP, []))
    assert run.game_state == GameState.IN_SHOP

    run._process_board_action(GameAction(BoardAction.NEXT_ROUND, []))
    assert run.game_state == GameState.IN_BLIND_SELECT


@pytest.mark.unit
def test_process_hand_action_state_transition_win() -> None:
    run = Run()
    assert run.game_state == GameState.IN_BLIND_SELECT
    run._process_board_action(GameAction(BoardAction.START_ROUND, []))
    assert run.blind_state
    req_score = run.blind_state.required_score
    with patch("balatro_gym.game.engine.score_hand", lambda x,y,z: req_score+1):
        assert run._process_hand_action(GameAction(HandAction.SCORE_HAND, [run.blind_state.hand[0]])) is True

@pytest.mark.unit
def test_process_hand_action_state_transition_loss() -> None:
    run = Run()
    assert run.game_state == GameState.IN_BLIND_SELECT
    run._process_board_action(GameAction(BoardAction.START_ROUND, []))
    assert run.blind_state
    num_hands = run.blind_state.num_hands_remaining
    terminal = False
    with patch("balatro_gym.game.engine.score_hand", lambda x,y,z: 0):
        for i in range(num_hands):
            terminal &= run._process_hand_action(GameAction(HandAction.SCORE_HAND, [run.blind_state.hand[0]]))
    assert terminal is False

@pytest.mark.unit
def test_process_hand_action_discard() -> None:
    run = Run()
    run._process_board_action(GameAction(BoardAction.START_ROUND, []))
    assert run.blind_state
    num_discards = run.blind_state.num_discards_remaining
    for i in range(1, num_discards+1):
        run._process_hand_action(GameAction(HandAction.DISCARD, [run.blind_state.hand[0]]))
        assert num_discards == run.blind_state.num_discards_remaining + i

    # Check that discards aren't processed after running out
    old_blind_state = copy.deepcopy(run.blind_state)
    run._process_hand_action(GameAction(HandAction.DISCARD, [run.blind_state.hand[0]]))
    assert old_blind_state == run.blind_state

@pytest.mark.unit
def test_setup_ante() -> None:
    run = Run()
    assert run.board_state.ante_num == 0
    run._setup_ante()
    assert run.board_state.ante_num == 1


@pytest.mark.unit
def test_setup_round() -> None:
    run = Run()
    assert run.board_state.round_num == 0
    assert run.blind_state is None
    run._setup_round()
    assert run.board_state.round_num == 1
    assert run.blind_state is not None

from balatro_gym.interfaces import BoardState
import pytest

from balatro_gym.game.engine import GameState, Run

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
def test_process_board_action() -> None:
    pass

@pytest.mark.unit
def test_process_hand_action() -> None:
    pass

@pytest.mark.unit
def test_end_ante() -> None:
    pass

@pytest.mark.unit
def test_setup_ante() -> None:
    pass

@pytest.mark.unit
def test_setup_step() -> None:
    pass

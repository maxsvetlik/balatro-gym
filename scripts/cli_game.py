from typing import Sequence
from balatro_gym.game.engine import BoardAction, GameAction, GameActionTypes, GameState, Run, RunObservation
from pprint import pprint


def _cards_valid(cards: Sequence[str]) -> bool:
    return all(isinstance(x, int) for x in cards) and len(cards) > 0


if __name__ == "__main__":
    run = Run()
    done = False

    while not done:
        obs = run.step(None)
        print("The board state is:")
        pprint(obs)
        if obs.blind_state is not None:
            print(f"Your hand is:")
            pprint(obs.blind_state.hand)
            cards: list[str] = []
            while not _cards_valid(cards):
                cards = input(
                    "Please enter the numbers of the cards you want to select, separated by a space: "
                ).split()
            action = ""
            while action not in ["DISCARD", "PLAY"]:
                action = input("Would you like to DISCARD or PLAY? : ")

        elif obs.game_state == GameState.IN_BLIND_SELECT:
            print("You are in blind selection.")
            input("You must select a blind. Press anything to continue.")
            run.step(GameAction(BoardAction.START_ANTE, []))

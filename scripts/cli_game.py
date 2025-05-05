from pprint import pprint
from typing import Sequence

from balatro_gym.game.engine import BoardAction, GameAction, GameState, HandAction, Run


def _cards_idxs(cards: Sequence[str]) -> Sequence[int]:
    card_idxs = []
    for card in cards:
        try:
            card_idxs.append(int(card))
        except ValueError:
            pass
    return card_idxs

if __name__ == "__main__":
    run = Run()
    done = False

    while not done:
        obs = run.step(None)
        print("The board state is:")
        pprint(obs)
        if obs.blind_state is not None:
            print("Your hand is:")
            for i, card in enumerate(obs.blind_state.hand):
                print(f"{i}: {card}")
            idxs: Sequence[int] = []
            while not idxs:
                idxs_str = input(
                    "Please enter the numbers of the cards you want to select, separated by a space: "
                ).split()
                idxs = _cards_idxs(idxs_str)
            cards = [obs.blind_state.hand[idx] for idx in idxs]

            action_str = ""
            while action_str.lower() not in ["d", "p"]:
                action_str = input("Would you like to (D)ISCARD or (P)LAY? : ")
            if action_str == "d":
                action = HandAction.DISCARD
            else:
                action = HandAction.SCORE_HAND
            run.step(GameAction(action, cards))
                

        elif obs.game_state == GameState.IN_BLIND_SELECT:
            print("You are in blind selection.")
            input("You must select a blind. Press anything to continue.")
            run.step(GameAction(BoardAction.START_ANTE, []))

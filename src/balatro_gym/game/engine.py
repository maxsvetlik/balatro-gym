import dataclasses
from enum import Enum, IntEnum, auto
from typing import Optional, Sequence, Union

from balatro_gym.game.scoring import score_hand

from ..cards.decks import discard
from ..cards.interfaces import PlayingCard
from ..interfaces import BlindState, BoardState
from .blinds import BlindInfo, generate_run_blinds, get_blind_required_score
from .shop import Shop, ShopState


class HandAction(IntEnum):
    DISCARD = auto()
    SCORE_HAND = auto()
    # USE_CONSUMABLE = auto()
    # SELL_CONSUMABLE = auto()
    # SELL_JOKER = auto()


class BoardAction(IntEnum):
    START_ANTE = auto()
    VIEW_SHOP = auto()
    NEXT_ROUND = auto()
    # USE_CONSUMABLE = auto()
    # SELL_CONSUMABLE = auto()
    # SELL_JOKER = auto()
    # SET_JOKER_ORDER = auto()
    # REROLL = auto()
    # BUY_CARD = auto()


class GameState(Enum):
    IN_ANTE = auto()
    IN_BLIND_SELECT = auto()
    GENERATE_SHOP = auto()
    IN_SHOP = auto()
    # IN_CONSUMABLE_REDEEM = auto()


@dataclasses.dataclass
class RunObservation:
    game_state: GameState
    board_state: BoardState
    shop_state: Optional[ShopState]
    blind_state: Optional[BlindState]
    action_counter: int
    done: bool


GameActionTypes = Union[HandAction, BoardAction]


@dataclasses.dataclass
class GameAction:
    action_type: GameActionTypes
    selected_playing: Sequence[PlayingCard]
    # selected_consummable: Sequence[Consummable]


class Run:
    _game_state: GameState
    _board_state: BoardState
    _shop_state: Optional[ShopState]
    _blind_state: Optional[BlindState]
    _run_blinds: Sequence[BlindInfo]
    _action_counter: int
    _shop: Shop

    def __init__(self) -> None:
        self.game_reset()

    @property
    def game_state(self) -> GameState:
        return self._game_state

    @property
    def board_state(self) -> BoardState:
        return self._board_state

    @property
    def blind_state(self) -> Optional[BlindState]:
        return self._blind_state

    @property
    def blinds(self) -> Sequence[BlindInfo]:
        return self._run_blinds

    @property
    def action_counter(self) -> int:
        return self._action_counter

    @property
    def shop_state(self) -> Optional[ShopState]:
        return self._shop_state

    def game_reset(self) -> None:
        # Resets the run to the start, with new randomness
        self._game_state = GameState.IN_BLIND_SELECT
        self._blind_state = None
        self._shop_state = None
        self._board_state = BoardState()
        self._run_blinds = generate_run_blinds()
        self._action_counter = 0
        self._shop = Shop()

    def _end_ante(self) -> None:
        # Call at the end of the ante
        self._board_state.deck.reset()
        self._blind_state = None

    def _process_board_action(self, action: GameAction) -> None:
        if action.action_type == BoardAction.START_ANTE:
            if self._game_state is GameState.IN_BLIND_SELECT:
                self._game_state = GameState.IN_ANTE
                self._setup_ante()
            else:
                return None
        elif action.action_type == BoardAction.VIEW_SHOP:
            self._shop_state = self._shop.generate_shop_state(self._board_state.round_num)
            self._game_state = GameState.IN_SHOP
        elif action.action_type == BoardAction.NEXT_ROUND:
            self._game_state = GameState.IN_BLIND_SELECT

    def _process_hand_action(self, action: GameAction) -> bool:
        if len(action.selected_playing) == 0:
            return False
        if self._game_state is GameState.IN_ANTE:
            assert self._blind_state is not None
            if action.action_type == HandAction.DISCARD:
                if self._blind_state.num_discards_reamining == 0:
                    return False
                new_cards = self._board_state.deck.deal(len(action.selected_playing))
                self._blind_state.hand = discard(self._blind_state.hand, action.selected_playing, new_cards)
                self._blind_state.num_discards_reamining -= 1

            if action.action_type == HandAction.SCORE_HAND:
                hand_score = score_hand(action.selected_playing, self._board_state, self._blind_state)
                self._blind_state.current_score += int(hand_score)
                self._blind_state.num_hands_remaining -= 1

                if self._blind_state.required_score <= self._blind_state.current_score:
                    # Ante is won. End ante and transition to next state
                    self._end_ante()
                    self._game_state = GameState.GENERATE_SHOP
                    return True

                if self._blind_state.num_hands_remaining < 0:
                    # Game loss
                    return True

                new_cards = self._board_state.deck.deal(len(action.selected_playing))
                self._blind_state.hand = discard(self._blind_state.hand, action.selected_playing, new_cards)

        return False

    def _setup_ante(self) -> None:
        self._board_state.ante_num += 1
        initial_hand = self._board_state.deck.deal(self._board_state.hand_size)
        req_score = get_blind_required_score(self._board_state.ante_num)
        self._blind_state = BlindState(
            initial_hand, req_score, 0, self._board_state.num_hands, self._board_state.num_discards
        )
        self._shop_state = None

    def step(self, action: Optional[GameAction]) -> RunObservation:
        done = False

        if action is not None:
            if isinstance(action.action_type, HandAction):
                done = self._process_hand_action(action)
            else:
                self._process_board_action(action)

        self._action_counter += 1
        return RunObservation(
            self._game_state, self._board_state, self._shop_state, self._blind_state, self._action_counter, done)

from dataclasses import dataclass
from enum import Enum


@dataclass
class Hand:
    fingers: int = 1

    def add(self, n: int):
        self.fingers += n
        if self.fingers > 5:
            self.fingers = 0
        


@dataclass
class Player:
    name: str
    is_human: bool = False
    left_hand: Hand = Hand()
    right_hand: Hand = Hand()


@dataclass
class GameState:
    human: Player
    computer: Player
    turn: int

    @property
    def current_player(self) -> Player:
        return self.human if self.turn % 2 == 0 else self.computer
    

    @property
    def other_player(self) -> Player:
        return self.human if self.turn % 2 != 0 else self.computer
    


class Action(Enum):
    ADD_LEFT_TO_LEFT = 1
    ADD_LEFT_TO_RIGHT = 2
    ADD_RIGHT_TO_LEFT = 3
    ADD_RIGHT_TO_RIGHT = 4
    SPLIT = 5



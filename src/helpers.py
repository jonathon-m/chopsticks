import math
import random
from typing import List
from models import Action
from constants import WAIT_MESSAGES
import time
from rich.progress import track

# game state
# [human_left, human_right, comp_left, comp_right, turn]

def human_left(game_state: List[int]):
     return game_state[0]

def human_right(game_state: List[int]):
     return game_state[1]

def comp_left(game_state: List[int]):
     return game_state[2]

def comp_right(game_state: List[int]):
     return game_state[3]

def turn(game_state: List[int]) -> bool:
    return game_state[4]



def is_game_over(game_state: List[int]) -> bool:
        return human_left(game_state) + human_right(game_state) == 0 or comp_left(game_state) + comp_right(game_state) == 0


def winner(name: str, game_state: List[int]) -> bool:
        if human_left(game_state) + human_right(game_state) == 0:
             return "Computer"
        else:
             return name


def new_game() -> List[int]:
    return [1, 1, 1, 1, random.randint(0, 1)]


def pretend_to_think():
    wait = random.randint(1, 3)
    message_index = random.randint(0, len(WAIT_MESSAGES)-1)
    for _ in track(range(wait), description=WAIT_MESSAGES[message_index]):
        time.sleep(1) 


def get_player_indexes(game_state: List[int]):
    curr_offset = (game_state[4] % 2) * 2
    other_offset = ((game_state[4] + 1) % 2) * 2
    curr_left_index = 0 + curr_offset
    curr_right_index = 1 + curr_offset
    other_left_index = 0 + other_offset
    other_right_index = 1 + other_offset
    return curr_left_index, curr_right_index, other_left_index, other_right_index


def get_available_moves(game_state: List[int]) -> List[Action]:
    available_moves = []
    curr_left_index, curr_right_index, other_left_index, other_right_index = get_player_indexes(game_state)
    if game_state[curr_left_index] > 0:
        if game_state[other_left_index] > 0:
            available_moves.append(Action.ADD_LEFT_TO_LEFT)
        if game_state[other_right_index] > 0:
            available_moves.append(Action.ADD_LEFT_TO_RIGHT)
    if game_state[curr_right_index] > 0:
        if game_state[other_left_index] > 0:
               available_moves.append(Action.ADD_RIGHT_TO_LEFT)
        if game_state[other_right_index] > 0:
               available_moves.append(Action.ADD_RIGHT_TO_RIGHT)
    if (game_state[curr_left_index] == 0 and game_state[curr_right_index] > 1) or (game_state[curr_right_index] == 0 and game_state[curr_left_index] > 1):
         available_moves.append(Action.SPLIT)
         
    return available_moves
    

def grade_game_state(game_state: List[int], max_depth = 5):

    score_mulitplier = max_depth * max_depth

    DEATH_PENALTY = 100 * score_mulitplier
    WIN_SCORE = -20 * score_mulitplier

    
    curr_left, curr_right, other_left, other_right = get_player_indexes(game_state)

    if game_state[other_left] == 0 and game_state[other_right] == 0:
        return WIN_SCORE if game_state[4] % 2 == 1 else DEATH_PENALTY
    
    if game_state[curr_left] == 0 and game_state[curr_right] == 0:
        return DEATH_PENALTY if game_state[4] % 2 == 1 else WIN_SCORE
    
    if max_depth == 0:
        return 0
    
    available_moves = get_available_moves(game_state)

    return sum([grade_game_state(make_move(game_state, move), max_depth - 1) for move in available_moves])



def get_best_move(game_state: List[int]) -> Action:
    available_moves = get_available_moves(game_state)

    move_scores = [(move, grade_game_state(make_move(game_state, move))) for move in available_moves]
    best_move = min(move_scores, key=lambda x: x[1])[0]

    return best_move


def add_max_five(a: int, b: int):
     finger_sum = a + b
     return finger_sum if finger_sum < 5 else 0

     

def make_move(game_state: List[int], action: Action) -> List[int]:
    next_game_state = [i for i in game_state]
    curr_left, curr_right, other_left, other_right = get_player_indexes(game_state)

    match action:
         case Action.ADD_LEFT_TO_LEFT:
              next_game_state[other_left] = add_max_five(game_state[curr_left], game_state[other_left])
         case Action.ADD_LEFT_TO_RIGHT:
              next_game_state[other_right] = add_max_five(game_state[curr_left], game_state[other_right])
         case Action.ADD_RIGHT_TO_LEFT:
              next_game_state[other_left] = add_max_five(game_state[curr_right], game_state[other_left])
         case Action.ADD_RIGHT_TO_RIGHT:
              next_game_state[other_right] = add_max_five(game_state[curr_right], game_state[other_right])
         case Action.SPLIT:
              if game_state[curr_left] == 0:
                   next_game_state[curr_left] = math.floor(game_state[curr_right] / 2)
                   next_game_state[curr_right] = math.ceil(game_state[curr_right] / 2)
              else:
                   next_game_state[curr_left] = math.floor(game_state[curr_left] / 2)
                   next_game_state[curr_right] = math.ceil(game_state[curr_left] / 2)
    next_game_state[4] += 1
    return next_game_state
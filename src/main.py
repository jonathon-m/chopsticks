
from typing import List
from models import Action

from rich.prompt import Prompt, Confirm, IntPrompt

from helpers import (
    pretend_to_think, get_available_moves, make_move, is_game_over,
    get_best_move, new_game, winner
)
from view import GameView, print
from constants import RESPONSE_TO_ACTION


def play_game(name: str):
    current_game_state = new_game()
    game_loop(name, current_game_state)


def ask_for_move(game_state: List[int]) -> Action:
    available_moves = get_available_moves(game_state)
    print("Available moves:")
    for action, response in RESPONSE_TO_ACTION.items():
        if action in available_moves:
            print(response)
    move = IntPrompt.ask(
        prompt="Choose your next move:",
        choices=[str(action.value) for action in RESPONSE_TO_ACTION.keys() if action in available_moves],
    )

    return Action(move)


def print_game(name: str, game_state: List[int]):
    print("----------------------------------")    
    print("_Computer_")
    print(f"**L {game_state[2]} - R {game_state[3]}**")
    print(f"_{name}_")
    print(f"**L {game_state[0]} - R {game_state[1]}**")
    print("----------------------------------")    

def game_loop(name: str, game_state: List[int]):
    while not is_game_over(game_state):
        print_game(name, game_state)
        move: Action
        if game_state[4] % 2 == 0:
            move = ask_for_move(game_state)
        else:
            pretend_to_think()
            move = get_best_move(game_state)

        game_state = make_move(game_state, move)
    print_game(name, game_state)
    print(f"Winner is {winner(name, game_state)}!")


def replay(name):
    will_play = Confirm.ask("Would you like to play chopsticks?", default=True)
    if will_play:
        play_game(name)
        replay(name)
    else:
        print("Goodbye")
    

def main():

    print('# Chopsticks')
    print('## by Jon')
    name = Prompt.ask("What is your name?", default="Jon")
    print(f"Welcome _{name}_")
    replay(name)


if __name__ == "__main__":
    main()
from models import Hand, GameState
from rich.markdown import Markdown

from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align

from rich.console import Console


console = Console()


class GameView():    

    def __init__(self, game_state: GameState, player_name: str):
        self.player_name = player_name
        self.game_state = game_state
        self.layout = self.get_game_layout()
        self.update()

    def __enter__(self):
        
        console.clear()
        with Live(self.layout, refresh_per_second=4):
            return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass


    def get_game_layout(self):

        layout = Layout()
        layout.split_column(
            Layout(name="upper", renderable=Markdown("# Computer"), size=3),
            Layout(name="computer"),
            Layout(name="player"),
            Layout(name="lower", renderable=Markdown(f"# {self.player_name}"))
        )
        layout["computer"].split_row(
            Layout(name="left"),
            Layout(name="right"),
        )
        layout["player"].split_row(
            Layout(name="left"),
            Layout(name="right"),
        )
        return layout

    def update(self):
        self.layout["player"]["left"].update(get_aligned_panel_for_hand(self.game_state.human.left_hand))
        self.layout["player"]["right"].update(get_aligned_panel_for_hand(self.game_state.human.right_hand))
        self.layout["computer"]["left"].update(get_aligned_panel_for_hand(self.game_state.computer.left_hand))
        self.layout["computer"]["right"].update(get_aligned_panel_for_hand(self.game_state.computer.right_hand))


def print(markdown: str):
    console.print(Markdown(markdown))


def get_aligned_panel_for_hand(hand: Hand):
    return Align.center(Panel(str(hand.fingers)), vertical="middle")





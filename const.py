from typing import List, Tuple, Dict

WIDTH: int, HEIGHT: int = 10, 20
TILE: int = 35
GAME_RES: tuple[int, int] = WIDTH * TILE, HEIGHT * TILE
RES: tuple[int, int] = 750, 750
FPS: int = 60

MAIN_MUSIC_PATH: str = 'music/Tetris_theme.ogg'

FIGURES_POSITIONS: List[List[Tuple[int, int]]] = [
    [(-2, -1), (-1, -1), (0, -1), (1, -1)],
    [(0, -1), (-1, -1), (-1, 0), (0, 0)],
    [(-1, -1), (0, 0), (-1, 0), (0, 1)],
    [(0, -1), (0, 0), (-1, 0), (-1, 1)],
    [(0, 0), (0, -1), (0, 1), (-1, -1)],
    [(0, -1), (-1, -1), (-1, 0), (-1, 1)],
    [(0, 0), (0, -1), (0, 1), (-1, 0)],
]

SCORES: Dict[int, int] = {
    0: 0,
    1: 100,
    2: 300,
    3: 900,
    4: 2000
}

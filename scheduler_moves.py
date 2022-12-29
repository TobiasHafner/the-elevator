# This enum contains all moves that can be suggested by the scheduler
from enum import Enum

class Moves(Enum):
    UP = 0
    DOWN = 1
    STOP = 2
    STAY = 3
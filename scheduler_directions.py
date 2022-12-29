# This enum contains all moves that can be suggested by the scheduler
from enum import Flag

class Directions(Flag):
    UP = True
    DOWN = False
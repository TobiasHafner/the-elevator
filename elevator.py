# This class represents an elevator that can move, open dors and tell it's current load

from safety_error import SafetyError

class Elevator:
    def __init__(self, floor_count, max_load):
        # number of floors
        self.FLOOR_COUNT = floor_count
        # max load of elevator
        self.MAX_LOAD = max_load
        # current position of the elevator
        self.position = 0
        # current load of the elevator
        self.load = 0
        # state of the elevator doors
        self.doors_open = False
    
    def move_up(self):
        if (self.position == self.FLOOR_COUNT):
            raise SafetyError("Elevator is at topmost floor! Moving up is not permitted!")
        # upadate position
        self.position += 1

    def move_down(self):
        if (self.position == 0):
            raise SafetyError("Elevator is at bottommost floor! Moving down is not permitted!")
        # update position
        self.position -= 1

    def close_doors(self):
        if (self.load > self.MAX_LOAD):
            raise SafetyError("Current elevator weight exceeds maximum permitted load!")
        self.doors_open = False

    def open_doors(self):
        self.doors_open = True

    def get_door_state(self):
        return self.doors_open

    def get_floor_count(self):
        return self.FLOOR_COUNT

    def get_max_load(self):
        return self.MAX_LOAD

    def get_load(self):
        return self.load

    def inc_load(self, amount):
        self.load += amount
        return

    def dec_load(self, amount):
        self.load -= amount
        return

    def get_position(self):
        return self.position
    
    def __repr__(self):
        return f"Elevator({self.FLOOR_COUNT}, {self.MAX_LOAD})"

    # string representation of the elevator
    def __str__(self):
        format_string = '{:<3} {:<3}\n'
        string = f'ELEVATOR:\nLOAD: {self.load} kg of {self.MAX_LOAD} kg.\n'
        for floor in range(self.FLOOR_COUNT, -1, -1):
            # elevator is at specified floor
            if (self.position == floor):
                # select symbol dependant on door state
                doors = ' ' if self.doors_open else 'X'
                cart = f'[{doors}]'
                string += format_string.format(floor, cart)
                continue
            # no elevator at that floor
            string += format_string.format(floor, ' | ')
        return string

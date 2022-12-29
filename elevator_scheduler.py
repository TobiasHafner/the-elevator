# This class schedules an elevator based on user input

from elevator import Elevator
from collections import deque
from scheduler_moves import Moves
from scheduler_directions import Directions

# Weight of an average person
PERSON_WEIGHT = 80

class Scheduler:
    def __init__(self, elevator: Elevator):
        # elevator data
        self.FLOOR_COUNT = elevator.get_floor_count()
        self.MAX_LOAD = elevator.get_max_load()
        self.elevator = elevator

        # scheduling data
        self.direction = True
        self.up_requests = [deque([]) for _ in range(self.FLOOR_COUNT + 1)]
        self.down_requests = [deque([]) for _ in range(self.FLOOR_COUNT + 1)]
        self.stop_requests = [0] * (self.FLOOR_COUNT + 1)
        # chase mode for scan
        self.is_chasing = False
    
    def get_next_move(self):
        # rest if no requests
        if (not self.has_pending_requests()):
            return Moves.STAY
        # chasing mode
        if (self.is_chasing):
            return self.run_chase_mode()
        # normal operation
        return self.run_normal_operation()        

    def run_chase_mode(self):
        # chasing up
        if (self.direction and self.get_outmost_request(Directions.UP) > self.elevator.get_position()):
            return Moves.UP
        # chasing down
        if ((not self.direction) and self.get_outmost_request(Directions.DOWN) < self.elevator.get_position()):
            return Moves.DOWN
        # leave chase mode
        self.is_chasing = False
        # continue in other direction
        self.direction = not self.direction
        # handle request
        if (self.direction):
            self.handle_down_destinations()
        else:
            self.handle_up_destinations()
        return Moves.STOP

    def run_normal_operation(self):
        # moving up
        if (self.direction):
            # upwards entry or stop request at current floor
            if ((self.up_requests[self.elevator.get_position()]
                and self.not_full())
                or self.stop_requests[self.elevator.get_position()]):

                self.handle_up_destinations()
                return Moves.STOP
            # check for requests further up
            if (self.preview(Directions.UP)):
                return Moves.UP
            # handled all up requests start chasing for down requests
            else:
                self.is_chasing = True
                return self.run_chase_mode()
        # moving down
        else:
            # downwards entry request at current floor
            if ((self.down_requests[self.elevator.get_position()]
                and self.not_full())
                or self.stop_requests[self.elevator.get_position()]):

                self.handle_down_destinations()
                return Moves.STOP
            # check for requests further down
            if (self.preview(Directions.DOWN)):
                return Moves.DOWN
            else:
                self.is_chasing = True
                return self.run_chase_mode()

    def add_up_destinations(self):
        while self.up_requests[self.elevator.get_position()] and self.not_full():
            destination = self.up_requests[self.elevator.get_position()].popleft()
            self.stop_requests[destination] += 1

        # ----------------------------------------------------------------------
        #   Update elevator weight model:
            self.elevator.inc_load(PERSON_WEIGHT)
        #-----------------------------------------------------------------------

    def add_down_destinations(self):
        while self.down_requests[self.elevator.get_position()] and self.not_full():
            destination = self.down_requests[self.elevator.get_position()].popleft()
            self.stop_requests[destination] += 1

        # ----------------------------------------------------------------------
        #   Update elevator weight model:
            self.elevator.inc_load(PERSON_WEIGHT)
        #-----------------------------------------------------------------------

    def handle_down_destinations(self):
    # --------------------------------------------------------------------------
    #   Update elevator weight model:
        self.elevator.dec_load(
            self.stop_requests[self.elevator.get_position()] * PERSON_WEIGHT)
    #---------------------------------------------------------------------------
        self.stop_requests[self.elevator.get_position()] = 0
        self.add_down_destinations()

    def handle_up_destinations(self):
    # --------------------------------------------------------------------------
    #   Update elevator weight model:
        self.elevator.dec_load(
            self.stop_requests[self.elevator.get_position()] * PERSON_WEIGHT)
    #---------------------------------------------------------------------------
        self.stop_requests[self.elevator.get_position()] = 0
        self.add_up_destinations()

    def preview(self, move_up):
        result = False
        # preview requests for travelling up or leaving
        if (move_up):
            for floor in range(self.elevator.get_position(), self.FLOOR_COUNT + 1):
                result |= bool(self.up_requests[floor])
                result |= self.stop_requests[floor] != 0
            return result
        # preview requests for travelling down or leaving
        else:
            for floor in range(self.elevator.get_position()):
                result |= bool(self.down_requests[floor])
                result |= self.stop_requests[floor] != 0
            return result

    def get_outmost_request(self, move_up):
        if (move_up):
            outmost = self.elevator.get_position()
            for floor in range(self.elevator.get_position(), self.FLOOR_COUNT + 1):
                if(self.down_requests[floor] and floor > outmost):
                    outmost = floor
            return outmost
        else:
            outmost = self.elevator.get_position()
            for floor in range(0, self.elevator.get_position()):
                if(self.up_requests[floor] and floor < outmost):
                    outmost = floor
            return outmost

    def has_pending_requests(self):
        result = False
        for floor in range(self.FLOOR_COUNT + 1):
            result |= bool(self.up_requests[floor])
            result |= bool(self.down_requests[floor])
            result |= self.stop_requests[floor] != 0
        return result

    def handle_request(self, start, end):
        # log move request
        if (end > start):
            self.up_requests[start].append(end)
        else:
            self.down_requests[start].append(end)

    def not_full(self):
        return self.elevator.get_load() + PERSON_WEIGHT <= self.MAX_LOAD

    def __repr__(self):
        return f"Scheduler({self.FLOOR_COUNT})"

    # string representation of the elevator
    def __str__(self):
        
        format_string = "{:<6} {:<24} {:<24} {:<24}\n"
        string = 'SCHEDULER:\n'
        string += format_string.format('FLOOR','UP_REQUESTS','DOWN_REQUESTS','STOP_REQUESTS')
        for floor in range(self.FLOOR_COUNT, -1, -1):
            up = ', '.join(map(str, self.up_requests[floor]))
            down = ', '.join(map(str, self.down_requests[floor]))
            req_count = self.stop_requests[floor]
            stop = req_count if req_count > 0 else ''
            string += format_string.format(floor, up, down, stop)
        return string

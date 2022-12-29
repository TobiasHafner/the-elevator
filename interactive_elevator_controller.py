# This class can take travel requests from std to control an elevator

import sys
import os
from elevator import Elevator
from elevator_scheduler import Scheduler
from scheduler_moves import Moves

# amonut of floors
FLOOR_COUNT = 16
# max load of elevator
MAX_LOAD = 500

def run_controller():
    elevator = Elevator(FLOOR_COUNT, MAX_LOAD)
    scheduler = Scheduler(elevator)

    for request in sys.stdin:
        # check for eyit request
        if (request == 'exit'):
            exit()
        #read
        # parse request
        split = request.split()
        if (len(split) != 0):
            start = int(split[0])
            end = int(split[1])

            scheduler.handle_request(start, end)

        # eval
        move = scheduler.get_next_move()      
        match move:
            case Moves.UP:
                elevator.close_doors()
                elevator.move_up()
            case Moves.STOP:
                    elevator.open_doors()
            case Moves.DOWN:
                elevator.close_doors()
                elevator.move_down()
            case Moves.STAY:
                elevator.close_doors()
        # print
        os.system('clear')
        print(elevator)
        print(scheduler)

if __name__ == "__main__":
    run_controller()
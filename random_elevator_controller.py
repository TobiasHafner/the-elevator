# This class can take travel requests from std to control an elevator

import time
import os
from elevator import Elevator
from elevator_scheduler import Scheduler
from scheduler_moves import Moves
from request_generator import RequestGenerator

# amonut of floors
FLOOR_COUNT = 16
# max load of elevator
MAX_LOAD = 1200
# probability for request
REQUEST_PROBABILITY = 0.3
# time between iterations
ITER_TIME = 0.5
# tiem waiting on floor
STOP_TIME = 0.75

def run_controller():
    elevator = Elevator(FLOOR_COUNT, MAX_LOAD)
    scheduler = Scheduler(elevator)
    generator = RequestGenerator(FLOOR_COUNT, REQUEST_PROBABILITY)

    while(True):
        # read
        request = generator.generate_request()
        split = request.split()
        if (len(split) != 0):
            start = int(split[0])
            end = int(split[1])

            scheduler.handle_request(start, end)

        # decide next move
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

        if (elevator.get_door_state()):
            time.sleep(STOP_TIME)
        time.sleep(ITER_TIME)


if __name__ == "__main__":
    run_controller()
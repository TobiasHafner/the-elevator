# This class generates random ride requests

import random
class RequestGenerator:
    def __init__(self, floor_count, request_controller):
        self.FLOOR_COUNT = floor_count
        self.request_controller = request_controller

    def generate_request(self):
        # if request should be generated
        request_probability = self.request_controller.get_request_probability()
        if (self.random_boolean(request_probability)):
            # get random start floor
            start = self.random_floor(self.FLOOR_COUNT)
            # get random destination floor
            end = self.random_floor(self.FLOOR_COUNT)
            # prevent start and destination from beeing equal
            while (start == end):
                end = self.random_floor(self.FLOOR_COUNT)
            return f'{start} {end}'
        return ""

    def random_floor(self, floor_count):
        return random.randint(0, floor_count)

    def random_boolean(self, request_probability):
        return random.random() < request_probability

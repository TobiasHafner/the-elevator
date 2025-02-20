from base_request_controller import BaseRequestController


class FixedRequestController(BaseRequestController):
    """Controller with a fixed probability of generating requests"""

    def __init__(self, request_probability):
        self.request_probability = request_probability

    def get_request_probability(self):
        return self.request_probability

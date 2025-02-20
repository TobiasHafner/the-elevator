import json
from collections import deque
from datetime import datetime


class RideLog:
    def __init__(self, clock, size=1000):
        """
        Initializes the RideLog object to track the last 1000 rides.
        :param clock: An optional clock object with a getter method returning the current time.
        """
        self.clock = clock
        self.rides = deque(maxlen=size)

    def log_ride(self, start, end, person_id=None):
        """
        Logs a ride with timestamps and API request data if available.
        :param start: The departure floor
        :param end: The destination floor
        :param id: Unique id of the user requesting the ride
        """
        ride_entry = {
            "virtual_time": self.clock.get_virtual_seconds_since_epoch(),
            "real_time": int(datetime.now().timestamp()),
            "start": start,
            "end": end,
            "person_id": person_id
        }
        self.rides.append(ride_entry)

    def get(self):
        """
        Returns the last 1000 rides as a list of dictionaries.
        """
        return list(self.rides)


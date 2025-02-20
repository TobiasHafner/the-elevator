import math


class FluctuatingRequestController:
    """Request probability controller that follows a daily human activity pattern."""

    def __init__(self, clock, base_probability=0.1):
        """
        :param clock: An instance of VirtualClock
        :param base_probability: The minimum request probability during low periods.
        """
        self.clock = clock  # Uses external clock
        self.base_probability = base_probability

    def get_request_probability(self):
        """Determines the request probability based on time of day."""
        hour = self.clock.get_virtual_hour()

        if 7 <= hour < 9:  # Morning peak (arrival at work)
            probability = self.scaled_gaussian(hour, peak_hour=8, spread=1.5, max_factor=6)
        elif 11 <= hour < 14:  # Lunch break
            probability = self.scaled_gaussian(hour, peak_hour=12, spread=2, max_factor=4)
        elif 15 <= hour < 21:  # People leaving work
            probability = self.scaled_gaussian(hour, peak_hour=18, spread=3, max_factor=3)
        elif 21 <= hour or hour < 6:  # Nighttime minimal activity
            probability = self.base_probability * 0.5
        else:  # Default probability outside peak hours
            probability = self.base_probability

        return probability

    def scaled_gaussian(self, hour, peak_hour, spread, max_factor):
        """
        Creates a smooth Gaussian-like peak for probability distribution.
        :param hour: Current hour
        :param peak_hour: Peak hour of activity
        :param spread: Spread of the peak (how broad the increase is)
        :param max_factor: Multiplier for peak request probability
        :return: Adjusted probability
        """
        distance = abs(hour - peak_hour)
        factor = math.exp(-((distance ** 2) / (2 * spread ** 2)))  # Gaussian decay
        return self.base_probability + (self.base_probability * (max_factor - 1) * factor)

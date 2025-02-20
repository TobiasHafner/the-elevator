import math
import random


class FluctuatingRequestController:
    """Request probability controller that follows a daily human activity pattern with randomized peak parameters."""

    def __init__(self, clock, base_probability=0.1):
        """
        :param clock: An instance of VirtualClock
        :param base_probability: The minimum request probability during low periods.
        """
        self.clock = clock  # Uses external clock
        self.base_probability = base_probability

    def get_request_probability(self):
        """Determines the request probability based on time of day with some randomness."""
        hour = self.clock.get_virtual_hour()

        if 7 <= hour < 9:  # Morning peak (arrival at work)
            probability = self.scaled_gaussian(
                hour,
                peak_hour=random.gauss(8, 0.5),  # Slight variation around 8 AM
                spread=random.uniform(1.2, 1.8),  # Randomized spread
                max_factor=random.uniform(5.5, 6.5)  # Randomized peak intensity
            )
        elif 11 <= hour < 14:  # Lunch break
            probability = self.scaled_gaussian(
                hour,
                peak_hour=random.gauss(12, 0.3),  # Slight variation around noon
                spread=random.uniform(1.8, 2.2),
                max_factor=random.uniform(3.5, 4.5)
            )
        elif 15 <= hour < 21:  # Evening peak (leaving work)
            probability = self.scaled_gaussian(
                hour,
                peak_hour=random.gauss(18, 0.7),
                spread=random.uniform(2.5, 3.5),
                max_factor=random.uniform(2.5, 3.5)
            )
        elif 21 <= hour or hour < 6:  # Nighttime minimal activity
            probability = self.base_probability * 0.5
        else:  # Default probability outside peak hours
            probability = self.base_probability

        return probability

    def scaled_gaussian(self, hour, peak_hour, spread, max_factor):
        """
        Creates a smooth Gaussian-like peak for probability distribution with added randomness.
        :param hour: Current hour
        :param peak_hour: Peak hour of activity (randomized)
        :param spread: Spread of the peak (randomized)
        :param max_factor: Multiplier for peak request probability (randomized)
        :return: Adjusted probability
        """
        distance = abs(hour - peak_hour)
        factor = math.exp(-((distance ** 2) / (2 * spread ** 2)))  # Gaussian decay
        return self.base_probability + (self.base_probability * (max_factor - 1) * factor)

import random
import hashlib


def generate_person_id(index):
    """Generates a unique SHA-256 ID for a person based on index."""
    return hashlib.sha256(f'person-{index}'.encode()).hexdigest()


def random_boolean(request_probability):
    """Returns True if a request should be generated based on probability."""
    return random.random() < request_probability


class RequestGenerator:
    def __init__(self, floor_count, request_controller, clock, num_people=100):
        """
        :param floor_count: Number of floors in the building.
        :param request_controller: Instance of FluctuatingRequestController.
        :param clock: Instance of VirtualClock for time-based movement patterns.
        :param num_people: Number of simulated people using the elevator.
        """
        self.FLOOR_COUNT = floor_count
        self.request_controller = request_controller
        self.clock = clock
        self.num_people = num_people

        # Initialize people with unique IDs and random starting floors (except 0)
        self.people = {
            generate_person_id(i): 0  # No one starts at 0
            for i in range(num_people)
        }

    def generate_request(self):
        """Generates a ride request based on people's movement patterns."""
        request_probability = self.request_controller.get_request_probability()
        if not random_boolean(request_probability):
            return ""

        hour = self.clock.get_virtual_hour()

        # Select a random person
        person_id = random.choice(list(self.people.keys()))
        start_floor = self.people[person_id]

        # Morning (7-10 AM): People enter the building (only those who were on floor 0)
        if 7 <= hour < 10:
            if start_floor == 0:  # Only those at floor 0 can move up
                end_floor = random.randint(1, self.FLOOR_COUNT - 1)
            else:  # Already inside, they move randomly between floors
                end_floor = self.random_different_floor(start_floor)

        # Lunch time (11 AM - 2 PM): Moving to/from cafeteria (2) or outside (0)
        elif 11 <= hour < 14:
            if start_floor in {0, 2}:  # Returning to offices
                end_floor = random.randint(3, self.FLOOR_COUNT - 1)
            else:  # Going for lunch
                end_floor = random.choice([0, 2])

        # Afternoon (3-6 PM): Random movement between floors
        elif 15 <= hour < 18:
            end_floor = self.random_different_floor(start_floor)

        # Evening (6-9 PM): People leave the office (only those not already at 0)
        elif 18 <= hour < 21:
            if start_floor != 0:  # Only those not already at floor 0 can move down
                end_floor = 0
            else:
                return ""  # Skip people already at 0

        # Night (9 PM - 6 AM): Security patrols move randomly
        else:
            end_floor = self.random_different_floor(start_floor)

        # Update the person's last known floor
        self.people[person_id] = end_floor

        return f'{person_id} {start_floor} {end_floor}'

    def random_different_floor(self, current_floor):
        """Chooses a random floor different from the current one."""
        end_floor = random.randint(0, self.FLOOR_COUNT - 1)
        while end_floor == current_floor:
            end_floor = random.randint(0, self.FLOOR_COUNT - 1)
        return end_floor

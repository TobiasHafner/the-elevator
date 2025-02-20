from collections import defaultdict


class Statistics:
    def __init__(self, clock):
        """
        Initializes the Statistics object.
        :param clock: An optional clock object with a getter method returning the current time.
        """
        self.clock = clock
        self.departures = defaultdict(int)  # Tracks departure floor counts
        self.destinations = defaultdict(int)  # Tracks destination floor counts
        self.total_rides = 0  # Total number of rides
        self.ride_timestamps = defaultdict(int)  # Heatmap data for 1-hour bins
        self.total_distance = 0  # Total distance traveled
        self.distance_by_floor = defaultdict(lambda: {'total_from_distance': 0, 'total_to_distance': 0, 'from_count': 0, 'to_count': 0})

    def track_ride(self, start, end):
        """
        Tracks an elevator ride from start floor to end floor.
        :param start: The departure floor
        :param end: The destination floor
        """
        if start == end:
            return  # Ignore rides with no movement

        self.departures[start] += 1
        self.destinations[end] += 1
        self.total_rides += 1

        # Track ride in hourly heatmap
        hour_bin = self.clock.get_virtual_hour()
        self.ride_timestamps[hour_bin] += 1

        # Track total and per-floor travel distances
        distance = abs(end - start)
        self.total_distance += distance
        self.distance_by_floor[start]['total_from_distance'] += distance
        self.distance_by_floor[start]['from_count'] += 1
        self.distance_by_floor[end]['total_to_distance'] += distance
        self.distance_by_floor[end]['to_count'] += 1

    def get_average_distance(self):
        """
        Returns the overall average distance of all rides.
        """
        if self.total_rides == 0:
            return 0
        return self.total_distance / self.total_rides

    def get_average_distance_to_floor(self):
        """
        Returns a dictionary mapping each floor to its average travel distance.
        """
        avg_distances = {}
        for floor, data in self.distance_by_floor.items():
            if data['to_count'] > 0:
                avg_distances[floor] = data['total_to_distance'] / data['to_count']
            else:
                avg_distances[floor] = 0
        return avg_distances

    def get_average_distance_from_floor(self):
        """
        Returns a dictionary mapping each floor to its average travel distance.
        """
        avg_distances = {}
        for floor, data in self.distance_by_floor.items():
            if data['from_count'] > 0:
                avg_distances[floor] = data['total_from_distance'] / data['from_count']
            else:
                avg_distances[floor] = 0
        return avg_distances

    def get_hourly_heatmap(self):
        """
        Returns the hourly ride distribution as a dictionary.
        """
        return dict(self.ride_timestamps)

    def get(self):
        """
        Returns all statistics.
        """
        stats = {
            "departures": dict(self.departures),
            "destinations": dict(self.destinations),
            "total_rides": self.total_rides,
            "hourly_heatmap": self.get_hourly_heatmap(),
            "average_distance": self.get_average_distance(),
            "average_from_distance_by_floor": self.get_average_distance_from_floor(),
            "average_to_distance_by_floor": self.get_average_distance_to_floor()
        }
        return stats

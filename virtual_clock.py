from datetime import datetime


class VirtualClock:
    """A virtual clock that maps real-world time to a compressed virtual day."""

    def __init__(self, scale=96):
        """
        :param scale: The factor that determines how fast the virtual time progresses.
                      A scale of 60 means 1 real second = 1 virtual minute.
        """
        self.scale = scale
        self.start_time = datetime.now()

    def get_virtual_seconds(self):
        """Calculates the virtual seconds based on real-world elapsed time."""
        elapsed_real_seconds = (datetime.now() - self.start_time).total_seconds()
        virtual_seconds = int((elapsed_real_seconds * self.scale) % 60)
        return virtual_seconds

    def get_virtual_minutes(self):
        """Calculates the virtual minutes based on real-world elapsed time."""
        elapsed_real_seconds = (datetime.now() - self.start_time).total_seconds()
        virtual_minutes = int((elapsed_real_seconds / 60) * self.scale) % (24 * 60)
        return virtual_minutes

    def get_virtual_hour(self):
        """Returns the current virtual hour (0-23)."""
        return self.get_virtual_minutes() // 60

    def get_virtual_seconds_since_epoch(self):
        return int((datetime.now() - self.start_time).total_seconds())

    def __str__(self):
        """Returns the current virtual time in HH:MM:SS format."""
        total_minutes = self.get_virtual_minutes()
        hour = total_minutes // 60
        minute = total_minutes % 60
        second = self.get_virtual_seconds()
        return f"{hour:02}:{minute:02}:{second:02}"

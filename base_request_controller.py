class BaseRequestController:
    """Abstract class for different request controllers"""
    def get_request_probability(self):
        raise NotImplementedError("Subclasses should implement this method.")
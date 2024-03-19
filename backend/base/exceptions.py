class AvailabilityValidationException(Exception):
    def __init__(
        self,
        message,
        conflicting_day=None,
        conflicting_start_time=None,
        conflicting_end_time=None,
    ):
        super().__init__(message)
        self.conflicting_day = conflicting_day
        self.conflicting_start_time = conflicting_start_time
        self.conflicting_end_time = conflicting_end_time

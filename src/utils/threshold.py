from src.utils.status import Status


class Threshold:
    LOW_CRITICAL_THRESHOLD = 54
    LOW_THRESHOLD = 70
    HIGH_THRESHOLD = 180
    HIGH_CRITICAL_THRESHOLD = 299

    @classmethod
    def get_status(cls, value: int) -> Status:
        if value <= cls.LOW_CRITICAL_THRESHOLD:
            return Status.LOW_CRITICAL
        elif value <= cls.LOW_THRESHOLD:
            return Status.LOW
        elif value >= cls.HIGH_CRITICAL_THRESHOLD:
            return Status.HIGH_CRITICAL
        elif value >= cls.HIGH_THRESHOLD:
            return Status.HIGH
        else:
            return Status.OK

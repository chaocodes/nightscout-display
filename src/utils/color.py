from src.utils.status import Status


class Color:
    LOW_CRITICAL = (133, 0, 0)
    LOW = (101, 0, 0)
    HIGH = (175, 149, 0)
    HIGH_CRITICAL = (204, 179, 59)
    OK = (0, 88, 65)

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    @classmethod
    def get_color(cls, status: Status) -> tuple[int, int, int]:
        match status:
            case Status.LOW_CRITICAL:
                return cls.LOW_CRITICAL
            case Status.LOW:
                return cls.LOW
            case Status.HIGH:
                return cls.HIGH
            case Status.HIGH_CRITICAL:
                return cls.HIGH_CRITICAL
            case Status.OK:
                return cls.OK

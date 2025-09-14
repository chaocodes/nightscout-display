from src.utils.threshold import Threshold
from src.utils.status import Status


def test_threshold() -> None:
    assert Threshold.get_status(100) == Status.OK
    assert Threshold.get_status(190) == Status.HIGH
    assert Threshold.get_status(299) == Status.HIGH_CRITICAL
    assert Threshold.get_status(70) == Status.LOW
    assert Threshold.get_status(50) == Status.LOW_CRITICAL

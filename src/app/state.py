from logging import getLogger
from typing import Callable
from src.utils.threshold import Threshold
from src.utils.trend import Trend
from src.utils.status import Status

logger = getLogger(__name__)


class AppState:
    BRIGHTNESS_MIN = 0.1
    BRIGHTNESS_MAX = 1.0

    def __init__(self) -> None:
        self.is_muted: bool = False
        self.is_alarm_on: bool = False
        self.is_alarm_acknowledged: bool = False
        self.brightness: float = 1.0

        self.is_loaded: bool = False
        self.latest_sgv: int = 0
        self.trend: Trend = Trend.NONE
        self.status: Status = Status.OK

        self._listeners: list[Callable[[AppState], None]] = []

    def __str__(self) -> str:
        return str({k: v for k, v in vars(self).items() if not k.startswith("_")})

    def _notify_listeners(self) -> None:
        logger.info(self)
        for listener in self._listeners:
            listener(self)

    def add_listener(self, listener: Callable[["AppState"], None]) -> None:
        self._listeners.append(listener)

    def set_latest_sgv(self, sgv: int, trend: Trend = Trend.NONE) -> None:
        old_status = self.status

        self.is_loaded = True
        self.latest_sgv = sgv
        self.trend = trend
        self.status = Threshold.get_status(sgv)

        if old_status != self.status:
            if self.status in [Status.LOW_CRITICAL, Status.HIGH_CRITICAL]:
                self.is_alarm_on = True
                self.is_alarm_acknowledged = False
            else:
                self.is_alarm_on = False
                self.is_alarm_acknowledged = False

        self._notify_listeners()

    def adjust_brightness(self, delta: float) -> None:
        self.brightness = max(
            self.BRIGHTNESS_MIN, min(self.BRIGHTNESS_MAX, self.brightness + delta)
        )
        self._notify_listeners()

    def acknowledge_alarm(self) -> None:
        self.is_alarm_acknowledged = True
        self._notify_listeners()

    def toggle_mute(self) -> None:
        self.is_muted = not self.is_muted
        self._notify_listeners()

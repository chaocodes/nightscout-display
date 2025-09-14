import threading
from logging import getLogger
from time import sleep

from src.app.state import AppState
from src.interfaces.interface import Interface
from src.interfaces.events import InterfaceEvents
from src.app.view import AppView
from src.clients.nightscout import NightscoutClient

from playsound3 import playsound, playsound3

logger = getLogger(__name__)


class AppController:
    ALARM_SOUND_PATH = "assets/audio/alarm.wav"

    NIGHTSCOUT_POLLING_INTERVAL = 30

    INTERFACE_UPDATE_INTERVAL = 0.1

    THREAD_JOIN_TIMEOUT = 1.0

    def __init__(
        self,
        view: AppView,
        state: AppState,
        interface: Interface,
        nightscout_client: NightscoutClient,
    ) -> None:
        self._is_running: bool = False

        self._view = view
        self._state = state
        self._interface = interface
        self._nightscout_client = nightscout_client

        self._alarm_sound: playsound3.Sound | None = None
        self._alarm_thread: threading.Thread | None = None

        self._polling_thread: threading.Thread | None = None

        self._state.add_listener(self._on_state_change)
        self._interface.add_listener(self._on_interface_event)

    def _on_state_change(self, state: AppState) -> None:
        if state.is_alarm_on and not state.is_muted and not state.is_alarm_acknowledged:
            self._play_alarm_sound()
        else:
            self._stop_alarm_sound()

    def _on_interface_event(self, event: InterfaceEvents) -> None:
        match event:
            case InterfaceEvents.TOGGLE_MUTE:
                self._state.toggle_mute()
            case InterfaceEvents.ACKNOWLEDGE_ALARM:
                self._state.acknowledge_alarm()
            case InterfaceEvents.INCREASE_BRIGHTNESS:
                self._state.adjust_brightness(0.1)
            case InterfaceEvents.DECREASE_BRIGHTNESS:
                self._state.adjust_brightness(-0.1)

    def _alarm_loop(self) -> None:
        while self._is_running and (
            not self._alarm_sound or not self._alarm_sound.is_alive()
        ):
            self._alarm_sound = playsound(self.ALARM_SOUND_PATH, block=False)

    def _play_alarm_sound(self) -> None:
        if not self._alarm_thread or not self._alarm_thread.is_alive():
            self._alarm_thread = threading.Thread(target=self._alarm_loop, daemon=True)
            self._alarm_thread.start()

    def _stop_alarm_sound(self) -> None:
        if self._alarm_sound:
            self._alarm_sound.stop()

        if self._alarm_thread and self._alarm_thread.is_alive():
            self._alarm_thread.join(timeout=self.THREAD_JOIN_TIMEOUT)

    def _poll_nightscout(self) -> None:
        while self._is_running:
            try:
                (latest_sgv, trend) = self._nightscout_client.get_latest_entry()
                self._state.set_latest_sgv(latest_sgv, trend)
            except Exception as e:
                logger.error(f"Error polling Nightscout: {e}")

            sleep(self.NIGHTSCOUT_POLLING_INTERVAL)

    def _start_poll_nightscout(self) -> None:
        if not self._polling_thread or not self._polling_thread.is_alive():
            self._polling_thread = threading.Thread(
                target=self._poll_nightscout, daemon=True
            )
            self._polling_thread.start()

    def _stop_poll_nightscout(self) -> None:
        if self._polling_thread and self._polling_thread.is_alive():
            self._polling_thread.join(timeout=self.THREAD_JOIN_TIMEOUT)

    def stop(self) -> None:
        self._is_running = False
        self._stop_alarm_sound()
        self._stop_poll_nightscout()
        self._interface.cleanup()

    def start(self) -> None:
        if self._is_running:
            return

        self._is_running = True
        self._start_poll_nightscout()

        try:
            while self._is_running:
                self._interface.update(self._view.draw())
                sleep(self.INTERFACE_UPDATE_INTERVAL)
        finally:
            self.stop()

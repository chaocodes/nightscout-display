from src.interfaces.interface import Interface
from src.interfaces.events import InterfaceEvents
from PIL import Image

try:
    import st7789  # type: ignore
    import RPi.GPIO as GPIO  # type: ignore

    ST7789_AVAILABLE = True
except ImportError:
    ST7789_AVAILABLE = False


class ST7789Interface(Interface):
    BUTTON_BOUNCE_TIME = 100
    BUTTONS = {
        5: InterfaceEvents.TOGGLE_MUTE,  # A
        6: InterfaceEvents.ACKNOWLEDGE_ALARM,  # B
        16: InterfaceEvents.INCREASE_BRIGHTNESS,  # X
        24: InterfaceEvents.DECREASE_BRIGHTNESS,  # Y
    }

    def __init__(
        self,
        width: int,
        height: int,
        rotation: int,
        port: int,
        cs: int,
        dc: int,
        backlight: int,
        spi_speed_hz: int,
    ):
        if not ST7789_AVAILABLE:
            raise ImportError(
                "st7789 library not available. Install with: pip install st7789"
            )

        super().__init__(width, height)

        self.display = st7789.ST7789(
            rotation=rotation,
            port=port,
            cs=cs,
            dc=dc,
            backlight=backlight,
            spi_speed_hz=spi_speed_hz,
        )

        self.display.begin()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(list(self.BUTTONS.keys()), GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for pin in self.BUTTONS.keys():
            GPIO.add_event_detect(
                pin,
                GPIO.FALLING,
                self._handle_button_press,
                bouncetime=self.BUTTON_BOUNCE_TIME,
            )

    def _handle_button_press(self, button: int) -> None:
        if button in self.BUTTONS:
            self._trigger_event(self.BUTTONS[button])

    def update(self, image: Image.Image) -> None:
        self.display.display(image)

    def cleanup(self) -> None:
        self.display.command(st7789.ST7789_DISPOFF)
        GPIO.cleanup()

    @staticmethod
    def is_available() -> bool:
        return ST7789_AVAILABLE

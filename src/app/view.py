from src.utils.status import Status
from src.utils.color import Color
from src.utils.trend import Trend
from src.app.state import AppState
from src.utils.image_utils import ImageUtils
from PIL import Image, ImageDraw


class AppView:
    GLUCOSE_VALUE_FONT_SIZE = 118
    GLUCOSE_VALUE_FONT_PATH = "assets/fonts/Doto_Rounded-ExtraBold.ttf"
    ARROW_SIZE = 36

    CONTROL_SIZE = 18
    CONTROL_HORIZONTAL_MARGIN = 8
    CONTROL_VERTICAL_MARGIN = 32
    VOLUME_OFF_ICON_PATH = "assets/images/controls/volume-off.png"
    VOLUME_ON_ICON_PATH = "assets/images/controls/volume-on.png"
    BRIGHTNESS_UP_ICON_PATH = "assets/images/controls/brightness-up.png"
    BRIGHTNESS_DOWN_ICON_PATH = "assets/images/controls/brightness-down.png"
    ACKNOWLEDGE_ALARM_ICON_PATH = "assets/images/controls/ack.png"

    CAT_SIZE = 70
    CAT_TOP_MARGIN = 12
    CATS = {
        Status.LOW_CRITICAL: ("assets/images/cats/injured", 5),
        Status.LOW: ("assets/images/cats/injured", 5),
        Status.HIGH: ("assets/images/cats/crying", 4),
        Status.HIGH_CRITICAL: ("assets/images/cats/crying", 4),
        Status.OK: ("assets/images/cats/dancing", 4),
    }

    ARROW_Y_OFFSET = 70
    ARROWS = {
        Trend.DOUBLE_UP: "assets/images/arrows/up.png",
        Trend.SINGLE_UP: "assets/images/arrows/upright.png",
        Trend.FORTY_FIVE_UP: "assets/images/arrows/upright.png",
        Trend.FLAT: "assets/images/arrows/right.png",
        Trend.FORTY_FIVE_DOWN: "assets/images/arrows/downright.png",
        Trend.SINGLE_DOWN: "assets/images/arrows/downright.png",
        Trend.DOUBLE_DOWN: "assets/images/arrows/down.png",
    }

    def __init__(self, width: int, height: int, state: AppState) -> None:
        self._width = width
        self._height = height

        self._state = state

        self._cat_frame = 0

    def _draw_cat(self, image: Image.Image) -> None:
        cat_type_path, total_frames = self.CATS[self._state.status]
        self._cat_frame = (self._cat_frame + 1) % total_frames
        cat_image = ImageUtils.get_image(
            f"{cat_type_path}/{self._cat_frame + 1}.png",
            size=(self.CAT_SIZE, self.CAT_SIZE),
        )
        image.paste(
            cat_image,
            (
                int(self._width / 2 - self.CAT_SIZE / 2),
                self.CAT_TOP_MARGIN,
            ),
            cat_image,
        )

    def _draw_control_panel(self, image: Image.Image) -> None:
        icon_size = (self.CONTROL_SIZE, self.CONTROL_SIZE)

        volume_icon_path = (
            self._state.is_muted
            and self.VOLUME_OFF_ICON_PATH
            or self.VOLUME_ON_ICON_PATH
        )
        volume_icon = ImageUtils.get_image(volume_icon_path, size=icon_size)
        image.paste(
            volume_icon,
            (self.CONTROL_HORIZONTAL_MARGIN, self.CONTROL_VERTICAL_MARGIN),
            volume_icon,
        )

        brightness_up_icon = ImageUtils.get_image(
            self.BRIGHTNESS_UP_ICON_PATH, size=icon_size
        )
        image.paste(
            brightness_up_icon,
            (
                self._width - self.CONTROL_HORIZONTAL_MARGIN - self.CONTROL_SIZE,
                self.CONTROL_VERTICAL_MARGIN,
            ),
            brightness_up_icon,
        )

        acknowledge_alarm_icon = ImageUtils.get_image(
            self.ACKNOWLEDGE_ALARM_ICON_PATH, size=icon_size
        )
        image.paste(
            acknowledge_alarm_icon,
            (
                self.CONTROL_HORIZONTAL_MARGIN,
                self._height - self.CONTROL_VERTICAL_MARGIN - self.CONTROL_SIZE,
            ),
            acknowledge_alarm_icon,
        )

        brightness_down_icon = ImageUtils.get_image(
            self.BRIGHTNESS_DOWN_ICON_PATH, size=icon_size
        )
        image.paste(
            brightness_down_icon,
            (
                self._width - self.CONTROL_HORIZONTAL_MARGIN - self.CONTROL_SIZE,
                self._height - self.CONTROL_VERTICAL_MARGIN - self.CONTROL_SIZE,
            ),
            brightness_down_icon,
        )

    def _draw_glucose_value(self, image: Image.Image) -> None:
        draw = ImageDraw.Draw(image)
        font = ImageUtils.get_font(
            self.GLUCOSE_VALUE_FONT_PATH, self.GLUCOSE_VALUE_FONT_SIZE
        )
        text_width, text_height, text_bbox = ImageUtils.get_text_dimensions(
            str(self._state.latest_sgv), font
        )
        text_x, text_y = ImageUtils.get_centered_position(
            self._width,
            self._height,
            int(text_width),
            int(text_height),
        )
        draw.text(
            (text_x - text_bbox[0], text_y - text_bbox[1]),
            str(self._state.latest_sgv),
            font=font,
            color=Color.WHITE,
        )

    def _draw_trend_arrow(self, image: Image.Image) -> None:
        arrow_path = self.ARROWS[self._state.trend]
        arrow_image = ImageUtils.get_image(
            arrow_path, size=(self.ARROW_SIZE, self.ARROW_SIZE)
        )
        x, y = ImageUtils.get_centered_position(
            self._width,
            self._height,
            self.ARROW_SIZE,
            self.ARROW_SIZE,
        )
        image.paste(arrow_image, (x, y + self.ARROW_Y_OFFSET), arrow_image)

    def draw(self) -> Image.Image:
        image = Image.new(
            "RGB", (self._width, self._height), Color.get_color(self._state.status)
        )
        self._draw_control_panel(image)

        if self._state.is_loaded:
            self._draw_trend_arrow(image)
            self._draw_cat(image)
            self._draw_glucose_value(image)

        return ImageUtils.set_brightness(image, self._state.brightness)

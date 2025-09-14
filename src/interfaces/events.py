from enum import Enum


class InterfaceEvents(Enum):
    TOGGLE_MUTE = "toggle_mute"
    INCREASE_BRIGHTNESS = "increase_brightness"
    DECREASE_BRIGHTNESS = "decrease_brightness"
    ACKNOWLEDGE_ALARM = "acknowledge_alarm"

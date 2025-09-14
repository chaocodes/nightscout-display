# Nightscout Display

A Raspberry Pi-powered glucose monitor display using Nightscout data, designed for Pirate Audio HAT and Raspberry Pi Zero 2 W.

## Features
- Real-time glucose readings from Nightscout
- Visual trend indicators and status colors
- Audio alarms for critical values
- Brightness and volume controls
- Animated status indicators

## Installation

### Install OS & HAT
Hardware requirements:
- Raspberry Pi Zero 2 W
- Pirate Audio HAT

Install & Configure [Raspberry Pi OS Lite 32 bit](https://www.raspberrypi.com/software/operating-systems/) using [Raspberry Pi Imager](https://www.raspberrypi.com/software/)

### Configure Pi & Install dependencies
Add to `/boot/firmware/config.txt`
```
# Pirate Audio
dtoverlay=hifiberry-dac
gpio=25=op,dh
```

Uncomment these lines
```
dtparam=i2c_arm=on
dtparam=spi=on
```

Install Dependencies
```
sudo apt update
sudo apt upgrade
sudo apt install python3-rpi.gpio python3-spidev python3-pip python3-pil python3-numpy
```

## Usage

#. Clone the repo on to your raspberry pi
#. Create a virtual env using system installed packages `uv venv --system-site-packages .venv`
#. Create a `config.ini` file in the root directory of the project. Set the `base_url` to point to your hosted nightscout project.
  ```
  [nightscout]
  base_url = https://website-with-nightscout-api.com
  ```
#. `uv run -m src.main --no-dev`

## Local Development

Run the app with `uv run -m src/main`

Outside of a raspberry pi, this will use PyGame to create the window.

You can use keys 1-4 to simulate the controls buttons.

Run `uv run pre-commit install` to install pre-commit hooks

## Typecheck, Linting, Formatting

`uv run mypy . && uv run ruff check --fix && uv run ruff format`

## Unit Testing

`uv run pytest`

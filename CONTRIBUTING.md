# Getting setup

You'll need desktop python, pip and git for this.

## Python tools

We use poetry to manage our environment. You can install it with:

```bash
pip install poetry
poetry install
```

To work in the project use `poetry shell` to activate the environment.

## Preparing the Raspberry Pi

Use the Raspberry Pi imager, select the Other Raspberry Pi OS versions and pick Raspberry Pi OS Lite (32-bit). Use the config to enable SSH, name the pi hostname, set the wifi passwords and country.

Write the image to the SD card.

## Modifying network on the Pi

Copy the VPA config example on wpa_supplicant.conf_example to wpa_supplicant.conf, swapping your own network credentials for the ones listed. Copy this onto the SD Card for the Pi.
Important: Do not commit Wi-Fi passwords in Git.

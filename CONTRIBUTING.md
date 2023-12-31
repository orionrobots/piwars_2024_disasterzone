# Getting setup

You'll need desktop python, pip and git for this.

## Python tools

We use poetry to manage our environment. You can install it with:

```bash
pip install poetry
poetry install
```

To work in the project use `poetry shell` to activate the environment.

## Preparing an ssh key

If you do not have one, an ssh key is recommended for this.
Generate an sh key if you don't have one, I suggest `ssh-keygen -t ecdsa -b 521`

## Preparing the Raspberry Pi

Use the Raspberry Pi imager, select the Other Raspberry Pi OS versions and pick Raspberry Pi OS Lite (32-bit). Use the config to enable SSH, name the pi hostname, set the wifi passwords and country.
Setup the ssh key.

Write the image to the SD card.

## Modifying network on the Pi

Copy the VPA config example on wpa_supplicant.conf_example to wpa_supplicant.conf, swapping your own network credentials for the ones listed. Copy this onto the SD Card for the Pi.
**Important**: Do not commit Wi-Fi passwords in Git.

## Running commands

We suggest making a copy of .env_example to .env, with your pi details.
That way, you can then use `source .env` to have your PI hostname in $HOST. Handy if you sometimes forget!

This project uses pyinfra. You can deploy with `pyinfra inventory.py deploy/install_base.py`. The other deploy commands are in the deploy folder.

## Note on updated joystick

npm install git+https://github.com/orionrobots/react-native-joystick

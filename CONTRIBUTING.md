# Getting setup

You'll need desktop python, pip and git for this.

## Python tools

We use poetry to manage our environment. You can install it with:

```bash
pip install poetry
poetry install
```

To work in the project use `poetry shell` to activate the environment.

## Modifying network on the Pi

Copy the VPA config example on wpa_supplicant.conf_example to wpa_supplicant.conf, swapping your own network credentials for the ones listed. Copy this onto the SD Card for the Pi.
Important: Do not commit Wi-Fi passwords in Git.

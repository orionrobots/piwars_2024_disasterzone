# Bus archtiecture

This project will be based on some connected MQTT components, using a mosquitto instance as the the broker.

## Installing

`fab setup_mqtt` -> Will become part of main setup when established

## Libraries

We want this to be asynchronous capable. We will use the asyncio-mqtt library <https://pypi.org/project/asyncio-mqtt/> along with [paho](https://github.com/eclipse/paho.mqtt.python).


## Messages and message types

### Motors

- Topic: `motors/left` and `motors/right`
  payloads: -1.0 to 1.0

- Topic: `motors/values`
  payload: left (-1 to 1.0), right (-1 to 1.0)

- Topic: `motors/forward`
  payload (optional): speed (0 to 1.0)- defaults to 1.0, optional curve (-1 to 1.0) - defaults to 0.0
- Topic: `motors/backward`
  payload (optional): speed (0 to 1.0)- defaults to 1.0, optional curve (-1 to 1.0) - defaults to 0.0
- Topic: `motors/stop`
- Maybe topic `motors/reverse`. Not 100% sure.

Assume 1 second duration, or until next command.


Links:
- https://www.google.com/search?q=mqtt+mosquito+broker+tutorial&oq=mqtt+mosquito+broker+tutorial&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIICAEQABgWGB4yCAgCEAAYFhgeMggIAxAAGBYYHjIKCAQQABiGAxiKBTIKCAUQABiGAxiKBTIKCAYQABiGAxiKBTIKCAcQABiGAxiKBTIKCAgQABiGAxiKBdIBCDY1NjlqMGo0qAIAsAIA&sourceid=chrome&ie=UTF-8
- https://mosquitto.org/
- https://cedalo.com/blog/configuring-paho-mqtt-python-client-with-examples/


## Project folder structure

Currently, a bit messy. Let's rejig - with service oriented setup.

Forget "src" which is generic, and have "robot".

```
.
├── .github                       # Directory for GitHub services and workflows
├── docs                          # Directory for roadmap and other documentation
│   └── roadmap.md                # File containing rough plans for the project
├── robot                         # Directory for code that runs on the robot
│   ├── services                  # Directory for collection of services that will be available on the robot
│   │   ├── common                # Directory for common code used for setting up a service
│   │   │   └── base_service.py   # File containing the RobotService base class for creating a service
│   │   ├── pimoroni_explorer_hat_pro  # Directory for services related to the Explorer HAT Pro
│   │   │   ├── hardware.py       # File containing the hardware interface code for the Explorer HAT Pro
│   │   │   ├── install.py        # File containing additional fab tasks for setting up the Explorer HAT Pro
│   │   │   └── service.py        # File containing the MQTT client with services offered by the Explorer HAT Pro
│   │   ├── pimoroni_inventor_hat_mini # Directory for services related to the Inventor HAT Mini
│   │   │   ├── hardware.py       # File containing the hardware interface code for the Inventor HAT Mini
│   │   │   ├── install.py        # File containing additional fab tasks for setting up the Inventor HAT Mini
│   │   │   └── service.py        # File containing the MQTT client with services offered by the Inventor HAT Mini
│   │   ├── bno055                # Directory for IMU (Inertial Measurement Unit) services
│   │   └── service_x             # Placeholder directory for additional services
│   ├── tests                     # Directory for collection of tests to run on the robot
│   ├── robot_settings.py         # Tool to read settings for the robot from the .env file
│   └── api.py                    # Deprecated file for interacting with the robot's API
├── fabfile.py                    # File for deployment and setup tasks
├── README.md                     # Main readme file for the project
├── .env_example                  # Example file for creating a .env file with settings for the robot
├── .gitignore                    # File specifying which files should not be tracked by Git
├── CONTRIBUTING.md               # Developer notes and guidelines for contributing to the project
├── LICENSE                       # License file for the repository
├── pyproject.toml                # File specifying the dependencies for managing the project with Poetry
├── poetry.lock                   # Lock file generated by Poetry to ensure consistent dependency resolution
```
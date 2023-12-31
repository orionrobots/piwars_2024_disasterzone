# Robot control app

This is an app designed to interact with the robot from a device.

It uses expo/react native.

## Installation

- Ensure you have up-to-date node.
- Install with `npm install`.
- Run with `npm run go`.
- Install the expo go app on your android/ios device.
- Scan the QR code with the camera, which shoudl launch the app.

You will need to close the app and re-open it with the QR code when you stop/start the
server.

## Testing with Docker

This is not usually necessary, but if you want to see how the build works in a Linux OS instead of your own, you can use Docker.

```bash
docker run --rm -it -p 8081:8081 -v${PWD}:${PWD} -w${PWD} -e REACT_NATIVE_PACKAGER_HOSTNAME=${HOSTNAME} node:21-bookworm bash
cd robot_control
npm install
npm run go
```

The Docker run maps your current directory to the container's current directory, along with a port. It sets the REACT NATIVE hostname to your current machine. It starts a bash prompt, letting you interact with the app. You can then run the app with `npm run go`.


# Camera commands we can use (pre-python)

- https://www.tomshardware.com/how-to/use-raspberry-pi-camera-with-bullseye
- https://www.raspberrypi.com/documentation/computers/camera_software.html - This is bookworm, so newer than the bullseye installed here.

## Getting a still

```bash
libcamera-still --datetime -e png --rotation 180
ls *.png
```

Retrieve it:

`
rsync danny@big-ole-yellow.local:0415195843.png .
`

You can now view locally

## Streaming

```bash
libcamera-vid --rotation 180 --listen -o

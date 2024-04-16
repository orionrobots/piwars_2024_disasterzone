from picamera2 import Picamera2
from libcamera import controls, Transform

from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.handler import Handler
from bokeh.plotting import figure, ColumnDataSource
from bokeh.document import Document

import numpy as np

picam2 = Picamera2()
transform = Transform(hflip=1)
picam2.configure(picam2.create_preview_configuration(main={"format": 'BGR888', "size": (640, 480)}, transform=transform))
picam2.set_controls({"AwbMode": controls.AwbModeEnum.Auto})
picam2.start()


class CameraStream(Handler):
    def modify_document(self, doc: Document) -> None:
        source = ColumnDataSource(data=dict(image=[]))
        def update():
            im = picam2.capture_array()
            # Add an alpha channel set to 255 (fully opaque)
            im_rgba = np.dstack((im, np.full((im.shape[0], im.shape[1], 1), 255, dtype=np.uint8)))
            im_rgba = im_rgba.view(dtype=np.uint32).reshape(im.shape[0], im.shape[1])
            source.data = dict(image=[im_rgba])
        doc.add_periodic_callback(update, 100)
        plot = figure(x_range=(0, 640), y_range=(0, 480), width=640, height=480)
        plot.image_rgba(image='image', x=0, y=0, dw=640, dh=480, source=source)
        doc.add_root(plot)

stream = CameraStream()
apps = {'/': Application(stream)}
server = Server(apps, port=5006, allow_websocket_origin=["*"])
server.start()
server.run_until_shutdown()

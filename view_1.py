## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2
from flask import Flask, render_template, Response
app = Flask(__name__)

###########################################################################################################
#%% imports
import pyrealsense2 as rs

#%% configure
ctx = rs.context()
device = ctx.devices[0]
serial_number = device.get_info(rs.camera_info.serial_number)
config = rs.config()
config.enable_device(serial_number)

#%% enable streams
config.enable_stream(rs.stream.infrared, 1, 1280,720, rs.format.y8, 6)
config.enable_stream(rs.stream.infrared, 2, 1280,720, rs.format.y8, 6)

#%% run pipeline
pipeline = rs.pipeline()
#profile = pipeline.start(config)
config = rs.config()

pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)

#pipeline_profile = pipeline.start(config)
device = pipeline_profile.get_device()
depth_sensor = device.query_sensors()[0]
emitter = depth_sensor.get_option(rs.option.emitter_enabled)
print("emitter = ", emitter)
set_emitter = 0
depth_sensor.set_option(rs.option.emitter_enabled, set_emitter)
emitter1 = depth_sensor.get_option(rs.option.emitter_enabled)
print("new emitter = ", emitter1)

#########################################################################################################################

# Configure depth and color streams
#pipeline = rs.pipeline()
#config = rs.config()

# Get device product line for setting a supporting resolution
#pipeline_wrapper = rs.pipeline_wrapper(pipeline)
#pipeline_profile = config.resolve(pipeline_wrapper)
#device = pipeline_profile.get_device()

device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        frames = pipeline.wait_for_frames()
        frame = frames.get_color_frame()
        if not frame:
            continue
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def gen_rgb():
    try:
        pipeline.start(config)
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue
            color_image = np.asanyarray(color_frame.get_data())
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + cv2.imencode(".jpeg", color_image)[1].tobytes() + b"\r\n")
    finally:
        pipeline.stop()

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_rgb(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/rgb")
def rgb():
    return Response(gen_rgb(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

#Import necessary libraries
from flask import Flask, render_template, Response
import cv2
import pyrealsense2
from realsense_depth import *

#Initialize the Flask app
app = Flask(__name__)

dc = DepthCamera()

def gen_frames():  
    while True:
        ret, depth_frame, frame = dc.get_frame()
        print(ret)
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

pipeline = " ! ".join(["v4l2src device=/dev/video0",
                       "video/x-raw, width=640, height=480, framerate=30/1",
                       "videoconvert",
                       "video/x-raw, format=(string)BGR",
                       "appsink"
                       ])

video_capture = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = video_capture.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
